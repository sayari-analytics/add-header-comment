#!/bin/bash

set -euo pipefail

coverage run --append add_header_comment \
  --header-filepath tests/header-multiline.txt \
  --comment-style "<!--||-->" \
  --newline-after-comment-start \
  --newline-before-comment-end \
  "$@"
