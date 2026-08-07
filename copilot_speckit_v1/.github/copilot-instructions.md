# SDD spec-kit — Copilot 用エントリポイント

共通ルールはすべて `AGENTS.md` にあります。ここでは重複記述せず、参照だけします。

@AGENTS.md

---

## このファイルの役割

`AGENTS.md` が中核（エージェント非依存の共通仕様）で、このファイルは
**GitHub Copilot 固有の差分だけ**を書く場所です。同じ内容を二重管理しません。

- Copilot CLI / coding agent … `AGENTS.md` を直接読みます。
- VS Code Copilot Chat … このファイルを読み、上の `@AGENTS.md` 参照で共通ルールを取り込みます。
- 常時適用ルール（`.github/instructions/*.instructions.md`）は `applyTo: "**"` により
  上記いずれの経路でも自動で読み込まれるため、ここにも `AGENTS.md` にも再掲しません。

## Copilot 固有の運用メモ

1. **スキルの呼び出し**
   `/init-task` のように `/<skill-name>` で明示起動できます。プロンプト中のどこに書いても構いません。
   description が合致すれば明示指定なしでも自動起動します。

2. **エージェントへの委譲は隔離コンテキスト**
   サブエージェントに会話履歴は引き継がれません。起動時に必ず対象ファイルのパスを明示してください
   （例：`skills/phase-02/SKILL.md`、`docs/`、`outputs/phase-01/`）。

3. **VS Code のプロンプトファイル**
   `.github/prompts/*.prompt.md` は VS Code 専用の薄いラッパです。手順の実体は
   `.github/skills/<name>/SKILL.md` にあります。**手順を変更するときは SKILL.md 側を直してください。**

4. **フック**
   `.github/hooks/sdd-hooks.json` は **Copilot CLI でのみ**有効です。
   VS Code / coding agent では発火しないため、フックが担っている警告（docs/ 未整備の検出、
   `/finalize` のリマインド）は人間または本ルールへの明示指示で代替してください。

5. **破壊的操作**
   `outputs/` 以外の削除、`git push --force`、認証情報ファイルの読み取りは行わないでください。
   Copilot にはツール権限の宣言的な allow/deny リストがないため、これは運用ルールとして守ります
   （CLI では `--deny-tool` / `--allow-tool` で部分的に強制できます。`docs/copilot-setup.md` 参照）。
