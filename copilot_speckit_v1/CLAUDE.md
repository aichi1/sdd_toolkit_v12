# CLAUDE.md

このリポジトリの共通ルールは `AGENTS.md` に集約されています。ここでは重複記述しません。

@AGENTS.md

---

## 補足（Claude Code で使う場合）

`copilot_speckit_v1` は GitHub Copilot 向けの spec-kit ですが、Claude Code も
`AGENTS.md` と `@参照` を解釈するため、そのまま読み込めます。ただし以下は Copilot 専用です。

| 要素 | Claude Code での扱い |
|---|---|
| `.github/skills/*/SKILL.md` | 読める（ただし `/name` のスラッシュコマンドとしては登録されない） |
| `.github/agents/*.agent.md` | サブエージェントとしては自動登録されない |
| `.github/instructions/*.instructions.md` | 自動適用されない（明示的に読ませる必要がある） |
| `.github/hooks/sdd-hooks.json` | 発火しない（Claude Code は `.claude/settings.json` の hooks を使う） |

Claude Code をメインで使う場合は、本家の `sdd_toolkit`（`.claude/` 構成）を利用してください。
両者の対応関係は `docs/porting-diff.md` にまとめてあります。
