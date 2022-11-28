from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QPushButton, QWidget, QVBoxLayout, QListWidget
import multiprocessing
from datetime import datetime
import Parser
import Utils
from multiprocessing import Pool
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.path = ''

    def initUI(self):

        self.setWindowTitle('Parser')

        self.setAcceptDrops(True)

        self.btn_start = QPushButton("Start scraping", self)
        self.label_file = QLabel()
        self.label_start = QLabel()
        self.label_finished = QLabel()
        self.label_saved = QLabel()
        self.label_time = QLabel()
        self.btn_start.clicked.connect(self.on_click)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('\tDrag and drop the *.txt file here:'))
        main_layout.addWidget(self.label_start)
        main_layout.addWidget(self.label_file)
        main_layout.addWidget(self.label_finished)
        main_layout.addWidget(self.label_saved)
        main_layout.addWidget(self.label_time)
        main_layout.addWidget(self.btn_start)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


    def on_click(self):

        self.btn_start.setEnabled(False)

        self.label_start.setText(f'[ - ]\tScraper is starting . . .')

        start = datetime.now()
        inns = Utils.get_inns(self.getPath())
        p = Pool(processes=multiprocessing.cpu_count())
        reestr = p.map(Parser.run, inns)

        self.label_finished.setText((f'[ - ]\tScraper has finished'))

        Utils.to_csv(reestr)

        self.label_saved.setText((f'[ - ]\tData saved {os.getcwd()}/output/reestr.csv'))

        stop = datetime.now()

        self.label_time.setText((f'[ - ]\tTime spent is : {stop - start}'))

    def dragEnterEvent(self, event):

        mime = event.mimeData()

        if mime.hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        for url in event.mimeData().urls():
            file_name = url.toLocalFile()
            self.setPath(file_name)
            print(file_name)
        self.label_file.setText(f'[ - ]\tFile: {self.getPath()}')

        return super().dropEvent(event)

    def setPath(self, value):
        self.path = value

    def getPath(self):
        path = self.path
        return path

def start():

    app = QApplication([])
    mw = MainWindow()
    mw.resize(500, 350)
    mw.show()
    app.exec()


