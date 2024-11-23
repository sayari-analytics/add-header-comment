#!/bin/bash

set -euo pipefail

coverage run --append add_header \
  --header-filepath tests/header-long.txt \
  --comment-style "/*| *| */" \
  --newline-before-comment-end \
  --max-line-length 110 \
  "$@"
