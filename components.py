from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class StatCard(QFrame):
    def __init__(self, title, value, color):
        super().__init__()
        self.setProperty("class", "stat-card")
        self.setMinimumHeight(100)
        lay = QVBoxLayout(self)
        
        t_lbl = QLabel(title)
        t_lbl.setProperty("class", "stat-title")
        
        v_lbl = QLabel(str(value))
        v_lbl.setProperty("class", "stat-value")
        # Dynamic color still needs inline or specific handling, 
        # but we moved font size/weight to QSS .stat-value
        v_lbl.setStyleSheet(f"color: {color};") 
        
        lay.addWidget(t_lbl)
        lay.addWidget(v_lbl)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
