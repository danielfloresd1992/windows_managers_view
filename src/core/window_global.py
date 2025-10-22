from PySide6.QtCore import QObject, Signal, QThread
import win32api
import win32gui
import win32con
import pythoncom
import time





class Windows_monitor(QObject):



    windows_event_detected = Signal(list)


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Windows_monitor, cls).__new__(cls)
            cls._instance._list_windows = cls._gather_list_windows()
        return cls._instance




    def __init__(self, parent=None):
        # Asegura que QObject.__init__ se llama solo una vez
        if not hasattr(self, '_initialized'):

  
            super().__init__(parent)
            self._initialized = True


    @property
    def show_windiws(self):
        return self._list_windows




    def _gather_list_windows(): 
        windows = []
        def enum_windows_proc(hwnd, param):

            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append({
                    'hwnd': hwnd,
                    'title': win32gui.GetWindowText(hwnd),
                    'class': win32gui.GetClassName(hwnd)
                })
            return True
        
        win32gui.EnumWindows(enum_windows_proc, None)
        return windows

  

