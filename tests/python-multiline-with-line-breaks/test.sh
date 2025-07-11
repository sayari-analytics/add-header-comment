#!/bin/bash

set -euo pipefail

coverage run --append add_header_comment \
  --header-filepath tests/header-multiline-with-line-breaks.txt \
  "$@"
