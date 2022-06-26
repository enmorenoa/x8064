from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon, QColor, QTextFormat, QPainter
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class LineNumberArea(QWidget):
    def __init__(self, interface):
        QWidget.__init__(self, parent=interface.text_code)
        self.interface = interface

    def sizeHint(self):
        return QSize(self.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.lineNumberAreaPaintEvent(event)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.interface.text_code.lineNumberArea)
        q = QColor()
        q.setRgb(46, 52, 54)
        painter.fillRect(event.rect(), q)

        block = self.interface.text_code.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.interface.text_code.blockBoundingGeometry(block).translated(self.interface.text_code.contentOffset()).top()
        bottom = top + self.interface.text_code.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                q2 = QColor()
                q2.setRgb(67, 81, 255)
                painter.setPen(q2)
                painter.drawText(0, int(top), self.interface.text_code.lineNumberArea.width(), 
                    self.interface.text_code.fontMetrics().height(),
                    Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.interface.text_code.blockBoundingRect(block).height()
            blockNumber += 1
            

    def lineNumberAreaWidth(self):
        digits = len(str(self.interface.text_code.blockCount()))
        space = 3 + self.interface.text_code.fontMetrics().width('9')*digits
        return space
    
    def resizeEvent(self, event):
        cr = self.contentsRect()
        self.interface.text_code.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 50 , cr.height()))

    @pyqtSlot(int)
    def updateLineNumberAreaWidth(self):
        self.interface.text_code.setViewportMargins(50, 0, 0, 0)

    @pyqtSlot(QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.interface.text_code.lineNumberArea.scroll(0, dy)
        else:
            self.interface.text_code.lineNumberArea.update(0, rect.y(), self.interface.text_code.lineNumberArea.width(), rect.height())

class LineNumberAreaExec(QWidget):
    def __init__(self, interface):
        QWidget.__init__(self, parent=interface.text_ejec_code)
        self.interface = interface

    def sizeHint(self):
        return QSize(self.lineNumberAreaWidthExec(), 0)

    def paintEvent(self, event):
        self.lineNumberAreaPaintEventExec(event)
    
    def lineNumberAreaPaintEventExec(self, event):
        painter = QPainter(self.interface.text_ejec_code.lineNumberArea)
        q = QColor()
        q.setRgb(46, 52, 54)
        painter.fillRect(event.rect(), q)

        block = self.interface.text_ejec_code.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.interface.text_ejec_code.blockBoundingGeometry(block).translated(self.interface.text_ejec_code.contentOffset()).top()
        bottom = top + self.interface.text_ejec_code.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                q2 = QColor()
                q2.setRgb(67, 81, 255)
                painter.setPen(q2)
                painter.drawText(0, int(top), self.interface.text_ejec_code.lineNumberArea.width(), 
                    self.interface.text_ejec_code.fontMetrics().height(),
                    Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.interface.text_ejec_code.blockBoundingRect(block).height()
            blockNumber += 1
    
    def lineNumberAreaWidthExec(self):
        digits = len(str(self.interface.text_ejec_code.blockCount()))
        space = 3 + self.interface.text_ejec_code.fontMetrics().width('9')*digits
        return space

    def resizeEvent(self, event):
        cr = self.contentsRect()
        self.interface.text_ejec_code.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 50 , cr.height()))

    @pyqtSlot(int)
    def updateLineNumberAreaWidthExec(self):
        self.interface.text_ejec_code.setViewportMargins(50, 0, 0, 0)

    @pyqtSlot(QRect, int)
    def updateLineNumberAreaExec(self, rect, dy):
        if dy:
            self.interface.text_ejec_code.lineNumberArea.scroll(0, dy)
        else:
            self.interface.text_ejec_code.lineNumberArea.update(0, rect.y(), self.interface.text_ejec_code.lineNumberArea.width(), rect.height())

class LineNumberAreaExec_2(QWidget):
    def __init__(self, interface):
        QWidget.__init__(self, parent=interface.text_ejec_code_2)
        self.interface = interface

    def sizeHint(self):
        return QSize(self.lineNumberAreaWidthExec(), 0)

    def paintEvent(self, event):
        self.lineNumberAreaPaintEventExec(event)
    
    def lineNumberAreaPaintEventExec(self, event):
        painter = QPainter(self.interface.text_ejec_code_2.lineNumberArea)
        q = QColor()
        q.setRgb(46, 52, 54)
        painter.fillRect(event.rect(), q)

        block = self.interface.text_ejec_code_2.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.interface.text_ejec_code_2.blockBoundingGeometry(block).translated(self.interface.text_ejec_code_2.contentOffset()).top()
        bottom = top + self.interface.text_ejec_code_2.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                q2 = QColor()
                q2.setRgb(67, 81, 255)
                painter.setPen(q2)
                painter.drawText(0, int(top), self.interface.text_ejec_code_2.lineNumberArea.width(), 
                    self.interface.text_ejec_code_2.fontMetrics().height(),
                    Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.interface.text_ejec_code_2.blockBoundingRect(block).height()
            blockNumber += 1
    
    def lineNumberAreaWidthExec(self):
        digits = len(str(self.interface.text_ejec_code_2.blockCount()))
        space = 3 + self.interface.text_ejec_code_2.fontMetrics().width('9')*digits
        return space

    def resizeEvent(self, event):
        cr = self.contentsRect()
        self.interface.text_ejec_code_2.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 50 , cr.height()))

    @pyqtSlot(int)
    def updateLineNumberAreaWidthExec(self):
        self.interface.text_ejec_code_2.setViewportMargins(50, 0, 0, 0)

    @pyqtSlot(QRect, int)
    def updateLineNumberAreaExec(self, rect, dy):
        if dy:
            self.interface.text_ejec_code_2.lineNumberArea.scroll(0, dy)
        else:
            self.interface.text_ejec_code_2.lineNumberArea.update(0, rect.y(), self.interface.text_ejec_code_2.lineNumberArea.width(), rect.height())
