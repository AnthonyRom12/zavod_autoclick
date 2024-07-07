import tkinter as tk
from gui import AutoClickerApp, DeviceManager
from redis_db import RedisDB
from logger import Logger


if __name__ == '__main__':
    root = tk.Tk()
    db = RedisDB()
    logger_widget = tk.Text(root, height=10, state=tk.DISABLED)
    logger_widget.pack(fill=tk.BOTH, expand=True, pady=10)
    logger = Logger(logger_widget)
    device_manager = DeviceManager(db, logger)
    app = AutoClickerApp(root, device_manager, logger)
    root.mainloop()
