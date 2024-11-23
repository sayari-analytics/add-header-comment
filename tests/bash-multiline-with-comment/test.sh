#!/bin/bash

set -euo pipefail

coverage run --append add_header \
  --header-filepath tests/header-multiline.txt \
  --start-header-after "#!/bin/bash" \
  --stop-at-ignore-below \
  "$@"
