## Organization API - справочник организаций

### Как запустить

```bash
# Клонируем репозиторий
git clone https://github.com/wpotoke/organization_service.git
cd organization_api

# Создаем виртуальное окружение (для Windows)
python -m venv venv && venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем .env файл с настройками БД
copy .env.example .env
# Затем отредактируйте .env файл:
POSTGRES_DB_NAME="your_db_name"
POSTGRES_USER_NAME="your_username"
POSTGRES_PASSWORD="your_password"

# Запускаем контейнеры
docker compose up -d

# Применяем миграции
docker compose exec organization_service alembic upgrade head
```

### API будет доступно по адресу:
http://localhost:8001/docs
