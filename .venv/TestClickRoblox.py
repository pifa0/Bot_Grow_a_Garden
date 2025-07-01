import time
from ahk import AHK

# 1. Настройки
ROBLOX_WINDOW_TITLE = "Roblox"  # Или "Roblox Player"
ahk = AHK()

def safe_click(x, y):
    # Проверяем существование окна
    if not ahk.win_exists(title=ROBLOX_WINDOW_TITLE):
        print("Окно Roblox не найдено!")
        return False

    # Активируем окно
    ahk.win_activate(title=ROBLOX_WINDOW_TITLE)
    time.sleep(0.5)  # Используем стандартный time.sleep()

    # Выполняем клик
    ahk.click(x, y)
    return True

# Пример использования
time.sleep(5)
safe_click(680, 140)