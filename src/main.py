import win32gui
import win32ui
import win32con
import sys
import cv2
import numpy as np
from PIL import Image
import time





### MODELS AND DATA
from model.windows.list_windows import show_list_windows


###    CONTROLLER AND LOGIC
from core.capture_exaple import capture_window_by_hwnd
from core.run_controller import check_admin_privileges
from core.window_controller import activate_window, set_window_always_on_top, lock_window_position, send_text_to_window
from core.app_singleton import  AppSingleton

from utils.files.print_png import buffer_to_png
### COMPONENTS AND UI
##from gui.components.modal_msm import ModalDialog
##from gui.windows_main import MainWindow
from gui.components.SplashScreen import SplashScreen
from PySide6.QtWidgets import QSplashScreen
from gui.windows_main import MainWindow 

from PySide6.QtGui import QPixmap





def main():
    try:

        app = AppSingleton.initialize(sys.argv)
        splashScreen = SplashScreen()
        splashScreen.show()

        windowsPrincipal = MainWindow()
        

       


       
        windowsPrincipal.show()
        splashScreen.finish(windowsPrincipal)

        return AppSingleton.exec()
    
    except Exception as e:
        print(f'Fatal crash: {e}')
        import traceback
        traceback.print_exc()
        return 1






if __name__ == '__main__':  # FUNCTION MAIN
    sys.exit(main())


    check_admin_privileges(show_error)
    list_windows = show_list_windows()
    windows_seleted = None

    TARGET_FPS = 30
    # 2. Calcular el tiempo que debe durar cada fotograma (en segundos)
    TIME_PER_FRAME = 1.0 / TARGET_FPS
    

    for windows in list_windows:
        
        if(windows['title'] == 'iVMS-4200'):

            window = windows
            windows_seleted  = window['hwnd']
            hwnd_seleted = window['hwnd']
            """
            set_window_always_on_top( hwnd_seleted)
            buffer_image = capture_window_by_hwnd(hwnd_seleted)
            buffer_image.show()
            """

   

    """
    while True:
        start_time = time.time()
        set_window_always_on_top(windows_seleted)
        buffer_image = capture_window_by_hwnd(windows_seleted)

        if buffer_image is not None:

            frame_rgb = np.array(buffer_image)

            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
            cv2.imshow('Ventana de Captura', frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
     """
            
