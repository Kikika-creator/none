import os
import sys

import requests
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton

SCREEN_SIZE = [1000, 700]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def getImage(self):
        api = "http://static-maps.yandex.ru/1.x/"

        params = {
            "ll": f"{self.first_coord.text()},{self.second_coord.text()}",
            "spn": f"{self.first_scale.text()},{self.second_scale.text()}",
            "l": "map"
        }

        response = requests.get(api, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)


        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Помогите, нас держат в заложниках')

        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 400)

        self.x = QLabel("x:", self)
        self.x.move(75, 427)

        self.y = QLabel("y:", self)
        self.y.move(75, 477)

        self.scale_x = QLabel("sclx:", self)
        self.scale_x.move(305, 427)

        self.scale_y = QLabel("scly:", self)
        self.scale_y.move(305, 477)

        self.first_coord = QLineEdit(self)
        self.first_coord.move(100, 425)

        self.second_coord = QLineEdit(self)
        self.second_coord.move(100, 475)

        self.first_scale = QLineEdit(self)
        self.first_scale.move(350, 425)

        self.second_scale = QLineEdit(self)
        self.second_scale.move(350, 475)

        self.show_map = QPushButton("Показать", self)
        self.show_map.move(150, 550)
        self.show_map.clicked.connect(self.getImage)


    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())