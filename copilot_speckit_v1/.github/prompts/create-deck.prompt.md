---
description: Markdown ファイルから .pptx プレゼンテーションを生成し、画像化してビジュアル QA まで行う
argument-hint: 複数可、スペース区切り
agent: agent
---

# /create-deck

**手順の実体は [`.github/skills/create-deck/SKILL.md`](../skills/create-deck/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/create-deck/SKILL.md` を編集してください。

まず `.github/skills/create-deck/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. pptxgenjs など依存パッケージの確認
2. 入力 Markdown の読み込みとスライド構成の設計
3. scripts/slide_template.js のデザインシステム適用
4. Node.js スクリプト生成と実行
5. PDF/画像化してビジュアル QA、問題があれば修正して再実行

引数（Markdown ファイルのパス）: ${input:args:複数可、スペース区切り}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
