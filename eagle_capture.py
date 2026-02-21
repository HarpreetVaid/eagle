import os
import threading
from pynput import keyboard, mouse
import mss
import requests
from datetime import datetime

# Optional: For cross-platform desktop notifications
try:
    from plyer import notification
    HAS_NOTIFICATIONS = True
except ImportError:
    HAS_NOTIFICATIONS = False

# --- Configuration ---
EAGLE_API_URL = "http://127.0.0.1:8002/api/v1/eagle-llm/inference"
EAGLE_KEY = os.environ.get("EAGLE_KEY", "") # Fallback to empty if not set
SAVE_DIR = "notes"
# ---------------------

class EagleCapture:
    def __init__(self):
        self.buffer = []
        self.is_processing = False
        self.capture_region = None
        
        # Ensure save directory exists
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            
        print(f"[*] Eagle Capture initialized.")

    def notify(self, title, message):
        """Show a system notification."""
        print(f"\n[{title}] {message}")
        if HAS_NOTIFICATIONS:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    app_name="Eagle Capture",
                    timeout=2
                )
            except Exception as e:
                pass

    def capture_screen(self):
        """Take a screenshot (full screen or selected region) and save to a temporary file."""
        temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_screenshot.png")
        with mss.mss() as sct:
            if self.capture_region:
                # Capture specific region
                img = sct.grab(self.capture_region)
                mss.tools.to_png(img.rgb, img.size, output=temp_file)
            else:
                sct.shot(mon=-1, output=temp_file) 
        return temp_file

    def send_to_eagle(self, image_path):
        """Send the image to the local Eagle API for markdown extraction."""
        try:
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f, "image/png")}
                
                # Payload matching the Eagle API endpoint requirements
                data = {
                    "query": "Extract all text and preserve exact document formatting as Markdown.",
                    "pipeline": "eagle_parse", 
                    "eagle_key": EAGLE_KEY,
                    "markdown": "true", # Tell eagle to format as markdown
                }
                
                response = requests.post(EAGLE_API_URL, data=data, files=files, timeout=60)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    self.notify("API Error", f"Status: {response.status_code}. {response.text}")
                    return None
        except requests.exceptions.ConnectionError:
            self.notify("Connection Error", "Is the Eagle API running on port 8002?")
            return None
        except Exception as e:
            self.notify("Error", str(e))
            return None
            
    def _process_capture_thread(self):
        """Background thread to handle capture and API call without freezing the hotkey listener."""
        self.is_processing = True
        self.notify("Capturing", "Taking screenshot...")
        
        try:
            image_path = self.capture_screen()
            self.notify("Processing", "Sending to Eagle API...")
            
            result = self.send_to_eagle(image_path)
            
            if result:
                # Assuming Eagle returns a JSON with an "answer" or direct text based on the pipeline
                content = ""
                if isinstance(result, dict):
                    content = result.get('answer', result.get('text', str(result)))
                else:
                    content = str(result)
                    
                self.buffer.append(content)
                self.notify("Success", f"Added to buffer. (Items: {len(self.buffer)})")
            
            # Cleanup temp image
            if os.path.exists(image_path):
                os.remove(image_path)
                
        finally:
            self.is_processing = False

    def on_capture(self):
        """Hotkey handler for 'P'."""
        if self.is_processing:
            self.notify("Busy", "Still processing previous capture...")
            return
            
        # Run in thread so keyboard listener isn't blocked out
        threading.Thread(target=self._process_capture_thread).start()

    def on_save(self):
        """Hotkey handler for 'S'."""
        if self.is_processing:
            self.notify("Busy", "Wait for current capture to finish before saving.")
            return
            
        if not self.buffer:
            self.notify("Empty", "Nothing to save. Capture something first!")
            return
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Capture_{timestamp}.md"
        filepath = os.path.join(SAVE_DIR, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# Eagle Capture: {timestamp}\n\n")
                
                for i, content in enumerate(self.buffer):
                    f.write(f"## Capture {i+1}\n\n")
                    f.write(content)
                    f.write("\n\n---\n\n")
                    
            self.notify("Saved!", f"Saved {len(self.buffer)} items to {filename}")
            # Reset buffer
            self.buffer = []
            
        except Exception as e:
            self.notify("Save Error", str(e))

    def wait_for_region(self):
        """Wait for the user to click two points on the screen to define a region."""
        points = []
        
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                points.append((int(x), int(y)))
                if len(points) == 1:
                    print(f"Top-left set at {x}, {y}. Now click bottom-right.")
                if len(points) >= 2:
                    print(f"Bottom-right set at {x}, {y}.")
                    return False # Stop listener
                    
        print("\n[REGION SELECTOR]")
        print("Click the Top-Left corner of your desired capture area.")
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
            
        if len(points) >= 2:
            x1, y1 = points[0]
            x2, y2 = points[1]
            return {"top": min(y1, y2), "left": min(x1, x2), "width": abs(x2 - x1), "height": abs(y2 - y1)}
        return None

    def on_reset_region(self):
        """Hotkey handler for 'O' to reset the capture region."""
        if self.is_processing:
            self.notify("Busy", "Cannot reset region while capturing.")
            return
            
        self.is_processing = True
        try:
            self.notify("Reset Region", "Click Top-Left, then Bottom-Right.")
            new_rect = self.wait_for_region()
            if new_rect:
                self.capture_region = new_rect
                self.notify("Region Updated", f"New size: {new_rect['width']}x{new_rect['height']}")
        finally:
            self.is_processing = False

    def run(self):
        """Start listening for hotkeys."""
        self.notify("Setup", "Select capture region. Click Top-Left, then Bottom-Right.")
        self.capture_region = self.wait_for_region()
        self.notify("Ready", "Press P to capture, O to reset region, S/X to save.")
        
        # Use pynput GlobalHotKeys which works nicely in user space on Windows/Mac/Linux
        with keyboard.GlobalHotKeys({
            'p': self.on_capture,
            's': self.on_save,
            'x': self.on_save,
            'o': self.on_reset_region
        }) as h:
            print("Listening...")
            h.join()
        
        print("Exiting Eagle Capture...")

if __name__ == "__main__":
    app = EagleCapture()
    app.run()
