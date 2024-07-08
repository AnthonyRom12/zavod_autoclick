from adb_function import ADBInterface


class DeviceManager:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def get_connected_devices(self):
        return ADBInterface.get_connected_device()

    def add_device(self, device_id, serial_number):
        self.db.add_device(device_id, serial_number)
        self.logger.log(f"Устройство {device_id} с серийным номером {serial_number} добавлено в БД.")

    def device_exists(self, serial_number):
        return self.db.device_exists(serial_number)

    def get_all_devices(self):
        return self.db.get_all_devices()

    def get_device_id(self, serial_number):
        all_devices = self.get_all_devices()
        for device_id, sn in all_devices.items():
            if sn == serial_number:
                return device_id
        return None

    def delete_device(self, device_id):
        self.db.delete_device(device_id)
        self.logger.log(f"Устройство {device_id} удалено из БД.")
