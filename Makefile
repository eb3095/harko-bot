#!make

all: depend test

test: check_format

depend:
	python3 -m pip install black

format:
	python3 -m black --line-length=88 harko-bot/harko-bot

check_format:
	python3 -m black --line-length=88 --diff --verbose --check harko-bot/harko-bot
