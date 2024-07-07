"""Координаты кнопок для каждого устройтва индивидуальны."""
import random
import time
from threading import Event
from adb_function import ADBInterface
from device_params import random_delay
# from device_monitor import DeviceMonitor


class AutoClicker:
    def __init__(self, serial_number, params, logger):
        self.serial_number = serial_number
        self.params = params
        self.logger = logger
        self.button_coodinates = [(259, 561), (262, 550), (250, 560), (245, 555), (248, 564)]  # координаты кнопки "ЗАБРАТЬ"

    def get_random_coordinates(self):
        return random.choice(self.button_coodinates)

    def run(self, running_event):
        self.logger(f"Соединение с устройством {self.serial_number} ...")

        if not ADBInterface.connect_device(self.serial_number):
            self.logger.log(f"Ошибка соединения с устройством {self.serial_number} ... '\n' Проверьте данное устройство {self.serial_number}")
            return

        self.logger(f"Устройство {self.serial_number} подключено.")

        while running_event.is_set():
            current_time = time.strftime("%H:%M")
            if self.params["work_start"] <= current_time <= self.params["work_end"]:
                ADBInterface.start_tg(self.serial_number)  # Открыть Телеграм с использованием идентификатора пакета
                time.sleep(5)  # Ожидание открытия приложения
                # DeviceMonitor.wait_and_check(running_event, 5)

                ADBInterface.tap(self.serial_number, 681, 121)  # Координаты поля поиска (1004, 109)
                time.sleep(3)  # Ожидание

                ADBInterface.name_input(self.serial_number)  # Ввод имени бота
                time.sleep(3)  # Ожидание

                ADBInterface.tap(self.serial_number, 201, 233)  # Координаты первого результата в поиске
                time.sleep(5)

                # Нажатие на кнопку для открытия мини приложения в боте
                ADBInterface.tap(self.serial_number, 406, 1390)  # координаты кнопки внутри бота
                time.sleep(random_delay(self.params["delay_min"], self.params["delay_max"]))

                # Нажатие на кнопку "ЗАБРАТЬ"
                button_x, button_y = self.get_random_coordinates()  # координаты кнопки "ЗАБРАТЬ"
                ADBInterface.tap(self.serial_number, button_x, button_y)
                time.sleep(random_delay(self.params["delay_min"], self.params["delay_max"]))  # Рандомное ожидание

                # Верстак
                verstak_button_x, verstak_button_y = 409, 1327  # Координаты кнопки верстака
                ADBInterface.tap(self.serial_number, verstak_button_x, verstak_button_y)
                time.sleep(random_delay(self.params["delay_min"], self.params["delay_max"]))  # Рандомное ожидание

                verstak_upgrade_button_x, verstak_upgrade_button_y = 246, 1390  # Координаты кнопки повышение уровня
                ADBInterface.tap(self.serial_number, verstak_upgrade_button_x, verstak_upgrade_button_y)
                time.sleep(random_delay(self.params["delay_min"], self.params["delay_max"]))  # Рандомное ожидание

                confirm_upgrade_x, confirm_upgrade_y = 300, 650
                ADBInterface.tap(self.serial_number, confirm_upgrade_x, confirm_upgrade_y)  # Подтвердить увеличение уровня
                time.sleep(random_delay(self.params["delay_min"], self.params["delay_max"]))  # Рандомное ожидание

                # Выход из мини приложения и Телеграмм
                ADBInterface.close(self.serial_number)
                ADBInterface.close(self.serial_number)
                ADBInterface.close(self.serial_number)
                ADBInterface.close(self.serial_number)

                # Повтор через каждые 2 часа + рандомная задержка 15-20 минут
                next_run_delay = 2 * 3600 + random_delay(self.params["start_delay_min"] * 60, self.params["start_delay_max"] * 60)
                self.logger.log(f"Следующий запуск через {next_run_delay} минут.")  # Update
            else:
                time.sleep(60)







# import random
# import time
# from adb_function import connect_device, tap
# from device_params import random_delay
# import subprocess
#
# # координаты кнопки "ЗАБРАТЬ"
# coordinates = [(259, 561), (262, 550), (250, 560), (245, 555), (248, 564)]
#
#
# def get_random_coordinates():
#     return random.choice(coordinates)
#
#
# def run_autoclicker(params, app):
#     # Настройка
#     serial_number = params["serial_number"]
#     app.log(f'"Connecting to device {serial_number}')
#     if not connect_device(serial_number):
#         print(f"Connection Error {serial_number}")
#         return
#     app.log(f"Device {serial_number} connected.")
#
#     while app.running:
#         current_time = time.strftime("%H:%M")
#         if params["work_start"] <= current_time <= params["work_end"]:
#             # Открыть Телеграм с использованием идентификатора пакета
#
#             subprocess.run(["adb", "-s", serial_number, "shell",
#                             'am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity'])
#             if not wait_and_check(app, 5):
#                 break
#             # time.sleep(5)  # Ожидание открытия приложения
#
#             # Найти и открыть чат с ботом
#             tap(serial_number, 681, 121)  # Координаты поля поиска (1004, 109)
#             if not wait_and_check(app, 3):
#                 break
#             # time.sleep(3)
#
#             subprocess.run(
#                 ["adb", "-s", serial_number, "shell", 'input text "MDAO Telegram Wallet"'])  # Ввод имени бота
#             if not wait_and_check(app, 3):
#                 break
#             # time.sleep(3)
#
#             tap(serial_number, 201, 233)  # Координаты первого результата в поиске
#             if not wait_and_check(app, 3):
#                 break
#             # time.sleep(3)
#
#             # Нажатие на кнопку для открытия мини приложения в боте
#             tap(serial_number, 406, 1390)  # координаты кнопки внутри бота
#             if not wait_and_check(app, random_delay(params["delay_min"], params["delay_max"])):
#                 break
#             # time.sleep(random_delay(params["delay_min"], params["delay_max"]))  # Рандомное ожидание
#
#             # Нажатие на кнопку "ЗАБРАТЬ"
#             button_x, button_y = get_random_coordinates()  # координаты кнопки "ЗАБРАТЬ"
#             tap(serial_number, button_x, button_y)
#             if not wait_and_check(app, random_delay(params["delay_min"], params["delay_max"])):
#                 break
#             # time.sleep(random_delay(params["delay_min"], params["delay_max"]))  # Рандомное ожидание
#
#             # Верстак
#             verstak_button_x, verstak_button_y = 409, 1327  # Координаты кнопки верстака
#             tap(serial_number, verstak_button_x, verstak_button_y)
#             if not wait_and_check(app, random_delay(params["delay_min"], params["delay_max"])):
#                 break
#             # time.sleep(random_delay(params["delay_min"], params["delay_max"]))
#
#             verstak_upgrade_button_x, verstak_upgrade_button_y = 246, 1390  # Координаты кнопки повышение уровня
#             tap(serial_number, verstak_upgrade_button_x, verstak_upgrade_button_y)
#             if not wait_and_check(app, random_delay(params["delay_min"], params["delay_max"])):
#                 break
#
#             confirm_upgrade_x, confirm_upgrade_y = 300, 650
#             tap(serial_number, confirm_upgrade_x, confirm_upgrade_y)  # Подтвердить увеличение уровня
#             if not wait_and_check(app, random_delay(params["delay_min"], params["delay_max"])):
#                 break
#             # time.sleep(random_delay(params["delay_min"], params["delay_max"]))
#
#             # Выход из мини приложения и Телеграмм
#             subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
#             if not wait_and_check(app, 1):
#                 break
#             subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
#             if not wait_and_check(app, 1):
#                 break
#             subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
#             if not wait_and_check(app, 1):
#                 break
#             subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])
#
#             # Повтор через каждые 2 часа + рандомная задержка 15-20 минут
#             next_run_delay = 2 * 3600 + random_delay(params["start_delay_min"] * 60, params["start_delay_max"] * 60)
#             app.update_next_run_delay(next_run_delay)  # Update
#             if not wait_and_check(app, next_run_delay):
#                 break
#             # time.sleep(next_run_delay)
#         else:
#             if not wait_and_check(app, 60):
#                 break  # Проверяем каждую минуту, если мы вне вабочего времени
#
#
# def wait_and_check(app, delay):
#     """Wait for a delay, but check if the app is still running every second."""
#     for _ in range(int(delay)):
#         if not app.running:
#             return False
#         time.sleep(1)
#
#     return True
