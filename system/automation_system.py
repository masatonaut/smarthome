import json
import time
import random
import threading
from devices import SmartLight, Thermostat, SecurityCamera
import os
from datetime import datetime
import csv

class AutomationSystem:
    def __init__(self):
        self.devices = []
        self._stop_event = threading.Event()  # Create an Event object to signal the thread to stop.
        self._automation_status = False  # Assuming automation is off by default
        self.stop_threads = False

    def set_automation_status(self, status):
        # Set automation status and perform any system-wide updates
        self.automation_active = status

        # If enabling automation, run automation tasks, else stop them
        if status:
            self.start_automation_tasks()
        else:
            self.stop_automation_tasks()

    def update_automation_status(self):
        if self.automation_system.automation_status:  # Assuming there is a boolean attribute 'automation_status'
            self.status_bar.config(text="Automation Status: ON", bg="green")
        else:
            self.status_bar.config(text="Automation Status: OFF", bg="red")

    def toggle_automation_status(self):
        self._automation_status = not self._automation_status
        # Add any logic here that should occur when automation status changes

    def get_automation_status(self):
        return self._automation_status

    def stop_automation_tasks(self):
        # Logic to stop automation tasks
        pass

    def discover_devices(self):
        # This is a placeholder for the actual discovery mechanism.
        # In a real-world scenario, you would have network requests or
        # other mechanisms to discover devices.
        pass

    def add_device(self, device):
        if device not in self.devices:
            self.devices.append(device)

    def get_device_by_id(self, device_id):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None

    def execute_automation_tasks(self):
        # This function could be expanded to include actual automation logic
        for device in self.devices:
            if isinstance(device, SecurityCamera) and device.is_motion_detected:
                for light in filter(lambda d: isinstance(d, SmartLight), self.devices):
                    light.set_brightness(50)

    def randomize_device_state(self):
        for device in self.devices:
            if isinstance(device, SmartLight):
                device.set_brightness(random.randint(0, 100))
            elif isinstance(device, Thermostat):
                device.set_target_temperature(random.randint(18, 26))

    def stop_threads_on(self):
        self.stop_threads = True

    def gather_sensor_data(self):
        while not self.stop_threads:
            for device in self.devices:
                if isinstance(device, SecurityCamera):
                    detected = device.is_motion_detected
                if isinstance(device, SmartLight):
                    brightness = device.brightness
                if isinstance(device, Thermostat):
                    temperature = device.get_status()['target_temperature']
            
        
            current_time = datetime.now()
            timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            sensor_data = [
                [timestamp , temperature, brightness, detected]
            ]

            file_path = "sensor_data.csv"
            write_header = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
            
            with open(file_path, mode="a") as file:
                writer = csv.writer(file)
                if write_header:
                    writer.writerow(["Timestamp", "Temperature (°C)", "Brightness", "Motion detected"])
                writer.writerows(sensor_data)

            time.sleep(1) #every 1 sec

    # def save_sensor_data_to_file(self):
    #     try:
    #         data = self.gather_sensor_data()
    #         with open('sensor_data.json', 'w') as file:
    #             json.dump(data, file, indent=4)
    #     except IOError as e:
    #         print(f"An error occurred while saving sensor data: {e}")


    def run(self):
        while not self._stop_event.is_set():  # Check the event in your loop.
            self.execute_automation_tasks()
            self.randomize_device_state()
            self.save_sensor_data_to_file()
            time.sleep(5)  # Sleep for 5 seconds, for example
            # It's a good practice to check the event again after sleeping
            if self._stop_event.is_set():
                break

    def stop(self):
        self._stop_event.set()  # Signal the thread to stop.

# Example of creating an AutomationSystem instance and adding devices
if __name__ == "__main__":
    system = AutomationSystem()
    # Create instances of your devices
    light = SmartLight('1', 'Living Room Light', 'off', 0)
    thermostat = Thermostat('2', 'Main Thermostat', 20)
    camera = SecurityCamera('3', 'Entrance Camera', False, 'off', False)

    # Add the devices to the tem
    system.add_device(light)
    system.add_device(thermostat)
    system.add_device(camera)

    # Here you could start the tem in a separate thread
    automation_thread = threading.Thread(target=system.run)
    automation_thread.start()
