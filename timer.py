import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtCore import QTimer, QPropertyAnimation
# import everything !!


class UiTimer(QWidget):
    def __init__(self, ui_path="timer_ui.ui"):
        super().__init__()
        uic.loadUi(ui_path, self)
        # get timer_ui.ui from qt designer

        self.remaining_ms = 0
        self.initial_ms = 0
        #initialising time remaining and time to count down from

        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self._tick)
        pushButton = self.pushButton
        self.pushButton = HoverButton(pushButton.text(), pushButton.parent())
        self.pushButton.setGeometry(pushButton.geometry())
        self.pushButton.setStyleSheet(pushButton.styleSheet())      
        self.pushButton.setFont(pushButton.font())                  
        self.pushButton.setSizePolicy(pushButton.sizePolicy())      
        self.pushButton.setCursor(pushButton.cursor())        
        pushButton.hide()
        self.pushButton.show()
        self.pushButton.clicked.connect(self.start)


        pushButton_2 = self.pushButton_2
        self.pushButton_2 = HoverButton(pushButton_2.text(), pushButton_2.parent())
        self.pushButton_2.setGeometry(pushButton_2.geometry())
        self.pushButton_2.setStyleSheet(pushButton_2.styleSheet())      
        self.pushButton_2.setFont(pushButton_2.font())                  
        self.pushButton_2.setSizePolicy(pushButton_2.sizePolicy())      
        self.pushButton_2.setCursor(pushButton_2.cursor())        
        pushButton_2.hide()
        self.pushButton_2.show()
        self.pushButton_2.clicked.connect(self.pause)


        pushButton_3 = self.pushButton_3
        self.pushButton_3 = HoverButton(pushButton_3.text(), pushButton_3.parent())
        self.pushButton_3.setGeometry(pushButton_3.geometry())
        self.pushButton_3.setStyleSheet(pushButton_3.styleSheet())      
        self.pushButton_3.setFont(pushButton_3.font())                  
        self.pushButton_3.setSizePolicy(pushButton_3.sizePolicy())      
        self.pushButton_3.setCursor(pushButton_3.cursor())        
        pushButton_3.hide()
        self.pushButton_3.show()
        self.pushButton_3.clicked.connect(self.reset)

        self.pushButton_2.setEnabled(False)

        self._update_lcd() 

    def _input_to_ms(self):
        mins = self.spinBox.value()
        secs = self.spinBox_2.value()
        return (mins * 60 + secs) * 1000

    def _update_lcd(self):
        total_sec = self.remaining_ms // 1000
        minutes = total_sec // 60
        seconds = total_sec % 60
        centis = (self.remaining_ms % 1000) // 10

        self.lcdMinutes.display(f"{minutes:02d}")
        self.lcdSeconds.display(f"{seconds:02d}")
        self.lcdCS.display(f"{centis:02d}")

    def start(self):

        if self.remaining_ms <= 0:
            ms = self._input_to_ms()
            if ms <= 0:
                return
            self.remaining_ms = ms
            self.initial_ms = ms

        self.timer.start()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.spinBox.setEnabled(False)
        self.spinBox_2.setEnabled(False)

    def pause(self):
        self.timer.stop()
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)

    def reset(self):
        self.timer.stop()
        self.remaining_ms = self.initial_ms
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.spinBox.setEnabled(True)
        self.spinBox_2.setEnabled(True)
        self._update_lcd()

    def _tick(self):
        self.remaining_ms -= 10
        if self.remaining_ms <= 0:
            self.remaining_ms = 0
            self.timer.stop()
            QApplication.beep()
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(False)
            self.spinBox.setEnabled(True)
            self.spinBox_2.setEnabled(True)

        self._update_lcd()

class HoverButton(QPushButton):
    def __init__(self,*args):
        super().__init__(*args)
        self.base_geometry = None

    def enterEvent(self, event):
        if self.base_geometry is None:
            self.base_geometry = self.geometry()

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(50)
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(self.base_geometry.adjusted(-2, -2, 2, 2))  
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(150)
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(self.base_geometry)
        self.anim.start()
        super().leaveEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UiTimer("timer.ui")
    w.show()
    sys.exit(app.exec())
