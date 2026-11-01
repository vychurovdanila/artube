# Архитектура ARTUBE

## 1. Технологический стек
- **Frontend:** React (Vite) + TypeScript + Tailwind CSS.
- **Backend:** Python (FastAPI) + SQLAlchemy (ORM) + SQLite (для старта) / PostgreSQL (для продакшена).
- **3D/AR:** Google `<model-viewer>`. Базовый холст — файл `canvas.glb` (1x1 метр), текстура натягивается динамически.
- **ИИ-генерация интерьеров:** Поиск бесплатных API (Hugging Face, Stable Diffusion API).

## 2. Структура монорепозитория
```
artube/
├── backend/          # Python FastAPI
│   ├── app/
│   │   ├── api/      # Эндпоинты (роуты)
│   │   ├── models/   # SQLAlchemy модели (БД)
│   │   ├── schemas/  # Pydantic схемы (валидация)
│   │   ├── services/ # Бизнес-логика (ИИ, модерация)
│   │   ├── static/   # Базовый canvas.glb, изображения
│   │   └── main.py   # Точка входа
│   └── requirements.txt  # Зависимости Python
├── frontend/         # React Vite
│   ├── src/
│   │   ├── components/  # UI компоненты (карточки, кнопки)
│   │   ├── pages/       # Страницы (Каталог, ЛК, Лендинг)
│   │   ├── store/       # Состояние (Zustand)
│   │   └── api/         # Запросы к бэкенду
│   └── package.json
├── .gitignore
└── README.md
```

## 3. Схема Базы Данных (Основные таблицы)
- **Users:** id, email, password_hash, role (author/designer/admin), name.
- **Artworks:** id, author_id, title, description, type (painting/sculpture/3d), status (draft/moderation/published), price, dimensions (width, height, depth), palette (JSON массив HEX).
- **Assets:** id, artwork_id, file_type (original_photo, glb, usdz, ai_interior), url.
- **Orders:** id, artwork_id, designer_id, type (cashback_claim, 3d_creation_order), status (pending/approved/rejected), proof_url (фото/рендер для кэшбека).
- **Media:** id, title, type (video/article), content, cover_url.

## 4. Сценарий онбординга (Типы контента)
1. **Painting:** Автор загружает фото, указывает размеры. Бэкенд создает запись в Artworks с типом `painting`. Для 3D-просмотра используется базовый `canvas.glb` + текстура.
2. **Sculpture:** Автор загружает фото. Тип `sculpture`. Статус `draft` (ждет заказа на 3D).
3. **3D Model:** Автор загружает свой GLB. Тип `3d`. Оплата оптимизации (пока через заявку).

## 5. API Эндпоинты (MVP)
- `POST /api/auth/register` — Регистрация.
- `POST /api/auth/login` — Авторизация (JWT токен).
- `GET /api/artworks` — Каталог (с фильтрами).
- `POST /api/artworks` — Загрузка работы (автор).
- `POST /api/ai/generate-interior` — Генерация интерьера (по промту).
- `POST /api/orders/cashback` — Загрузка доказательства продажи (дизайнер).

## 6. Правила модерации (Бизнес-логика)
- Все новые работы попадают в статус `moderation`.
- ИИ (через Vision API) проверяет: 1) Это картина/скульптура? 2) Соответствует ли "современному стилю" (по заданным критериям)?
- Если ИИ одобряет, работа уходит на ручную проверку админу (Даниле). Если админ одобряет — статус `published`.