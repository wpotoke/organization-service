#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    -- Создаем пользователя если не существует
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$POSTGRES_USER_NAME') THEN
            EXECUTE format('CREATE USER %I WITH PASSWORD %L', '$POSTGRES_USER_NAME', '$POSTGRES_PASSWORD');
        END IF;
    END
    \$\$;

    -- Создаем базу данных если не существует
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '$POSTGRES_DB_NAME') THEN
            EXECUTE format('CREATE DATABASE %I OWNER %I ENCODING ''UTF8''', '$POSTGRES_DB_NAME', '$POSTGRES_USER_NAME');
        END IF;
    END
    \$\$;

    -- Даем права на базу данных
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB_NAME TO $POSTGRES_USER_NAME;
EOSQL

# Даем права на таблицы в созданной базе
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d "$POSTGRES_DB_NAME" <<-EOSQL
    -- Даем права на схему public
    GRANT USAGE ON SCHEMA public TO $POSTGRES_USER_NAME;
    
    -- Даем права на ВСЕ существующие таблицы
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $POSTGRES_USER_NAME;
    
    -- Даем права на ВСЕ существующие последовательности
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $POSTGRES_USER_NAME;
    
    -- Даем права на ВСЕ существующие функции
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO $POSTGRES_USER_NAME;
    
    -- Настраиваем права по умолчанию для будущих таблиц
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO $POSTGRES_USER_NAME;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO $POSTGRES_USER_NAME;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO $POSTGRES_USER_NAME;
EOSQL