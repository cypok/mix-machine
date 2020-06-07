#!/usr/bin/env python

from __future__ import with_statement

import sys
import os.path
import codecs

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from main_ui import Ui_MainWindow

from dock_mem import MemoryDockWidget
from dock_cpu import CPUDockWidget
from devices import DevDockWidget, QTextEditInputDevice, QTextEditOutputDevice

from asm_data import *
from vm_data import VMData

PROGRAM_NAME = "Mix Machine"

class MainWindow(QMainWindow, Ui_MainWindow):

  inited = pyqtSignal()

  setNewSource = pyqtSignal()
  fontChanged = pyqtSignal(QFont)

  sourceTabFocused = pyqtSignal()
  traceTabFocused = pyqtSignal()

  beforeTrace = pyqtSignal()
  afterTrace = pyqtSignal()
  beforeRun = pyqtSignal()
  afterRun = pyqtSignal("PyQt_PyObject")

  assembleSuccess = pyqtSignal("PyQt_PyObject", "PyQt_PyObject")
  assembleGotErrors = pyqtSignal("int", "QStringList")

  breaked = pyqtSignal()

  stoppedAction = pyqtSignal()

  def __init__(self, parent=None):
    QMainWindow.__init__(self, parent)

    self.mem_dock = MemoryDockWidget(self)
    # dock areas really would be Left and Right :)
    self.addDockWidget(Qt.RightDockWidgetArea, self.mem_dock)

    self.cpu_dock = CPUDockWidget(self)
    # dock areas really would be Left and Right :)
    self.addDockWidget(Qt.LeftDockWidgetArea, self.cpu_dock)

    self.dev_dock = DevDockWidget(self)
    # dock areas really would be Left and Right :)
    self.addDockWidget(Qt.RightDockWidgetArea, self.dev_dock)

    self.setAttribute(Qt.WA_DeleteOnClose)
    self.setupUi(self)

    self.connect_all()

    self.action_Quit.triggered.connect(qApp.closeAllWindows)
    self.txt_source.textChanged.connect(lambda: self.setWindowModified(True))

    self.action_Open.triggered.connect(self.slot_File_Open)
    self.action_New.triggered.connect(self.slot_File_New)
    self.action_Save.triggered.connect(self.slot_File_Save)
    self.action_Save_as.triggered.connect(self.slot_File_SaveAs)

    self.action_Assemble.triggered.connect(self.slot_Assemble)
    self.action_Step.triggered.connect(self.slot_Step)
    self.action_Trace.triggered.connect(self.slot_Trace)
    self.action_Run.triggered.connect(self.slot_Run)
    self.action_Break.triggered.connect(self.slot_Break)

    self.action_Change_font.triggered.connect(self.slot_Change_font)

    self.errors_list.setBuddyText(self.txt_source)

    self.file_filters = self.tr("MIX source files (*.mix);;All files (*.*)")
    self.slot_File_New()

    about_text = self.tr("""
    <h2>Mix Machine</h2><br><br>
    An implementation of Don Knuth's MIX machine in Python with GUI<br>
    Project's homepage - <a href="http://github.com/be9/mix-machine">http://github.com/be9/mix-machine</a>
    """)
    self.action_About_Mix_Machine.triggered.connect(lambda: QMessageBox.about(self, self.tr("About Mix Machine"), about_text))
    self.action_About_Qt.triggered.connect(qApp.aboutQt)

    self.tabWidget.currentChanged.connect(self.slot_cur_tab_changed)

    self.inited.emit()

    self.output_device = QTextEditOutputDevice(
        mode = "w", block_size = 24 * 5, lock_time = 24*2, text_edit = self.dev_dock.text_printer
    )
    self.input_device = QTextEditInputDevice(
        mode = "r", block_size = 14 * 5, lock_time = 14*2, text_edit = self.dev_dock.text_terminal
    )

  def slot_cur_tab_changed(self, index):
    if index == 0:
      self.sourceTabFocused.emit()
    else:
      self.traceTabFocused.emit()

  def slot_Change_font(self):
    new_font, ok = QFontDialog.getFont(self.txt_source.font())
    if ok:
      self.fontChanged.emit(new_font)

  def slot_File_New(self):
    if not self.checkUnsaved(): 
      return

    self.txt_source.setPlainText(u"")

    self.setWindowModified(False)

    self.setCurrentFile("")

    self.setNewSource.emit()

    self.statusBar().showMessage(self.tr("Empty source file has been created."), 2000)

  def checkUnsaved(self):
    if not self.isWindowModified():
      return True

    button = QMessageBox.information(self, PROGRAM_NAME,
        self.tr("Document was changed!"),
        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

    if button == QMessageBox.Save:
      self.slot_File_Save()
    elif button == QMessageBox.Cancel:
      return False

    return True

  def setCurrentFile(self, fname):
    self.cur_file = fname

    self.setWindowModified(False)

    shown_name = self.tr("Untitled")

    if self.cur_file != "":
      path, shown_name = os.path.split(self.cur_file)

    self.setWindowTitle(self.tr("{0}[*] - {1}").format(shown_name, PROGRAM_NAME))

  def slot_File_Save(self):
    if self.cur_file == "":
      self.slot_File_SaveAs()
    else:
      self.saveToFile(self.cur_file)

  def slot_File_SaveAs(self):
    fn = QFileDialog.getSaveFileName(self, self.tr("Choose file to save to..."),
        self.cur_file, self.file_filters)

    if fn != "":
      fn = QDir.toNativeSeparators(fn)

      base, ext = os.path.splitext(fn)
      if ext == '' or ext == '.':
        fn = base + '.mix'

      if self.saveToFile(fn):
        self.setCurrentFile(fn)

  def closeEvent(self, ce):
    self.slot_Break() # break machine if running
    if self.checkUnsaved():
      ce.accept()
    else:
      ce.ignore()

  def slot_File_Open(self):
    if not self.checkUnsaved():
      return

    fn, _ = QFileDialog.getOpenFileName(self, self.tr("Open file..."), "", self.file_filters)

    if fn != "":
      self.loadFromFile(QDir.toNativeSeparators(fn))

  def saveToFile(self, filename):
    try:
      with codecs.open(filename, "w", "UTF-8") as f:
        f.write(self.txt_source.toPlainText())

      self.setWindowModified(False)

      self.statusBar().showMessage(self.tr("File has been saved."), 2000)

    except IOError as e:
      QMessageBox.critical(None, self.tr("Error"), e.strerror)
      self.statusBar().showMessage(self.tr("Error saving file."), 2000)

    else:
      return True

    return False

  def loadFromFile(self, filename):
    try:
      with codecs.open(filename, "r", "UTF-8") as f:
        self.txt_source.setPlainText(f.read())
      
      self.setWindowModified(False)

    except IOError as e:
      QMessageBox.critical(None, self.tr("Error"), e.strerror)
      self.statusBar().showMessage(self.tr("Error loading file."), 2000)

    else:
      self.setNewSource.emit()

      self.setCurrentFile(filename)

  def cpu_hook(self, item, old, new):
    self.cpu_dock.hook(item, old, new)
    self.listing_view.hook(item, old, new)
    self.disasm_view.hook(item, old, new)

  def mem_hook(self, addr, old, new):
    self.mem_dock.hook(addr, old, new)
    self.listing_view.hook(addr, old, new)
    self.disasm_view.hook(addr, old, new)

  def lock_hook(self, mode, old, new):
    self.mem_dock.hook(mode, old, new)
    self.listing_view.hook(mode, old, new)
    self.disasm_view.hook(mode, old, new)

  def slot_Assemble(self):
    ret_type, content = asm(self.txt_source.toPlainText())
    if ret_type == ASM_NO_ERRORS:
      self.asm_data = content # mem, start_addr, listing
      self.vm_data = VMData(self.asm_data) # vm, listing

      # add printer
      self.output_device.reset()
      self.vm_data.addDevice(18, self.output_device)
      # add input terminal
      self.input_device.reset()
      self.vm_data.addDevice(19, self.input_device)

      self.assembleSuccess.emit(self.vm_data, self.asm_data)
      return

    # we have errors! (emit type of errors and list of errors)
    self.assembleGotErrors(ret_type, [ "%i: %s" % err for err in content ])

  def enableHooks(self, enable = True):
    if enable:
      self.vm_data.setCPUHook(self.cpu_hook)
      self.vm_data.setMemHook(self.mem_hook)
      self.vm_data.setLockHook(self.lock_hook)
    else:
      self.vm_data.setCPUHook(None)
      self.vm_data.setMemHook(None)
      self.vm_data.setLockHook(None)

  def start_action(self):
    self.running = True
    #self.startedAction.emit() # not used

  def stop_action(self):
    self.running = False
    self.stoppedAction.emit()

  def doAction(self, action):
    if self.vm_data.halted():
      QMessageBox.information(self, self.tr("Mix machine"), self.tr("Mix machine is halted."))
      return

    try:
      self.start_action()
      action()
    except Exception as err:
      self.stop_action()
      if type(err) in self.vm_data.vm_errors:
        QMessageBox.critical(self, self.tr("Runtime error"), str(err))
      else:
        raise err
    else:
      self.stop_action()
      if self.vm_data.halted():
        QMessageBox.information(self, self.tr("Mix machine"), self.tr("Mix machine was halted."))

  def slot_Step(self):
    self.beforeTrace.emit()
    self.doAction(self.vm_data.step)
    self.afterTrace.emit()

  def trace_vm(self):
    while not self.vm_data.halted() and self.running:
      self.cpu_dock.resetHighlight() # it's necessary
      self.vm_data.step()
      QCoreApplication.processEvents()
      if self.vm_data.ca() in self.breaks:
        break

  def run_vm(self):
    while not self.vm_data.halted() and self.running:
      self.vm_data.step()
      QCoreApplication.processEvents()
      if self.vm_data.ca() in self.breaks:
        break

  def slot_Trace(self):
    self.beforeTrace.emit()
    self.doAction(self.trace_vm)
    self.afterTrace.emit()

  def slot_Run(self):
    self.beforeRun.emit()

    self.progress = QProgressDialog(self.tr("Running ({0} cycles passed)").format(0), self.tr("Break run"), 0, 10, self)
    self.progress.setMinimumDuration(0)
    self.progress.setAutoClose(False)
    self.progress.setAutoReset(False)
    self.progress.canceled.connect(self.slot_Break)

    self.progress_timer = QTimer(self)
    self.progress_timer.timeout.connect(self.progressTick)
    self.stoppedAction.connect(self.progress_timer.stop)
    self.progress_timer.start(100)

    self.progress.setValue(0)
    self.doAction(self.run_vm)

    self.progress_timer.stop()
    self.progress.cancel()
    del self.progress, self.progress_timer

    self.afterRun.emit(self.vm_data)

  def progressTick(self):
    self.progress.setLabelText(self.tr("Running ({0} cycles passed)").format(self.vm_data.cycles()))
    if self.progress.value() == self.progress.maximum():
      self.progress.setValue(0)
    else:
      self.progress.setValue(self.progress.value() + 1)

  def slot_Break(self):
    self.breaked.emit()
    self.running = False

  def resetBreakpointSet(self):
    self.breaks = set()
    self.listing_view.setBreakpointSet(self.breaks)
    self.disasm_view.setBreakpointSet(self.breaks)

  # menubar slots
  def menuBarHideRun(self):
    self.menu_File.setEnabled(        True)
    self.menu_Options.setEnabled(     True)
    self.action_Assemble.setEnabled(  True)
    self.action_Step.setEnabled(      False)
    self.action_Trace.setEnabled(     False)
    self.action_Run.setEnabled(       False)
    self.action_Break.setEnabled(     False)
  def menuBarShowRun(self):
    self.menu_File.setEnabled(        True)
    self.menu_Options.setEnabled(     True)
    self.action_Assemble.setEnabled(  True)
    self.action_Step.setEnabled(      True)
    self.action_Trace.setEnabled(     True)
    self.action_Run.setEnabled(       True)
    self.action_Break.setEnabled(     False)
  def menuBarShowBreak(self):
    self.menu_File.setEnabled(        False)
    self.menu_Options.setEnabled(     False)
    self.action_Assemble.setEnabled(  False)
    self.action_Step.setEnabled(      False)
    self.action_Trace.setEnabled(     False)
    self.action_Run.setEnabled(       False)
    self.action_Break.setEnabled(     True)

  def connect_all(self):
    # errors_list
    self.inited.connect(            self.errors_list.hide)
    self.setNewSource.connect(      self.errors_list.hide)
    self.assembleSuccess.connect(   self.errors_list.hide)
    self.assembleGotErrors.connect( self.errors_list.setErrors)

    # menubar
    self.inited.connect(            self.menuBarHideRun)
    self.setNewSource.connect(      self.menuBarHideRun)
    self.assembleGotErrors.connect( self.menuBarHideRun)
    self.assembleSuccess.connect(   self.menuBarShowRun)
    self.afterTrace.connect(        self.menuBarShowRun)
    self.afterRun.connect(          self.menuBarShowRun)
    self.beforeTrace.connect(       self.menuBarShowBreak)
    self.beforeRun.connect(         self.menuBarShowBreak)

    # tabs
    self.inited.connect(            self.tabWidget.hideRun)
    self.setNewSource.connect(      self.tabWidget.hideRun)
    self.assembleGotErrors.connect( self.tabWidget.hideRun)
    self.assembleSuccess.connect(   self.tabWidget.showRun)
    self.traceTabFocused.connect(   self.tabWidget.rememberRunTab)

    # enable and disable hooks
    self.beforeTrace.connect(       lambda: self.enableHooks(True))
    self.beforeRun.connect(         lambda: self.enableHooks(False))

    # txt_source
    self.fontChanged.connect(       self.txt_source.setFont)

    # listing and disassembler
    for widget in (self.listing_view, self.disasm_view):
      self.inited.connect(          widget.init)
      self.fontChanged.connect(     widget.changeFont)
      self.assembleSuccess.connect( widget.resetVM)
      self.beforeRun.connect(       widget.snapshotMem)
      self.afterRun.connect(        widget.updateVM)

    # all trace widgets visibility
    for widget in (self.cpu_dock, self.mem_dock, self.dev_dock):
      self.inited.connect(          widget.hide)
      self.sourceTabFocused.connect(widget.hide)
      self.traceTabFocused.connect( widget.show)

    # cpu_dock
    self.assembleSuccess.connect(   self.cpu_dock.init)
    self.afterRun.connect(          self.cpu_dock.reload)
    self.beforeRun.connect(         self.cpu_dock.resetHighlight)
    self.beforeTrace.connect(       self.cpu_dock.resetHighlight)

    # mem_dock
    self.assembleSuccess.connect(   self.mem_dock.init)
    self.afterRun.connect(          self.mem_dock.reload)

    self.setNewSource.connect(      self.resetBreakpointSet)

if __name__ == "__main__":
  app = QApplication(sys.argv)

  mw = MainWindow()
  mw.show()
  sys.exit(app.exec_())
