.DEFAULT_GOAL := help

#uvicorn
HOST ?= 0.0.0.0
PORT ?= 8000

#migrations
MSG ?= auto_migration

run:
	gunicorn main:app -c infra/gunicorn.conf.py

migrate-create:
	alembic revision --autogenerate -m "$(MSG)"

migrate-apply:
	alembic upgrade head

migrate-history:
	alembic history --verbose

migrate-downgrade:
	alembic downgrade $(REVISION)
