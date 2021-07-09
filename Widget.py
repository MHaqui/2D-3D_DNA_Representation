import PySide2
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import requests
class MyWidget(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        
        # Requête http
        # data = self.get_pfam_id("P04637")
        data = self.get_pfam_name("EGFR", "HUMAN") # en majuscule

        # Data index
        self.mutation = [["mutation_1", 115],["mutation_2", 68]]
        self.proteins = [["proteins",255]]
        self.silents = [["silent", 167]]
        self.index = [self.mutation, self.silents, self.proteins]        

        # Color
        # Red for mutation
        # Green for silent
        # Blue for protein
        # Grey for scaling
        self.colors = [Qt.red, Qt.green, Qt.blue, Qt.gray]

        #Length = x, Height = y
        self.x = data[0]["length"]
        self.y = 200
        self.resize(self.x ,self.y)
        # if self.x <500:
        #     self.resize(self.x ,self.y)
        # else : 
        #     self.resize(500, self.y)
        
        self.y_position = 80 # Valeur entre 25 et 95
        self.height_ind = self.y_position -20 # Permet une y_position des points fxes

        # Extract usefull data
        self.values =[]
        for i in data[0]["regions"]:
            self.values.append([i["start"],i["end"],i["colour"], i["text"]])
        
        # self.list_labels = []

        # Event
        
        # self.machine = QStateMachine()
        # self.state1 = QState()

        # self.state1.assignProperty()
        # self.button = QPushButton("hi")
        # self.animation = QPropertyAnimation(self.button, bytes("geometry", encoding="utf8"))
        # self.animation.setDuration(10000)
        # self.animation.setStartValue(QRect(0,0,100,30))
        # self.animation.setEndValue(QRect(0,0,150,50))
        # self.animation.start()

        scrollbar = QScrollBar(Qt.Orientation.Horizontal)
        scrollbar.setContentsMargins(0,0,0,0)
         # Layout
        self.layout = QGridLayout()
        # self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        # self.layout.addWidget(scrollbar)
        # self.layout.menuBar

    def paintEvent(self, event : QPaintEvent) :

        # QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        # painter.setBrush(QBrush(Qt.gray))
        # painter.drawRect(self.rect().adjusted(0,self.y_position,0,-self.y_position))

        # Painting region
        start = 0
        for value in self.values: 
            
            painter.setBrush(QBrush(Qt.gray))
            painter.drawRect(self.rect().adjusted(start,self.y_position,value[0]-self.x,-self.y_position))
            start = value[1]
            painter.setBrush(QBrush(QColor(value[2])))
            self.domaine = self.rect().adjusted(value[0],self.y_position, value[1]-self.x,-self.y_position)
            painter.drawRect(self.domaine)
            painter.setPen(QPen(Qt.black))
            font = QFont()
            font.setPixelSize(10)
            painter.setFont(font)
            painter.drawText(self.domaine, Qt.AlignCenter, value[3])

        painter.setBrush(QBrush(Qt.gray))
        painter.drawRect(self.rect().adjusted(start,self.y_position,0,-self.y_position))            

        # Scale painted
        y_scale_position = 150
        y_scale_height = 15
        painter.setPen(QPen(self.colors[3]))
        line = QLine(0,y_scale_position,self.x,y_scale_position)
        painter.drawLine(line)
        index = 0
        while index < self.x :
            index += 20
            painter.drawLine(QLine(index,y_scale_position,index,y_scale_position-y_scale_height))
            if index%100 == 0:
                painter.drawText(index-10,y_scale_position+10, 30, 10, Qt.AlignLeft, str(index))

        # Add index
        for i, list_ind in enumerate(self.index) :
            for ind in list_ind:
                self.addIndex(ind[0], ind[1], painter, self.colors[i])

    def addIndex (self, name, position, painter, color):
        painter.setPen(QPen(color))
        painter.drawLine(QLine(position,self.y_position,position, self.y_position-self.height_ind))
        painter.drawEllipse(position-2,self.y_position-self.height_ind,5,5)
        painter.setPen(QPen("dark"))
        painter.drawText(position-10, 0, 50, 10, Qt.AlignLeft, name)

    # def view(self): 
    #     print(self.values)

    # def mouseMoveEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
    #     for list_ind in self.index  :
    #         for ind in list_ind:
    #             if abs((event.x()-ind[1])+(event.y()-20)) < 1 :
    #                 print(ind[0])
    #     return super().mouseMoveEvent(event)  


    # Atention conversion
    def mousePressEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
        for list_ind in self.index  :
            for ind in list_ind:
                if (event.x()-ind[1])**2+(event.y()-20)**2 < 8 :
                    print(ind[0])

    def get_pfam_id(self, id_prot):
        r = requests.get(f"https://pfam.xfam.org/protein/" + id_prot + "/graphic")
        if r.status_code == 200 :
           return r.json()
        else :
            print("Echec request")
            return None

    def get_pfam_name(self, name_prot, species_prot):
        r = requests.get(f"https://pfam.xfam.org/protein/" + name_prot + "_" + species_prot + "/graphic")
        if r.status_code == 200 :
           return r.json()
        else :
            print("Echec request")
            return None
#         #!/usr/bin/env python2
# # -*- coding: utf-8 -*-
#         xml = """<?xml version='1.0' encoding='utf-8'?>
#         <a>б</a>"""
#         headers = {'Content-Type': 'application/xml'} # set what your server accepts
#         print requests.post('http://httpbin.org/post', data=xml, headers=headers).text
#         return None


        
if __name__ == '__main__' :


    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.setWindowTitle("P04637")
    
    widget.show()

    app.exec_() 