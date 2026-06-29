# 💎 WebLabsSec — Ювелирный интернет-магазин

Добро пожаловать в **WebLabsSec** — веб-приложение интернет-магазина ювелирных украшений.  
Проект разработан с использованием Flask и демонстрирует базовую логику e-commerce сайта: каталог товаров, загрузка изображений, работа с пользователями и безопасность.
Разработан в рамках учебного проекта

---

## 🚀 Быстрый старт

### 🔧 Установка

1. Клонируй репозиторий:

```bash
git clone https://github.com/Militans/WebLabsSec.git
cd WebLabsSec
```
2. Создай и активируй виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3. Установи зависимости
```bash
pip install -r requirements.txt
```
4. 🛠 Настройка базы данных (MariaDB)
1. Убедись, что MariaDB установлена и запущена.
2. Создай базу данных и пользователя:
```sql
CREATE DATABASE jeweldb;
CREATE USER 'jeweluser'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON jeweldb.* TO 'jeweluser'@'localhost';
FLUSH PRIVILEGES;
```
3. Обнови параметры подключения в moduls.py
```python
db_host = 'localhost'
db_user = 'jeweluser'
db_pass = 'your_secure_password'
db_name = 'jeweldb'
```

▶️ Запуск приложения
```python
python app.py
```
Открой в браузере: http://localhost:5000
🛍️ Функциональность
📦 Каталог ювелирных изделий

🔐 Авторизация / регистрация пользователей

📁 Загрузка и отображение изображений товаров

🛒 Добавление товаров

⚙️ Панель администратора (добавление, удаление)

📂 Работа с сессиями и безопасностью


🗂 Структура проекта

```csharp
WebLabsSec/
├── app.py            # Основной файл приложения
├── downloads.py      # Работа с файлами
├── moduls.py         # Бизнес-логика
├── users.py          # Работа с пользователями и сессиями
├── static/           # CSS, JS, изображения
├── templates/        # HTML-шаблоны (Jinja2)
├── requirements.txt  # Зависимости проекта
└── README.md         # Этот файл
```
🧪 Используемые технологии
Python 3.8+

Flask

Jinja2

HTML / CSS

Werkzeug

(и другие, см. requirements.txt)

💬 Контакты
Автор проекта: Militans
Если у тебя есть предложения, замечания или вопросы — создавай issue или пиши напрямую на GitHub.







