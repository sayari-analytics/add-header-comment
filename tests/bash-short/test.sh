#!/bin/bash

set -euo pipefail

coverage run --append add_header \
  --header-filepath tests/header-short.txt \
  --start-header-after "#!/bin/bash" \
  "$@"
