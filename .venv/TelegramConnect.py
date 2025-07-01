import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime

CHANNEL_URL = "https://csgo-guides.ru/blog/grow-a-garden-stock/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

last_message = None


def get_last_message():
    global last_message

    try:
        # отправляем get запрос
        response = requests.get(CHANNEL_URL)
        # проверяем спешность запроса, если не успешен будет исключение
        response.raise_for_status()

        # парсим HTML через BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # ищет все элементы <div> с классом tgme_widget_message_text (это контейнеры сообщений в Telegram Web)
        messages = soup.find('h1').get_text(strip=True)
        print(soup)

        if not messages:
            print("❌ Сообщений не найдено.")
            return None

        # Берём САМОЕ ПОСЛЕДНЕЕ в истории (самое старое) — messages[-1]
        current_message = messages[-1].get_text(separator="|").strip()

        if current_message != last_message:
            last_message = current_message
            return current_message

        return None

    except requests.RequestException as e:
        print(f"🚫 Ошибка запроса: {e}")
    except Exception as e:
        print(f"⚠️ Ошибка: {e}")

    return None


if __name__ == "__main__":
    print("Ожидание новых сообщений... (Ctrl+C для выхода)")

    while True:
        new_message = get_last_message()

        if new_message:
            print("\n" + "=" * 50)
            print(f"Новое сообщение ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):")
            print("=" * 50)
            print(new_message)

        sleep(5)