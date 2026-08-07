---
description: 現イテレーション完了後に新しいイテレーションを開始する（差分ヒアリング＋フェーズ追加）
argument-hint: 追加要件や変更点（省略可）
agent: agent
---

# /re-init-task

**手順の実体は [`.github/skills/re-init-task/SKILL.md`](../skills/re-init-task/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/re-init-task/SKILL.md` を編集してください。

まず `.github/skills/re-init-task/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. 前提条件チェック（全フェーズが completed / completed_with_issues か）
2. 現在のステータスサマリ表示
3. 差分インテーク（最大5問：目的・機能・制約・フェーズ数・docs）
4. docs/ の更新（上書きではなく追記）
5. 新フェーズの skills/ 作成（フェーズ番号は連番で継続）
6. metadata.json への iterations[] 追加と phase_count 更新
7. iteration_history.md と AGENTS.md の更新

引数（追加・変更したい内容）: ${input:args:追加要件や変更点（省略可）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
