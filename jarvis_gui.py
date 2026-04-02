# jarvis_cinematic_core.py
# Minimal Cinematic J.A.R.V.I.S Core (Video-Style)
# pip install PySide6

import sys, math, time
from PySide6.QtCore import Qt, QTimer, QRectF, QPointF
from PySide6.QtGui import (
    QPainter, QColor, QPen, QFont,
    QRadialGradient
)
from PySide6.QtWidgets import QApplication, QWidget

# ---------------- Cinematic Core ----------------
class CinematicCore(QWidget):
    def __init__(self):
        super().__init__()
        self.phase = 0.0
        self.setWindowTitle("J.A.R.V.I.S")
        self.showFullScreen()
        self.setStyleSheet("background:black;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def animate(self):
        self.phase = (self.phase + 0.0018) % 1.0
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        center = rect.center()

        base_r = min(rect.width(), rect.height()) * 0.32
        glow = 80 + 40 * math.sin(time.time() * 1.2)

        # Background glow
        bg = QRadialGradient(center, base_r * 2.2)
        bg.setColorAt(0, QColor(10, 16, 22))
        bg.setColorAt(1, QColor(0, 0, 0))
        p.fillRect(rect, bg)

        # Rings (slow, cinematic)
        rings = [
            (base_r * 1.15, 14, QColor(80, 220, 255, glow)),
            (base_r * 0.95, 8, QColor(255, 170, 90, 200)),
            (base_r * 0.75, 5, QColor(180, 120, 255, 180)),
            (base_r * 0.58, 3, QColor(120, 220, 200, 160)),
        ]

        for i, (radius, width, color) in enumerate(rings):
            start = (self.phase + i * 0.27) * 360
            pen = QPen(color, width, Qt.SolidLine, Qt.RoundCap)
            p.setPen(pen)
            arc_rect = QRectF(
                center.x() - radius,
                center.y() - radius,
                radius * 2,
                radius * 2
            )
            p.drawArc(arc_rect, int(-start * 16), int(-260 * 16))

        # Inner faint ring
        p.setPen(QPen(QColor(140, 200, 240, 120), 2))
        p.drawEllipse(center, base_r * 0.42, base_r * 0.42)

        # Core text
        p.setPen(QColor(220, 245, 255))
        p.setFont(QFont("Segoe UI", 40, QFont.Black))
        p.drawText(rect, Qt.AlignCenter, "J.A.R.V.I.S")

        # Status text (very minimal)
        p.setFont(QFont("Consolas", 12))
        p.setPen(QColor(140, 190, 220))
        p.drawText(
            rect.adjusted(0, base_r * 0.9, 0, 0),
            Qt.AlignHCenter | Qt.AlignTop,
            "AUTOMATION MODE • SYSTEM ACTIVE"
        )

        # Scanlines
        p.setPen(QPen(QColor(0, 0, 0, 35), 1))
        for y in range(0, rect.height(), 4):
            p.drawLine(0, y, rect.width(), y)

# ---------------- Run ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    w = CinematicCore()
    sys.exit(app.exec())