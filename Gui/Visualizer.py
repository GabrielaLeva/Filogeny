from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QVBoxLayout, QWidget)
#Qt Graphics Framework
from PySide6.QtWidgets import (QGraphicsScene, QGraphicsView, 
    QGraphicsRectItem, QGraphicsEllipseItem)
from PySide6.QtGui import QBrush, QPen, QPainter
from Lib.TreeObject import PhyloTree,Node
#NOTE: This will eventually become an independent window for the visualisation of trees
# Temp input for the visualizer, 
class Visualizer(QWidget):
    def __init__(self):
        super().__init__()
    def DisplayTree(self,tree:PhyloTree):
        
        layout = QVBoxLayout()
        
        mult=100
        root=tree.root
        leafcount=root.leaves
        height=(leafcount-1)*mult
        width=(root.height)*mult
        #Potentially parameters
        paddingx=0.1*width
        paddingy=0.1*height

        height+=0.2*height
        width+=0.2*width

        pen=QPen(Qt.black)
        scene = QGraphicsScene(0,0,width,height)
        scene.setBackgroundBrush(QBrush(Qt.white))

        ## Function for traversing the tree
        def drawTree(x1,y1, distance, node:Node, starting_leaf):
            x2=x1+distance
            scene.addLine(x1,y1,x2,y1)
            if(node.height>0):
                for child,d in node.children:
                    leafcount2=child.leaves 
                    y2=(starting_leaf+(leafcount2-1)/2)*mult+paddingy
                    scene.addLine(x2,y1,x2,y2)
                    label0=scene.addText(str(d))
                    centering=label0.boundingRect().right()/2
                    label0.setPos(x2+d*mult/2-centering,y2)
                    label0.setDefaultTextColor(Qt.black)
                    drawTree(x2,y2,d*mult,child,starting_leaf)
                    starting_leaf+=leafcount2
            else:
                label0=scene.addText(node.name)
                r=label0.boundingRect().bottomRight()
                label0.setPos(x2-r.x(),y1-r.y())
                label0.setDefaultTextColor(Qt.black)


        drawTree(0,height/2,paddingx,root,0)

        view=QGraphicsView(scene)
        view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(view)
        self.setLayout(layout)