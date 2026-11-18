# KODEX Telegram Keepalive

GitHub Actions запускает скрипт каждые 5 минут. Скрипт отправляет `/start` вашему боту от имени отдельного Telegram-аккаунта.

**Целевой бот по умолчанию:** `@KodexAIMGroupBot`

## Важно знать

- Используйте только собственный второй Telegram-аккаунт и собственного бота.
- GitHub Actions не гарантирует запуск ровно по минутам: расписание может задерживаться из-за нагрузки GitHub.
- Это не гарантирует, что Render не будет засыпать или что бот всегда ответит мгновенно.
- Повторные `/start` создают сообщения в чате. Скрипт пытается отметить этот чат прочитанным после отправки.
- Никогда не публикуйте код входа, пароль двухэтапной проверки или строку Telegram-сессии. Не отправляйте их в ChatGPT и не помещайте в файлы репозитория.

## 1. Получить Telegram API ID и API Hash

1. Войдите под вторым Telegram-аккаунтом на [my.telegram.org](https://my.telegram.org).
2. Откройте **API development tools** и создайте приложение.
3. Сохраните `api_id` и `api_hash` у себя. Это секретные данные.

## 2. Создать строку сессии на своём устройстве

Установите Python 3 и выполните в папке проекта:

```bash
pip install -r requirements.txt
python generate_session.py
```

Введите API ID, API Hash, номер второго аккаунта, код подтверждения и пароль 2FA (если включён) только в локальном терминале/Pydroid. Скрипт выведет длинную строку сессии.

**Строка сессии даёт доступ к аккаунту. Никому её не отправляйте и не добавляйте в репозиторий.**

## 3. Добавить GitHub Secrets

Откройте **Settings → Secrets and variables → Actions → New repository secret** и создайте три секрета:

| Name | Value |
|---|---|
| `TG_API_ID` | ваш Telegram API ID |
| `TG_API_HASH` | ваш Telegram API Hash |
| `TG_SESSION` | строка сессии, созданная локально |

Не вставляйте значения секретов в Issues, README, код или сообщения чата.

## 4. Запустить проверку

Откройте вкладку **Actions → Telegram Keepalive → Run workflow**. Если запуск прошёл успешно, в логе появится `Sent /start`.

Затем workflow будет запускаться по расписанию `*/5 * * * *` (каждые 5 минут, UTC).

## Отключение

Вкладка **Actions → Telegram Keepalive → ... → Disable workflow**.

## Файлы

- `main.py` — отправляет `/start` и отмечает чат с ботом прочитанным.
- `generate_session.py` — локальное создание Telegram-сессии.
- `requirements.txt` — зависимости.
- `.github/workflows/keepalive.yml` — расписание GitHub Actions.
