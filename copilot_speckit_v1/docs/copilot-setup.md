# セットアップ手順（チーム向け）

`copilot_speckit_v1` を自分の環境で動かすための手順です。所要 10〜15 分。

---

## 0. 前提

- GitHub Copilot のライセンス（Individual / Business / Enterprise のいずれか）
- Python 3.9 以上（補助スクリプト用）
- Node.js（`/create-deck` を使う場合のみ）

---

## 1. spec-kit をプロジェクトに配置する

### パターンA：この spec-kit を土台に新規プロジェクトを始める

```bash
git clone <this-repo-url> my-project
cd my-project
rm -rf .git && git init
```

### パターンB：既存プロジェクトに spec-kit だけ持ち込む

```bash
# 既存プロジェクトのルートで
git clone --depth 1 <this-repo-url> /tmp/speckit
cp -r /tmp/speckit/.github/skills   .github/
cp -r /tmp/speckit/.github/agents   .github/
cp -r /tmp/speckit/.github/prompts  .github/
cp -r /tmp/speckit/.github/instructions .github/
cp -r /tmp/speckit/.github/hooks    .github/
cp    /tmp/speckit/.github/copilot-instructions.md .github/
cp    /tmp/speckit/AGENTS.md .
cp -r /tmp/speckit/scripts /tmp/speckit/templates /tmp/speckit/eval .
```

既に `AGENTS.md` や `.github/copilot-instructions.md` がある場合は上書きせず、
自分のファイルの末尾に `@AGENTS.md` 相当の参照を足すか、内容をマージしてください。

---

## 2. VS Code（Copilot Chat）で使う

1. VS Code と GitHub Copilot Chat 拡張を最新にする。
2. ワークスペースをリポジトリのルートで開く（`.github/` がワークスペース直下に見えること）。
3. Copilot Chat を開き、入力欄で `/` を打つ。`/init-task` などが候補に出れば認識されている。
4. 出てこない場合の確認ポイント：
   - ファイル名が `.github/prompts/<name>.prompt.md` になっているか（`.prompt.md` が必要）
   - リポジトリのルートでワークスペースを開いているか。モノレポでサブディレクトリを開いている場合は
     設定 `chat.useCustomizationsInParentRepositories` を有効にする
   - 追加の場所に置きたい場合は設定 `chat.promptFilesLocations` にパスを足す
5. 常時ルール（`.github/instructions/*.instructions.md`）は `applyTo: "**"` により自動適用される。
   チャットの参照一覧に出ていれば読み込まれている。

### VS Code 側の推奨設定（`.vscode/settings.json`）

```jsonc
{
  // モノレポでサブフォルダを開く場合に、親リポジトリの .github/ を探索する
  "chat.useCustomizationsInParentRepositories": true
}
```

---

## 3. Copilot CLI で使う

```bash
npm install -g @github/copilot     # 未インストールの場合
cd /path/to/my-project
copilot
```

対話セッションで：

```
/init-task 社内向けの技術調査レポートを作りたい
/run-phase 1
/finalize
```

非対話（CI などで回す場合）：

```bash
copilot -p "/run-phase 1-3" --allow-tool 'shell(python3 scripts/*)'
```

### 確認コマンド

| 目的 | コマンド |
|---|---|
| スキルが認識されているか | セッション内で `/skills list`（または `/` を打って候補を見る） |
| エージェントが認識されているか | セッション内で `/agent` |
| カスタム指示を一時的に切る | `copilot --no-custom-instructions` |

`/init-task` などが候補に出ない場合は、`.github/skills/<name>/SKILL.md` の frontmatter に
`name` と `description` が両方あるか確認してください（両方必須）。

---

## 4. フックを有効にする（Copilot CLI のみ）

`.github/hooks/sdd-hooks.json` はリポジトリに置くだけで CLI が読み込みます。
スクリプトに実行権限を付けてください。

```bash
chmod +x .github/hooks/*.py .github/hooks/*.sh
```

有効になるフック：

| イベント | スクリプト | 動作 |
|---|---|---|
| `sessionStart` | `session-start-info.py` | `~/.sdd-knowledge/` のスターター・教訓件数を表示 |
| `preToolUse` | `check-docs-exist.py` | `outputs/` へ書き込む前に `docs/` の整備状況を警告（ブロックはしない） |
| `postToolUse` | `post-phase-complete.sh` | `outputs/` 書き込み後に再利用コンポーネント候補を抽出 |
| `sessionEnd` | `remind-finalize.py` | 成果物があるのに `/finalize` 未実行ならリマインド |

**VS Code と coding agent ではフックは発火しません。** 詳細は `docs/porting-diff.md` を参照。

個人設定として全プロジェクトに効かせたい場合は `~/.copilot/hooks/` に同じ JSON を置きます
（その場合スクリプトのパスは絶対パスにしてください）。

---

## 5. Python 依存関係

コアのワークフロー（`/init-task` 〜 `/retrospective`）は**標準ライブラリのみ**で動きます。
以下は任意機能を使う場合のみ必要です。

```bash
python3 -m pip install matplotlib      # /plot のグラフ生成
python3 -m pip install fastapi uvicorn # scripts/mcp_server/ の REST API（後述）
```

matplotlib が無い場合、`/eval` の JSON / CSV 集計は動作し、PNG 生成だけがスキップされます。

---

## 6. MCP について（動作保証の範囲）

**注意：`scripts/mcp_server/` は名前に反して MCP プロトコルのサーバーではありません。**
中身は FastAPI の REST API（`127.0.0.1:8741` にバインド）で、知識ベースへの検索・推薦を
HTTP で提供するものです。そのため **Copilot の MCP 設定にそのまま登録することはできません**。

| 使い方 | 可否 |
|---|---|
| `python3 -m scripts.mcp_server.server` で起動し、スクリプトや curl から叩く | ✅ 動く |
| Copilot の MCP サーバーとして登録する | ❌ 不可（MCP プロトコル非対応） |
| MCP ラッパを別途書いて登録する | ⚠️ 可能だが本リポジトリには含まれない |

Copilot 側で MCP サーバーを使いたい場合の設定ファイルの置き場所は次のとおりです。

| スコープ | パス |
|---|---|
| 個人（全プロジェクト） | `~/.copilot/mcp-config.json` |
| リポジトリ | `.github/mcp.json`（他に `.mcp.json` / `.vscode/mcp.json` も読まれる） |

雛形として `.github/mcp.json.example` を同梱しています。使う場合は `.github/mcp.json` にリネームしてください。
このリポジトリの機能は MCP に依存していないので、設定しなくてもすべてのコマンドが動きます。

---

## 7. 権限まわりの運用ルール

Copilot には Claude Code の `permissions.allow / ask / deny` に相当する宣言的な設定がありません。
そのため次の方針で運用します。

1. **無確認で使ってよいツールはスキル側で宣言する** — `SKILL.md` の `allowed-tools`。
2. **禁止事項は指示として明記する** — `.github/copilot-instructions.md` の「破壊的操作」節。
3. **CI や自動実行では CLI フラグで縛る** — 例：

   ```bash
   copilot -p "/run-phase all" \
     --allow-tool 'shell(python3 scripts/*)' \
     --deny-tool  'shell(rm *)' \
     --deny-tool  'shell(git push *)'
   ```

4. `--allow-all-tools` は対話的にレビューできる場面以外では使わないでください。

---

## 8. 動作確認チェックリスト

フレッシュクローン直後に、以下がすべて通ることを確認してください。

- [ ] VS Code のチャットで `/` を打つと `/init-task` 〜 `/create-deck` の12個が候補に出る
- [ ] Copilot CLI で `/agent` を実行すると `sdd-builder` `sdd-validator` などが並ぶ
- [ ] Copilot CLI のセッション開始時に `📚 SDD知識ベース:` の行が出る
      （`~/.sdd-knowledge/` が空なら無言なのが正常）
- [ ] `python3 scripts/validate-outputs.py --help` がエラーなく動く
- [ ] `AGENTS.md` の `@` 参照と各ドキュメントのリンク切れがない
      （`python3 scripts/check_references.py` で一括チェックできる）
