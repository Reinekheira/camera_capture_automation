import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Paths
watch_folder = "./camera_captures"  # Folder where the camera saves images
uploaded_folder = "./uploaded"      # Folder for uploaded images
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b66f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure uploaded folder exists
os.makedirs(uploaded_folder, exist_ok=True)

# Event Handler
class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if file_path.endswith((".jpg", ".png", ".jpeg")):  # Only process image files
            print(f"New file detected: {file_path}")
            
            # Wait for 30 seconds
            time.sleep(30)
            
            # Upload the image
            print(f"Uploading {file_path}...")
            command = f'curl -X POST -F imageFile=@{file_path} {upload_url}'
            result = os.system(command)
            
            # If upload is successful, move the file
            if result == 0:
                print(f"Upload successful! Moving {file_path} to {uploaded_folder}")
                shutil.move(file_path, os.path.join(uploaded_folder, os.path.basename(file_path)))
            else:
                print(f"Failed to upload {file_path}. Retrying might be necessary.")

# Set up Watchdog Observer
observer = Observer()
event_handler = ImageHandler()
observer.schedule(event_handler, watch_folder, recursive=False)

# Start monitoring
print(f"Monitoring folder: {watch_folder}")
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
