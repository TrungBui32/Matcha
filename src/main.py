import sys
from PyQt5.QtWidgets import QApplication
from editor_window import EditorWindow

def main():
    app = QApplication(sys.argv)
    editor = EditorWindow()
    editor.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()