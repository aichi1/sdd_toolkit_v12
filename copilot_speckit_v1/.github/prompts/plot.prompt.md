---
description: 評価履歴からレーダーチャートと時系列グラフを生成・更新する
agent: agent
---

# /plot

**手順の実体は [`.github/skills/plot/SKILL.md`](../skills/plot/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/plot/SKILL.md` を編集してください。

まず `.github/skills/plot/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. python3 eval/make_plots.py の実行
2. eval/plots/radar_latest.png と timeseries_overall.png の確認
3. matplotlib が無い場合は eval/plots/README.md に理由と導入方法を記載

このコマンドは引数を取りません。
