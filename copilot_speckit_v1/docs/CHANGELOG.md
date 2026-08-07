# CHANGELOG

## v1.0.0 — 初版（sdd_toolkit_v12 からの移植）

Claude Code 用の SDD toolkit（`sdd_toolkit_v12`）を GitHub Copilot 向けに移植した初版。

### 追加

- `AGENTS.md` — エージェント非依存の共通エントリポイント。中核ルールをここに集約
- `CLAUDE.md` / `.github/copilot-instructions.md` — `@AGENTS.md` を参照する薄いラッパ
- `.github/instructions/*.instructions.md` × 5 — `applyTo: "**"` の常時適用ルール
- `.github/skills/<name>/SKILL.md` × 12 — 手順の実体。Copilot CLI では `/<name>` で直接起動
- `.github/agents/*.agent.md` × 5 — sdd-planner / sdd-researcher / sdd-builder / sdd-validator / knowledge-curator
- `.github/prompts/*.prompt.md` × 12 — VS Code Copilot Chat 用の薄いラッパ
- `.github/hooks/sdd-hooks.json` ＋ スクリプト4本 — Copilot CLI 用フック
- `.github/mcp.json.example` — MCP 設定の雛形（任意）
- `scripts/check_references.py` — `@参照` とリンク切れ、frontmatter 必須項目の一括チェッカ
- `docs/copilot-setup.md` — チーム向けセットアップ手順
- `docs/porting-diff.md` — Claude Code 版との差分・非対応機能一覧

### 移植にあたっての変更

- スラッシュコマンドを二段構えにした。Copilot CLI は `.github/prompts/` を読まないため、
  CLI / coding agent では Agent Skills が `/<name>` を担い、VS Code ではプロンプトファイルが担う。
  手順の実体は SKILL.md 側にのみ置き、二重管理を避けた
- フックのイベント名を Copilot に合わせた（`Stop` → `sessionEnd` ほか）。
  Copilot にはマッチャがないため、対象の絞り込みを各スクリプト冒頭に実装した
- stdin ペイロードのフィールド名差（`tool_name` → `toolName`）を吸収する
  `.github/hooks/_payload.py` を追加した
- エージェント frontmatter の `tools` を Copilot の別名（read / search / edit / execute / agent）に変換し、
  `model` / `memory` / `maxTurns` を削除した
- `/init-task` の専門家エージェント生成先を `.github/agents/<key>.agent.md` に変更した
  （`.agent.md` 拡張子が必須、サブディレクトリ探索は非保証のため）
- `knowledge-curator` の agent memory を `~/.sdd-knowledge/curator-history.md` にファイルで代替した

### 移植していないもの

`permissions`（allow / ask / deny）、`sandbox`、フックの matcher、`Stop` イベント、
VS Code / coding agent でのフック、エージェントの `memory` / `maxTurns`。
理由と代替策は `docs/porting-diff.md` を参照。
