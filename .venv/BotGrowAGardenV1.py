import requests
import time
import threading
import keyboard
from datetime import datetime, time as dt_time
import win32gui
import win32con
from ahk import AHK

# Конфигурация
FRUITS_TO_HANDLE = ["Carrot", "Piapple", "Tomato", "Blueberry"]  # Список нужных фруктов
INTERVAL_MINUTES = 5  # Интервал в минутах
ahk = AHK()


def focus_roblox_window():
    """Активирует окно Roblox по названию."""
    window = win32gui.FindWindow(None, "Roblox")
    if window:
        win32gui.ShowWindow(window, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window)
        return True
    return False

class FruitProcessor:
    def __init__(self):
        self.running = False
        self.thread = None
        self.fruit_handlers = {
            "Carrot": self.handle_carrot,
            "Blueberry": self.handle_blueberry,
            "Pineapple": self.handle_pineapple,
            "Tomato": self.handle_tomato,
            # Добавьте обработчики для других фруктов
        }

        # Регистрируем горячие клавиши
        keyboard.add_hotkey('alt+f2', self.start)
        keyboard.add_hotkey('alt+f3', self.stop)
        print("Скрипт готов. Нажмите Alt+F2 для старта, Alt+F3 для остановки")

    def get_fruits_data(self):
        url = "https://www.growagardenvalues.com/stock/refresh_stock.php?type=seeds&_=1751206959094"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {item['Data']['Name']: item['Amount'] for item in data['data']['records']}
        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
            return {}

    # Обработчики для каждого типа фруктов
    def handle_carrot(self, amount):
        print(f"Обрабатываем {amount} морковок")
        # Логика для морковки

        time.sleep(5)
        ahk.click(680,140)
        if not self.safe_click(680, 140):  # Кнопка Seeds
            return



        time.sleep(5)

        time.sleep(5)
        keyboard.press_and_release('E')
        time.sleep(5)
        pyautogui.moveTo(725,465) # Морковь
        time.sleep(5)
        pyautogui.doubleClick()
        time.sleep(5)
        pyautogui.moveTo(770,640) # Цена моркови
        time.sleep(5)
        for i in range(amount):
            if not self.running:
                pyautogui.click()
                time.sleep(2)
        time.sleep(5)
        pyautogui.moveTo(1300,277)
        time.sleep(5)
        pyautogui.doubleClick()
        time.sleep(5)

    def handle_pineapple(self, amount):
        print(f"Обрабатываем {amount} ананасов")
        # Логика для ананаса
        for i in range(amount):
            if not self.running:
                break
            # Ваша логика для ананаса
            time.sleep(0.5)

    def handle_tomato(self, amount):
        print(f"Обрабатываем {amount} помидоров")
        # Логика для помидора
        for i in range(amount):
            if not self.running:
                break
            # Ваша логика для помидора
            time.sleep(0.5)

    def handle_blueberry(self, amount):
        print(f"Обрабатываем {amount} смородины")
        # Логика для смородины
        pyautogui.moveTo(680, 140)  # Кнопка Seeds
        pyautogui.click()
        keyboard.press_and_release('E')
        pyautogui.moveTo(715, 470)  # Смородина
        pyautogui.scroll(-400)
        pyautogui.click()
        pyautogui.moveTo(770, 665)
        for i in range(amount):
            if not self.running:
                pyautogui.click()
        pyautogui.moveTo(1300, 277)
        pyautogui.click()
        time.sleep(0.5)

    def worker(self):
        print("Скрипт начал работу")

        while self.running:
            now = datetime.now()
            print(f"[{now.time()}] Проверка данных...")

            fruits_data = self.get_fruits_data()
            if fruits_data:
                for fruit in FRUITS_TO_HANDLE:
                    if fruit in fruits_data and fruits_data[fruit] > 0:
                        if fruit in self.fruit_handlers:
                            self.fruit_handlers[fruit](fruits_data[fruit])
                        else:
                            print(f"Нет обработчика для фрукта: {fruit}")

            # Ожидаем до следующего интервала
            sleep_time = INTERVAL_MINUTES * 60 - (time.time() % (INTERVAL_MINUTES * 60))
            for _ in range(int(sleep_time)):
                if not self.running:
                    break
                time.sleep(1)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.worker)
            self.thread.start()
            print("Скрипт запущен")

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            print("Скрипт остановлен")


if __name__ == "__main__":
    processor = FruitProcessor()

    try:
        # Ожидаем нажатия Ctrl+C для выхода
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        processor.stop()
        print("Программа завершена")