import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from device_params import generate_device_params
from main_logic import run_autoclicker


class AutoClickerApp:

    def __init__(self, root):
        self.threads = []
        self.root = root
        self.root.title("Автокликер для Telegram")

        self.devices = []   # [{"1": "R5CW325L9SL"}]  # Добавить новое устройство
        self.device_params = []


        # # Генерация параметров для каждого устройства
        # for device in self.devices:
        #     params = generate_device_params()

            # self.device_params.append(params)

        # Отображение параметров в интерфейсе
        self.create_interface()
        self.running = False

    def create_interface(self):
        columns = (
            "Device_ID", "Serial Number", "Delay Min", "Delay Max", "Start Delay Min", "Start Delay Max", "Work Start",
            "Work End"
        )
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.add_device_frame = tk.Frame(self.root)
        self.add_device_frame.pack(pady=10)

        tk.Label(self.add_device_frame, text="Device ID").grid(row=0, column=0)
        self.device_id_entry = tk.Entry(self.add_device_frame)
        self.device_id_entry.grid(row=0, column=1)

        tk.Label(self.add_device_frame, text="Serial Number").grid(row=1, column=0)
        self.serial_number_entry = tk.Entry(self.add_device_frame)
        self.serial_number_entry.grid(row=1, column=1)

        self.add_device_button = tk.Button(self.add_device_frame, text="Добавить Устройство", command=self.add_device)
        self.add_device_button.grid(row=2, column=2)

        self.start_button = tk.Button(self.root, text="Запустить", command=self.start_autoclicker)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Остановить", command=self.stop_autoclicker)
        self.stop_button.pack(pady=10)

        self.next_run_delay_label = tk.Label(self.root, text="Следующий пуск: N/A") # Следующий пуск
        self.next_run_delay_label.pack(side=tk.LEFT, padx=10, pady=10)

    def add_device(self):
        device_id = self.device_id_entry.get()
        serial_number = self.serial_number_entry.get()

        if device_id and serial_number:
            params = generate_device_params()
            self.devices.append({"device_id": device_id, "serial_number": serial_number})
            # self.device_params.append(params)
            self.device_params.append({"device_id": device_id, "serial_number": serial_number, **params})

            self.tree.insert("", "end", values=(
                device_id,
                serial_number,
                params["delay_min"],
                params["delay_max"],
                params["start_delay_min"],
                params["start_delay_max"],
                params["work_start"],
                params["work_end"]
            ))
            self.device_id_entry.delete(0, tk.END)
            self.serial_number_entry.delete(0, tk.END)

    def start_autoclicker(self):
        self.running = True
        self.threads = []

        for device, params in zip(self.devices, self.device_params):
            t = Thread(target=run_autoclicker, args=(params, self))  #, params
            self.threads.append(t)
            t.start()

    def stop_autoclicker(self):
        self.running = False
        for t in self.threads:
            t.join()
        self.threads = []

    def update_next_run_delay(self, delay):
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.next_run_delay_label.config(text=f"Следующий пуск: {int(hours)}ч {int(minutes)}м {int(seconds)}с")
