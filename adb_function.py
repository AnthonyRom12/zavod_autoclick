import subprocess


def tap(device_serial, x, y):
    subprocess.run(["adb", "-s", device_serial, "shell", f"input tap {x} {y}"])


def connect_device(serial_number):
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)

    if serial_number in result.stdout:
        return True
    else:
        return False


