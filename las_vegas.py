from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPalette, QImage

app = QApplication([])

widget = QWidget()
palette = widget.palette()
background_image = QPixmap("lasvegas.png")  # Замените "path_to_your_image.jpg" на путь к вашему изображению
palette.setBrush(widget.backgroundRole(), background_image)
widget.setPalette(palette)

widget.show()

app.exec_()