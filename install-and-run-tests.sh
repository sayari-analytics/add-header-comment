#!/bin/bash

set -euo pipefail

set -x

pip install -r requirements/test.txt
pip install -e .

set +x

./run-tests.sh
