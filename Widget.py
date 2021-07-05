import PySide2
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import json

class MyWidget(QWidget):
    def __init__(self,parent = None):
        super().__init__()

        # Data extract from JSON file
        data = json.load(open("graphic.json"))

        # Data index
        self.mutation = [["mutation", 115]]
        self.proteins = [["proteins",255]]

        # Color
        # Red for mutation
        # Grey for scaling
        # Green for silent
        # Blue for protein
        self.colors = [Qt.red, Qt.gray, Qt.green, Qt.blue]

        #Length = x, Height = y
        self.x = data[0]["length"]
        self.y = 200
        self.resize(self.x ,self.y)
        self.values =[]
        # print(data)

        # Extract usefull data
        for i in data[0]["regions"]:
            self.values.append([i["start"],i["end"],i["colour"], i["text"]])

        # print(self.values)

        # Layout
        # layout = QVBoxLayout()
        # self.setLayout(layout)

    def paintEvent(self, event : QPaintEvent) :

        # QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        painter.setBrush(QBrush(Qt.gray))
        painter.drawRect(self.rect().adjusted(0,80,0,-80))

        # Painting region
        for value in self.values:
            painter.setBrush(QBrush(QColor(value[2])))
            self.domaine = self.rect().adjusted(value[0],80, value[1]-self.x,-80)
            painter.drawRect(self.domaine)
            painter.setPen(QPen(Qt.black))
            font = QFont()
            font.setPixelSize(10)
            painter.setFont(font)
            painter.drawText(self.domaine, Qt.AlignCenter, value[3])

        # Scale
        y_scale_position = 150
        y_scale_height = 15
        painter.setPen(QPen(self.colors[1]))
        line = QLine(0,y_scale_position,self.x,y_scale_position)
        painter.drawLine(line)
        index = 0
        while index < self.x :
            index += 20
            painter.drawLine(QLine(index,y_scale_position,index,y_scale_position-y_scale_height))
            if index%100 == 0:
                painter.drawText(index-10,y_scale_position+10, 15, 10, Qt.AlignLeft, str(index))

        
        # Mutation
        for mutation in self.mutation :
            self.addIndex(mutation[0], mutation[1], painter, self.colors[0])

        # Protein
        for protein in self.proteins :
            self.addIndex(protein[0], protein[1], painter, self.colors[3])


    def addIndex (self, name, position, painter, color):
        painter.setPen(QPen(color))
        painter.drawLine(QLine(position,80,position, 20))
        painter.drawEllipse(position-2,20,5,5)
        painter.drawText(position-10, 0, 40, 10, Qt.AlignLeft, name)



        
if __name__ == '__main__' :


    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setWindowTitle("PO4637")
    
    widget.show()

    app.exec_() 