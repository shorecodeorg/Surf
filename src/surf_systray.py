import pystray
import threading
import psutil
import os
import sys
import subprocess
from dataclasses import dataclass
from PIL import Image
import PySide6
from qt_material import apply_stylesheet
from PySide6.QtWidgets import QApplication
from surf_filepaths import Files
from surf_main import Ui_MainWindow

files = Files()
filelist = files.get_files_list()
# Path to the Excel file
icon_fp = filelist[3]
surf_main_fp = filelist[2]

def chat_main():
    subprocess.run(['python3', surf_main_fp])
    

def on_exit(icon, pid):
    os.kill(pid, 9)
    icon.stop()
    print("Exiting")  # Or add any other code if needed
    exit(0)

@dataclass
class Surf:
    def run_surf(self):
        pids = self.get_pids()
        surf_thread = threading.Thread(target=self.launch_gui)
        surf_thread.start()
        new_pids = self.get_pids()
        for np in new_pids:
            if np not in pids:
                self.surf_pid = np
    def get_pids(self):
        pids = list()
        for proc in psutil.process_iter(['pid', 'name']):
            pids.append(proc.info['pid'])
        return pids
    def launch_gui(self):
        surf = QApplication(sys.argv)
    
        # Apply your UI setup to this main window instance
        ui = Ui_MainWindow()
        ui.setupUi(ui)  # Pass the instance to setupUi
        
        # setup stylesheet
        apply_stylesheet(surf, theme='dark_orange.xml')
        # Show the main window
        ui.show()
        
        sys.exit(surf.exec())        

surf = Surf()
surf.surf_pid = 0

# Create an image to be used as the tray icon
image = Image.open(icon_fp)  # Replace "icon.png" with the path to your icon image file

# Create a menu for the system tray icon
menu = (
    pystray.MenuItem('Run SURF', lambda: surf.run_surf()),
    pystray.MenuItem('Exit', lambda: on_exit(icon, surf.surf_pid)))


# Create the system tray icon with the menu
icon = pystray.Icon("SURF", image, "SURF", menu)

# Run the script as long as the icon is visible
if __name__ == '__main__':
    icon.run()
