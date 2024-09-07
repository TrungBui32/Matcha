from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QDockWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from verilog_editor import VerilogEditor


class EditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Verilog Editor')
        self.setGeometry(100, 100, 1000, 600)

        self.editor = VerilogEditor(self)
        self.setCentralWidget(self.editor)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('File')

        new_action = QAction(QIcon('new.png'), 'New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        open_action = QAction(QIcon('open.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon('save.png'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Edit menu
        edit_menu = menubar.addMenu('Edit')

        format_action = QAction('Format Verilog', self)
        format_action.setShortcut('Ctrl+F')
        format_action.triggered.connect(self.editor.format_verilog)
        edit_menu.addAction(format_action)

    def new_file(self):
        self.editor.clear()

    def open_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Verilog File", "",
                                                  "Verilog Files (*.v *.sv);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'r') as f:
                self.editor.setPlainText(f.read())

    def save_file(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Verilog File", "",
                                                  "Verilog Files (*.v *.sv);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'w') as f:
                f.write(self.editor.toPlainText())
            QMessageBox.information(self, "File Saved", "File has been saved successfully.")
