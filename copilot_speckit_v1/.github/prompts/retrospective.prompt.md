---
description: 構造化された振り返りを行い、機械可読な学びを知識ベースに蓄積する
argument-hint: 重点的に振り返りたい観点（省略可）
agent: agent
---

# /retrospective

**手順の実体は [`.github/skills/retrospective/SKILL.md`](../skills/retrospective/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/retrospective/SKILL.md` を編集してください。

まず `.github/skills/retrospective/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. プロジェクトデータ収集（metadata.json / 検証レポート / finalization-report.md）
2. ユーザーとの構造化対話（成功・課題・発見）
3. 教訓の抽出とパターン認識
4. ./retrospective.md（人間用）の生成
5. ~/.sdd-knowledge/retrospectives/ への JSON 保存（機械用）
6. summary.json の更新

引数（注目したい領域）: ${input:args:重点的に振り返りたい観点（省略可）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
