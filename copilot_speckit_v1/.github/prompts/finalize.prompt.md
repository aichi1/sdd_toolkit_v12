---
description: SDD プロジェクトの完了処理（パッケージ化 → アーカイブ → スターター抽出 → レポート生成）
argument-hint: --skip-archive / --skip-starter / --force（省略可）
agent: agent
---

# /finalize

**手順の実体は [`.github/skills/finalize/SKILL.md`](../skills/finalize/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/finalize/SKILL.md` を編集してください。

まず `.github/skills/finalize/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. 完了チェック（全フェーズのステータス確認）
2. 成果物パッケージ化
3. ~/.sdd-knowledge/docs-archive/ へのアーカイブ
4. スターターテンプレートの抽出・更新
5. finalization-report.md の生成
6. metadata.json を finalized に更新

引数（オプション）: ${input:args:--skip-archive / --skip-starter / --force（省略可）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
