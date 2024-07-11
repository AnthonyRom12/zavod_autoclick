import asyncio
# from threading import Event
from main_logic import AutoClicker


class DeviceController:
    def __init__(self, device_manager, logger):
        self.device_manager = device_manager
        self.logger = logger
        self.devices = {}
        self.running_events = {}

    async def add_device(self, device_id, serial_number):
        username = await self.device_manager.get_device_username(serial_number)
        await self.device_manager.add_device(device_id, serial_number)
        self.devices[device_id] = {"serial_number": serial_number,
                                   "username": username,
                                   "task": None}
        return username

    async def start_device(self, device_id, params):
        running_event = asyncio.Event()
        self.running_events[device_id] = running_event
        autoclicker = AutoClicker(self.devices[device_id]["serial_number"], params, self.logger)
        task = asyncio.create_task(autoclicker.run(running_event))
        self.devices[device_id]["task"] = task

    async def stop_device(self, device_id):
        if device_id in self.running_events:
            self.running_events[device_id].clear()
            await self.devices[device_id]["task"]
            del self.running_events[device_id]

    async def delete_device(self, device_id):
        await self.stop_device(device_id)
        await self.device_manager.delete_device(device_id)
        del self.devices[device_id]

