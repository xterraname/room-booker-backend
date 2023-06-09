.PHONY: migrate
migrate:
	poetry run python -m room_booker.manage migrate

.PHONY: migrations
migrations:
	poetry run python -m room_booker.manage makemigrations

.PHONY: run-server
run-server:
	poetry run python -m room_booker.manage runserver

.PHONY: shell
shell:
	poetry run python -m room_booker.manage shell

.PHONY: superuser
superuser:
	poetry run python -m room_booker.manage createsuperuser
