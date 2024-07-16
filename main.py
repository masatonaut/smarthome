from tkinter import Tk
import threading
from system import AutomationSystem
from devices import SmartLight
from devices import Thermostat
from devices import SecurityCamera
from gui import Dashboard


def main():

    # Instantiate the automation system
    system = AutomationSystem()

    # Create instances of your devices
    light = SmartLight(device_id='1', device_name='Living Room Light', status='off', brightness=0)
    thermostat = Thermostat(device_id='2', device_name='Main Thermostat', target_temperature=10)
    camera = SecurityCamera(device_id='3', device_name='Entrance Camera', is_motion_detected=False, status='off', is_streaming=False)

    # Add the devices to the automation system
    system.add_device(light)
    system.add_device(thermostat)
    system.add_device(camera)

    # Initialize Tkinter root and the dashboard
    root = Tk()
    dashboard = Dashboard(root, system)
    
    store_sensor_data_thread = threading.Thread(target=system.gather_sensor_data)
    store_sensor_data_thread.start()
    
    # This will block until the window is closed
    dashboard.run()


    # Print initial states if needed (or you could log these)
    root.after(100, lambda: dashboard.log_event(f"Initial state of light: {light.get_status()}"))
    root.after(100, lambda: dashboard.log_event(f"Initial state of thermostat: {thermostat.get_status()}"))
    root.after(100, lambda: dashboard.log_event(f"Initial state of camera: {camera.get_status()}"))

    # After the window is closed and the dashboard.run() has finished executing, perform any cleanup if necessary
    system.stop()  # Ensure you have implemented this method
    system.stop_threads_on()
    store_sensor_data_thread.join()

if __name__ == "__main__":
    main()
