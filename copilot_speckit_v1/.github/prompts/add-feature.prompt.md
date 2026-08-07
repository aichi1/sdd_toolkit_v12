---
description: 計画外の機能追加を .steering/ で管理し、tasklist.md を完全消化するまで自律実装する
argument-hint: 例: ユーザープロフィール編集
agent: agent
---

# /add-feature

**手順の実体は [`.github/skills/add-feature/SKILL.md`](../skills/add-feature/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/add-feature/SKILL.md` を編集してください。

まず `.github/skills/add-feature/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. .steering/[日付]-[機能名]/ の作成と3ファイル（requirements / design / tasklist）の初期化
2. プロジェクト理解と SDD 知識ベースの活用
3. requirements.md → design.md → tasklist.md の順で作成
4. tasklist.md のタスクを上から順に実装し、完了ごとにチェック
5. 全タスク消化まで中断せず自律実行

引数（機能名）: ${input:args:例: ユーザープロフィール編集}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
