---
description: docs/ 配下の仕様ドキュメントを対話的に充実させる
argument-hint: ファイル名 / gaps / validate（空なら全体診断）
agent: agent
---

# /update-docs

**手順の実体は [`.github/skills/update-docs/SKILL.md`](../skills/update-docs/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/update-docs/SKILL.md` を編集してください。

まず `.github/skills/update-docs/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. docs/ 配下の全ファイル読み込みと充実度診断
2. 未解決マーカー（TODO, 要確認 等）の洗い出し
3. skills/ が期待する情報との整合チェック
4. 優先度付きの改善提案
5. ユーザーとの対話による段階的充実化

引数（対象）: ${input:args:ファイル名 / gaps / validate（空なら全体診断）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
