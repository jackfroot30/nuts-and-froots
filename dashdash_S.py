import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QCompleter, QWidget, QHBoxLayout, 
                             QFrame, QListView, QVBoxLayout,
                             QButtonGroup, QLabel, QSpinBox,
                             QMessageBox)
from PyQt6 import uic, QtGui
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QDate, QPropertyAnimation, pyqtSignal,QTimer
import pandas as pd
import sqlite3
from sqlite3 import Error
import database
from datetime import date
import cv2
import google.generativeai as genai
from PIL import Image
import numpy as np
import time
import re 


class StartScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("HomeScreen.ui",self)
        start_btn = self.start_btn
        self.start_btn = HoverButton(start_btn.text(), start_btn.parent())
        self.start_btn.setGeometry(start_btn.geometry())
        self.start_btn.setStyleSheet(start_btn.styleSheet())      
        self.start_btn.setFont(start_btn.font())                  
        self.start_btn.setSizePolicy(start_btn.sizePolicy())      
        self.start_btn.setCursor(start_btn.cursor())        
        start_btn.hide()
        self.start_btn.show()
        self.start_btn.clicked.connect(self.profile_info)
        self.food_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_f.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.recipe_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_r.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.workout_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_w.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scrollArea.setWidgetResizable(True)
        self.page_contents.setMinimumHeight(1000)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.layout = QVBoxLayout(self.page_contents)
        self.open = MainWindow()
        self.food_scan_button.clicked.connect(self.open.open_Scanner)
        self.show()


    def profile_info(self):
        self.win = Profile()
        self.win.show()
        self.hide()


class Profile(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Profile.ui",self)
        view1 = QListView()
        view2 = QListView()
        view1.setFrameShape(QFrame.Shape.NoFrame)
        view2.setFrameShape(QFrame.Shape.NoFrame)
        profile_btn = self.profile_btn
        self.profile_btn = HoverButton(profile_btn.text(), self)
        self.profile_btn.setGeometry(profile_btn.geometry())
        self.profile_btn.setStyleSheet(profile_btn.styleSheet())      
        self.profile_btn.setFont(profile_btn.font())                  
        self.profile_btn.setSizePolicy(profile_btn.sizePolicy())      
        self.profile_btn.setCursor(profile_btn.cursor())        
        profile_btn.hide()
        self.profile_btn.clicked.connect(self.main_window)
        self.init_db()
        self.save_db()
        self.line_name.returnPressed.connect(self.save_db)
        self.line_goal.returnPressed.connect(self.save_db)
        self.line_height.returnPressed.connect(self.save_db)
        self.line_age.returnPressed.connect(self.save_db)
        self.line_weight.returnPressed.connect(self.save_db)

            
    def init_db(self):
        connection = sqlite3.connect("entries.db")
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                        name TEXT,
                        age INTEGER,
                        weight INTEGER,
                        goal_weight INTEGER,
                        height INTEGER
                        )
                """)
                connection.commit()
            except Error as e:
                print(e)
                sys.exit(1)
            finally:
                connection.close()

    def save_db(self):
        ipn = self.line_name.text().strip()
        ipa = self.line_age.text().strip()
        ipg = self.line_goal.text().strip()
        ipw = self.line_weight.text().strip()
        iph = self.line_height.text().strip()
        connection = sqlite3.connect("entries.db")
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO entries (name, age, goal_weight, weight, height)
    VALUES (?, ?, ?, ?, ?)""", (ipn, ipa, ipg, ipw, iph))
        connection.commit()
        connection.close()
        print('Inserted')

    def main_window(self):
        self.win = MainWindow()
        self.win.show()
        self.hide()
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Main.ui", self)
        self.setGeometry(300,0,890,1000)
        self.df = pd.read_csv("fitness_data.csv")
        ingredients = self.df['Ingredient']
        self.completer = QCompleter(set(ingredients))
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        popup = self.completer.popup()
        popup.setMinimumWidth(400)
        popup.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        popup.setStyleSheet("""
                            QListView{
                            background-color:white;
                            border:1px solid #C0C0C0;
                            border-radius:10px;
                            color:#000000;
                            font: 300 13pt "Epilogue";
                            padding-left:5px;
                            min-height:40px;
                        }
                        QListView::item
                        {
                        background-color: #ebebeb;
                        font:200 10px "Epilogue";
                        border:none;
                        padding:5px;
                        min-height:30px;
                        }
                        QListView::item:hover {
                        background-color: #C0C0C0;
                        color: black;
                }
        """)
        self.nav_buttons = QButtonGroup(self)
        self.nav_buttons.addButton(self.dashboard_btn,0)
        self.nav_buttons.addButton(self.recipe_btn, 1)
        self.nav_buttons.addButton(self.exercise_btn, 2)
        self.nav_buttons.addButton(self.mediation_btn, 3)
        self.nav_buttons.addButton(self.profile_btn, 4)
        self.nav_buttons.idClicked.connect(self.tabWidget.setCurrentIndex)
        self.dashboard_btn.setChecked(True)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().hide()
        self.today = QDate.currentDate()
        self.date_text = self.today.toString("dddd, MMMM d, yyyy")
        self.day_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prog_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if hasattr(self, "day_lbl"):
            self.day_lbl.setText(self.date_text)
        self.cal_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prot_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.carbs_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fats_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rows = []
        self.total_cal = 0
        self.total_prot = 0
        self.total_carbs = 0
        self.total_fat = 0
        self.update_totals()
        self.cal_counter.setText(f"{self.total_cal:.0f} kcal")
        self.prot_counter.setText(f"{self.total_prot:.1f} g")
        self.carbs_counter.setText(f"{self.total_carbs:.1f} g")
        self.fats_counter.setText(f"{self.total_fat:.1f} g")
        self.scrollArea.setWidgetResizable(True)
        self.scroll_contents.setMinimumHeight(1400)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        QVBoxLayout(self.scroll_contents)
        scan_btn = self.scan_btn
        self.scan_btn = HoverButton(scan_btn.text(), scan_btn.parent())
        self.scan_btn.setGeometry(scan_btn.geometry())
        self.scan_btn.setStyleSheet(scan_btn.styleSheet())      
        self.scan_btn.setFont(scan_btn.font())                      
        self.scan_btn.setSizePolicy(scan_btn.sizePolicy())      
        self.scan_btn.setCursor(scan_btn.cursor())        
        scan_btn.hide()
        self.scan_btn.show()
        self.scan_btn.clicked.connect(self.open_Scanner)
        if hasattr(self, 'search_bar'):
            self.search_bar.setCompleter(self.completer)
        self.ingredients_layout = QVBoxLayout()
        self.ingr_add.setLayout(self.ingredients_layout)
        self.ingredients_layout.setContentsMargins(10,10,10,10)
        self.ingredients_layout.setSpacing(10)
        self.search_bar.returnPressed.connect(self.fetch_data)
        self.save_recipe_btn.clicked.connect(self.save_recipe)
        recipe_t = self.recipe_t
        self.recipe_t = HoverButton(recipe_t.text(), recipe_t.parent())
        self.recipe_t.setGeometry(recipe_t.geometry())
        self.recipe_t.setStyleSheet(recipe_t.styleSheet())      
        self.recipe_t.setFont(recipe_t.font())                      
        self.recipe_t.setSizePolicy(recipe_t.sizePolicy())      
        self.recipe_t.setCursor(recipe_t.cursor())        
        recipe_t.hide()
        self.recipe_t.show()
        self.load_profile()
        self.recipe_t.clicked.connect(lambda : self.tabWidget.setCurrentIndex(1))
        


    def counters(self):
        self.rows = []
        self.calories = 0
        self.protein = 0
        self.carbs = 0 
        self.fats = 0
        
    def fetch_data(self):
        name = self.search_bar.text().strip().lower()
        if name == "":
            return
        self.df["Ingredient_clean"] = (
            self.df["Ingredient"]
            .str.replace('"', '', regex=False)
            .str.strip()
            .str.lower()
        )
        data = self.df[self.df["Ingredient_clean"].str.contains(name, regex=False)]
        if data.empty:
            print("Ingredient not found")
            return
        row = data.iloc[0]
        macros = {
            "cal": float(row["Calories"]),
            "prot": float(row["Protein"]),
            "carbs": float(row["Carbs"]),
            "fat": float(row["Fat"])
        }
        self.add_ingr(row["Ingredient"].replace('"', '').strip(), macros)
        self.search_bar.clear()


    def add_ingr(self, ingredient_name, macros):
        row = IngredientAdd(ingredient_name, macros)
        row.setStyleSheet("""
            QWidget {
                background-color: #f9f6ff;
                border-radius: 12px;
                font: 14px 'Epilogue';
                color: #1D1D1D;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #d7d7d7; 
                border-radius: 8px;
                padding: 6px 10px;
                color: #1D1D1D;
            }
            QPushButton:hover {
                background-color: #C0C0C0;
            }
            QSpinBox {
                border: 1px solid #d7d7d7;
                border-radius: 8px;
                padding: 4px;
                color: #1D1D1D;
                background-color: white; /* Ensure background is white */
            }
            
            /* THIS HIDES THE WEIRD ARROWS */
            QSpinBox::up-button, QSpinBox::down-button {
                width: 0px;
                border: none;
                background: transparent;
            }
        """)
        row.change.connect(self.update_totals)
        row.removed.connect(self.remove_row)
        self.rows.append(row)
        self.ingredients_layout.addWidget(row)
        self.update_totals()
    
    def save_recipe(self):
        recipe_name = self.recipe_name_input.text().strip()
        if recipe_name == "":
            QMessageBox.warning(self, "Error", "Enter recipe name")
            return
        for row in self.rows:
            macros = row.macros
            qty = row.qty.value()
            self.save_to_db(recipe_name, row.name,{
                "cal": float(macros["cal"])*qty,
                "prot": float(macros["prot"])*qty,
                "carbs": float(macros["carbs"])*qty,
                "fat": float(macros["fat"])*qty
            })
        self.load_today_meals()
        print("Recipe saved")
    
    def remove_row(self, row):
        self.ingredients_layout.removeWidget(row)
        self.rows.remove(row)
        row.deleteLater()
        self.update_totals()

    def update_totals(self):
        self.total_cal = self.total_prot = self.total_carbs = self.total_fat = 0
        for row in self.rows:
            qty = row.qty.value()
            macros = row.macros
            self.total_cal += round(float(macros["cal"]) * qty,2)
            self.total_prot += round(float(macros["prot"]) * qty,2)
            self.total_carbs += round(float(macros["carbs"]) * qty,2)
            self.total_fat += round(float(macros["fat"]) * qty,2)
        self.cal_counter.setText(f"{self.total_cal} kcal")
        self.prot_counter.setText(f"{self.total_prot} g")
        self.carbs_counter.setText(f"{self.total_carbs} g")
        self.fats_counter.setText(f"{self.total_fat} g")
    
    def save_to_db(self,recipe_name,name,macros):
        conn = sqlite3.connect("recipes.db")
        curr = conn.cursor()
        curr.execute("""
            INSERT INTO recipe_ingredients (recipe_name, ingredient, calories, protein, carbs, fat, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (recipe_name,
             name,
             macros["cal"], macros["prot"], macros["carbs"], macros["fat"], date.today().isoformat())
             )
        conn.commit()
        curr.close()

    def load_recipe(self, recipe_name):
        conn = sqlite3.connect("recipes.db")
        curr = conn.cursor()
        curr.execute("SELECT ingredient, calories, protein, carbs, fat FROM recipe_ingredients WHERE recipe_name=?", (recipe_name,))
        rows = curr.fetchall()
        conn.close()
        return rows 
    
    def load_today_meals(self):
        layout = self.meal_log
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
            else:
                layout.removeItem(item)
        conn = sqlite3.connect("recipes.db")
        curr = conn.cursor()
        today = date.today().isoformat()
        curr.execute("""
            SELECT DISTINCT recipe_name 
            FROM recipe_ingredients 
            WHERE date = ?
        """, (today,))
        recipes = curr.fetchall()
        conn.close()
        if not recipes:
            placeholder = QLabel("No recipes logged today")
            placeholder.setStyleSheet("font-size: 18px; padding: 6px; color: gray;")
            layout.addWidget(placeholder)
            return
        for recipe in recipes:
            name = recipe[0]
            label = QLabel(name)
            label.setStyleSheet("""
                QWidget{
            font: 400 20px "Epilogue";
            color:#1d1d1d;
            border-radius:10px;
            background-color:rgb(242, 242, 242);
            border:1px solid #c0c0c0
            }
            """)
            layout.addWidget(label)

    
    def load_profile(self):
        connection = sqlite3.connect("entries.db")
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name, age, goal_weight, weight, height FROM entries ORDER BY rowid DESC LIMIT 1")
            row = cursor.fetchone()
            connection.close()
            if row:
                name,age,goal_weight,weight,height = row
                self.name_lbl.setText(f"{name}")
                self.age_lbl.setText(f"{age}")
                self.goal_lbl.setText(f"{goal_weight}")
                self.weight_lbl.setText(f"{weight}")
                self.height_lbl.setText(f"{height}")
        else:
            print("problem w connection")

    def open_Scanner(self):
        self.window = Scanner()
        self.window.show()
        self.hide()

class IngredientAdd(QWidget):
    change = pyqtSignal()
    removed = pyqtSignal(QWidget)
    def __init__(self,name,macros,parent=None):
        super().__init__(parent)
        self.name = name 
        self.macros = macros
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,5,0,5)
        self.name_lbl = QLabel(name)
        self.qty = QSpinBox()
        self.qty.setMinimum(1)
        self.qty.setMaximum(20)
        self.qty.valueChanged.connect(self.change.emit)
        self.unit_lbl = QLabel("x 100g")
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(lambda: self.removed.emit(self))
        layout.addWidget(self.name_lbl)
        self.name_lbl.setMinimumSize(520,20)
        self.name_lbl.setMaximumHeight(40)
        layout.addStretch()
        layout.addWidget(self.qty)
        self.qty.setMaximumHeight(40)
        layout.addWidget(self.unit_lbl)
        self.unit_lbl.setMaximumHeight(40)
        layout.addWidget(self.remove_btn)

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



class Scanner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Scanner.ui",self)
        self.window = QMainWindow()
        genai.configure(api_key="AIzaSyDO0R3cCxvrM_G_qgIe7xzjft08OCGWRpo")
        self.model = genai.GenerativeModel("gemini-2.5-pro")
        self.video_label = QLabel(self.cam_frame)
        self.video_label.setGeometry(0, 0, self.cam_frame.width(), self.cam_frame.height())
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.last_request_time = 0
        self.search_btn.clicked.connect(self.freeze_and_scan)

    def freeze_and_scan(self):
        self.timer.stop()
        if self.last_frame is not None:
            self.recognize_object(self.last_frame)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.last_frame = frame.copy()
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            img_qt = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(img_qt)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.width(), self.video_label.height()))

    def recognize_object(self, frame):
        try:
            pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            import io
            img_bytes = io.BytesIO()
            pil_image.save(img_bytes, format="JPEG")
            img_bytes.seek(0)
            response = self.model.generate_content(
                [
                    "Identify the food item and list only macros (calories, protein, carbs, fats) if possible. in the format: The item is: item_name \n Calories: \n Protein: \n Carbs: \n Fats:",
                    {"mime_type": "image/jpeg", "data": img_bytes.read()},
                ]
            )
            print("Gemini:", response.text)
            cleaned = self.clean_markdown(response.text)
            self.listWidget.addItem(cleaned)

        
        except Exception as e:
            print("Gemini Error:", e)

    def clean_markdown(self, text):
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text) 
        text = re.sub(r"[*#`>-]", "", text)          
        return text.strip()

    def closeEvent(self, event):
        self.cap.release()


if __name__=="__main__":
    app = QApplication(sys.argv)
    window = StartScreen()
    sys.exit(app.exec())
