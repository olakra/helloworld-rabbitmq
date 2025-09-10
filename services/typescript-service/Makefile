.PHONY: build start dev test docker

build:
	npm ci
	npm run build

dev:
	npm ci
	npm run dev

test:
	npm ci
	npm test

docker:
	docker build -t ts-rabbitmq-rpc .
