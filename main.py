import sys
import os
from PySide6.QtWidgets import (QApplication,QSlider,QLabel,QFileDialog,QTextEdit,QComboBox,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QStackedWidget)
from PySide6.QtCore import Qt,QUrl,QTimer
from PySide6.QtGui import QMovie,QPixmap
from TreeAlgs import NJ,UPMGA
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner
from random import choice
from SettingsObjects import AlgorithmSettings
from Visualizer import Visualizer
from Bio import SeqIO
import pygame

from MainWIndow import *


if __name__ == "__main__":
    app=QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())