from email.mime import image
import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QPainter, QBrush, QColor, QImage, QAction, QTransform
from PyQt6.QtCore import Qt, QPoint, QEventLoop
from PyQt6.QtWidgets import QMainWindow
from PIL import Image
import logging
class AreaSelector(QMainWindow):
    def __init__(self, points=[], image : Image=None):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        # geometry a4 size and window 
        if image is not None:
            logging.debug("image present")
            self.raw_image = image
            # pil image get dimensions
            width, height = image.size
            logging.debug(f"image size: {width}x{height}")

            # convert to qt image
            self.image = QImage(image.tobytes(), width, height, QImage.Format.Format_RGB888)
            # rotate image
            self.image = self.image.transformed(QTransform().rotate(90))
        else:
            self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
            
            self.image.fill(Qt.GlobalColor.white)
            self.raw_image = None

        # making image color to white
        
        self.br = QBrush(QColor(100, 10, 10, 40))  

        self.drawing = False

        # 
        
        self.current_index = 0
        self.points : list = points

        self.initUI()


    def initUI(self):
        self.toolbar = QtWidgets.QToolBar()
        self.addToolBar(self.toolbar)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)

        self.bottomBar = QtWidgets.QToolBar()
        # border
        self.bottomBar.setStyleSheet("QToolBar { border: 1px solid gray; border-radius: 3px;}")


        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.bottomBar)

        self.a_clear = self.toolbar.addAction("Clear")
        self.a_clear.triggered.connect(self.clear_image)

        self.a_output = self.toolbar.addAction("Output")
        self.a_output.triggered.connect(self.output)

        self.a_label = QtWidgets.QLabel("Press Done to finish\t\t\t\t")
        self.bottomBar.addWidget(self.a_label)
        self.a_done = self.bottomBar.addAction("Done")
        self.a_done.triggered.connect(self.close)

        


        self.show()


    def rotate_image_clockwise(self):
        self.image = self.image.transformed(QTransform().rotate(90))
        self.setGeometry(self.x(), self.y(), self.raw_image.size[1], self.raw_image.size[0])

    def clear_image(self):
        if self.raw_image is None:
            self.image.fill(Qt.GlobalColor.white)
        else:
            # reload from pil image
            self.image = QImage(self.raw_image.tobytes(), self.raw_image.size[0], self.raw_image.size[1], QImage.Format.Format_RGB888)
        self.points.clear()
        self.current_index = 0
        self.update()

    def output(self):
        # create dialog window
        dlg = QtWidgets.QDialog()
        dlg.setWindowTitle("Output")
        dlg.setFixedSize(400, 400)
        message = QtWidgets.QLabel(dlg)
        
        if len(self.points) == 0:
            text = "No points"
        else:
            text = ""
            for i, x in enumerate(self.points):
                x : QPoint
                text += f"{i}: ({x[0].x()}, {x[0].y()}) - ({x[1].x()}, {x[1].y()})\n"

        message.setText(text)
        dlg.exec()



    # ANCHOR points handle

    def get_begin(self):
        return self.points[self.current_index][0]
    
    def get_end(self):
        return self.points[self.current_index][1]

    def init_points(self):
        if len(self.points) < self.current_index or self.points == []:
            self.points.append([QPoint(0, 0), QPoint(0, 0)])
            self.current_index = 0
            return

        if self.points[self.current_index][0] != self.points[self.current_index][1]:
            self.current_index += 1
            self.points.append([QPoint(), QPoint()])
        
    
    def update_points(self, begin = None, end = None):
        if begin != None:
            self.points[self.current_index][0] = begin
        if end != None:
            self.points[self.current_index][1] = end

    def get_points(self):
        return self.points[self.current_index]

    def has_points(self, index=None):
        if index == None:
            index = self.current_index
        try:
            ret = self.points[index]
            return True
        except IndexError:
            return False
    #
    def constant_update(self):
        self.statusBar.showMessage(f"{self.current_index}")


    def mousePressEvent(self, event : QtWidgets.QGraphicsSceneMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.init_points()
            self.update_points(begin=event.pos(), end=event.pos())

        self.constant_update()
        
        
    def mouseMoveEvent(self, event : QtWidgets.QGraphicsSceneMouseEvent):
        if (event.buttons() & Qt.MouseButton.LeftButton) and self.drawing:
            self.update_points(end=event.pos())
            self.update()

    def mouseReleaseEvent(self, event : QtWidgets.QGraphicsSceneMouseEvent):
        if (event.button() == Qt.MouseButton.LeftButton
            and self.get_begin() != self.get_end()
        ):
            painter = QPainter(self.image)
            painter.setBrush(self.br)
            painter.drawRect(QtCore.QRect(*self.get_points()))
            self.update()
            painter.end()
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        
        # draw rectangle  on the canvas
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

        if self.has_points():
            canvasPainter.drawRect(QtCore.QRect(*self.get_points()))
        self.constant_update()

def create_area_selector(image_path : str = None):
    img = None
    if image_path is not None:  
        img = Image.open(image_path)

    points = []
    loop = QEventLoop()
    window = AreaSelector(points=points, image=img)
    window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    window.destroyed.connect(loop.quit)
    window.show()
    loop.exec()

    return points


if __name__ == '__main__':
    import logging,sys
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    app = QtWidgets.QApplication(sys.argv)
    create_area_selector("./test.jpg")