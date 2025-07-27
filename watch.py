import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

class Watcher(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or event.src_path.endswith('.git') or os.path.basename(event.src_path) in ['watch.py', 'push.bat']:
            return  # Ignore directories, .git, and the script itself to avoid loops
        print(f"Change detected in {event.src_path}, auto-uploading to GitHub...")
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", f"Auto commit: {time.ctime()}"])
        subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    path = "."
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Watching for changes... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()