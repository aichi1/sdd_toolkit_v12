---
description: SDD プロジェクトを初期化する（タスク分類 → docs/ 生成 → skills/ 作成 → 専門家エージェント召喚 → AGENTS.md / metadata.json）
argument-hint: タスクの説明（例: 社内向けの技術調査レポートを作りたい）
agent: agent
---

# /init-task

**手順の実体は [`.github/skills/init-task/SKILL.md`](../skills/init-task/SKILL.md) にあります。**
このプロンプトファイルは VS Code Copilot Chat 用の薄いラッパです。
手順を変更するときは、このファイルではなく `.github/skills/init-task/SKILL.md` を編集してください。

まず `.github/skills/init-task/SKILL.md` を読み込み、そこに書かれた手順に厳密に従って、以下を実行してください。

1. タスク分類（task_type の判定）
2. docs/ 生成（requirements.md, plan.md, team.md, _manifest.json ＋ カテゴリ固有ファイル）
3. skills/phase-{N}/SKILL.md の作成
4. 専門家エージェント召喚（templates/team-roster.json → .github/agents/<key>.agent.md）
5. AGENTS.md（プロジェクト仕様）と metadata.json の作成
6. 次に実行すべきコマンドの案内

引数（作りたいものの説明）: ${input:args:タスクの説明（例: 社内向けの技術調査レポートを作りたい）}

SKILL.md 中の `$ARGUMENTS` は、上の引数の値を指します。指定がなければ SKILL.md の既定動作に従ってください。
