#!/usr/bin/env python3
"""
Copilot hooks の stdin ペイロードを読むための共通ヘルパー。

GitHub Copilot のフックは stdin に JSON を渡す（フィールドは camelCase: toolName / toolInput）。
イベント種別やバージョンによって欠落・命名差があり得るため、
- stdin が空/不正でも落ちない
- camelCase / snake_case の両方を拾う
という方針で正規化する。

出力規約（Copilot 共通）:
- exit 0  : 続行（stdout/stderr のテキストはユーザーに表示される）
- exit !=0: preToolUse ではツール実行をブロックする
SDD spec-kit のフックは「警告するがブロックしない」方針のため、常に exit 0 を返す。
"""
import json
import os
import sys


def read_payload() -> dict:
    """stdin の JSON を読む。空・不正でも {} を返す。"""
    try:
        raw = sys.stdin.read()
    except Exception:
        return {}
    if not raw or not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def get(data: dict, *names, default=None):
    """camelCase / snake_case のどちらでも値を取得する。"""
    for n in names:
        if n in data and data[n] not in (None, ""):
            return data[n]
    return default


def tool_name(data: dict) -> str:
    return str(get(data, "toolName", "tool_name", default="") or "")


def tool_input(data: dict) -> dict:
    ti = get(data, "toolInput", "tool_input", "arguments", default={})
    if isinstance(ti, str):
        try:
            ti = json.loads(ti)
        except Exception:
            return {}
    return ti if isinstance(ti, dict) else {}


def target_path(data: dict) -> str:
    """書き込み系ツールの対象パスを推定する（ツールごとにキー名が違うため総当たり）。"""
    ti = tool_input(data)
    for key in ("path", "filePath", "file_path", "file", "target", "uri"):
        v = ti.get(key)
        if isinstance(v, str) and v:
            return v
    return ""


def project_root(data: dict) -> str:
    """フックは hooks.json の cwd 設定によりリポジトリルートで実行される。"""
    return str(get(data, "cwd", "workspaceRoot", "workspace_root", default=os.getcwd()))


def notify(message: str) -> None:
    """ユーザー向けメッセージを出力する（Copilot は stdout をセッションに表示する）。"""
    print(message)
