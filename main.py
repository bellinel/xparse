
import time
from playwright.sync_api import sync_playwright

from database.orm import add_post
from database.engine import init_db





def load_auth_and_read_posts_forever(file_path: str, auth_file: str = "auth_state.json", delay_sec: int = 10):
    init_db()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=auth_file)
        page = context.new_page()

        while True:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip()]

            for url in urls:
                print(f"Обрабатываем {url}")
                try:
                    page.goto(url)
                    page.wait_for_selector('article', timeout=15000)
                except Exception as e:
                    print(f"Ошибка при загрузке {url}: {e}")
                    continue

                tweets = page.query_selector_all('article[data-testid="tweet"]')
                if not tweets:
                    print("❌ Посты не найдены")
                    continue

                for post in tweets:
                    chek_pin = post.query_selector('div[data-testid="socialContext"]:has-text("Pinned")')
                    if chek_pin:
                        print("❌ Пост закреплен, пропускаем")
                        continue

                    tweet_el = post.query_selector('div[data-testid="tweetText"]')
                    tweet = tweet_el.text_content() if tweet_el else ''

                    nickname_el = post.query_selector('a[role="link"] div[dir="ltr"]')
                    nickname = nickname_el.inner_text() if nickname_el else '—'

                    post_in_db = add_post(nickname, tweet)
                    if post_in_db:
                        print(f"✅ Пост {nickname} сохранен в базу данных")
                    break
                time.sleep(2)  # небольшая пауза между URL

            print(f"Закончили обход всех ссылок, ждем {delay_sec} секунд перед следующим циклом...")
            time.sleep(delay_sec)

       




if __name__ == "__main__":
    # Первый запуск — логинимся, сохраняем сессию
    # save_auth_state("RoflyUrist33470", "123546abc")

    # Второй и последующие — читаем посты, не логинясь
    load_auth_and_read_posts_forever("links.txt")
