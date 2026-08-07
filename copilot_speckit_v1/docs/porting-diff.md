# Claude Code 版 ↔ GitHub Copilot 版 差分表

`sdd_toolkit`（Claude Code 用）を GitHub Copilot 向けに移植した `copilot_speckit_v1` の対応関係と、
**等価物がないため移植していない機能**をまとめます。

調査時点：2026-08。Copilot の機能は変化が速いため、挙動が変わった場合はこのファイルを更新してください。

---

## 1. 対応マップ（移植できたもの）

| Claude Code | GitHub Copilot | 本リポジトリでの実体 | 備考 |
|---|---|---|---|
| `CLAUDE.md`（共通ルール） | `AGENTS.md` | `AGENTS.md` | Copilot CLI / coding agent が直接読む。中核はここに集約 |
| （VS Code 向け常時注入） | `.github/copilot-instructions.md` | 同左 | `@AGENTS.md` で共通ルールを取り込む薄いラッパ |
| `.claude/rules/*.md` | `.github/instructions/*.instructions.md` | 5ファイル | `applyTo: "**"` で常時適用 |
| `.claude/skills/<n>/SKILL.md` | `.github/skills/<n>/SKILL.md` | 12スキル | **手順の唯一の正**。`/<name>` で直接起動できる |
| `.claude/commands/*.md` | `.github/prompts/*.prompt.md` | 12プロンプト | **VS Code 専用**の薄いラッパ（後述） |
| `.claude/agents/*.md` | `.github/agents/*.agent.md` | 5エージェント | 自動委譲 / `/agent` / `--agent` |
| `templates/agents/*.md`（召喚テンプレ） | 同左 | 9専門家 | frontmatter を Copilot 形式に変換済み |
| `.claude/settings.json` の `hooks` | `.github/hooks/*.json` | `sdd-hooks.json` ＋ 4スクリプト | **Copilot CLI のみ**（後述） |
| `scripts/`, `templates/`, `eval/` | 変更なし | 同左 | エージェント非依存のためそのまま流用 |

---

## 2. 仕様差により作りを変えたもの

### 2.1 スラッシュコマンド：`.github/prompts/` は Copilot CLI では読まれない

VS Code Copilot Chat は `.github/prompts/*.prompt.md` を `/name` として認識しますが、
**Copilot CLI はこれを読み込みません**（機能要望が未実装のまま）。

そのため本リポジトリでは次の二段構えにしています。

| 面 | 呼び出し経路 |
|---|---|
| Copilot CLI | `.github/skills/<name>/SKILL.md` を `/name` で直接起動（Agent Skills は user-invocable） |
| Copilot coding agent | 同上（`.github/skills/` を読む） |
| VS Code Copilot Chat | `.github/prompts/<name>.prompt.md` を `/name` で起動 → 中で SKILL.md を読ませる |

**手順の実体は SKILL.md 側にしかありません。** プロンプトファイルは「SKILL.md を読んで従え」と
指示するだけの薄いラッパなので、手順を変更するときは必ず SKILL.md を編集してください。

### 2.2 フック：イベント名と適用範囲が違う

Copilot もフックに対応していますが、Claude Code とは以下が異なります。

| 項目 | Claude Code | GitHub Copilot |
|---|---|---|
| 設定ファイル | `.claude/settings.json` の `hooks` | `.github/hooks/*.json`（リポジトリ）／ `~/.copilot/hooks/*.json`（個人） |
| 有効な面 | Claude Code 全体 | **Copilot CLI のみ**（VS Code / coding agent では発火しない） |
| イベント名 | `PreToolUse` / `PostToolUse` / `Stop` / `SessionStart` | `preToolUse` / `postToolUse` / `sessionEnd` / `sessionStart` / `userPromptSubmitted` / `errorOccurred` |
| マッチャ | `"matcher": "Write(outputs/**)"` のようにツール・パスで絞れる | **マッチャなし**。絞り込みはスクリプト側で行う |
| `Stop` 相当 | あり | なし → `sessionEnd` で代替 |
| stdin のフィールド名 | `tool_name` / `tool_input` / `cwd` | `toolName` / `toolInput`（camelCase） |
| 出力 | JSON（`{"message": ...}`） | 標準出力のテキスト。exit != 0 で `preToolUse` はブロック |

移植したフック4本はすべて「警告するがブロックしない」方針のため常に exit 0 を返します。
マッチャがない分の絞り込みは各スクリプト冒頭で行っています
（`check-docs-exist.py` はツール名とパスを見て `outputs/` 配下の書き込み以外は即 return）。

### 2.3 エージェントの frontmatter

| フィールド | Claude Code | Copilot |
|---|---|---|
| `name` / `description` | あり | あり（`description` が自動委譲のトリガー） |
| `tools` | `Read, Glob, Grep, Bash, Write, Edit, Task` | 別名 `read` / `search` / `edit` / `execute` / `agent` に変換 |
| `model` | 使える | **CLI では無視される**（VS Code のみ）→ 削除した |
| `memory` | 使える | 等価物なし → `~/.sdd-knowledge/curator-history.md` にファイルで代替 |
| `maxTurns` | 使える | 等価物なし → 削除した |

### 2.4 生成エージェントの置き場所

`/init-task` の専門家エージェント召喚先を `.claude/agents/generated/<key>.md` から
`.github/agents/<key>.agent.md` に変更しました。理由は2つ。

- Copilot はカスタムエージェントを **`.agent.md` 拡張子**で認識する
- サブディレクトリ配下の探索が保証されていないため、フラットに置く

代わりに、生成したファイル名を `metadata.json` の `generated_agents` に記録し、
`/finalize` で追跡・アーカイブできるようにしています。

### 2.5 引数の渡し方

| 面 | 書き方 |
|---|---|
| Copilot CLI | `/run-phase 1-3` のようにスキル名の後ろに続けて書く |
| VS Code | プロンプトファイルの `${input:args:...}`（`/run-phase args=1-3`） |

SKILL.md 内に残っている `$ARGUMENTS` は「呼び出し時に渡されたテキスト」を指す、と各所で定義しています。

---

## 3. 移植していないもの（Copilot に等価物がない）

| 機能 | Claude Code での役割 | Copilot 版での扱い |
|---|---|---|
| `permissions.allow` / `ask` / `deny` | ツール実行の宣言的な許可・確認・禁止リスト | **非対応**。宣言的に同じことはできない。CLI の `--allow-tool` / `--deny-tool` / `--allow-all-tools` と、SKILL.md の `allowed-tools`（無確認で使えるツールの列挙）で部分的に近似する。禁止事項は `.github/copilot-instructions.md` に運用ルールとして明記 |
| `sandbox`（ネットワーク許可ドメイン等） | 実行環境の隔離 | **非対応**。Copilot CLI に同等の宣言的サンドボックス設定はない |
| `env`（セッション環境変数） | 実験フラグ等の注入 | **部分対応**。フック定義の `env` でフックプロセスにのみ環境変数を渡せる。セッション全体には渡せない |
| フックの matcher | ツール名・パスでの発火条件指定 | **非対応**。スクリプト側で自前判定（移植済み） |
| `Stop` フック | ターン終了時の処理 | **非対応**。`sessionEnd`（セッション終了時）で代替。発火頻度が違う点に注意 |
| VS Code / coding agent でのフック | — | **非対応**。フックは Copilot CLI 限定 |
| エージェントの `memory` | サブエージェントの永続メモリ | **非対応**。ファイル（`~/.sdd-knowledge/curator-history.md`）で代替 |
| `scripts/mcp_server/` | 知識ベースの API 提供 | **MCP ではない**。中身は FastAPI の REST API（`127.0.0.1:8741`）で、MCP プロトコルを話さないため Copilot の MCP 設定にそのままは登録できない。詳細は `docs/copilot-setup.md` の MCP 節 |

---

## 4. デグレ確認の観点

Claude Code 版（`sdd_toolkit`）は本リポジトリとは別管理であり、本移植では一切変更していません。
両方を併用する場合の注意点だけ挙げます。

- `~/.sdd-knowledge/` は両者で**共有**されます（スターター・教訓・アーカイブ）。スキーマは同一なので相互運用できます。
- 同一プロジェクトディレクトリで両方を使うと、プロジェクト仕様ファイルが `CLAUDE.md` と `AGENTS.md` に
  分かれます。本リポジトリでは `CLAUDE.md` を `@AGENTS.md` 参照だけの薄いラッパにして二重管理を避けています。
- `.claude/` と `.github/` は互いに干渉しません。片方を消してももう片方は動きます。
