import random

class Thermostat:
    def __init__(self, device_id, device_name, target_temperature=10):
        self.device_id = device_id
        self.device_name = device_name
        self.current_temperature = random.randint(10, 30)  # Random starting temperature
        self.target_temperature = target_temperature
        self.status = 'off'
    
    def get_status(self):
        return {
            'current_temperature': self.current_temperature,
            'target_temperature': self.target_temperature,
            'status': self.status
        }

    def turn_on(self):
        if self.status == 'on':
            print("Thermostat is already on.")
        else:
            self.status = 'on'

    def turn_off(self):
        if self.status == 'off':
            print("Thermostat is already off.")
        else:
            self.status = 'off'

    def set_target_temperature(self, temperature):
        if 10 <= temperature <= 30:
            self.target_temperature = temperature
        else:
            raise ValueError("Target temperature must be between 10 and 30 degrees.")

    def update_temperature(self):
        if self.status == 'on':
            difference = self.target_temperature - self.current_temperature
            self.current_temperature += difference / 10

    def randomize_temperature(self):
        fluctuation = random.uniform(-0.5, 0.5)
        new_temp = self.current_temperature + fluctuation
        self.current_temperature = max(0, min(new_temp, 40))

    def __repr__(self):
        return f"Thermostat(device_id={self.device_id}, current_temperature={self.current_temperature}, target_temperature={self.target_temperature}, status={self.status})"

    def toggle_status(self):
        self.status = 'on' if self.status == 'off' else 'off'