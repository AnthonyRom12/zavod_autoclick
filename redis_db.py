import redis


class RedisDB:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def add_device(self, device_id, serial_number):
        self.client.hset('devices', device_id, serial_number)

    def get_all_devices(self):
        devices = self.client.hgetall('devices')
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in devices.items()}  # .hgetall('devices')

    def device_exists(self, serial_number):
        devices = self.get_all_devices()
        return serial_number in devices.values()  # serial_number.encode()

    def delete_device(self, device_id):
        self.client.hdel('devices', device_id)