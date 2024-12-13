# Marketplace

- docker compose build
- docker compose up
- docker compose run backend bash -c "cd marketplace/db && alembic upgrade head"
- docker compose run backend bash -c "cd marketplace/db && alembic revision --autogenerate"