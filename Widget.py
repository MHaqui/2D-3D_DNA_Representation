import sys
import requests
import json
import urllib.parse
import urllib.request
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class PfamWidget(QWidget):
    """Widget display PFAM"""

    def __init__(self, prot_name: str, parent=None):
        super().__init__()

        # Init

        # Constant
        self.y_scale_position = 150
        self.y_position = 80  # Value betwenn 25 and 90
        self.height_ind = 60

        # Load
        self.load(prot_name)

        # Object
        self.cursor = QLine(0, self.y_scale_position, 0, 80)

        # Data index
        self.variants = [
            {"name": "G32X", "position": 150, "height": 60, "color": "red"},
            {"name": "G32X", "position": 50, "height": 60, "color": "green"},
            {"name": "G32X", "position": 250, "height": 60, "color": "blue"},
        ]
        self.groups = [
            {
                "name": "Mutation",
                "color": "red",
            }
        ]
        # self.index = []  # list grouped index
        # self.full_index = []  # list ungrouped index
        # self.colors = []
        # self.list_labels = []

        # Layout
        # self.layout1 = QHBoxLayout()
        # self.setLayout(self.layout1)

        # Add object

        # Parameter
        self.resize(600, 250)
        self.setMouseTracking(True)

        # Scrolbar

    def paintEvent(self, event: QPaintEvent):
        """Override"""
        # QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Paint Cursor
        font_metrics = QFontMetrics(painter.font())
        # Legend
        x_legend = self.rect().left()
        y_legend = self.rect().bottom()
        for group in self.groups:
            painter.setPen(QPen(QColor(group["color"])))
            painter.setBrush(QBrush(QColor(group["color"])))
            painter.drawEllipse(x_legend, y_legend - 10, 10, 10)
            painter.setPen(QPen(Qt.black))
            painter.drawText(x_legend + 15, y_legend, group["name"])
            x_legend += 85

        # Painting region
        start = 0
        end = self.data[0]["length"]
        for value in self.values:
            painter.setPen(QPen(Qt.black))
            painter.setBrush(QBrush(Qt.gray))
            painter.drawRect(
                self.rect().adjusted(
                    self.protein_to_pixel(start),
                    self.y_position,
                    self.protein_to_pixel(value[0]) - self.width(),
                    -self.y_position,
                )
            )
            start = value[1]
            painter.setBrush(QBrush(QColor(value[2])))
            self.domaine = self.rect().adjusted(
                self.protein_to_pixel(value[0]),
                self.y_position,
                self.protein_to_pixel(value[1]) - self.width(),
                -self.y_position,
            )
            painter.drawRect(self.domaine)
            painter.setPen(QPen(Qt.black))
            font = QFont()
            font.setPixelSize(10)
            painter.setFont(font)
            painter.drawText(
                self.domaine, Qt.AlignCenter, self.protein_to_pixel(value[3])
            )
        painter.setBrush(QBrush(Qt.gray))
        painter.drawRect(
            self.rect().adjusted(
                self.protein_to_pixel(start),
                self.y_position,
                self.protein_to_pixel(end) - self.width(),
                -self.y_position,
            )
        )

        # Scale painted
        y_scale_height = 15
        painter.setPen(QPen(Qt.gray))
        line = QLine(0, self.y_scale_position, end, self.y_scale_position)
        painter.drawLine(line)
        index = 0
        while index < end - 20:
            index += 20
            painter.drawLine(
                QLine(
                    index,
                    self.y_scale_position,
                    index,
                    self.y_scale_position - y_scale_height + 5,
                )
            )
            if index % 100 == 0:
                painter.drawLine(
                    QLine(
                        index,
                        self.y_scale_position,
                        index,
                        self.y_scale_position - y_scale_height,
                    )
                )
                painter.drawText(
                    index - 10,
                    self.y_scale_position + 10,
                    30,
                    10,
                    Qt.AlignLeft,
                    str(index),
                )

        # Add index
        for variant in self.variants:

            self.paint_index(
                variant["position"],
                variant["height"],
                variant["color"],
            )

    # Fonctions
    def add_group(self, name: str, color: str):
        """add a new group legend

        Args:
            name (str): group name
            color (str): group color
        """
        self.groups.append(
            {
                "name": name,
                "color": color,
            }
        )
        self.update()

    def add_index(self, name, position, color_given, height=60):
        groupe = None
        self.variants.append(
            {"name": name, "position": position, "height": height, "color": color_given}
        )

    def paint_index(self, position, height, color):
        # paint an index
        painter = QPainter(self)
        painter.setPen(QPen(color))
        painter.setBrush(QBrush(color))
        painter.drawLine(
            QLine(position, self.y_position, position, self.y_position - height)
        )
        painter.drawEllipse(position - 2, self.y_position - height, 5, 5)
        painter.setPen(QPen("dark"))

    def distance(self, x1, y1, x2, y2):
        # square distances between 2 points (x1,y1), (x2,y2)
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    # def mouseMoveEvent(self, event: QMouseEvent) -> None:
    #     # move the cursor
    #     self.cursor.setLine(event.x(), self.y_scale_position, event.x(), 80)
    #     self.update()
    def protein_to_pixel(self, value):
        return value * 0.5

    def pixel_to_protein(self, value):
        return value * 2

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # paint index name in the template
        for i, ind in enumerate(self.full_index):
            if (
                self.distance(event.x(), event.y(), ind[1], self.y_position - ind[2])
                < 10
            ):
                self.layout1.setContentsMargins(
                    QMargins(ind[1] - 15, 0, 0, 120 + ind[2])
                )
                print(self.list_labels[i])
                self.list_labels[i].setHidden(False)
                print(ind[0])
            else:
                self.list_labels[i].setHidden(True)

    def get_pfam(self, name_prot):
        # get json file thanks protein name or protein id
        r = requests.get(f"https://pfam.xfam.org/protein/" + name_prot + "/graphic")
        if r.status_code == 200:
            return r.json()
        else:
            print("Echec request")
            return None

    def load(self, prot_name):
        # load json data
        """load PFAM from protein or ID"""
        self.data = self.get_pfam(prot_name)
        # self.data = json.load(open("graphic.json"))
        self.values = []
        for i in self.data[0]["regions"]:
            self.values.append([i["start"], i["end"], i["colour"], i["text"]])
        print("end_loading")

    def gene_to_protein(self, fromf, to, query, format="tab"):
        # Permet l'extraction des noms des protéines
        # DOC :https://www.uniprot.org/help/api_idmapping
        url = "https://www.uniprot.org/uploadlists/"

        params = {"from": fromf, "to": to, "format": format, "query": query}

        data = urllib.parse.urlencode(params)
        data = data.encode("utf-8")
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()
        print(response.decode("utf-8"))
        return None


if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = PfamWidget("EGFR_HUMAN")
    # Test Fonction
    widget.add_group("New Group", "blue")
    widget.add_index("added", 350, "red", 40)
    widget.show()
    app.exec_()
