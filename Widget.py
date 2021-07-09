import PySide2
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import sys
import requests
import json
import urllib.parse
import urllib.request
class PfamWidget(QWidget):
    def __init__(self, prot_name, parent = None):
        super().__init__()

        # Init
        self.prot_name = prot_name

        # Constant
        self.y_scale_position = 150
        self.y_position = 80 # Valeur entre 25 et 95
        self.height_ind = self.y_position -20 # Permet une y_position des points fxes

        # Load
        self.load()

        # Object
        self.cursor = QLine(0, self.y_scale_position, 0, 80)
        
        # Data index
        self.group = ["Mutation", "Silent", "Protein"]
        self.mutation = [["mutation_1", 115],["mutation_2", 68]]
        self.proteins = [["proteins",255]]
        self.silents = [["silent", 167]]
        self.index = [self.mutation, self.silents, self.proteins]
        self.full_index = [] # liste des index non groupés
        for list_ind in self.index :
            for ind in list_ind:
                self.full_index.append(ind)

        self.list_labels = [] 
        for list_ind in self.index:
            for ind in list_ind:
                self.list_labels.append(QLabel(str(ind[0])))

        # Color Index
        # Red for mutation
        # Green for silent
        # Blue for protein
        self.colors = [Qt.red, Qt.green, Qt.blue]

        # Layout
        self.layout1 = QHBoxLayout()
        for label in self.list_labels:
            label.setHidden(True)
            self.layout1.addWidget(label)
        self.setLayout(self.layout1)

        # Param
        self.resize(600 ,200)
        self.setMouseTracking(True)
        # Event
        
        # self.machine = QStateMachine()
        # self.state1 = QState()

        # self.state1.assignProperty()
        # QVariantanimation
        # self.button = QPushButton("hi")
        # self.animation = QPropertyAnimation(self.button, bytes("geometry", encoding="utf8"))
        # self.animation.setDuration(10000)
        # self.animation.setStartValue(QRect(0,0,100,30))
        # self.animation.setEndValue(QRect(0,0,150,50))
        # self.animation.start()

        # self.vanimation = QVariantAnimation()
        # self.vanimation.setStartValue(1)
        # self.vanimation.setEndValue(1000)
        # self.vanimation.setDuration(20000)
        # self.vanimation.valueChanged.connect(self.update)
        # self.vanimation.setEasingCurve(QEasingCurve.OutElastic)

        # self.vanimation_2 = QVariantAnimation()
        # self.vanimation_2.setStartValue(0)
        # self.vanimation_2.setEndValue(90)
        # self.vanimation_2.setDuration(20000)
        # self.vanimation_2.valueChanged.connect(self.update)
        # self.vanimation_2.setEasingCurve(QEasingCurve.OutElastic)
        
        # self.anim = QParallelAnimationGroup()
        # self.anim.addAnimation(self.vanimation)
        # self.anim.addAnimation(self.vanimation_2)

        # self.anim.start()

        # Scrolbar
        self.area = QScrollArea()
        self.area.setWidget(self)
        self.area.show()

    def paintEvent(self, event : QPaintEvent) :
        
        # QPainter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # transform = QTransform()
        # transform.translate(*self.rect().center().toTuple())
        # transform.scale(self.vanimation.currentValue()/1000, self.vanimation.currentValue()/1000)
        # transform.rotate(self.vanimation_2.currentValue())
        # painter.setTransform(transform)

        # Paint Cursor
        painter.setPen(QPen(Qt.yellow))
        painter.drawLine(self.cursor)

        # Legend
        x_legend = 15
        y_legend = 180
        for i, group in enumerate(self.group):
            painter.setPen(QPen(self.colors[i]))
            painter.setBrush(QBrush(self.colors[i]))
            painter.drawEllipse(x_legend, y_legend, 10, 10)
            painter.setPen(QPen(Qt.black))
            painter.drawText(x_legend + 15, y_legend -2 , 50, 15, Qt.AlignLeft, group)
            x_legend += 75

        # Painting region
        start = 0
        end = self.data[0]["length"]
        self.resize(end + 200, 200)
        for value in self.values:
            painter.setPen(QPen(Qt.black))
            painter.setBrush(QBrush(Qt.gray))
            painter.drawRect(self.rect().adjusted(start,self.y_position,value[0]-self.width(),-self.y_position))
            start = value[1]
            painter.setBrush(QBrush(QColor(value[2])))
            self.domaine = self.rect().adjusted(value[0],self.y_position, value[1]-self.width(),-self.y_position)
            painter.drawRect(self.domaine)
            painter.setPen(QPen(Qt.black))
            font = QFont()
            font.setPixelSize(10)
            painter.setFont(font)
            painter.drawText(self.domaine, Qt.AlignCenter, value[3])    
        painter.setBrush(QBrush(Qt.gray))
        painter.drawRect(self.rect().adjusted(start,self.y_position,end-self.width(),-self.y_position))            

        # Scale painted
        y_scale_height = 15
        painter.setPen(QPen(Qt.gray))
        line = QLine(0,self.y_scale_position,end,self.y_scale_position)
        painter.drawLine(line)
        index = 0
        while index < end - 20 :
            index += 20
            painter.drawLine(QLine(index,self.y_scale_position,index,self.y_scale_position-y_scale_height))
            if index%100 == 0:
                painter.drawText(index-10,self.y_scale_position+10, 30, 10, Qt.AlignLeft, str(index))

        # Add index
        for i, list_ind in enumerate(self.index) :
            for ind in list_ind:
                self.paintIndex(ind[0], ind[1], self.colors[i])
    
    # Fonctions
    def paintIndex (self, name, position, color):
        painter = QPainter(self)
        painter.setPen(QPen(color))
        painter.setBrush(QBrush(color))
        painter.drawLine(QLine(position,self.y_position,position, self.y_position-self.height_ind))
        painter.drawEllipse(position-2,self.y_position-self.height_ind,5,5)
        painter.setPen(QPen("dark"))
        
    
    def addIndex(self,name,position,color_given):
        groupe = None
        for i, color in enumerate(self.colors):
            if color == color_given:
                groupe = i
        if groupe == None:
            print("No color associated")
            return None
        self.index[groupe].append([name,position])
        self.full_index.append([name,position])
        label = QLabel(name)
        label.setHidden(True)
        self.list_labels.append(label)
        print(self.list_labels)
        self.layout1.addWidget(label)
        self.update()

    def mouseMoveEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
        self.cursor.setLine(event.x(),self.y_scale_position, event.x(), 80)
        self.update()

    def distance(self, x1, y1, x2, y2):
        return((x1-x2)**2 + (y1-y2)**2)

    def mousePressEvent(self, event: PySide2.QtGui.QMouseEvent) -> None:
        for i, ind in enumerate(self.full_index):
            if self.distance(event.x(), event.y(), ind[1], 20) < 10 :
                self.layout1.setContentsMargins(QMargins(ind[1]-15,0,0,180))
                print(self.list_labels[i])
                self.list_labels[i].setHidden(False)
                print(ind[0])
            else : 
                self.list_labels[i].setHidden(True)
            

    def get_pfam_from_id(self, id_prot):
        r = requests.get(f"https://pfam.xfam.org/protein/" + id_prot + "/graphic")
        if r.status_code == 200 :
           return r.json()
        else :
            print("Echec request")
            return None

    def get_pfam_from_name(self, name_prot):
        r = requests.get(f"https://pfam.xfam.org/protein/" + name_prot  + "/graphic")
        if r.status_code == 200 :
           return r.json()
        else :
            print("Echec request")
            return None
    
    def load(self):
        # self.data = self.get_pfam_from_name(self.prot_name)
        self.data = json.load(open("graphic.json"))
        self.values =[]
        for i in self.data[0]["regions"]:
            self.values.append([i["start"],i["end"],i["colour"], i["text"]])
        print("end_loading")
    
    def Mapping_gene2prot (self, froml, to, query, format = "tab"):
        url = 'https://www.uniprot.org/uploadlists/'
        # DOC :https://www.uniprot.org/help/api_idmapping

        params = {
        "from": froml,
        "to": to,
        "format": format,
        "query": query}

        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()
        print(response.decode('utf-8'))
        return None
    
        
if __name__ == '__main__' :


    app = QApplication(sys.argv)
    widget = PfamWidget("EGFR_HUMAN")
    # widget.setWindowTitle("hello")
    widget.addIndex("added", 300, widget.colors[1])
    # widget.Mapping_gene2prot('ACC+ID', 'ENSEMBL_ID', 'P40925 P40926 O43175 Q9UM73 P97793', 'tab')
    app.exec_()