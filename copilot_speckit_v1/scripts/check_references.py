#!/usr/bin/env python3
"""spec-kit の内部参照と frontmatter の健全性をチェックする。

チェック内容:
  1. `@相対パス` 参照（AGENTS.md / copilot-instructions.md / CLAUDE.md）の参照先が存在するか
  2. `*.instructions.md` に `@参照` が書かれていないか（Copilot は展開しないため）
  3. Markdown リンク `[...](相対パス)` の参照先が存在するか
  4. 本文中でバッククォート引用されたリポジトリ内パスが存在するか
  5. skills / agents / prompts の frontmatter 必須フィールド

使い方:
    python3 scripts/check_references.py           # チェックのみ（問題があれば exit 1）
    python3 scripts/check_references.py --quiet   # エラーだけ表示
"""
from __future__ import annotations

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AT_REF = re.compile(r'(?<![\w`])@([A-Za-z0-9_./\-]+\.(?:md|json|ya?ml|py|sh|js))')
MD_LINK = re.compile(r'\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)')
CODE_PATH = re.compile(r'`([A-Za-z0-9_][A-Za-z0-9_./\-]*\.(?:md|json|ya?ml|py|sh|js))`')

# 生成物・実行時にしか存在しないパスは除外する
RUNTIME_ONLY = (
    'docs/', 'skills/', 'outputs/', 'eval/runs/', 'eval/history/', 'eval/reports/',
    'eval/plots/', '.steering/', '.validation/', 'metadata.json', 'AGENTS.md',
    'retrospective.md', 'finalization-report.md', 'iteration_history.md',
    '.metadata.json', 'CLAUDE.md', 'GEMINI.md', 'README-deliverables.md',
    'generate_slides.js', 'output.pptx', 'report.md', 'summary.json',
    'registry.json', 'candidates.jsonl', 'curator-history.md',
)


def is_runtime_only(path: str) -> bool:
    p = path.lstrip('./')
    return any(p.startswith(r) or p.endswith('/' + r) or p == r for r in RUNTIME_ONLY)


def md_files() -> list[str]:
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for f in files:
            if f.endswith('.md'):
                out.append(os.path.join(base, f))
    return sorted(out)


def check_frontmatter(errors: list[str]) -> None:
    def fm_of(path: str) -> dict[str, str]:
        text = open(path, encoding='utf-8').read()
        if not text.startswith('---'):
            return {}
        block = text.split('---', 2)[1]
        fm = {}
        for line in block.strip().split('\n'):
            if ':' in line and not line.startswith(' '):
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip()
        return fm

    skills_dir = os.path.join(ROOT, '.github', 'skills')
    for name in sorted(os.listdir(skills_dir)) if os.path.isdir(skills_dir) else []:
        p = os.path.join(skills_dir, name, 'SKILL.md')
        if not os.path.isfile(p):
            errors.append(f'skills: {name}/SKILL.md がありません')
            continue
        fm = fm_of(p)
        for key in ('name', 'description'):
            if not fm.get(key):
                errors.append(f'skills/{name}/SKILL.md: frontmatter に {key} がありません（必須）')
        if fm.get('name') and fm['name'] != name:
            errors.append(f'skills/{name}/SKILL.md: name "{fm["name"]}" がディレクトリ名と一致しません')

    agents_dir = os.path.join(ROOT, '.github', 'agents')
    for f in sorted(os.listdir(agents_dir)) if os.path.isdir(agents_dir) else []:
        if not f.endswith('.md'):
            continue
        if not f.endswith('.agent.md'):
            errors.append(f'agents/{f}: 拡張子は .agent.md である必要があります')
            continue
        fm = fm_of(os.path.join(agents_dir, f))
        if not fm.get('description'):
            errors.append(f'agents/{f}: frontmatter に description がありません（必須）')

    prompts_dir = os.path.join(ROOT, '.github', 'prompts')
    for f in sorted(os.listdir(prompts_dir)) if os.path.isdir(prompts_dir) else []:
        if not f.endswith('.md'):
            continue
        if not f.endswith('.prompt.md'):
            errors.append(f'prompts/{f}: 拡張子は .prompt.md である必要があります')
            continue
        if not fm_of(os.path.join(prompts_dir, f)).get('description'):
            errors.append(f'prompts/{f}: frontmatter に description がありません（必須）')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()

    errors: list[str] = []
    checked = 0

    for path in md_files():
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding='utf-8').read()
        base = os.path.dirname(path)

        # 1) @参照
        for ref in AT_REF.findall(text):
            checked += 1
            if ref.startswith('/') or ref.startswith('~'):
                errors.append(f'{rel}: @参照 "{ref}" は絶対パス/ホーム参照のため展開されません')
                continue
            if not os.path.isfile(os.path.join(ROOT, ref)):
                errors.append(f'{rel}: @参照 "{ref}" の参照先が存在しません')

        # 2) instructions では @参照を使わない
        if rel.endswith('.instructions.md'):
            body = re.sub(r'<!--.*?-->', '', text, flags=re.S)
            if AT_REF.search(body):
                errors.append(f'{rel}: *.instructions.md では @参照が展開されません。自己完結で記述してください')

        # 3) Markdown リンク
        for link in MD_LINK.findall(text):
            if link.startswith(('http://', 'https://', 'mailto:')):
                continue
            checked += 1
            target = os.path.normpath(os.path.join(base, link))
            if not os.path.exists(target) and not is_runtime_only(link):
                errors.append(f'{rel}: リンク "{link}" の参照先が存在しません')

        # 4) バッククォート内のリポジトリ内パス
        for cand in CODE_PATH.findall(text):
            if is_runtime_only(cand) or '{' in cand or '*' in cand or '<' in cand:
                continue
            if not cand.startswith(('.github/', 'scripts/', 'templates/', 'eval/', 'docs/')):
                continue
            checked += 1
            if not os.path.exists(os.path.join(ROOT, cand)):
                errors.append(f'{rel}: パス "{cand}" が存在しません')

    check_frontmatter(errors)

    if errors:
        print(f'❌ {len(errors)} 件の問題が見つかりました\n')
        for e in errors:
            print('  -', e)
        return 1

    if not args.quiet:
        print(f'✅ 参照チェック OK（{checked} 件の参照を検証）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
