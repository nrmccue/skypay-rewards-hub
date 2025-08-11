.PHONY: run test lint docker-build docker-run
run:
	uvicorn app.main:app --reload
test:
	pytest -q
lint:
	flake8 app tests
docker-build:
	docker build -t skypay:dev .
docker-run:
	docker run -p 8000:8000 skypay:dev
