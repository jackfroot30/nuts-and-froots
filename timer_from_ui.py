import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer
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
        #timer object of QTimer (a cclass), the timeout function calls the function in connect(connect attaches a fn to the signal emitted by timeout, the signal is emitted after a certain interval, which is defined in line 19 as 10 ms) 

        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.pause)
        self.pushButton_3.clicked.connect(self.reset)
        # 

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UiTimer("timer_ui.ui")
    w.show()
    sys.exit(app.exec_())
