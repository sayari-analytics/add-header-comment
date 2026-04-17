#!/bin/bash

set -euo pipefail

set -x

uv pip install --system -r requirements/test.txt --exclude-newer $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
uv pip install --system -e . --exclude-newer $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)

set +x

./run-tests.sh

coverage report -m | tee coverage.log

