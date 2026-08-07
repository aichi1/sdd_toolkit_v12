#!/usr/bin/env python3
"""
preToolUse hook: outputs/ にファイルを書き込む前に docs/ の存在と最低限の仕様ファイルを確認する。

- docs/ が存在しない → 警告（ブロックはしない）
- docs/_manifest.json がある → required_files を検証し、不足があれば警告
- manifest がない → docs/ に Markdown が1つでもあればOK（空なら警告）

Copilot の preToolUse にはマッチャがないため、対象ツール・対象パスの絞り込みは
このスクリプト自身で行う。常に exit 0（＝ツール実行はブロックしない）。
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _payload import read_payload, tool_name, target_path, project_root, notify  # noqa: E402

MANIFEST = "_manifest.json"
WRITE_TOOLS = ("write", "edit", "create", "str_replace", "apply_patch", "multiedit")


def is_write_tool(name: str) -> bool:
    n = name.lower()
    return any(w in n for w in WRITE_TOOLS)


def main():
    data = read_payload()

    # 書き込み系ツール以外は対象外
    if not is_write_tool(tool_name(data)):
        sys.exit(0)

    path = target_path(data).replace("\\", "/")
    root = project_root(data)

    # outputs/ 配下への書き込みだけを対象にする（絶対パスでも判定できるようにする）
    rel = path
    try:
        if os.path.isabs(path):
            rel = os.path.relpath(path, root).replace("\\", "/")
    except Exception:
        pass
    if not rel.startswith("outputs/"):
        sys.exit(0)

    docs_dir = os.path.join(root, "docs")
    manifest_path = os.path.join(docs_dir, MANIFEST)

    if not os.path.isdir(docs_dir):
        notify("⚠️ SDD警告: docs/ ディレクトリが存在しません。仕様なしで成果物を生成しています。"
               "先に /init-task で仕様を定義することを推奨します。")
        sys.exit(0)

    # manifest がある場合は required_files を検証
    if os.path.isfile(manifest_path):
        try:
            import json
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
            required = manifest.get("required_files", []) or []
            missing = [p for p in required if not os.path.isfile(os.path.join(docs_dir, p))]
            if missing:
                notify("⚠️ SDD警告: docs/ に不足ファイルがあります（" + ", ".join(missing) + "）。"
                       "/init-task の仕様ファイル作成が未完了か、削除された可能性があります。")
        except Exception:
            notify("⚠️ SDD警告: docs/_manifest.json の読み取りに失敗しました。仕様ファイルの整合性を確認してください。")
        sys.exit(0)

    # manifest がない場合は、docs/ に Markdown が1つでもあればOK（空なら警告）
    if len(glob.glob(os.path.join(docs_dir, "*.md"))) == 0:
        notify("⚠️ SDD警告: docs/ は存在しますが仕様ファイル（*.md）が見つかりません。"
               "先に /init-task で仕様を定義することを推奨します。")

    sys.exit(0)


if __name__ == "__main__":
    main()
