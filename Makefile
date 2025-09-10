.PHONY: up down build all test

up:
	docker-compose up --build

down:
	docker-compose down

build:
	docker-compose build

test:
	cd services/typescript-service && make test
	cd services/go-service && make test || true
	cd services/python-service && make test || true
	cd services/java-service && make test || true

all: build
