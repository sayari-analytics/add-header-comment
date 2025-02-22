#!/bin/bash
# Updates release version, makes a commit, and git tag.

set -euo pipefail

usage() {
  echo "Usage: $0 [-h] <new-version>"
  echo "  -h             Display this help message"
  echo "  new-version    New version to update package to"
  exit $1
}

# new version
newVersion="${1:-}"

if [[ -z "$newVersion" ]]; then
  echo "Please provide a version number"
  usage 1
fi

# display help if requested
if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || "${1:-}" == "-help" || "${1:-}" == "help" ]]; then
  usage 0
fi

# get current version from setup.py
currentVersion=$(grep -oP 'version="\K[^"]+' setup.py)

# modify files with the version in it
operatingSystem=$(uname -s)
if [[ "$operatingSystem" == "Darwin" ]]; then
  sed -i '.old' "s+$currentVersion+$newVersion+g" README.md setup.py
  rm README.md.old setup.py.old
elif [[ "$operatingSystem" == "Linux" ]]; then
  sed -i "s+$currentVersion+$newVersion+g" README.md setup.py
else
  echo "Unsupported operating system"
  exit 1
fi

# commit and tag
git add README.md
git add setup.py
git commit -m "chore(release): v$newVersion"
echo "Creating git tag v$newVersion"
git tag "v$newVersion"

# print instructions
echo "Run the following command to push the changes:"
echo "git push origin main"
echo "git push origin tag v$newVersion"
