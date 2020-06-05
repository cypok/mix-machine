from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ErrorsList(QListWidget):
  def __init__(self, parent = None):
    QListWidget.__init__(self, parent)

  def setBuddyText(self, text_edit):
    self.buddy_text = text_edit

  def setErrors(self, type, errors_str):
    self.clear()
    self.addItems(errors_str)
    self.show()

  def mouseDoubleClickEvent(self, mouse_event):
    item = self.itemAt(mouse_event.pos())
    line = item.text()
    line_num = int( line[0:line.find(':')] ) # cut all before ':'

    # find absolute position
    text = self.buddy_text.toPlainText()
    pos = 0
    for _ in range(line_num - 1):
      pos = text.find('\n', pos) + 1

    cursor = self.buddy_text.textCursor()
    cursor.setPosition(pos)
    cursor.select(QTextCursor.LineUnderCursor)
    self.buddy_text.setTextCursor(cursor)
