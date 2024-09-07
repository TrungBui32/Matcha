from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt5.QtGui import QFont, QPainter, QColor, QTextFormat
from PyQt5.QtCore import Qt, QRect
from verilog_highlighter import VerilogHighlighter
from verilog_formatter import format_verilog
from line_number_area import LineNumberArea


class VerilogEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont('Courier', 10))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        # Set up syntax highlighting
        self.highlighter = VerilogHighlighter(self.document())

        # Set up line numbering
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        # Set up auto-indentation
        self.auto_indent = True

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.line_number_area.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlightCurrentLine(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.darkGray).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def keyPressEvent(self, event):
        if self.auto_indent and event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            block = cursor.block()
            text = block.text()
            indent = len(text) - len(text.lstrip())
            cursor.insertText('\n' + ' ' * indent)
        else:
            super().keyPressEvent(event)

    def format_verilog(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        # Format the entire document
        formatted_text = format_verilog(self.toPlainText())
        self.setPlainText(formatted_text)

        cursor.endEditBlock()