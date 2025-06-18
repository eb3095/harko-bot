#!/bin/bash

set -euxo pipefail

cp LICENSE ./harko-bot/LICENSE.txt || true
cp README.md ./harko-bot/README.md || true

cd ./harko-bot
python setup.py sdist bdist_wheel
python3 -m twine upload dist/*.tar.gz

rm -rf  harko-bot/dist harko-bot/harko-bot.egg-info harko-bot/build harko-bot/__pycache__