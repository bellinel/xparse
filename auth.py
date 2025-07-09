import time
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
print(USERNAME, PASSWORD)

def save_auth_state(username: str, password: str, auth_file: str = "auth_state.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        print('Запускаем браузер')
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            locale="ru-RU",
        )

        # Anti-detect: скрываем автоматизацию
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = context.new_page()
        page.goto("https://x.com/i/flow/login")

        # Ввод логина
        
        username = input('Введите логин: ')
        page.wait_for_selector('input[autocapitalize="sentences"]').fill(username)
        page.mouse.move(200, 300)
        page.wait_for_timeout(500)
        page.mouse.click(200, 300)
        time.sleep(1.5)
        page.click('button:has-text("Далее")')
        time.sleep(2)

        # Иногда просят ещё раз логин
        try:
            
            page.wait_for_selector('input[data-testid="ocfEnterTextTextInput"]', timeout=5000)
            page.fill('input[data-testid="ocfEnterTextTextInput"]', username)
            time.sleep(1.5)
            page.click('button:has-text("Далее")')
            time.sleep(2)
        except:
            pass

        # Ввод пароля
        
        password = input('Введите пароль: ')
        page.wait_for_selector('input[type="password"]', timeout=15000).fill(password)
        time.sleep(1)
        page.click('button:has-text("Войти")')

        # Если просит код — вводим вручную
        max_attempts = 5

        for attempt in range(max_attempts):
            try:
                page.wait_for_selector('input[data-testid="ocfEnterTextTextInput"]', timeout=5000)
                code = input(f"⚠️ Введите код подтверждения (попытка {attempt + 1}/{max_attempts}): ")
                page.fill('input[data-testid="ocfEnterTextTextInput"]', code)
                time.sleep(1)
                page.click('button:has-text("Далее")')

                # Ждем 3 секунды, чтобы страница обновилась и проверить есть ли сообщение
                time.sleep(3)

                # Проверяем, есть ли надпись "Проверьте свою электронную почту"
                try:
                    page.wait_for_selector('span:has-text("Проверьте свою электронную почту")', timeout=3000)
                    print("❌ Код неверный или требуется повторный ввод.")
                    # Цикл повторится, попросит ввести код заново
                except:
                    # Сообщение не появилось — значит, код принят, выходим из цикла
                    print("✅ Код подтверждения принят.")
                    break
            except Exception as e:
                print(f"Ошибка при вводе кода: {e}")
                break
        else:
            print("❌ Максимальное число попыток ввода кода превышено.")

        page.wait_for_timeout(5000)

        # Сохраняем авторизованную сессию (все куки, localStorage, sessionStorage)
        context.storage_state(path=auth_file)
        print(f"✅ Сессия сохранена в {auth_file}")

        browser.close()

if __name__ == "__main__":
    # Первый запуск — логинимся, сохраняем сессию
    save_auth_state(USERNAME, PASSWORD)