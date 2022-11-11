#!/usr/bin/env bash

set -e

VERSION=$1
BRANCH=$2

USAGE_MSG='Usage: build.sh [VERSION] [BRANCH]'

if [ -z "$1" ]
then
    (>&2 echo 'You should provide version')
    echo $USAGE_MSG
    exit 1
fi

if [ -z "$2" ]
then
    (>&2 echo 'You should provide git branch')
    echo $USAGE_MSG
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PARENT_DIR="$(dirname "$DIR")"

OS=`uname -s`-`uname -m`
LATEST_COMMIT=$(git rev-parse HEAD)
CURRENT_DATETIME="`date "+%Y-%m-%d %H:%M:%S"`";
DIST_INFO_FILEPATH=$PARENT_DIR/cli/info.py

touch $DIST_INFO_FILEPATH

echo "BUILD_DATETIME = '$CURRENT_DATETIME'" > $DIST_INFO_FILEPATH
echo "COMMIT = '$LATEST_COMMIT'" >> $DIST_INFO_FILEPATH
echo "BRANCH = '$BRANCH'" >> $DIST_INFO_FILEPATH
echo "OS = '$OS'" >> $DIST_INFO_FILEPATH
echo "VERSION = '$VERSION'" >> $DIST_INFO_FILEPATH

EXECUTABLE_NAME=sk-val-$VERSION-$OS

UNAME_RES="$(uname -s)"

pyinstaller main.spec

mv $PARENT_DIR/dist/main $PARENT_DIR/dist/$EXECUTABLE_NAME

echo "========================================================================================="
echo "Built validator-cli v$VERSION, branch: $BRANCH"
echo "Executable: $EXECUTABLE_NAME"
