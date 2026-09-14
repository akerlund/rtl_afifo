#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${REPO_ROOT:-$(cd "${SCRIPT_DIR}/.." && pwd)}"
VIP_ROOT="${REPO_ROOT}/submodules/vip_axi4s_agent"
CORE="akerlund::afifo_example_py:0"

export REPO_ROOT
export PYTHONPATH="${SCRIPT_DIR}/tb:${SCRIPT_DIR}/tc:${VIP_ROOT}/py:${VIP_ROOT}/submodules/vip_gauss/py${PYTHONPATH:+:${PYTHONPATH}}"

if [ "$#" -eq 0 ]; then
  fusesoc --cores-root "${REPO_ROOT}" run --target sim "${CORE}"
else
  fusesoc --cores-root "${REPO_ROOT}" run "$@" "${CORE}"
fi
