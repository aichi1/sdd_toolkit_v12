---
description: 固定3シナリオで spec-kit を自己評価し、スコアを履歴化してグラフを更新する
argument-hint: 例: v1.0（--review-interval N を付けられる）
agent: agent
---

# /eval

**手順の実体は [`.github/skills/eval/SKILL.md`](../skills/eval/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/eval/SKILL.md` を編集してください。

まず `.github/skills/eval/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. eval/rubric.json と eval/SCORING_GUIDE.md の確認
2. eval/scenarios/ の3シナリオ（T1/T2/T3）の理解
3. 7軸を 0〜5 で採点し eval/runs/<id>/<scenario>/score.json に保存
4. python3 eval/aggregate.py --iteration <id> で集計・履歴化
5. eval/reports/<date>_<id>.md にレポート作成
6. シナリオ見直しトリガーの判定

引数（iteration_id）: ${input:args:例: v1.0（--review-interval N を付けられる）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
