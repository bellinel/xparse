# xparse

Парсер Twitter/X с использованием Playwright и SQLAlchemy

## Установка Playwright

Перед началом работы установите Playwright и необходимые браузеры:
```bash
pip install playwright
playwright install
```

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/bellinel/xparse.git
   cd xparse
   ```
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   # Для Linux/Mac:
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Переменные окружения

Создайте файл `.env` в корне проекта и добавьте ваши данные:

```
USERNAME=ваш_логин
PASSWORD=ваш_пароль
```

## Порядок запуска

1. Сначала запустите файл для авторизации (auth):
   ```python
   python auth.py
   ```
   Это сохранит сессию в файл auth_state.json.

2. Затем запускайте основной парсер:
   ```python
   python main.py
   ```

---

- Для работы нужен Python 3.8+ 