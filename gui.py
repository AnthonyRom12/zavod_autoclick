import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread, Event
from logger import Logger
from main_logic import AutoClicker
from device_params import generate_device_params
# from adb_function import ADBInterface
# from DeviceManager import DeviceManager


class AutoClickerApp:
    def __init__(self, root, device_manager):
        self.root = root
        self.root.title("Автокликер для Telegram")

        self.devices = []
        self.device_params = []
        self.running_event = Event()
        self.device_manager = device_manager

        self.setup_ui()
        self.load_devices_from_db()
        self.check_devices()

    def setup_ui(self):
        self.log_text = tk.Text(self.root, height=10, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        self.logger = Logger(self.log_text)

        self.create_interface()

    def create_interface(self):
        columns = (
            "Device_ID", "Serial Number", "Delay Min", "Delay Max",
            "Start Delay Min", "Start Delay Max", "Work Start", "Work End"
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

        self.add_device_button = tk.Button(self.add_device_frame, text="Добавить Устройство", command=self.manual_add)
        self.add_device_button.grid(row=2, column=2)

        self.start_button = tk.Button(self.root, text="Запустить", command=self.start_autoclicker)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Остановить", command=self.stop_autoclicker)
        self.stop_button.pack(pady=10)

        self.next_run_delay_label = tk.Label(self.root, text="Следующий пуск: N/A")
        self.next_run_delay_label.pack(side=tk.LEFT, padx=10, pady=10)

    def log(self, message):
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state=tk.DISABLED)
        self.log_text.yview(tk.END)

    def check_devices(self):
        connected_devices = self.device_manager.get_connected_devices()
        all_devices = self.device_manager.get_all_devices()
        for serial_number in connected_devices:
            # serial_number = serial_number  # .decode('utf-8')
            if not self.device_manager.device_exists(serial_number):
                self.prompt_add_device(serial_number)
            else:
                device_id = self.device_manager.get_device_id(serial_number)
                self.add_device(device_id, serial_number)
                self.logger.log("Соедененные устройства автоматически добавлены.")

        # connected_devices = ADBInterface.get_connected_device()
        # for device in connected_devices:
        #     serial_number = device[0]
        #     if not self.device_manager.device_exists(serial_number):
        #         self.prompt_add_device(serial_number)
        #     else:
        #         self.add_device_to_ui(serial_number)

    def prompt_add_device(self, serial_number):
        def add_to_db():
            device_id = device_id_entry.get()
            if device_id:
                self.device_manager.add_device(device_id, serial_number)
                self.add_device(device_id, serial_number)
                add_device_window.destroy()

        add_device_window = tk.Toplevel(self.root)
        add_device_window.title("Добавить Новое Устройство")
        tk.Label(add_device_window, text="Device ID").grid(row=0, column=1)

        device_id_entry = tk.Entry(add_device_window)
        device_id_entry.grid(row=0, column=2)
        add_button = tk.Button(add_device_window, text="Добавить Устройство", command=add_to_db)
        add_button.grid(row=1, column=1)
        cancel_button = tk.Button(add_device_window, text="Отмена", command=add_device_window.destroy)
        cancel_button.grid(row=1, column=2)

    def add_device_to_ui(self, serial_number):
        device = self.device_manager.device_exists(serial_number)
        # device_id = device['device_id']
        # params = generate_device_params()
        if device:
            device_id = self.device_manager.get_device_id(serial_number) #
            # device['device_id'].decode('utf-8')
            params = generate_device_params()  # {k.decode('utf-8'): v.decode('utf-8') for k, v in device[
            # 'params'].items()}

            self.devices.append({"device_id": device_id, "serial_number": serial_number})
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

            self.logger.log(f"Устройство {device_id} с серийным номером {serial_number} добавлено.")

    def add_device(self, device_id, serial_number):
        if device_id and serial_number:
            params = generate_device_params()
            self.devices.append({"device_id": device_id, "serial_number": serial_number})
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

            self.logger.log(f"Устройство {device_id} с серийным номером {serial_number} добавлено.")

    def manual_add(self):
        device_id = self.device_id_entry.get()
        serial_number = self.serial_number_entry.get()
        if device_id and serial_number:
            self.device_manager.add_device(device_id, serial_number)
            self.add_device(device_id, serial_number)

    def load_devices_from_db(self):
        devices = self.device_manager.get_all_devices()
        for device_id, serial_number in devices.items():
            # device_id = device['device_id'].decode('utf-8')
            # serial_number = device['serial_number']
            self.add_device_to_ui(serial_number)

    def start_autoclicker(self):
        self.running_event.set()
        self.threads = []

        for device, params in zip(self.devices, self.device_params):
            autoclicker = AutoClicker(device["serial_number"], params, self.logger.log)
            t = Thread(target=autoclicker.run, args=(self.running_event,))
            self.threads.append(t)
            t.start()
            self.logger.log(f"Autoclicker started for device {device['device_id']}.")

    def stop_autoclicker(self):
        self.running_event.clear()
        for t in self.threads:
            t.join()
        self.logger.log("Autoclicker stopped.")

    def update_next_run_delay(self, delay):
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.next_run_delay_label.config(text=f"Следующий пуск: {int(hours)}ч {int(minutes)}м {int(seconds)}с")

