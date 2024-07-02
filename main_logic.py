"""Координаты кнопок для каждого устройтва индивидуальны."""

import time
from adb_function import connect_device, tap
from device_params import random_delay
import subprocess


def run_autoclicker(params, app):
    # Настройка
    serial_number = params["serial_number"]
    if not connect_device(serial_number):
        print(f"Connection Error {serial_number}")
        return

    while app.running:
        current_time = time.strftime("%H:%M")
        if params["work_start"] <= current_time <= params["work_end"]:
            # Открыть Телеграм с использованием идентификатора пакета

            subprocess.run(["adb", "-s", serial_number, "shell", 'am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity'])
            time.sleep(5)  # Ожидание открытия приложения

            # Найти и открыть чат с ботом
            tap(serial_number, 1004, 109)  # Координаты поля поиска
            time.sleep(3)

            subprocess.run(["adb", "-s", serial_number, "shell", 'input text "MDAO Telegram Wallet"'])  # Ввод имени бота
            time.sleep(3)

            tap(serial_number, 322, 526)  # Координаты первого результата в поиске
            time.sleep(3)

            # Нажатие на кнопку для открытия мини приложения в боте
            tap(serial_number, 787, 2081)  # координаты кнопки внутри бота
            time.sleep(random_delay(params["delay_min"], params["delay_max"]))  # Рандомное ожидание

            # Нажатие на кнопку "ЗАБРАТЬ"
            button_x, button_y = 375, 810  # координаты кнопки "ЗАБРАТЬ"
            tap(serial_number, button_x, button_y)
            time.sleep(random_delay(params["delay_min"], params["delay_max"]))  # Рандомное ожидание

            # Верстак
            verstak_button_x, verstak_button_y = 609, 1920  # Координаты кнопки верстака
            tap(serial_number, verstak_button_x, verstak_button_y)
            time.sleep(random_delay(params["delay_min"], params["delay_max"]))

            verstak_upgrade_button_x, verstak_upgrade_button_y = 430, 2116  # Координаты кнопки повышение уровня
            tap(serial_number, verstak_upgrade_button_x, verstak_upgrade_button_y)
            time.sleep(random_delay(params["delay_min"], params["delay_max"]))

            # Выход из мини приложения и Телеграмм
            subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
            time.sleep(1)
            subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
            time.sleep(1)
            subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
            subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])

            # Повтор через каждые 2 часа + рандомная задержка 15-20 минут
            next_run_delay = 2 * 3600 + random_delay(params["start_delay_min"] * 60, params["start_delay_max"] * 60)
            time.sleep(next_run_delay)
        else:
            time.sleep(60)  #  Проверяем каждую минуту, если мы вне вабочего времени

