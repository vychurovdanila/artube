# STATE — ARTUBE

**Обновлено:** 2026-11-02
**Фаза:** design
**Ответственный:** Данила (CEO) + AI-партнёр (техдир)

## Что сделано
- SQLAlchemy-модели (User, Artwork, Asset, Order, Media) созданы, database.py перенесён в app/, БД SQLite инициализирована (5 таблиц: users, artworks, assets, orders, media).
- Auth: регистрация (author/designer/client), логин, JWT (24ч, HS256), /api/auth/me. Роль admin через API недостижима — назначается только вручную в БД. SECRET_KEY в .env (64 hex), .env в .gitignore.
- API artworks: POST /api/artworks (только author, status=draft принудительно), GET /api/artworks (фильтры type/status/price, пагинация skip/limit, по умолчанию только published), GET /api/artworks/{id} (черновик виден только владельцу, иначе 404). Роль-гард require_role("author").
- Схема users подготовлена к OAuth: email/password_hash nullable, telegram_id (BigInteger unique), telegram_username, avatar_url. verify_password защищён от None. login отдаёт 401 "This account uses Telegram login" для юзеров без пароля. БД пересоздана (тестовые данные утеряны, dev-БД).
- Telegram-вход: POST /api/auth/telegram. HMAC-SHA256 проверка подписи (все поля payload кроме hash, включая photo_url и extra-поля). Создание TG-юзера (role=client, email=None, password_hash=None) или логин существующего с обновлением avatar_url/telegram_username. JWT subject = email or f"tg:{telegram_id}". get_current_user умеет искать по email или telegram_id через _find_user_by_subject.
- Фронт-каркас ARTUBE: React Router (4 роута), AuthContext (JWT в localStorage, fetchMe при старте), apiFetch с автоматическим Bearer и редиректом на /login при 401. Страницы: Catalog (сетка 3x2, мок-картинки), Login, Register (роли author/designer/client), Profile (аватар/имя/email/роль-бейдж, кнопка Выйти). Layout: логотип, меню FURNITURE/DECOR/FINISHING/COMPLECTS, поиск, UPLOAD только для author.
- Мульти-роли: поле roles (JSON-массив). Регистрация -> ["client"]. API POST /api/users/me/become-author и /become-partner. Кнопка UPLOAD видна всем авторизованным (ведет на /upload). При создании работы не-автором: статус "moderation" + авто-выдача роли "author".

## Что в работе
- Формирование брифа и критериев приёмки (текущий документ)
- Определение логики онбординга (3 ветки: картина, скульптура, 3D-модель)
- Выбор технологического стека (React + FastAPI + model-viewer)

## Что дальше
1. Загрузка файлов (assets): POST /api/artworks/{id}/assets + локальное хранилище backend/static/uploads/, привязка файлов к работе. На фронте — кнопка UPLOAD с формой (title, type, photo).
2. Модерация: draft → moderation → published (админ-эндпоинт + ручное одобрение).
3. Фронт: кнопка «Войти через Telegram» (deep link основной, виджет fallback) — когда будет bot_token и домен/ngrok.
4. Спроектировать схему БД (каталог, пользователи, заказы услуг)
5. Разработать прототип онбординга с выбором типа контента
6. Реализовать калькулятор стоимости услуг
7. Разработать промт-инженерную логику для ИИ-генератора интерьеров
8. Подготовить 3D-шаблоны комнат

## Блокеры
- Нет чёткого прайса на услуги (нужен для калькулятора)
- Не выбран провайдер ИИ-генерации

## Контекст для следующей сессии
- ARTUBE — независимый коммерческий продукт, не связан с Artester.
- Онбординг разделён на 3 ветки: картина (бесплатно → 3D-холст), скульптура (платно → заказ 3D-модели), готовая 3D-модель (платно → оптимизация/AR).
- Бэкенд на Python (FastAPI), фронтенд на React (Vite) + Tailwind.
- ИИ-генерация интерьеров — по шаблонам пространств через внешнее API.
- WebAR через `<model-viewer>` (GLB/USDZ).
- Репозиторий: D:\Makefab\projects\artube (git init выполнен, GitHub не подключён).
- Правило: если входящий текст ТЗ искажён фильтром (секреты, идентификаторы) — Cline не копирует его буквально, а собирает идентификатор в рантайме и проверяет байтово.
- Техдолг: SECRET_KEY в .env — сгенерирован, но не вынесен в секрет-менеджер. Перед деплоем — openssl rand -hex 32 на сервере.
- Техдолг: favorites (избранное) для client — отдельное ТЗ после artworks.
- Решение по Telegram-OAuth: схема users готовится заранее (одна миграция, до наполнения БД). user_identities НЕ вводим на MVP — достаточно колонок telegram_id/telegram_username/avatar_url в users. Роль по умолчанию для Telegram-входа = client (авторы регистрируются через email).
- Avatar: Telegram возвращает photo_url при логине. На MVP храним URL как есть в users.avatar_url, обновляем при каждом логине. Скачивание и локальное хранение (static/avatars/{user_id}.jpg) — отдельное ТЗ, когда появится storage. HMAC: photo_url участвует в data_check_string наравне с остальными полями payload.
- Бизнес-логика: Кнопка UPLOAD доступна всем. Если клиент загружает работу, он автоматически становится автором, а работа уходит в модерацию. (Устарело: ранее client не мог создавать artworks — только author.)
- Бизнес-логика: черновики и moderation видны только владельцу, анонимам и чужим — 404 (не 403), чтобы не светить существование.
- Telegram-OAuth: два сценария входа (архитектурное решение). (A) Основной — Deep Link / LoginUrl (tg://resolve или inline-кнопка бота): работает, когда Telegram установлен и пользователь залогинен в приложении; на новом устройстве пользователь входит в TG внутри приложения (нативно и безопасно). (B) Fallback — Login Widget (веб-виджет): показываем, если deep link не сработал (десктоп без TG, браузер без handler); пользователь входит в TG через попап. (C) Email/password — всегда доступен как независимый путь. Эндпоинт /api/auth/telegram не зависит от сценария: оба пути дают одинаковый payload (id, first_name, username, photo_url, auth_date, hash), HMAC-проверка идентична.
- Telegram-OAuth: для dev без домена E2E невозможен. Тестирование — юнит-тест HMAC (генерируем подпись с известным bot_token, проверяем, что сервер принимает). Реальный E2E — после домена или ngrok.
- Техдолг: subject в JWT для Telegram-юзеров. Сейчас subject=user.email, но у TG-юзеров email=None → JWT сломается. При реализации /api/auth/telegram: subject = user.email or f"tg:{user.telegram_id}", а get_current_user ищет User.email == sub OR User.telegram_id == <число>.
- Техдолг: guard в login (if user and not user.password_hash → 401) блокирует вход по паролю даже для TG-юзера с привязанным email. Если понадобится «привязка пароля к TG-аккаунту» — смягчить до if user and not user.password_hash and form.password. Пока не трогаем.
- Avatar: на MVP храним photo_url от Telegram в users.avatar_url как есть, обновляем при каждом логине. Скачивание и локальное хранение (static/avatars/{user_id}.jpg) — отдельное ТЗ, когда появится storage.
- Правило Pydantic+HMAC: при проверке подписи Telegram использовать model_dump(exclude_none=True). Telegram не присылает null — опускает поля. Если Pydantic вставит None для отсутствующих Optional-полей, data_check_string не сойдётся. Дополнительно в verify_telegram_signature пропускаем None-значения.
- Техдолг (UX): apiFetch при 401 делает window.location.href='/login'. Для анонимного пользователя с протухшим токеном это редирект с главной. Не блокер; если станет мешать — на главной не редиректить, только чистить токен.
- Фронт: мок-данные каталога жёстко в MOCK_ITEMS (frontend/src/pages/Catalog.tsx). При подключении реального GET /api/artworks — заменить на fetch.
- Фронт: vite.config.ts содержит server.host='127.0.0.1' (Windows: иначе Vite слушает только IPv6). Не удалять.
- Правило git: после каждого атомарного коммита (в конце каждой микро-задачи обновления STATE/TASKS) — git push origin main. Cline делает это сам. Если origin/main ушёл вперёд — стоп, не мержить, сообщить в чат.
- Правило токенов: Cline делает точечные правки, не выводит полные файлы. В отчете пишет только "Готово" и список измененных файлов. Если ошибка — только текст ошибки.
- Бизнес-логика: Партнер (partner) получает комиссию с продаж через свои визуализации/ссылки, но НЕ получает комиссию со своих же авторских работ (защита от накрутки).
- Бизнес-логика: Кнопка UPLOAD доступна всем. Если клиент загружает работу, он автоматически становится автором, а работа уходит в модерацию.

## Ссылки
- BRIEF.md — бриф и критерии приёмки
- AGENTS.md — команда проекта
- TASKS.md — очередь задач
- Репозиторий: D:\Makefab\projects\artube (локальный)
- Деплой: не настроен
