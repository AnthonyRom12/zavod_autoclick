import tkinter as tk
from tkinter import ttk
import time
import random
from threading import Thread
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner


def tap(device, x, y):
    device.shell(f'input tap {x} {y}')


def connect_device(host, port, private_key_path, public_key_path):
    with open(private_key_path) as f:
        private_key = f.read()
    with open(public_key_path) as f:
        public_key = f.read()

    signer = PythonRSASigner(public_key, private_key)
    device = AdbDeviceTcp(host, port)
    try:
        device.connect(rsa_keys=[signer], auth_timeout_s=10)
        print(f"Устройство {host}:{port} подключено")
    except Exception as e:
        print(f"Ошибка подключения {host}:{port}: {e}")
        return None
    return device


def random_delay(min_val, max_val):
    return random.uniform(min_val, max_val)


def generate_device_params():
    delay_min = random.randint(2, 5)
    delay_max = random.randint(5, 10)
    start_delay_min = random.randint(10, 15)
    start_delay_max = random.randint(15, 20)
    work_start = "09:00"
    work_end = "21:00"
    return {
        "delay_min": delay_min,
        "delay_max": delay_max,
        "start_delay_min": start_delay_min,
        "start_delay_max": start_delay_max,
        "work_start": work_start,
        "work_end": work_end
    }


class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Автокликер для Telegram")

        self.devices = [
            {"host": "192.168.10.121", "port": 5555},
             {"host": "192.168.10.123", "port": 5555},
            # Добавьте остальные устройства здесь
        ]

        self.device_params = []

        # Генерация параметров для каждого устройства
        for device in self.devices:
            params = generate_device_params()
            self.device_params.append(params)

        # Отображение параметров в интерфейсе
        self.create_interface()

        self.running = False

    def create_interface(self):
        columns = (
            "Host", "Port", "Delay Min", "Delay Max", "Start Delay Min", "Start Delay Max", "Work Start", "Work End")

        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        for device, params in zip(self.devices, self.device_params):
            self.tree.insert("", "end", values=(
                device["host"],
                device["port"],
                params["delay_min"],
                params["delay_max"],
                params["start_delay_min"],
                params["start_delay_max"],
                params["work_start"],
                params["work_end"]
            ))

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.start_button = tk.Button(self.root, text="Запустить", command=self.start_autoclicker)
        self.start_button.pack(pady=10)
        self.stop_button = tk.Button(self.root, text="Остановить", command=self.stop_autoclicker)
        self.stop_button.pack(pady=10)

    def start_autoclicker(self):
        self.running = True
        self.threads = []

        for device, params in zip(self.devices, self.device_params):
            t = Thread(target=self.run_autoclicker, args=(device, params))
            self.threads.append(t)
            t.start()

    def stop_autoclicker(self):
        self.running = False
        for t in self.threads:
            t.join()

    def run_autoclicker(self, device_info, params):
        # Настройки
        host = device_info["host"]
        port = device_info["port"]
        private_key_path = "./adbkey"  # Путь к закрытому ключу
        public_key_path = "./adbkey.pub"  # Путь к открытому ключу

        device = connect_device(host, port, private_key_path, public_key_path)
        if device is None:
            return

        # TODO: массив с координатами для рандомного нажатия
        # collect_button = [(190, 730), (200, 730), (220, 730)]  # Координаты для кнопки ЗАБРАТЬ

        while self.running:
            current_time = time.strftime("%H:%M")
            if params["work_start"] <= current_time <= params["work_end"]:
                # Открытие Телеграм
                device.shell('am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity')
                time.sleep(5)
                tap(device, 1015, 138)  # Координаты для кнопки поиск
                time.sleep(3)
                device.shell('input text "MDAO Telegram Wallet"')
                time.sleep(3)
                tap(device, 482, 526)  # Открытие первого результата в поиске
                # Нажатие на кнопку для открытия мини-приложения в боте
                tap(device, 787, 2081)  # Пример координат кнопки внутри бота

                time.sleep(random_delay(params["delay_min"], params["delay_max"]))  # Ожидание

                # Нажатие на кнопку "ЗАБРАТЬ"
                button_x, button_y = 190, 730  # Пример координат кнопки "ЗАБРАТЬ"   # TODO: массив с координатами
                                                                                # TODO: для рандомного нажатия  Вставить сюда
                tap(device, button_x, button_y)

                # Рандомная задержка
                time.sleep(random_delay(params["delay_min"], params["delay_max"]))

                # Верстак
                verstak_button_x, verstak_button_y = 609, 1920  # Координаты верстака
                tap(device, verstak_button_x, verstak_button_y)

                # Рандомная задержка
                time.sleep(random_delay(params["delay_min"], params["delay_max"]))

                verstak_upgrade_x, verstak_upgrade_y = 430, 2116  # Кнопка повышения уровня
                tap(device, verstak_upgrade_x, verstak_upgrade_y)

                # Рандомная задержка
                time.sleep(random_delay(params["delay_min"], params["delay_max"]))

                # Выход из мини-приложения и Telegram
                device.shell('input keyevent 4')  # Нажатие кнопки "Назад" выход из Верстака
                time.sleep(1)
                device.shell('input keyevent 4')  # Нажатие кнопки "Назад" выход из завода
                time.sleep(1)
                device.shell('input keyevent 4')  # Нажатие кнопки "Назад" выход из чата
                time.sleep(1)
                device.shell('input keyevent 4')  # Еще одно нажатие "Назад" для выхода из Телеграм
                # device.shell('input keyevent 4')  # Еще раз нажатие кнопки "Назад" для выхода из Telegram

                # Повтор через каждые 2 часа + рандомная задержка 15-20 минут
                next_run_delay = 2 * 3600 + random_delay(params["start_delay_min"] * 60,
                                                         params["start_delay_max"] * 60)
                time.sleep(next_run_delay)
            else:
                time.sleep(60)  # Проверяем каждую минуту, если мы вне рабочего времени


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
