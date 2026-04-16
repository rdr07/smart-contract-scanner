import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_backend():
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    subprocess.run([sys.executable, 'app.py'], cwd=backend_path)

def run_frontend():
    time.sleep(3)
    main_path = os.path.dirname(__file__)
    subprocess.run([sys.executable, 'serve.py'], cwd=main_path)

def open_browser():
    time.sleep(5)
    webbrowser.open('http://127.0.0.1:3000')

print("Starting SmartScan AI...")

Thread(target=run_backend, daemon=True).start()
Thread(target=run_frontend, daemon=True).start()
Thread(target=open_browser, daemon=True).start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")