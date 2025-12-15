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
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QDockWidget, QTextEdit
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
        list_windows = open_windows_windows()
        app = AppSingleton.initialize(sys.argv)
        app.setStyleSheet(load_stylesheet())
        
        splashScreen = SplashScreen()
        splashScreen.show()

        window_containter = MainWindow()
        windowsPrincipal = window_containter.window_child 
    
        
        
        asidebar = Sidebar_Dock(parent=None, title='Visión', src_ico='src/resources/ico.png')
        asidebar.print_list(list_windows)
        
        dock = QDockWidget(None)
        dock.setWidget(asidebar)
        dock.setStyleSheet("""
            QDockWidget::title {
                padding: 0px;       /* elimina espacio interno */
                margin: 0px;        /* elimina espacio externo */
                spacing: 0px;       /* elimina separación entre ícono y texto */
                text-align: center; /* centra el texto */
            }
            QDockWidget::close-button, QDockWidget::float-button {
                width: 0px;
                height: 0px;
            }
        """)
        
        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dock.setTitleBarWidget(QWidget())
        windowsPrincipal.addDockWidget(Qt.LeftDockWidgetArea, dock)  # lo acoplas a la izquierda
    
    
        box = Render_box()
        windowsPrincipal.setCentralWidget(box)
        
        
        
        window_containter.show()
        splashScreen.finish(windowsPrincipal)

        return app.exec()
    
    except Exception as e:
        print(f'Fatal crash: {e}')
        import traceback
        traceback.print_exc()
        return 1






if __name__ == '__main__':  # FUNCTION MAIN

    sys.exit(main())