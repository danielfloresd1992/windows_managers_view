import win32gui
import win32ui
import win32con
from PIL import Image
import ctypes
from ctypes import wintypes
import io



# Configurar PrintWindow
PrintWindow = ctypes.windll.user32.PrintWindow
PrintWindow.argtypes = [wintypes.HWND, wintypes.HDC, wintypes.UINT]
PrintWindow.restype = wintypes.BOOL


def capture_window_by_hwnd(hwnd):
    """
    Captura el contenido de una ventana específica por su HWND usando PrintWindow.
    Devuelve un objeto PIL Image o None si falla.
    """
    try:
        # Obtener dimensiones de la ventana
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top
        
        # Si la ventana está fuera de la pantalla (coordenadas negativas grandes) o tiene tamaño cero, puede fallar
        if width <= 0 or height <= 0:
            print("❌ Ventana con tamaño cero o negativo")
            return None

        # Obtener el contexto del dispositivo de la ventana
        hwndDC = win32gui.GetWindowDC(hwnd)
        if not hwndDC:
            print("❌ No se pudo obtener el DC de la ventana")
            return None

        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()
        
        # Crear bitmap compatible
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)
        
        # Intentar capturar con PrintWindow (PW_RENDERFULLCONTENT = 0x00000002)
        # PrintWindow puede capturar ventanas incluso si no están en primer plano
        result = PrintWindow(hwnd, saveDC.GetSafeHdc(), 2)
        
        if not result:
            print("❌ PrintWindow falló, intentando BitBlt...")
            # Fallback a BitBlt
            result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
        
        if result:
            # Convertir a formato PIL Image
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            im = Image.frombuffer(
                'RGB',
                (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                bmpstr, 'raw', 'BGRX', 0, 1
            )
            
            # Limpiar recursos
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            
            return im
        else:
            # Limpiar recursos en caso de error
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwndDC)
            return None
            
    except Exception as e:
        print(f"💥 Error capturando ventana: {e}")
        return None
    





def pil_image_to_png_bytes(imagen_pil):
    try:
        buffer = io.BytesIO()

        # 3. Guardar la imagen PIL en el buffer de memoria en formato PNG
        #    Esto codifica la imagen como bytes PNG.
        imagen_pil.save(buffer, format="PNG")
        
        # 4. Obtener los bytes codificados
        png_bytes = buffer.getvalue()
        buffer.close()
        
        # 5. Cargar los bytes PNG en QPixmap
        return png_bytes

    except Exception as e:
        print(f"💥 Error al convertir la imagen a QPixmap: {e}")
        return None