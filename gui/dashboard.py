import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, messagebox, scrolledtext
from system import AutomationSystem
from devices import SmartLight, Thermostat, SecurityCamera
import datetime

class Dashboard:
    def __init__(self, master, automation_system):
        self.master = master
        self.automation_system = automation_system
        self.device_controls = {}  # Initialize the dictionary here
        self.master.title("Smart Home IoT Simulator")
        self.create_widgets()
        self.update_automation_status()

    def create_widgets(self):
        # Create a custom font
        customFont = tkFont.Font(family="Helvetica", size=12)

        # Automation status toggle
        self.automation_status = False  # Start with automation off
        self.automation_status_button = tk.Button(
            self.master, text="Toggle Automation System", bg="grey", fg="white",
            font=customFont, relief="raised", borderwidth=2,
            command=self.toggle_automation_status
        )
        self.automation_status_button.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        # Automation status bar
        self.status_bar = tk.Label(self.master, text="Automation Status: OFF", bg="red", fg="white", relief="sunken", anchor="w")
        self.status_bar.pack(side=tk.TOP, fill=tk.X)

        # Create a status frame at the top
        status_frame = tk.Frame(self.master)
        status_frame.pack(side=tk.TOP, fill=tk.X)

        # Initialize a dictionary to keep track of the status labels
        self.status_labels = {}

        # Create status labels for each device type
        self.status_labels['light'] = tk.Label(status_frame, text="Living Room Light: SmartLight Status: Off")
        self.status_labels['light'].pack(side=tk.TOP, fill=tk.X)

        self.status_labels['thermostat'] = tk.Label(status_frame, text="Living Room Thermostat: Thermostat Status: Off")
        self.status_labels['thermostat'].pack(side=tk.TOP, fill=tk.X)

        self.status_labels['camera'] = tk.Label(status_frame, text="Front Door Camera: SecurityCamera Status: Off")
        self.status_labels['camera'].pack(side=tk.TOP, fill=tk.X)

        # Device frames and controls
        for device in self.automation_system.devices:
            frame = tk.LabelFrame(self.master, text=device.device_name)
            
            # Create a status indicator for each device
            self.create_status_indicator(frame, device)
            
            # Create specific controls for each type of device
            if isinstance(device, SmartLight):
                self.create_light_controls(frame, device)
            elif isinstance(device, Thermostat):
                self.create_thermostat_controls(frame, device)
            elif isinstance(device, SecurityCamera):
                self.create_camera_controls(frame, device)
            
            frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Create a frame for log messages
        self.log_frame = tk.LabelFrame(self.master, text='Log')
        self.log_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Add a scrolled text area for logs
        self.log_area = scrolledtext.ScrolledText(self.log_frame, state='disabled', height=8)
        self.log_area.pack(fill='both', expand=True)

    def update_device_status_labels(self):
        # Updates the status labels based on the current status of each device
        for device in self.automation_system.devices:
            if isinstance(device, SmartLight):
                status = 'On' if device.status == 'on' else 'Off'
                self.status_labels['light'].config(text=f"Living Room Light: SmartLight Status: {status}")
            elif isinstance(device, Thermostat):
                status = 'On' if device.status == 'on' else 'Off'
                self.status_labels['thermostat'].config(text=f"Living Room Thermostat: Thermostat Status: {status}")
            elif isinstance(device, SecurityCamera):
                status = 'Streaming' if device.is_streaming else 'Not Streaming'  # Changed from 'device.status' to 'device.is_streaming'
                self.status_labels['camera'].config(text=f"Front Door Camera: SecurityCamera Status: {status}")


    def create_status_indicator(self, frame, device):
        # Initialize the controls dictionary for this device if it doesn't exist
        if device.device_id not in self.device_controls:
            self.device_controls[device.device_id] = {}
        
        # Create a canvas to draw the status circle
        canvas = tk.Canvas(frame, width=20, height=20)
        # Draw a circle on the canvas
        status_circle = canvas.create_oval(5, 5, 15, 15, fill='red')  # Red for 'off', green for 'on'
        
        # Update the status_circle color based on the device status
        if device.status == 'on':
            canvas.itemconfig(status_circle, fill='green')
        else:
            canvas.itemconfig(status_circle, fill='red')
        
        # Place the canvas on the frame
        canvas.pack(side=tk.LEFT, padx=5)
        
        # Store the canvas and status_circle in the controls dictionary for later access
        self.device_controls[device.device_id]['status_canvas'] = canvas
        self.device_controls[device.device_id]['status_circle'] = status_circle


    def update_status_indicator(self, device_id, new_status):
        if device_id in self.device_controls and 'status_circle' in self.device_controls[device_id]:
            canvas = self.device_controls[device_id]['status_canvas']
            status_circle = self.device_controls[device_id]['status_circle']
            # Determine color based on new_status, which can be 'on', 'off', True, or False
            color = 'green' if new_status == 'on' or new_status is True else 'red'
            canvas.itemconfig(status_circle, fill=color)
        else:
            print(f"Status circle not found for device {device_id}")



    def toggle_automation_status(self):
        # Toggle the automation status in the automation system
        self.automation_system.toggle_automation_status()

        # Update the automation system and status bar
        self.update_automation_status()

        # Log the event to the log area
        status_text = "ON" if self.automation_system.get_automation_status() else "OFF"
        self.log_event(f"Automation turned {status_text}")

    def update_automation_status(self):
            # Update the status bar based on the current automation status
            status = self.automation_system.get_automation_status()
            status_text = "ON" if status else "OFF"
            self.status_bar.config(text=f"Automation Status: {status_text}", bg="green" if status else "red")
        

    def create_light_controls(self, frame, light):
        # Slider for brightness
        brightness_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal")
        brightness_slider.set(50 if light.status == 'on' else 0)  # Initial position based on status
        brightness_slider.pack(side=tk.LEFT)
        brightness_slider.config(state=tk.NORMAL if light.status == 'on' else tk.DISABLED)
        brightness_slider.bind('<B1-Motion>', lambda event: self.change_brightness(light, brightness_slider.get()))

        # Toggle button for light
        toggle_button_text = tk.StringVar()
        toggle_button_text.set("Toggle OFF" if light.status == 'off' else "Toggle ON")
        toggle_button = tk.Button(frame, textvariable=toggle_button_text, command=lambda: self.toggle_light(light, brightness_slider, toggle_button_text))
        toggle_button.pack(side=tk.LEFT)

    def create_thermostat_controls(self, frame, thermostat):
        # Slider for temperature
        temp_slider = tk.Scale(frame, from_=10, to=30, orient="horizontal")
        temp_slider.set(20 if thermostat.status == 'on' else 0)  # Set the initial position of the slider
        temp_slider.pack(side=tk.LEFT)
        temp_slider.config(state=tk.ACTIVE if thermostat.status == 'on' else tk.DISABLED)
        temp_slider.bind('<B1-Motion>', lambda event: self.change_temperature(thermostat, temp_slider.get()))

        # Toggle button for thermostat
        toggle_button_text = tk.StringVar()
        toggle_button_text.set("Toggle OFF" if thermostat.status == 'off' else "Toggle ON")
        toggle_button = tk.Button(frame, textvariable=toggle_button_text, command=lambda: self.toggle_thermostat(thermostat, temp_slider, toggle_button_text))
        toggle_button.pack(side=tk.LEFT)

    def create_camera_controls(self, frame, camera):
        # Checkbox for motion detection
        motion_var = tk.BooleanVar(value=camera.is_motion_detected)
        motion_checkbox = tk.Checkbutton(frame, text="Motion Detection",
                                         variable=motion_var,
                                         command=lambda c=camera: self.toggle_motion_detection(c, motion_var.get()))
        motion_checkbox.pack(side=tk.LEFT)

        # Toggle button for camera streaming
        toggle_button = tk.Button(frame, text="Toggle Streaming", command=lambda c=camera: self.toggle_camera_streaming(c))
        toggle_button.pack(side=tk.LEFT)

    def change_brightness(self, light, brightness):
        # Check if the brightness is actually different to prevent redundant logs
        if light.brightness != brightness:
            light.set_brightness(brightness)  # Assuming set_brightness is a method of SmartLight
            self.log_event(f"{light.device_name} brightness set to {brightness}%")

    def change_temperature(self, thermostat, temperature):
        # Check if the temperature is actually different to prevent redundant logs
        if thermostat.target_temperature != temperature:
            thermostat.set_target_temperature(temperature)  # Assuming set_target_temperature is a method of Thermostat
            self.log_event(f"{thermostat.device_name} target temperature set to {temperature}°C")
            
    def toggle_thermostat(self, thermostat, slider, toggle_button_text):
        # Assuming the thermostat object has a method to toggle its status
        thermostat.toggle_status()
        new_status = thermostat.status

        # Update slider based on the new status
        slider.set(20 if new_status == 'on' else 10)
        slider.config(state=tk.ACTIVE if new_status == 'on' else tk.DISABLED)

        # Update button text based on the new status
        toggle_button_text.set("Toggle OFF" if new_status == 'off' else "Toggle ON")

        # Log the event
        self.log_event(f"{thermostat.device_name} turned {new_status}")
        self.update_device_status_labels()
        self.update_status_indicator(thermostat.device_id, thermostat.status)


    def toggle_motion_detection(self, camera, is_detected):
        camera.is_motion_detected = is_detected  # Directly set the attribute
        status = 'enabled' if is_detected else 'disabled'
        self.log_event(f"Motion detection for {camera.device_name} {status}")

        # If motion is detected, turn on the light and set the brightness to 50
        if is_detected:
            # Assuming you have a method to get the first light or a specific light
            light = self.automation_system.get_first_light()  # Implement this method accordingly
            if light:
                self.turn_on_light_by_motion(light)

    def turn_on_light_by_motion(self, light):
        # Set the light's brightness to 50 and status to 'on'
        light.set_brightness(50)  # Assuming there's a method in your SmartLight class
        light.status = 'on'

        # Log the event
        self.log_event(f"{light.device_name} brightness set to 50% due to motion detection")
        self.log_event(f"{light.device_name} turned on due to motion detection")

        # You can then call the update_device_status method to refresh the UI
        self.update_device_status()


    def toggle_camera_streaming(self, camera):
        # Assuming the camera object has a method to toggle its streaming status
        camera.toggle_streaming()
        new_status = 'Streaming' if camera.is_streaming else 'Not Streaming'

        # Update the status label for the camera
        self.update_status_indicator(camera.device_id, camera.is_streaming)

        # Log the event
        self.log_event(f"{camera.device_name} is now {new_status}")

        # Update the device status labels
        self.update_device_status_labels()
        self.update_status_indicator(camera.device_id, camera.is_streaming)


    def toggle_light(self, light, slider, toggle_button_text):
        # Determine the new status
        new_status = 'off' if light.status == 'on' else 'on'
        
        # Only proceed if the status is actually changing
        if light.status != new_status:
            light.status = new_status  # Update the light's status

            # Update the slider based on the new status
            slider.set(50 if new_status == 'on' else 0)
            slider.config(state=tk.NORMAL if new_status == 'on' else tk.DISABLED)

            # Update the toggle button text based on the new status
            toggle_button_text.set("Toggle ON" if new_status == 'on' else "Toggle OFF")

            # Log the event
            self.log_event(f"{light.device_name} turned {new_status}")

            # Update the status indicator for the light
            self.update_status_indicator(light.device_id, new_status)

            # Update the device status labels in the main status frame
            self.update_device_status_labels()
        else:
            # Log that the light is already in the requested state
            self.log_event(f"{light.device_name} is already {light.status}")

    def toggle_motion_detection(self, camera, is_detected):
        camera.is_motion_detected = is_detected  # Directly set the attribute
        status = 'enabled' if is_detected else 'disabled'
        self.log_event(f"Motion detection for {camera.device_name} {status}")
        # Update the dashboard UI if necessary

    def apply_style(self):
        style = ttk.Style()
        style.configure("TButton", font=('Helvetica', 12), padding=6)
        style.configure("TLabel", font=('Helvetica', 12), background="#e1e1e1")
        style.configure("TLabelframe", font=('Helvetica', 12), background="#e1e1e1")
        style.configure("TLabelframe.Label", font=('Helvetica', 12, 'bold'), background="#e1e1e1")
        # Apply styles to other widgets as needed


    def update_device_status(self):
        for device_id, control_dict in self.device_controls.items():
            device = self.automation_system.get_device_by_id(device_id)
            status_label = control_dict['status_label']
            status_label.config(text=f"Status: {device.status}")
            # Check if a slider exists for this device and update only if the status has changed
            if 'slider' in control_dict:
                # If the light is on, do not change the slider value
                # If the light is off, set it to 0
                if device.status == 'off':
                    control_dict['slider'].set(0)
                control_dict['slider'].config(state=tk.NORMAL if device.status == 'on' else tk.DISABLED)


    def log_event(self, message):
        # Check if the root Tkinter window is still existing
        if self.master.winfo_exists():
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {message}"
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, log_message + "\n")
            self.log_area.config(state='disabled')
            self.log_area.yview(tk.END)

    def run(self):
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        self.master.mainloop()

    def close(self):
        # This method handles the closure of the dashboard
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.automation_system.stop()
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    system = AutomationSystem()
    dashboard = Dashboard(root, system)
    dashboard.run()
