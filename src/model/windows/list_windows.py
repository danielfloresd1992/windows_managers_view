import win32gui
import win32con
import pyautogui
import time


# ASSEMBLES A LIST OF EXISTING WINDOWS
def show_list_windows(): 
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
