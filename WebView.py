from posixpath import abspath
import sys
import PySide2
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWebEngineWidgets import *
import os


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = QWebEngineView()
    view.settings().setAttribute(
        QWebEngineSettings().LocalContentCanAccessRemoteUrls, True
    )
    view.settings().setAttribute(QWebEngineSettings().FullScreenSupportEnabled, True)
    view.load(
        QUrl().fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0] + r"/test.html"
        )
    )
    view.show()
    app.exec_()
