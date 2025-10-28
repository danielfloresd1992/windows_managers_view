# capture_worker.py
import sys, os, json, base64, time
import time
from datetime import datetime

# Añadir src/ al sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, src_path)
from core.capture_exaple import capture_window_by_hwnd, pil_image_to_png_bytes

hwnd = int(sys.argv[1])


while True:
    buffer = capture_window_by_hwnd(hwnd)
    if buffer:
        image_bytes = pil_image_to_png_bytes(buffer, 'JPEG', 75)
        if image_bytes:
            header = {
                "timestamp": datetime.now().isoformat(),
                "size": len(image_bytes),
                "format": "JPEG"
            }
            print(json.dumps(header))  # Línea 1: encabezado JSON
            print(base64.b64encode(image_bytes).decode())  # Línea 2: imagen codificada
            sys.stdout.flush()
    time.sleep(1 / 120)