#!/bin/bash

set -euo pipefail

coverage run --append add_header_comment \
  --header-filepath tests/header-short.txt \
  --max-line-length 120 \
  "$@"
