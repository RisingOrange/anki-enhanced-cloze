#!/usr/bin/env bash
declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
set -e

# cd "$DIR";
# git submodule update --init

cd "$DIR/anki";
ANKI_BASE="$DIR/profile" "$DIR/anki/tools/ts-run"
