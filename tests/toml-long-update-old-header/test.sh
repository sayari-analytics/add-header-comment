#!/bin/bash

set -euo pipefail

coverage run --append add_header \
  --header-filepath tests/header-long.txt \
  --start-header-after "header-is-above-this" \
  --max-line-length 120 \
  "$@"
