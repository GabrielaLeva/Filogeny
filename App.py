from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import ( QApplication, QMainWindow, 
    QPushButton,QListWidget, QVBoxLayout, QWidget)

from random import choice
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner
from SettingsObjects import AlgorithmSettings
import Visualizer

from TreeAlgs import UPMGA, NJ

#Helpers, to be moved
def score_to_distance(score,max):
    return max-score+1
def align_dataset(settings:AlgorithmSettings):
    Aligner=PairwiseAligner()
    Aligner.mode=settings.algorithm_mode
    distance_matrix=[]
    #TO:DO Loading screen progress % by alignments done
    m=float("-inf")
    for i,seqi in enumerate(settings.dataset):
        distance_matrix.append([Aligner.score(seqi,seqj) for seqj in settings.dataset[i+1:]])
    distance_matrix.pop()
    for i in distance_matrix:
        n=max(i)
        if m<=n:
            m=n
    distance_matrix=[[score_to_distance(j,m) for j in i] for i in distance_matrix]
    return distance_matrix

app = QApplication([])
#NOTE: This is a very basic GUI for demonstration purposes only
#NOTE: Error handling and input methods are to be implemented
#NOTE: This is in no way a good Main window, Should be made into a submenu
#NOTE: Dear god it might be a UX mess for now because I'm waiting for the UI to be done and  it might not be a good idea to put on the repo, 
# but it's as close to a working prototype as I'm gonna get without further plans clarified, my job here is done, for now
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

        self.visualizer=None
        
    def on_button_clicked(self):
        s=AlgorithmSettings()
        s.algorithm_mode="global"
        num_seq=10      
        taxa_labels=[f"seq{i}" for i in range(num_seq)]
        test_seq=[Seq(''.join([choice(["A","C","T","G"]) for _ in range(1000)])) for _ in range(num_seq)]
        s.dataset=test_seq
        align=align_dataset(s)
        taxa=[[0 for _ in range(len(align)+1)]for _ in range(len(align)+1)]
        for i,seqi in enumerate(align):
            for j,seqj in enumerate(seqi):
                taxa[i][i+j+1]=seqj
                taxa[i+j+1][i]=seqj
        if self.alg_list.currentItem().text() == "UPMGA":
            tree = UPMGA(taxa,taxa_labels)
        elif self.alg_list.currentItem().text() == "Neighbour Joining":
            tree = NJ(taxa,taxa_labels)
        print(tree.to_dict())
        if self.visualizer is None:
            self.visualizer=Visualizer.Visualizer()
        self.visualizer.show()
        self.visualizer.DisplayTree(tree)
        
window = MainWindow()
window.show()
app.exec()