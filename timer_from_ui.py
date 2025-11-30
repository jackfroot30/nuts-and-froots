import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer


class UiTimer(QWidget):
    def __init__(self, ui_path="timer_ui.ui"):
        super().__init__()
        uic.loadUi(ui_path, self)

        # Internal countdown state (milliseconds)
        self.remaining_ms = 0
        self.initial_ms = 0

        # Timer: tick every 10 ms → centisecond resolution
        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self._tick)

        # Buttons from your UI:
        # pushButton     = Start
        # pushButton_2   = Pause
        # pushButton_3   = Reset
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.pause)
        self.pushButton_3.clicked.connect(self.reset)

        self.pushButton_2.setEnabled(False)  # pause disabled at start

        self._update_lcd()  # show 00:00:00

    # --- Helpers -------------------------------------------------------------

    def _input_to_ms(self):
        mins = self.spinBox.value()
        secs = self.spinBox_2.value()
        return (mins * 60 + secs) * 1000

    def _update_lcd(self):
        total_sec = self.remaining_ms // 1000
        minutes = total_sec // 60
        seconds = total_sec % 60
        centis = (self.remaining_ms % 1000) // 10

        # EXACT widget mapping from your UI
        self.lcdMinutes.display(f"{minutes:02d}")
        self.lcdSeconds.display(f"{seconds:02d}")
        self.lcdCS.display(f"{centis:02d}")

    # --- Controls ------------------------------------------------------------

    def start(self):
        # If fresh start → load from spinboxes
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

    # --- Tick logic ----------------------------------------------------------

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


# Run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UiTimer("timer_ui.ui")
    w.show()
    sys.exit(app.exec_())
