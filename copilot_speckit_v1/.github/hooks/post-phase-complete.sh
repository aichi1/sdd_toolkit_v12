#!/usr/bin/env bash
# postToolUse hook: outputs/ への書き込みが起きたときだけ、コンポーネント候補を自動抽出する。
#
# Copilot の postToolUse にはマッチャがないため、対象の絞り込みはこのスクリプト側で行う。
# stdin には {"toolName": "...", "toolInput": {...}} 形式の JSON が渡される。

PROJECT_ROOT="${1:-.}"
SCRIPTS_DIR="${PROJECT_ROOT}/scripts"
KB_DIR="${HOME}/.sdd-knowledge"

# --- 対象イベントの絞り込み -------------------------------------------------
PAYLOAD="$(cat 2>/dev/null || true)"

# outputs/ への書き込み以外は何もしない
case "${PAYLOAD}" in
    *outputs/*) : ;;
    *) exit 0 ;;
esac

# 書き込み系ツール以外は何もしない（toolName の大文字小文字は問わない）
LOWER_PAYLOAD="$(printf '%s' "${PAYLOAD}" | tr '[:upper:]' '[:lower:]')"
case "${LOWER_PAYLOAD}" in
    *'"toolname"'*write*|*'"toolname"'*edit*|*'"toolname"'*create*|*'"toolname"'*patch*) : ;;
    *) exit 0 ;;
esac

# --- 抽出スクリプトの解決 ---------------------------------------------------
EXTRACT_SCRIPT=""
if [ -f "${SCRIPTS_DIR}/extract_components.py" ]; then
    EXTRACT_SCRIPT="${SCRIPTS_DIR}/extract_components.py"
elif [ -f "${PROJECT_ROOT}/outputs/phase-02/src/extract_components.py" ]; then
    EXTRACT_SCRIPT="${PROJECT_ROOT}/outputs/phase-02/src/extract_components.py"
fi

if [ -z "${EXTRACT_SCRIPT}" ]; then
    echo "[hook] extract_components.py not found, skipping" >&2
    exit 0
fi

PROJECT_NAME=$(basename "$(cd "${PROJECT_ROOT}" && pwd)")
echo "[hook] Extracting component candidates from ${PROJECT_NAME}..."
python3 "${EXTRACT_SCRIPT}" "${PROJECT_ROOT}" --project-name "${PROJECT_NAME}" --kb-dir "${KB_DIR}" 2>&1 || true
echo "[hook] Done."
exit 0
