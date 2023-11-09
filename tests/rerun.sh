#!/usr/bin/env bash
cd ..
pip install .
cd tests
pytest -s -v --cov
