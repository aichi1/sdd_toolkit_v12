---
description: spec-kit 自身を改良し、同じ固定シナリオで評価して改善を数値で示す
argument-hint: 例: v1.1
agent: agent
---

# /improve-toolkit

**手順の実体は [`.github/skills/improve-toolkit/SKILL.md`](../skills/improve-toolkit/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/improve-toolkit/SKILL.md` を編集してください。

まず `.github/skills/improve-toolkit/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. 改善テーマを1つに絞る
2. 変更案の実装（必要なら docs/ と templates/ も修正）
3. eval/rubric.json のどの軸が上がるか仮説を明記
4. /eval <iteration_id> の実行
5. eval/reports/<date>_<id>.md への記録
6. docs/CHANGELOG.md への追記

引数（iteration_id）: ${input:args:例: v1.1}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
