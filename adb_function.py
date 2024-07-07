import subprocess


class ADBInterface:
    @staticmethod
    def get_connected_device():
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        devices = []
        lines = result.stdout.splitlines()

        for line in lines[1:]:
            if "device" in line:
                serial = line.split()[0]

                devices.append(serial)
            return devices

    @staticmethod
    def start_tg(serial_number):
        subprocess.run(["adb", "-s", serial_number, "shell",
                                                    'am start -n org.telegram.messenger/org.telegram.ui.LaunchActivity'])

    @staticmethod
    def name_input(serial_number):
        subprocess.run(["adb", "-s", serial_number, "shell", 'input text "MDAO Telegram Wallet"'])  # Ввод имени бота

    @staticmethod
    def tap(device_serial, x, y):
        subprocess.run(["adb", "-s", device_serial, "shell", f"input tap {x} {y}"])

    @staticmethod
    def close(serial_number):
        subprocess.run(["adb", "-s", serial_number, "shell", 'input keyevent 4'])

    @staticmethod
    def connect_device(serial_number):
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if serial_number in result.stdout:
            return True
        else:
            return False


# def tap(device_serial, x, y):
#     subprocess.run(["adb", "-s", device_serial, "shell", f"input tap {x} {y}"])
#
#
# def connect_device(serial_number):
#     result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
#
#     if serial_number in result.stdout:
#         return True
#     else:
#         return False


