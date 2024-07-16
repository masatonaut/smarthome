from time import sleep

class SmartLight:
    def __init__(self, device_id, device_name, status='off', brightness=0):
        self.device_id = device_id
        self.device_name = device_name
        self.status = status
        self.brightness = brightness

    def get_status(self):
        return {
            'status': self.status,
            'brightness': self.brightness
        }

    def turn_on(self):
        if self.status == "on":
            print("Light is already on.")
            return
        self.status = "on"
        for i in range(0, 101, 10):
            self.brightness = i
            sleep(0.1)  # simulating gradual increase

    def turn_off(self):
        if self.status == "off":
            print("Light is already off.")
            return
        self.status = "off"
        self.brightness = 0

    def set_brightness(self, level):
        if 0 <= level <= 100:
            if self.status != "on":
                self.turn_on()
            self.brightness = level
        else:
            raise ValueError("Brightness level must be between 0 and 100")

    def __repr__(self):
        return f"SmartLight(device_id={self.device_id}, status={self.status}, brightness={self.brightness})"

    def toggle_status(self):
        self.status = 'on' if self.status == 'off' else 'off'