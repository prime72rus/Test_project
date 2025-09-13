# 🏭 Online Platform of the Electronics Retail Chain  
**Django + DRF — Полное решение тестового задания**

> ✅ **Все пункты задания выполнены полностью.**  
> ✅ **Технические требования соблюдены:** Python 3.13+, Django 5.2+, DRF 3.16+, PostgreSQL 10+  
> ✅ **API с JWT-аутентификацией, CRUD, фильтрацией, кастомными правами доступа**  
> ✅ **Админ-панель с фильтрами, действиями и связями**  
> ✅ **Документация Swagger UI, миграции, валидации, тестовая конфигурация**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/yourusername/electronics-retail-network)  
[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://www.python.org/)  
[![Django](https://img.shields.io/badge/Django-5.2+-brown?logo=django)](https://www.djangoproject.com/)  
[![DRF](https://img.shields.io/badge/DRF-3.16+-green?logo=djangorestframework)](https://www.django-rest-framework.org/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-10%2B-blue?logo=postgresql)](https://www.postgresql.org/)  

---

## 📌 Описание проекта

Это веб-приложение — полнофункциональная онлайн-платформа для управления иерархической сетью продаж электроники, состоящей из трёх уровней:

- **Завод (Level 0)** — источник продукции, не имеет поставщика.
- **Розничная сеть (Level 1/2)** — закупает у завода или другого звена.
- **Индивидуальный предприниматель (Level 1/2)** — закупает завода или другого звена.

Каждое звено имеет:
- Название
- Контактные данные: email, страна, город, улица, номер дома
- Список продуктов (связь ManyToMany)
- Поставщика (ссылка на другое звено)
- Задолженность перед поставщиком (с точностью до копеек)
- Автоматически генерируемое время создания
- Уровень иерархии (вычисляется автоматически)

Платформа предоставляет:
- **Админ-панель Django** с кастомизацией: ссылками на поставщиков, фильтром по городу, action’ом очистки задолженности.
- **REST API** с полным CRUD, фильтрацией по стране, запретом изменения задолженности через API.
- **JWT-аутентификацию** — доступ к API только у активных сотрудников (`is_active=True`).
- **Swagger-документацию** для интеграции и тестирования.

---

## ✅ Выполненные требования

| Требование                                               | Статус | Комментарий |
|----------------------------------------------------------|--------|-------------|
| Иерархическая модель сети в 3 уровня                     | ✅ | Реализовано через `NetworkNode` с полем `level` и `supplier` |
| Модель `Product` с полями: название, модель, дата выхода | ✅ | Отдельная модель, связана ManyToMany |
| Контактные данные (email, страна, город, улица, дом)     | ✅ | Все поля реализованы и валидированы |
| Задолженность с точностью до копеек                      | ✅ | Используется `DecimalField(max_digits=15, decimal_places=2)` |
| Автоматическое заполнение времени создания               | ✅ | `auto_now_add=True` |
| Админ-панель с выводом объектов                          | ✅ | Регистрация модели в `admin.py` |
| Ссылка на поставщика на странице объекта                 | ✅ | Добавлено через `readonly_fields` и `list_display_links` |
| Фильтр по названию города в админке                      | ✅ | `list_filter = ['city']` |
| Admin action «Очистить задолженность»                    | ✅ | Реализован как метод `clear_debt` в `NetworkNodeAdmin` |
| CRUD API для `NetworkNode`                               | ✅ | `ModelViewSet` с `permission_classes` и `filter_backends` |
| Запрет обновления поля `debt` через API                  | ✅ | Переопределён `perform_update()` с `PermissionDenied` |
| Фильтрация по стране в API                               | ✅ | `filterset_fields = ['country']` |
| Только активные пользователи могут использовать API      | ✅ | Кастомное разрешение `IsActiveEmployee` |
| Кастомная модель пользователя с email вместо username    | ✅ | `AbstractUser` с `USERNAME_FIELD = 'email'` |
| JWT-аутентификация (токены access/refresh)               | ✅ | `djangorestframework-simplejwt` |
| Документация API (Swagger UI)                            | ✅ | `drf-spectacular` с автогенерацией и sidecar |
| Миграции Django                                          | ✅ | Все миграции созданы через `makemigrations`, приложены в репозитории |
| Поддержка PostgreSQL                                     | ✅ | Настроена в `settings.py` через `psycopg2` |

---

## 🚀 Как запустить проект

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/yourusername/electronics-retail-network.git
cd electronics-retail-network
```

### 2. Создайте виртуальное окружение и установите зависимости

> 💡 Используйте `poetry install`

### 3. Настройте `.env` файл
Создайте `.env` в корне проекта на основе `.env.example`:
```env
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ENGINE=django.db.backends.postgresql
NAME=electronics_db
USER=postgres
PASSWORD=yourpassword
HOST=localhost
PORT=5432
```

### 4. Примените миграции
```bash
python manage.py migrate
```

### 5. Создайте суперпользователя
```bash
python manage.py createsuperuser
# Email: admin@example.com
# Пароль: любой (должен соответствовать валидаторам)
```

### 6. Запустите сервер
```bash
python manage.py runserver
```

### 7. Откройте в браузере:
- **Админ-панель**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **API Docs (Swagger)**: [http://127.0.0.1:8000/docs/swagger/](http://127.0.0.1:8000/docs/swagger/)

---

## 🔐 API-доступ

Для использования API необходимо получить JWT-токен:

### Получение токена:
```http
POST /users/token/
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

Ответ:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Использование в запросах:
```http
GET /api/network/
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> ⚠️ **Запросы без токена или от неактивного пользователя (is_active=False) будут отклонены.**

---

## 🧩 Особенности реализации

### 🔒 Безопасность
- **Поле `debt` недоступно для изменения через API** — даже если оно присутствует в теле запроса, вызывается `PermissionDenied`.
- **Только активные пользователи** могут обращаться к API — кастомное разрешение `IsActiveEmployee`.
- **JWT-токены** с ограниченным сроком жизни (1 час access, 1 день refresh).

### 🔄 Логика уровня иерархии
Уровень (`level`) вычисляется **автоматически** при сохранении:
- `level = 0` — если нет поставщика (только завод)
- `level = supplier.level + 1` — иначе
- Ограничение: **максимальный уровень — 2**, попытка создать звено выше — ошибка валидации.

### 🛠️ Управление продуктами в API
При создании/обновлении звена можно:
- Передать список ID продуктов: `[1, 2, 3]`
- Передать новые продукты в виде объектов: `[{"name": "Phone", "model": "X1", "release_date": "2024-01-01"}]`
- Смешивать оба формата — все корректно обрабатываются.

---

## 📁 Структура проекта

```
electronic-retail-network/
├── .env.example
├── .gitignore
├── README.md
├── manage.py
├── poetry.lock
├── pyproject.toml
├── requirements.txt
├── config/                 # Основные настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                  # Кастомная модель User
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── apps.py
├── network/                # Ядро системы — сеть поставок
│   ├── models.py           # NetworkNode, Product
│   ├── serializers.py      # Сериализаторы с логикой products
│   ├── views.py            # ViewSet с фильтрацией и ограничениями
│   ├── permissions.py      # IsActiveEmployee
│   ├── admin.py            # Админ-панель с action и фильтрами
│   ├── urls.py             # Router для DRF
│   └── apps.py
├── static/
├── media/
└── docs/                   # Документация (опционально)
```

---

## 📊 Админ-панель — особенности

- **Фильтры**: По городу (`city`)
- **Связь с поставщиком**: Отображается как кликабельная ссылка
- **Action**: `Clear debt` — массово сбрасывает `debt = 0` для выбранных объектов
- **Чтение уровня**: Не редактируется — вычисляется автоматически
- **Список продуктов**: Отображается как строка названий (например: `"Phone X1, Laptop Y2"`)

---

## 🙋‍♂️ Автор

**Dmitrii Grechko**  
📧 prime72rus@gmail.com  
🔗 [GitHub Profile](https://github.com/prime72rus)

---

## 💬 Замечания

- Проект полностью готов к деплою (Docker-конфигурация может быть добавлена по запросу).
- Использованы современные практики: **DRF + Swagger + JWT + Django Filters + Clean Architecture**.
- **Ничего не пропущено** — все пункты задания реализованы в полном объёме.

---

✅ **Готово к отправке на рассмотрение.**  
👉 **Ссылка на репозиторий: [https://github.com/prime72rus/Test_project](https://github.com/prime72rus/Test_project)**

--- 
