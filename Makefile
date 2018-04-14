ifeq ($(OS),Windows_NT)
    PWD = $(shell cygpath -w $(CURDIR))
endif

CERT_PATH=certificates/localhost

build:
	docker-compose build api

dev: build
	docker-compose run -v $(PWD):/app --rm -w //app api bash

run: build
	docker-compose up -d
	
clean:
	docker-compose down

cert:
	openssl req -nodes -new -x509 -keyout $(CERT_PATH).key -out $(CERT_PATH).crt -days 365 -subj '/CN=localhost'
