class SecurityCamera:
    def __init__(self, device_id, device_name, is_motion_detected=False, status='off', is_streaming=False):
        self.device_id = device_id
        self.device_name = device_name
        self.is_motion_detected = is_motion_detected
        self.status = status
        self.is_streaming = is_streaming

    def get_status(self):
        return {
            'is_motion_detected': self.is_motion_detected,
            'is_streaming': self.is_streaming
        }

    def toggle_streaming(self):
        if self.is_streaming:
            print("Camera is already streaming.")
        else:
            self.is_streaming = True
            print("Camera streaming started.")

    def stop_streaming(self):
        if not self.is_streaming:
            print("Camera is not streaming.")
        else:
            self.is_streaming = False
            print("Camera streaming stopped.")

    def detect_motion(self, motion):
        self.is_motion_detected = motion
        if motion:
            print("Motion detected!")
        else:
            print("No motion detected.")

    def __repr__(self):
        return f"SecurityCamera(device_id={self.device_id}, is_motion_detected={self.is_motion_detected}, is_streaming={self.is_streaming})"

    def toggle_motion_detection(self, is_detected):
        self.is_motion_detected = is_detected
        # Additional code to handle the motion detection change
        
    def toggle_streaming(self):
        self.is_streaming = not self.is_streaming
        # Additional code to handle the camera streaming status change

    def set_motion_detection(self, is_detected):
        self.is_motion_detected = is_detected