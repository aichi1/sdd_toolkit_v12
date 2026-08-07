---
description: Builder / Validator パターンで SDD のフェーズを実行する（生成 → 検証 → 修正ループ）
argument-hint: 1 | 1-3 | all（--review-only / --no-validation / --checkpoint / --batch）
agent: agent
---

# /run-phase

**手順の実体は [`.github/skills/run-phase/SKILL.md`](../skills/run-phase/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/run-phase/SKILL.md` を編集してください。

まず `.github/skills/run-phase/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. 環境チェック（docs/, skills/, AGENTS.md, metadata.json の存在確認）
2. 依存関係バリデーション（前フェーズの完了確認）
3. sdd-builder に委譲して成果物を生成（outputs/phase-{N}/）
4. scripts/validate-outputs.py による事前チェック
5. sdd-validator に委譲して docs/ と SKILL.md の要件を検証
6. 修正ループ（NEEDS_REVISION なら最大2回まで自動修正）
7. metadata.json 更新と次アクション提示

引数（フェーズ指定）: ${input:args:1 | 1-3 | all（--review-only / --no-validation / --checkpoint / --batch）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
