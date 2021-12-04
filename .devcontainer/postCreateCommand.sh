#!/usr/bin/env bash
set -ex

poetry config virtualenvs.in-project true && poetry install
