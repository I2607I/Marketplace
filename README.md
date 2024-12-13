# Marketplace

  ## Развёртывание
- Запуск приложения: `docker compose build` и `docker compose up`
- Создать миграцию:
  `docker compose run backend bash -c "cd marketplace/db && alembic revision --autogenerate"`
  
- Применить эту миграцию: `docker compose run backend bash -c "cd marketplace/db && alembic upgrade head"`
- Swagger: `http://127.0.0.1:7432/swagger`
- в файле `Marketplace_collection.json` находится коллекция для Postman

## Эндпоинты

- **GET** `/api/v1/products` — Список товаров
- **POST** `/api/v1/products` — Создание товара
- **GET** `/api/v1/products/{product_id}` — Получение информации о товаре
- **PUT** `/api/v1/products/{product_id}` — Обновление товара
- **DELETE** `/api/v1/products/{product_id}` — Удаление товара
