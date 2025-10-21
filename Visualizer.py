from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import ( QApplication, QMainWindow, 
    QPushButton, QVBoxLayout, QWidget)
#Qt Graphics Framework
from PySide6.QtWidgets import (QGraphicsScene, QGraphicsView, 
    QGraphicsRectItem, QGraphicsEllipseItem)
from PySide6.QtGui import QBrush, QPen, QPainter
#NOTE: This will eventually become an independent window for the visualisation of trees
# Temp input for the visualizer, 
from TreeAlgs import UPMGA

app = QApplication([])

tree={'AC': {'A': 1.0, 'C': 1.0, 'to_end': 1.0}, 'ACD': {'AC': 1.0, 'D': 2.0, 'to_end': 2.0}, 'ACDB': {'ACD': 1.0, 'B': 3.0, 'to_end': 3.0}}
leafcount=4

#this is inneficient
#TODO: find a way to store the result or moddify the algorithms to have the 
def get_leaf_count(tree,node):
    if node in tree.keys():
        return sum([get_leaf_count(tree,x) for x in tree[node] if x!="to_end"])
    else:
        return 1

mult=100
root = sorted(list(tree.keys()),key=len)[-1]
height=(leafcount-1)*mult
width=tree[root]["to_end"]*mult
#Potentially parameters
paddingx=0.1*width
paddingy=0.1*height

height+=0.2*height
width+=0.2*width

pen=QPen(Qt.black)
scene = QGraphicsScene(0,0,width,height)
scene.setBackgroundBrush(QBrush(Qt.white))

## Function for traversing the tree
def drawTree(x1,y1, distance, node, starting_leaf, leaves):
    x2=x1+distance
    scene.addLine(x1,y1,x2,y1)
    if(node in tree.keys()):
        children=list(tree[node].keys())
        children.remove("to_end")
        leafcount0=get_leaf_count(tree,children[0])

        y20=(starting_leaf+(leafcount0-1)/2)*mult+paddingy
        scene.addLine(x2,y1,x2,y20)
        d=tree[node][children[0]]
        label0=scene.addText(str(d))
        label0.setPos(x2+d*mult/2,y20)
        label0.setDefaultTextColor(Qt.black)
        drawTree(x2,y20,d*mult,children[0],starting_leaf,leafcount0)

        y21=(leafcount0+(leaves-leafcount0-1)/2)*mult+paddingy
        d=tree[node][children[1]]
        label0=scene.addText(str(d))
        label0.setPos(x2+d*mult/2,y21)
        label0.setDefaultTextColor(Qt.black)
        scene.addLine(x2,y1,x2,y21)
        drawTree(x2,y21,tree[node][children[1]]*mult,children[1],starting_leaf+leafcount0,leaves-leafcount0)
    else:
        label0=scene.addText(node)
        label0.setPos(x2,y1)
        label0.setDefaultTextColor(Qt.black)


drawTree(0,height/2,paddingx,root,0,leafcount)

view=QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing)
view.show()
app.exec()