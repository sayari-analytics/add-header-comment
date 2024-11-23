#!/bin/bash

set -euo pipefail

coverage run --append add_header \
  --header-filepath tests/header-multiline.txt \
  --start-header-after "custom-start-header-search" \
  --ignore-below-string "custom-ignore-below" \
  --stop-at-ignore-below \
  --max-line-length 80 \
  "$@"
