#!/bin/bash

set -euo pipefail

coverage run --append add_header_comment \
  --header-filepath tests/header-long.txt \
  --comment-style "///" \
  --max-line-length 80 \
  "$@"
