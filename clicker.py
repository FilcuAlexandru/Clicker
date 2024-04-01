import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpinBox, QComboBox, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
import pyautogui
import threading
import time

class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AutoClicker')
        self.setGeometry(200, 200, 400, 200)

        self.autoclicking = False

        layout = QVBoxLayout()

        duration_title = QLabel('Set clicker duration:')
        layout.addWidget(duration_title)

        duration_layout = QHBoxLayout()

        self.hour_spin = QSpinBox()
        self.hour_spin.setMaximum(9999)
        self.hour_spin.setSuffix(' hours')
        duration_layout.addWidget(self.hour_spin)

        self.minute_spin = QSpinBox()
        self.minute_spin.setMaximum(9999)
        self.minute_spin.setSuffix(' minutes')
        duration_layout.addWidget(self.minute_spin)

        self.second_spin = QSpinBox()
        self.second_spin.setMaximum(9999)
        self.second_spin.setSuffix(' seconds')
        duration_layout.addWidget(self.second_spin)

        layout.addLayout(duration_layout)

        options_title = QLabel('Click options:')
        layout.addWidget(options_title)

        self.click_button_combo = QComboBox()
        self.click_button_combo.addItems(["Left Click", "Right Click"])
        layout.addWidget(self.click_button_combo)

        self.click_type_combo = QComboBox()
        self.click_type_combo.addItems(["Single Click", "Double Click"])
        layout.addWidget(self.click_type_combo)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_autoclick)
        layout.addWidget(self.start_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_autoclick)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def start_autoclick(self):
        if not self.autoclicking:
            self.autoclicking = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.autoclick_thread = threading.Thread(target=self.autoclick_loop)
            self.autoclick_thread.start()

    def stop_autoclick(self):
        if self.autoclicking:
            self.autoclicking = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)

    def autoclick_loop(self):
        try:
            while self.autoclicking:
                interval = self.hour_spin.value() * 3600 + self.minute_spin.value() * 60 + self.second_spin.value()
                if interval == 0:
                    print("Interval cannot be zero. Autoclicking stopped.")
                    self.stop_autoclick()
                    break
                if self.click_button_combo.currentIndex() == 0:
                    button = 'left'
                else:
                    button = 'right'
                if self.click_type_combo.currentIndex() == 0:
                    click_type = 'single'
                else:
                    click_type = 'double'
                
                pyautogui.click(button=button, clicks=1, interval=0)
                time.sleep(interval)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoClickerApp()
    window.show()
    sys.exit(app.exec())
