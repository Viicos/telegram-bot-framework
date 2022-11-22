#!/bin/bash

#
# Compile the dependencies for production, CI and development.
#
# Usage, in the root of the project:
#
#     ./bin/compile_dependencies.sh
#
# Any extra flags/arguments passed to this wrapper script are passed down to pip-compile.
# E.g. to update a package:
#
#     ./bin/compile_dependencies.sh --upgrade-package pydantic

set -ex

toplevel=$(git rev-parse --show-toplevel)

cd $toplevel

export CUSTOM_COMPILE_COMMAND="./bin/compile_dependencies.sh"


# Build base dependencies
pip-compile \
    --no-emit-index-url \
    --resolver backtracking \
    -o requirements/requirements.txt \
    "$@" \
    pyproject.toml

# Build dev dependencies
pip-compile \
    --no-emit-index-url \
    --resolver backtracking \
    --extra=dev \
    -o requirements/dev.txt \
    "$@" \
    pyproject.toml
