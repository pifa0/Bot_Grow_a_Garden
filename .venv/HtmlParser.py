import requests
from bs4 import BeautifulSoup


def get_seeds_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_='entry-content')

        seeds_info = {}

        # Ищем все элементы, содержащие "x" с цифрой (формат количества)
        for element in content.find_all(['p', 'li', 'div']):
            text = element.get_text().strip()
            if 'x' in text and any(char.isdigit() for char in text.split('x')[-1]):
                # Очищаем текст от лишних символов
                parts = [p.strip() for p in text.split('x')]
                if len(parts) >= 2:
                    name = parts[0]
                    quantity = ''.join(c for c in parts[1] if c.isdigit())
                    if name and quantity:
                        seeds_info[name] = quantity

        return seeds_info

    except Exception as e:
        print(f"Ошибка: {e}")
        return {}


url = 'https://csgo-guides.ru/blog/grow-a-garden-stock/'
seeds_info = get_seeds_info(url)

if seeds_info:
    print("Найдены семена:")
    for name, quantity in seeds_info.items():
        print(f"{name}: x{quantity}")
else:
    print("Информация о семенах не найдена.")