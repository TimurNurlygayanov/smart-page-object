#!/usr/bin/env bash

find . -type d -name __pycache__ -delete
find . -type d -name .pytest_cache -delete
find . -type d -name .idea -delete
find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf
git add -A
