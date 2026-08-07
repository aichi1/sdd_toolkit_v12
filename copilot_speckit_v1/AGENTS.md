# copilot_speckit_v1 — Spec-Driven Development spec-kit for GitHub Copilot

このリポジトリは **仕様駆動開発（Spec-Driven Development, SDD）** を GitHub Copilot 上で回すための
spec-kit です。VS Code の Copilot Chat / Copilot CLI / Copilot coding agent の3面で動きます。

> 目的：Copilot に「順序立てて考え、仕様を作り、成果物を生成し、検証し、最後に知見を残す」運用を定着させる。

このファイルは**エージェント非依存の共通エントリポイント**です。
`CLAUDE.md` と `.github/copilot-instructions.md` はこのファイルを参照する薄いラッパであり、
中核ルールをここ以外に二重記述しません。

---

## 1. 中核となる考え方

| 概念 | 置き場所 | 役割 |
|---|---|---|
| **What（仕様）** | `docs/` | 背景・要件・スコープ・対象読者・フォーマット。**唯一の正**。 |
| **How（手順）** | `skills/phase-{NN}/SKILL.md` | そのフェーズを実行する具体的手順と品質基準。docs/ を参照するが複製しない。 |
| **成果物** | `outputs/phase-{NN}/` | Builder の出力。`.metadata.json` と `.validation/` を伴う。 |
| **知識ベース** | `~/.sdd-knowledge/` | 完了プロジェクトのアーカイブ・スターター・教訓（ローカル、リポジトリ外）。 |

**Builder / Validator 分離**が本 spec-kit の背骨です。生成する主体と検証する主体を必ず分け、
検証者はファイルを書き換えず、生成者は自己採点しません。

---

## 2. ワークフロー

```
/init-task  →  /run-phase N  →  [ /re-init-task  →  /run-phase N ]*  →  /finalize  →  /retrospective
```

補助コマンド：`/update-docs`（仕様の充実化・実行前に推奨）、`/lessons`（過去の教訓の参照）、
`/add-feature`（フェーズ外のアドホック実装）、`/eval` `/plot` `/improve-toolkit`（spec-kit 自身の自己評価・自己改善）、
`/create-deck`（Markdown → pptx）。

---

## 3. コマンド一覧

すべて `.github/skills/<name>/SKILL.md` に手順の実体があり、`/<name>` で呼び出せます。

| コマンド | 何をするか | 実体 |
|---|---|---|
| `/init-task` | プロジェクト初期化（docs/・skills/・専門家エージェント・metadata.json） | `.github/skills/init-task/SKILL.md` |
| `/run-phase` | Builder / Validator でフェーズ実行 | `.github/skills/run-phase/SKILL.md` |
| `/re-init-task` | 新イテレーション開始（差分ヒアリング＋フェーズ追加） | `.github/skills/re-init-task/SKILL.md` |
| `/finalize` | 完了処理・アーカイブ・スターター抽出 | `.github/skills/finalize/SKILL.md` |
| `/retrospective` | 構造化振り返り・教訓の機械可読保存 | `.github/skills/retrospective/SKILL.md` |
| `/lessons` | 蓄積された教訓の検索・表示 | `.github/skills/lessons/SKILL.md` |
| `/update-docs` | docs/ の充実度診断と対話的補完 | `.github/skills/update-docs/SKILL.md` |
| `/add-feature` | `.steering/` でのアドホック機能追加 | `.github/skills/add-feature/SKILL.md` |
| `/eval` | 固定3シナリオでの自己評価 | `.github/skills/eval/SKILL.md` |
| `/plot` | 評価履歴のグラフ生成 | `.github/skills/plot/SKILL.md` |
| `/improve-toolkit` | spec-kit 自身の改良ループ | `.github/skills/improve-toolkit/SKILL.md` |
| `/create-deck` | Markdown からスライド生成 | `.github/skills/create-deck/SKILL.md` |

---

## 4. エージェント

`.github/agents/*.agent.md` に定義。description に合致すると Copilot が自動でサブエージェントに委譲します。
明示指定は CLI では `/agent`、非対話では `copilot --agent <name>`、VS Code ではチャットのエージェント選択。

| エージェント | 役割 | tools |
|---|---|---|
| `sdd-planner` | タスク分類・フェーズ分解・docs/ 構造設計 | read, search, execute |
| `sdd-researcher` | `~/.sdd-knowledge/` からの過去知見の探索 | read, search |
| `sdd-builder` | SKILL.md に従った成果物生成 | read, search, edit, execute |
| `sdd-validator` | 要件・品質基準との照合と判定（**書き換え禁止**） | read, search |
| `knowledge-curator` | 知識ベースの改善候補生成 | read, search, edit |

`/init-task` はタスク種別に応じて `templates/agents/` から専門家エージェント
（`sdd-security-reviewer` など）を `.github/agents/<key>.agent.md` として追加生成します。

---

## 5. 常時適用されるルール

以下は `.github/instructions/*.instructions.md` に置かれ、`applyTo: "**"` により自動で読み込まれます。
**このファイルには再掲しません**（二重管理を避けるため）。

- `core-workflow.instructions.md` — コマンド順序、各コマンドの入出力、フェーズ依存、エラー処理
- `builder-validator.instructions.md` — 責務分離、検証判定、修正サイクル上限、引き継ぎ
- `file-conventions.instructions.md` — ディレクトリ構造、命名規則、主要ファイル、禁止事項
- `quality-standards.instructions.md` — 品質ゲート Gate 0〜3、フェーズ別追加チェック、例外規定
- `session-guidelines.instructions.md` — セッション開始・終了の手順

より詳しい解説は `docs/rules-reference/` にあります（自動読み込みはされません。必要時に参照）。

---

## 6. 補助スクリプト

| スクリプト | 用途 |
|---|---|
| `scripts/validate-outputs.py` | `/run-phase` の事前チェック（成果物の存在・メタデータ検証） |
| `scripts/generate_context.py` | 知識ベースから関連コンテキストを生成 |
| `scripts/search_knowledge.py` / `build_search_index.py` | 過去プロジェクト・教訓の検索 |
| `scripts/extract_components.py` | 再利用可能コンポーネントの候補抽出（postToolUse フックから自動実行） |
| `scripts/knowledge_curator.py` / `promote_candidates.py` / `registry_utils.py` | 知識ベースの更新・候補の昇格 |
| `eval/aggregate.py` / `eval/make_plots.py` | 自己評価の集計とグラフ生成 |

---

## 7. 守るべき最低限のこと

1. **docs/ が無い状態で outputs/ を作らない。** 仕様が先、成果物が後。
2. **Validator はファイルを書き換えない。** 指摘だけを `.validation/report.md` に書く。
3. **Builder は指摘された箇所だけ直す。**「ついでに」の改変をしない。
4. **自動修正は最大2サイクル。** 3回目も失敗したら止めてユーザーに根本原因を報告する。
5. **フェーズ番号は連番。** 欠番を作らない（`phase-01`, `phase-02`, ...）。
6. **不明点は推測せず質問する。**

---

## 8. セットアップ

チーム向けの導入手順は `docs/copilot-setup.md` を参照してください。
Claude Code 版（`sdd_toolkit`）との差分・非対応機能の一覧は `docs/porting-diff.md` にあります。
