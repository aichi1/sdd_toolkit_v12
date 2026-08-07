---
description: 過去のレトロスペクティブから蓄積された学びを検索・表示する
argument-hint: カテゴリ名 / キーワード / --priority high（省略可）
agent: agent
---

# /lessons

**手順の実体は [`.github/skills/lessons/SKILL.md`](../skills/lessons/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/lessons/SKILL.md` を編集してください。

まず `.github/skills/lessons/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. ~/.sdd-knowledge/retrospectives/ のスキャン
2. フィルタ適用（カテゴリ・優先度・キーワード）
3. パターン分析（カテゴリ別・横断的インサイト）
4. 実行可能な推奨アクションの提示

引数（フィルタ）: ${input:args:カテゴリ名 / キーワード / --priority high（省略可）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
