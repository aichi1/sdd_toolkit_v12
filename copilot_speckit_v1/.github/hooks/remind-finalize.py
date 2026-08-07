#!/usr/bin/env python3
"""
sessionEnd hook:
- outputs/ に成果物があるのに /finalize が未実行の場合にリマインドする。
- README-deliverables.md を /finalize 済みのマーカーとして扱う。

（Claude Code の Stop hook 相当。Copilot には Stop がないため sessionEnd に割り当てている）
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _payload import read_payload, project_root, notify  # noqa: E402

IGNORE_FILES = {".DS_Store", "Thumbs.db"}


def main():
    data = read_payload()
    root = project_root(data)

    outputs_dir = os.path.join(root, "outputs")
    deliverables_readme = os.path.join(outputs_dir, "README-deliverables.md")

    if not os.path.isdir(outputs_dir):
        sys.exit(0)

    # /finalize 済みなら何もしない
    if os.path.isfile(deliverables_readme):
        sys.exit(0)

    # outputs/ 配下を再帰的に走査して成果物ファイル数を数える（サブディレクトリも含む）
    output_files = []
    for root_dir, _dirs, files in os.walk(outputs_dir):
        for f in files:
            if f in IGNORE_FILES:
                continue
            full = os.path.join(root_dir, f)
            # /finalize マーカーは除外
            if os.path.abspath(full) == os.path.abspath(deliverables_readme):
                continue
            output_files.append(full)

    if len(output_files) == 0:
        sys.exit(0)

    notify(f"💡 outputs/ に {len(output_files)} 件の成果物があります。"
           "完了したら /finalize でパッケージングと教訓の蓄積をお忘れなく。")
    sys.exit(0)


if __name__ == "__main__":
    main()
