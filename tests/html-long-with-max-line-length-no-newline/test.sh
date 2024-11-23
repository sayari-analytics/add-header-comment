#!/bin/bash

set -euo pipefail

coverage run --append add_header \
  --header-filepath tests/header-long.txt \
  --comment-style "<!--||-->" \
  --max-line-length 100 \
  "$@"
