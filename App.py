from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import ( QApplication, QMainWindow, 
    QPushButton,QListWidget, QVBoxLayout, QWidget)

from TreeAlgs import UPMGA, NJ

app = QApplication([])
#NOTE: This is a very basic GUI for demonstration purposes only
#NOTE: Error handling and input methods are to be implemented
#NOTE: This is in no way a good Main window, Should be made into a submenu
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filogeny")
        self.setMinimumSize(QSize(800, 600))

        self.alg_list = QListWidget()
        self.alg_list.addItems(["UPMGA", "Neighbour Joining"])
        layout = QVBoxLayout()
        layout.addWidget(self.alg_list)

        confirm_button = QPushButton("Run Algorithm")
        confirm_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(confirm_button)


        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    def on_button_clicked(self):
        ## Placeholder for actual data
        taxa=[[0, 5, 6, 3], [5, 0 ,2, 4], [6,2,0,7], [3,4,7,0]]
        taxa_labels=["A", "B", "C", "D"]
        if self.alg_list.currentItem().text() == "UPMGA":
            tree = UPMGA(taxa,taxa_labels)
            print(tree)
        elif self.alg_list.currentItem().text() == "Neighbour Joining":
            tree = NJ(taxa,taxa_labels)
            print(tree)
window = MainWindow()
window.show()
app.exec()