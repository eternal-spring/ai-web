## Семинар 3: Chat Sessions

Реализована поддержка чат-сессий. Сообщения теперь группируются по сессиям: `User -> ChatSession -> ChatHistory`.

### Новые эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/users/{user_id}/sessions` | Создать новую сессию |
| `GET` | `/users/{user_id}/sessions` | Список сессий пользователя |
| `GET` | `/users/{user_id}/sessions/{session_id}` | История сообщений сессии |

### Обновлённые эндпоинты

| Метод | Путь | Изменение |
|-------|------|-----------|
| `POST` | `/chat` | Теперь принимает `session_id` (обязательное поле) |
| `POST` | `/chat/stream` | Теперь принимает `session_id` (обязательное поле) |

### Пример использования

```bash
# 1. Создать пользователя
POST /users  {"username": "alice", "email": "alice@example.com"}

# 2. Создать API-ключ
POST /users/{user_id}/api-keys  {"name": "my key"}

# 3. Создать сессию
POST /users/{user_id}/sessions  {"title": "Первый чат"}

# 4. Отправить сообщение в сессию
POST /chat  {"session_id": 1, "messages": [{"role": "user", "message": "Привет"}]}

# 5. Получить историю сессии
GET /users/{user_id}/sessions/1
```

---

## Запуск

1. Запустите PostgreSQL. (например, 
docker run -d -p 5433:5432 -e POSTGRES_PASSWORD=root -e POSTGRES_DB=ai_web_db -e POSTGRES_USER=postgres postgres:16.9-alpine
https://docs.docker.com/engine/install/
)
2. Создайте `.env` с переменной `DATABASE_URL`.
3. Установите зависимости:
```bash
uv sync
```
4. Примените миграции:
```bash
uv run alembic upgrade head
```
5. Запустите API:
```bash
uv run uvicorn app.main:app --reload --port <..порт..>
```
