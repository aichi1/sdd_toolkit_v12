# copilot_speckit_v1

**GitHub Copilot 向けの Spec-Driven Development（仕様駆動開発）spec-kit。**

Claude Code 用に開発・運用してきた SDD toolkit（`sdd_toolkit`）を、GitHub Copilot の
カスタマイズ機構（Agent Skills / Custom Agents / Custom Instructions / Hooks）に移植したものです。
**VS Code Copilot Chat / Copilot CLI / Copilot coding agent** の3面で動きます。

> 「順序立てて考え、仕様を作り、成果物を生成し、検証し、最後に知見を残す」を Copilot に定着させる。

---

## 何ができるか

```
/init-task  →  /run-phase N  →  [ /re-init-task → /run-phase N ]*  →  /finalize  →  /retrospective
```

1. `/init-task` — やりたいことを説明すると、タスク種別を判定して `docs/`（What）と
   `skills/phase-NN/SKILL.md`（How）を生成し、タスクに合った専門家エージェントを召喚します。
2. `/run-phase N` — **Builder** が成果物を生成し、**Validator** が docs/ と品質基準に照らして検証、
   NEEDS_REVISION なら最大2サイクルまで自動修正します。
3. `/finalize` — 成果物をパッケージ化し、`~/.sdd-knowledge/` にアーカイブして再利用スターターを抽出。
4. `/retrospective` — 構造化された振り返りを行い、機械可読な教訓として蓄積します。

蓄積した教訓は次のプロジェクトの `/init-task` と `/lessons` で自動的に効いてきます。

---

## コマンド一覧

| コマンド | 用途 |
|---|---|
| `/init-task` | プロジェクト初期化（仕様・手順・エージェント・メタデータの生成） |
| `/run-phase` | Builder / Validator によるフェーズ実行 |
| `/re-init-task` | 新イテレーション開始（差分ヒアリング＋フェーズ追加） |
| `/finalize` | 完了処理・アーカイブ・スターター抽出 |
| `/retrospective` | 構造化振り返りと教訓の蓄積 |
| `/lessons` | 過去の教訓の検索・表示 |
| `/update-docs` | `docs/` の充実度診断と対話的補完 |
| `/add-feature` | `.steering/` でのアドホック機能追加（フェーズ外） |
| `/eval` | 固定3シナリオでの spec-kit 自己評価 |
| `/plot` | 評価履歴のグラフ生成 |
| `/improve-toolkit` | spec-kit 自身の改良ループ |
| `/create-deck` | Markdown → .pptx スライド生成 |

Copilot CLI では `/コマンド名` がそのまま Agent Skill として起動します。
VS Code では同名のプロンプトファイルが `/コマンド名` として登録されます。

---

## ディレクトリ構成

```text
AGENTS.md                          # ★共通エントリポイント（中核ルールはここに集約）
CLAUDE.md                          # @AGENTS.md を参照するだけの薄いラッパ
.github/
├── copilot-instructions.md        # @AGENTS.md ＋ Copilot 固有の差分のみ
├── instructions/*.instructions.md # 常時適用ルール5種（applyTo: "**"、自己完結）
├── skills/<name>/SKILL.md         # ★手順の実体（12コマンド）。/name で起動
├── agents/*.agent.md              # サブエージェント5種（自動委譲 / /agent）
├── prompts/*.prompt.md            # VS Code 用の薄いラッパ（12個）
├── hooks/sdd-hooks.json           # Copilot CLI 用フック定義＋スクリプト4本
└── mcp.json.example               # MCP 設定の雛形（任意）
scripts/                           # 補助スクリプト（検証・知識ベース・参照チェック）
templates/                         # 生成テンプレ（team-roster.json, agents/, fragments/ 等）
eval/                              # 自己評価フレームワーク（3シナリオ＋ルーブリック）
docs/
├── copilot-setup.md               # ★チーム向けセットアップ手順
├── porting-diff.md                # ★Claude Code 版との差分・非対応機能一覧
└── rules-reference/               # ルールの詳細解説（必要時に参照）
```

**手順の実体は `.github/skills/` にしかありません。** `.github/prompts/` はそれを読ませるだけの
ラッパなので、手順を変えるときは SKILL.md を編集してください。

---

## セットアップ

最短：

```bash
git clone <this-repo-url> my-project
cd my-project && rm -rf .git && git init
chmod +x .github/hooks/*.py .github/hooks/*.sh
copilot            # または VS Code で開く
```

既存プロジェクトへの組み込み方、VS Code の設定、フックの有効化、権限運用、MCP の扱いは
**[`docs/copilot-setup.md`](docs/copilot-setup.md)** を参照してください。

導入後の健全性チェック：

```bash
python3 scripts/check_references.py
```

---

## Claude Code 版との違い

| 主な差分 | 内容 |
|---|---|
| スラッシュコマンド | Copilot CLI は `.github/prompts/` を読まない。CLI では Agent Skills が `/name` になる |
| フック | Copilot でも使えるが **CLI 限定**。イベント名が異なり、マッチャがない（`Stop` は `sessionEnd` で代替） |
| 権限設定 | `permissions.allow / ask / deny` に相当する宣言的設定は**存在しない**。CLI フラグと運用ルールで代替 |
| サンドボックス | 等価物なし |
| エージェント | `model` は CLI では無視、`memory` / `maxTurns` は等価物なし |

全項目は **[`docs/porting-diff.md`](docs/porting-diff.md)** にまとめています。

---

## 知識ベース（ローカル）

`~/.sdd-knowledge/` に以下が蓄積されます（リポジトリ外・ローカルのみ）。

- `starters/` — 再利用できるプロジェクト雛形
- `retrospectives/` — 振り返り（機械可読な教訓）
- `docs-archive/` — 完了プロジェクトのアーカイブ

Claude Code 版（`sdd_toolkit`）とスキーマが同一なので、両方を使っていても知見は共有されます。

---

## ライセンス / 由来

`sdd_toolkit_v12`（Claude Code 用 SDD toolkit）からの移植。移植の判断根拠と調査結果は
`docs/porting-diff.md` に記録しています。
