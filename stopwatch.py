import sys
from PyQt5 import (uic, QtWidgets)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsView, QGraphicsOpacityEffect,QLabel,QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QTimer, QTime, Qt, QPropertyAnimation, QEvent, QRect, QEasingCurve, QSequentialAnimationGroup, QPauseAnimation, QAbstractAnimation
from PyQt5.QtTest import QTest


class Stopwatch(QMainWindow):
    def __init__(self,ui_path="Main_med.ui"):
        super().__init__()
        uic.loadUi(ui_path,self)
        self.tabWidget.setCurrentIndex(3)
        self.time = QTime(0,0,1,0)
        self.time_1 = QTime(0,0,1,0)
        self.time_1 = QTime(0,0,1,0)
        self.btime = QTime(0,0,0,0)
        self.timer = QTimer(self)
        self.timer.setInterval(10)
        self.timer_1 = QTimer(self)
        self.timer_1.setInterval(10)
        self.timer_1.setInterval(12000)
        self.btimer = QTimer(self)
        self.btimer.setInterval(4000)

        # not sure if i like the opacity settings
        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(.7)
        self.label_2.setGraphicsEffect(self.opacity_effect)

        self.cycles = 0 

        self.timer.timeout.connect(self.update_display)
        self.timer_1.timeout.connect(self.update_display_1)
        self.btimer.timeout.connect(self.update_display4)
        self.prog_lbl_7.setHidden(True)
        self.label_2.setHidden(True)
        self.prog_lbl_8.setHidden(True)
        self.prog_lbl_9.setHidden(True)
        self.prog_lbl_10.setHidden(True)
        self.scan_btn_4.clicked.connect(self.start_sesh)
    
    def start_sesh(self):
        self.prog_lbl_7.setText("Ready") # sets the text to ready
        self.lbl_timer = QTimer() # making timer
        self.lbl_timer.setSingleShot(True) # turning the timer into a timer that works just once
        self.lbl_timer.setInterval(1000) # setting the duration of the timer to 1 sec
        self.lbl_timer.start()
        self.lbl_timer.timeout.connect(self.lbl_change)
        self.start()
        # self.timer.timeout.connect(lambda:self.reset())

    def lbl_change(self):
        self.prog_lbl_7.setText("Go!")
        self.prog_lbl_4.setText("Breathe In")

    def start(self):
        QTimer.singleShot(1000, self.start1)

    def start1(self):
        self.time = QTime(0, 0, 1, 0)
        self.btime = QTime(0, 0, 0, 0)
        self.prog_lbl_8.setText(self.format_time(self.time))
        self.cycles = 0

        self.timer.start()    
        self.btimer.start()

        loops = int(self.spinBox_2.value())*5
        self.circ_anim(loop_count=loops, ms=4000)
        
    def stop(self):
        self.timer.stop()
        self.btimer.stop()
        self.timer_1.stop()

    def reset(self):
        self.timer.stop()
        self.time = QTime(0, 0, 1, 0)
        self.prog_lbl_8.setText(self.format_time(self.time))

    def format_time(self, time):
        seconds = time.second()
        return f"{seconds:01}"
    
    def format_time_1(self, time):
        seconds = time.second()//12
        return f"Number of Cycles Completed: {seconds:02}"

    def update_display(self):
        self.time = self.time.addMSecs(10)
        self.prog_lbl_8.setText(self.format_time(self.time))
    
    def update_display_1(self):
        # self.time_1 = self.time_1.addMSecs(10)
        self.time_1 = self.time_1.addMSecs(12000)
        self.prog_lbl_10.setText(self.format_time_1(self.time_1))
        self.cycles+=1
        if self.cycles==(self.spinBox_2.value()*5):
           self.stop()

    def update_display4(self):
        self.btime = self.btime.addMSecs(4000)
        s = int(self.format_time(self.btime))//4
        if s%3==0:
            self.prog_lbl_4.setText("Breathe In")
        elif s%3==1:
            self.prog_lbl_4.setText("Hold your Breath")
        elif s%3==2:
            self.prog_lbl_4.setText("Breathe Out")
        self.reset()

        if self.cycles!=(self.spinBox_2.value()*5):
            self.timer.start()
    
    def eventFilter(self, source, event):
        if source is self.label_2 and event.type() == QEvent.Resize:
            w = self.label_2.width()
            h = self.label_2.height()
            side = min(w, h)

            self.label_2.setStyleSheet("""
                background-color: qradialgradient(
                                       spread:pad, 
                                       cx:0.5, 
                                       cy:0.5,
                                       radius:0.8, 
                                       fx:0.5, 
                                       fy:0.5, 
                                       stop:0 #FFD5D5, 
                                       stop:0.26 #FFB5B5, 
                                       stop:1 #FFD5F6); 
                border:0px; 
                border-radius: {side//2}px;
            """)
        return super().eventFilter(source, event)
    
    #285,270,300,300

    def circ_anim(self, loop_count=1, ms=4000):
        if hasattr(self, "anim_group") and self.anim_group is not None:
            try:
                self.anim_group.stop()
            except Exception:
                pass

        start_rect = self.label_2.geometry()
        side = min(start_rect.width(), start_rect.height())
        cx = start_rect.center().x()
        cy = start_rect.center().y()
        start_rect = QRect(cx - side//2, cy - side//2, side, side)
        end_side = side + 250
        end_rect = QRect(cx - end_side//2, cy - end_side//2, end_side, end_side)
        anim_expand = QPropertyAnimation(self.label_2, b"geometry")
        anim_expand.setDuration(ms)
        anim_expand.setStartValue(start_rect)
        anim_expand.setEndValue(end_rect)
        anim_expand.setEasingCurve(QEasingCurve.InOutQuad)
        pause = QPauseAnimation(ms)
        anim_contract = QPropertyAnimation(self.label_2, b"geometry")
        anim_contract.setDuration(ms)
        anim_contract.setStartValue(end_rect)
        anim_contract.setEndValue(start_rect)
        anim_contract.setEasingCurve(QEasingCurve.InOutQuad)
        anim_expand.valueChanged.connect(self.update_circle_radius)
        anim_contract.valueChanged.connect(self.update_circle_radius)
        self.anim_group = QSequentialAnimationGroup(self)
        self.anim_group.addAnimation(anim_expand)
        self.anim_group.addAnimation(pause)
        self.anim_group.addAnimation(anim_contract)
        self.anim_group.setLoopCount(loop_count)
        if hasattr(self.anim_group, "currentLoopChanged"):
            self.anim_group.currentLoopChanged.connect(self.on_loop_changed)
        self.anim_group.finished.connect(self.on_anim_finished)
        self.anim_group.start()

    def update_circle_radius(self, _value):
        w = self.label_2.width()
        h = self.label_2.height()
        side = min(w, h)
        self.label_2.setStyleSheet(
            f"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, "
            f"radius:0.8, fx:0.5, fy:0.5, stop:0 #FFD5D5, stop:0.26 #FFB5B5, stop:1 #FFD5F6); "
            f"border:0px; border-radius: {side//2}px;"
        )

    def on_loop_changed(self, loop_index):
        current_cycle = loop_index
        self.prog_lbl_10.setText(f"Number of Cycles Completed: {current_cycle:02}")

    def on_anim_finished(self):
        self.stop()
        self.prog_lbl_10.setText(f"Number of Cycles completed: {self.spinBox_2.value()*5:02}")
        self.prog_lbl_7.setText("Done")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())

#insane enough to use decorators, get runtime of each timer, find the difference in runtime then put the former timers to sleep for that long? (timer starts - put to sleep for a vvv short amt of time - continues working when the next one starts working) - ??? - increase in runtime due to increase in statements? - maybe dont do this
