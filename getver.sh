#!/bin/bash

file_path="src/nats_js_prom/__init__.py"

version=$(grep -oP '(?<=__version__ = ")[^"]*' "$file_path")

if [[ $version == "" ]]; then
    echo "Version not found in $file_path"
    exit 1
else
    echo "$version"
fi
