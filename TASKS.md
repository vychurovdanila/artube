# TASKS — ARTUBE

**Обновлено:** 2026-11-01

## В работе
- [ ] Загрузка файлов: POST /api/artworks/{id}/assets + статика backend/static/uploads/ + форма UPLOAD на фронте.
- [ ] Спроектировать логику онбординга (выбор типа контента)
- [ ] Разработать калькулятор стоимости услуг
- [ ] Разработать промт-инженерную логику для ИИ-генератора интерьеров
- [ ] Подготовить 3D-шаблоны комнат

## Ждёт (заблокировано)
- (нет)

## Сдано
- [x] Модели БД + database.py в app/ + инициализация SQLite — 2026-11-01
- [x] Pydantic-схемы + auth (register/login/JWT, roles: author/designer/client) — 2026-11-01
- [x] API artworks (POST/GET/by-id, фильтры, пагинация, require_role) — 2026-11-01
- [x] Схема users под Telegram-OAuth (nullable email/password_hash, telegram_id, telegram_username, avatar_url) + пересоздание БД — 2026-11-02
- [x] POST /api/auth/telegram (HMAC-SHA256, TG-юзер, avatar_url, subject=tg:{id}) — 2026-11-02
- [x] Фронт-каркас (React Router, AuthContext, apiFetch, Catalog/Login/Register/Profile, Layout) — 2026-11-02