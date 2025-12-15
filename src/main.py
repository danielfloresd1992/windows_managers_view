import sys
import os
import numpy as np
from PIL import Image



### MODELS AND DATA
from model.windows.list_windows import open_windows_windows


###    CONTROLLER AND LOGIC
from core.capture_exaple import capture_window_by_hwnd
from core.run_controller import check_admin_privileges
from core.window_controller import activate_window, set_window_always_on_top, lock_window_position, send_text_to_window
from core.app_singleton import  AppSingleton


### COMPONENTS AND UI
##from gui.components.modal_msm import ModalDialog
##from gui.windows_main import MainWindow

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

from gui.windows_main import MainWindow 
from gui.components.SplashScreen import SplashScreen
from gui.components.render_box.render_box import Render_box
from gui.components.sidebar.sidebar_dock import Sidebar_Dock


        

def load_stylesheet():
    qss_path = os.path.join(os.path.dirname(__file__), 'gui\styles\global.qss')

    if os.path.exists(qss_path):
        print('Loading stylesheet from:', qss_path)
        with open(qss_path, 'r') as f:
            return f.read()
    else: print('Stylesheet file not found:', qss_path)





def main():
    try:
        app = AppSingleton.initialize(sys.argv)
        app.setStyleSheet(load_stylesheet())

        splashScreen = SplashScreen()
        splashScreen.show()

        windowsPrincipal = MainWindow()
    
        #asidebar = Sidebar_Dock(windowsPrincipal, title='Ventanas disponibles', src_ico='src/resources/ico.png')
        
       
    
        
        windowsPrincipal.show()
        splashScreen.finish(windowsPrincipal)

        return app.exec()
    
    except Exception as e:
        print(f'Fatal crash: {e}')
        import traceback
        traceback.print_exc()
        return 1






if __name__ == '__main__':  # FUNCTION MAIN

    sys.exit(main())