import os
import sys
import asyncio
import threading
import importlib

from pathlib import Path
from PySide2 import QtWidgets
from PySide2.QtWidgets import QFileDialog, QPushButton, QLabel

from watchfiles import awatch

sys.path.append(os.path.dirname(__file__))

from module_utils import find_module_by_path, get_package_dependencies

class AutoReloaderUI(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(AutoReloaderUI, self).__init__(parent)
        
        self.setWindowTitle("Auto Reloader")
        
        main_widget = QtWidgets.QWidget()
        self.setWidget(main_widget)
        
        main_widget.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
 
        open_file_button = QPushButton("Select folder")
        open_file_button.clicked.connect(self.open_file_dialog)

        self.selected_folder_label = QLabel("")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(open_file_button)
        layout.addWidget(self.selected_folder_label)
        main_widget.setLayout(layout)
 
        self._thread = None
        
       
    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setOption(QFileDialog.ShowDirsOnly)
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self._selected_path = file_path
            self.selected_folder_label.setText(self._selected_path)
            print(f"Selected folder: {file_path}")

            self.reset()
            
    def reset(self):
        if (self._thread):
            self._stop_event.set()
            self._thread.join()
        
        self._stop_event = asyncio.Event()
        self._thread = threading.Thread(target=asyncio.run, args=(self.file_watcher_wrapper(),)) 
        self._thread.start()
        
    def closeEvent(self, event) -> None:
        self._stop_event.set()
        self._thread.join()
        print("Closing Auto Reloader")
        
    async def file_watcher(self):
        async for changes in awatch(self._selected_path, stop_event=self._stop_event):
            with open(r"C:\temp\hello_world.txt", "a+") as file:
                try:
                    mod = find_module_by_path(str(Path(next(iter(changes), (None, None))[1])))
                    node_pkg_dict, node_depth_dict = get_package_dependencies(mod)
                    for (d,v) in sorted([(d,v) for v,d in node_depth_dict.items()], reverse=True):
                        try:
                            importlib.reload(node_pkg_dict[v])
                        except Exception as e:
                            file.writelines(e)
                    file.write(f"{mod}\n")
                    file.writelines(str(Path(next(iter(changes), (None, None))[1])))
                except Exception as e:
                    file.writelines(e)
	
    async def file_watcher_wrapper(self):
        await self.file_watcher()

def main():
    from qtmax import GetQMaxMainWindow

    main_window = AutoReloaderUI(parent=GetQMaxMainWindow())
    main_window.setFloating(True)
    main_window.show()
    
    
if __name__ == "__main__":
    main()