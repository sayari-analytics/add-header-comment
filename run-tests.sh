#!/bin/bash
# Run all tests in the tests directory and outputs code coverage. Optionally, you can pass any number folders as
# arguments to this script to only run those tests.

set -euo pipefail

# variables to keep track of the test results
exitCode=0
testCaseCount=0
testCasePassCount=0

function checkTestFolder() {
  # checks if test folder and required files in test folder exist
  # exits with 1 if any of the required files do not exist
  # returns the input file if it exists
  testFolder="$1"
  if [[ ! -d "$testFolder" ]]; then
    >&2 echo "Test folder $testFolder does not exist"
    exit 1
  elif [[ ! -f "$testFolder/test.sh" ]]; then
    >&2 echo "No test.sh script found in $testFolder"
    exit 1
  fi

  set +o pipefail
  inputFile="$(ls "$testFolder/input"* | head -n 1)"
  set -o pipefail

  if [[ -z "$inputFile" ]]; then
    >&2 echo "No input file found in $testFolder"
    exit 1
  fi

  echo "$inputFile"
}

function testCaseAssert() {
  # prints the result of the test and updates counts
  testName="$1"
  actualExitCode="$2"
  additionalMsg="${3:-}"
  if [[ $actualExitCode -eq 0 ]]; then
    echo "Test passed for $testName$additionalMsg"
    testCasePassCount=$((testCasePassCount + 1))
  else
    echo "Test failed for $testName$additionalMsg"
    exitCode=1
  fi

  # prints a separator between tests
  echo "--------------------------------"
}

# tests the console script
add-header --help > /dev/null
# intializes the coverage file
# uses coverage cli to call the Python module so that the code coverage can be calculated
coverage run add_header_comment --help > /dev/null

# runs main test cases
for testPath in ${@:-tests/*/}; do
  testCaseCount=$((testCaseCount + 1))

  testFolder="${testPath%/}"

  set +e
  inputFile="$(checkTestFolder "$testFolder")"
  testCaseExitCode=$?
  set -e

  if [[ $testCaseExitCode -eq 0 ]]; then
    extension="${inputFile##*.}"
    expectedFile="$testFolder/expected.$extension"
    if [[ ! -f "$expectedFile" ]]; then
      >&2 echo "No expected file ($(basename "$expectedFile")) found in $testFolder"
      testCaseExitCode=1
    else
      # runs the test if the input and expected files exist
      actualFile="$testFolder/actual.$extension"
      cp "$inputFile" "$actualFile"

      eval "$testFolder/test.sh" "$actualFile"
      set +e
      diff "$actualFile" "$expectedFile"
      testCaseExitCode=$?
      set -e
    fi
  fi

  testCaseAssert "$testFolder" "$testCaseExitCode"
done

# runs fail on fix test cases
# creates temporary directory for the input files
tmpDir="$(mktemp -d)"

failOnFixTests=("tests/toml-long-empty-file" "tests/toml-long-update-old-header")

if [[ $# -eq 0 ]]; then
  # includes all fail on fix tests if no arguments are passed
  failOnFixTestsToRun=("${failOnFixTests[@]}")
else
  # includes the intersection of the fail on fix tests and the arguments passed
  failOnFixTestsToRun=()
  for testPath in "$@"; do
    testFolder="${testPath%/}"
    for failOnFixTestFolder in "${failOnFixTests[@]}"; do
      if [[ "$failOnFixTestFolder" == "$testFolder" ]]; then
        failOnFixTestsToRun+=("$testFolder")
        break
      fi
    done
  done
fi

for testFolder in "${failOnFixTestsToRun[@]}"; do
  testCaseCount=$((testCaseCount + 1))

  set +e
  inputFile="$(checkTestFolder "$testFolder")"
  testCaseExitCode=$?
  set -e

  if [[ $testCaseExitCode -eq 0 ]]; then
    # runs the test if the input file exists
    tmpInputFile="$tmpDir/$(basename "$inputFile")"
    cp "$inputFile" "$tmpInputFile"

    set +e
    eval "$testFolder/test.sh" --fail-on-fix "$tmpInputFile"
    # the expected result here is to fail
    testCaseExitCode=!$?
    set +e
  fi

  testCaseAssert "$testFolder" "$testCaseExitCode" " with --fail-on-fix"
done

rm -r "$tmpDir"

# prints the test case summary
echo "Test cases passed: $testCasePassCount/$testCaseCount"

# exits with the final exit code of 1 if at least one test failed
exit "$exitCode"
