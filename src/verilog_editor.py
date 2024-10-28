from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QApplication
from PyQt5.QtGui import QFont, QPainter, QColor, QTextFormat, QTextCursor, QTextDocument, QPalette
from PyQt5.QtCore import Qt, QRect
from verilog_highlighter import VerilogHighlighter
from verilog_formatter import format_verilog
from line_number_area import LineNumberArea


class VerilogEditor(QPlainTextEdit):
    """
    Custom text editor specifically designed for Verilog HDL code editing.
    Provides features like syntax highlighting, line numbering, auto-indentation,
    and code formatting. Inherits from QPlainTextEdit for efficient text handling.
    """

    def __init__(self, parent=None, config=None):
        """
        Initialize the Verilog editor with custom features and styling.

        Args:
            parent: Parent widget
            config: Configuration object containing editor settings
        """
        super().__init__(parent)
        self.config = config or {}

        # Initialize core editor components
        self.setup_editor()  # Set up basic appearance
        self.highlighter = VerilogHighlighter(self.document(), config)  # Syntax highlighting

        # Set up line numbering components
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        # Configure editor behavior settings
        self.auto_indent = self.config.editor.get('auto_indent', True) if hasattr(self.config, 'editor') else True
        self.setTabStopWidth(self.fontMetrics().horizontalAdvance(' ') * 4)  # Set tab width
        self.setLineWrapMode(QPlainTextEdit.NoWrap)  # Disable word wrap
        self.document().setUndoRedoEnabled(True)  # Enable undo/redo

    def setup_editor(self):
        """
        Configure the editor's visual appearance.
        Sets up color scheme and font based on configuration.
        """
        # Apply color scheme from configuration
        palette = self.palette()
        palette.setColor(QPalette.Base, QColor(self.config.theme['background']))
        palette.setColor(QPalette.Text, QColor(self.config.theme['foreground']))
        self.setPalette(palette)

        # Configure font settings
        font = QFont(self.config.editor['font_family'],
                     self.config.editor['font_size'])
        font.setFixedPitch(True)  # Ensure monospace font
        self.setFont(font)

    def lineNumberAreaWidth(self):
        """
        Calculate the width needed for the line number area.
        Width is based on the number of digits in the highest line number.

        Returns:
            int: Width in pixels needed for line numbers
        """
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        """
        Update the editor's left margin to accommodate line numbers.
        Called when the number of lines changes.
        """
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """
        Update the line number area when the editor's viewport changes.

        Args:
            rect: The rectangle that needs updating
            dy: The vertical scroll amount
        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        """
        Handle editor resize events.
        Ensures line number area is resized properly with the editor.
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        """
        Paint the line numbers in the line number area.

        Args:
            event: Paint event containing the area to be updated
        """
        painter = QPainter(self.line_number_area)

        # Set colors from theme
        bg_color = QColor(self.config.theme.get('line_number_bg', '#252526'))
        fg_color = QColor(self.config.theme.get('line_number_fg', '#858585'))
        painter.fillRect(event.rect(), bg_color)

        # Paint line numbers
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(fg_color)
                painter.drawText(0, int(top), self.line_number_area.width(),
                                 self.fontMetrics().height(), Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlightCurrentLine(self):
        """
        Highlight the line containing the text cursor.
        Uses the theme's current line highlight color.
        """
        if not hasattr(self.config, 'editor') or self.config.editor.get('highlight_current_line', True):
            extra_selections = []
            if not self.isReadOnly():
                selection = QTextEdit.ExtraSelection()
                line_color = QColor(self.config.theme.get('current_line', '#282828'))
                selection.format.setBackground(line_color)
                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                selection.cursor = self.textCursor()
                selection.cursor.clearSelection()
                extra_selections.append(selection)
            self.setExtraSelections(extra_selections)

    def getLineIndentation(self, text):
        """
        Get the indentation string at the start of the line.

        Args:
            text: The line of text to analyze

        Returns:
            str: The indentation string (tabs and spaces)
        """
        indent = ''
        for char in text:
            if char == '\t':
                indent += '\t'
            elif char.isspace():
                indent += char
            else:
                break
        return indent

    def shouldAddExtraIndent(self, text):
        """
        Determine if an extra indentation level should be added.
        Checks for keywords and constructs that typically require indentation.

        Args:
            text: The line of text to analyze

        Returns:
            bool: True if extra indentation should be added
        """
        text = text.strip()
        return text.endswith('begin') or text.endswith('(')

    def keyPressEvent(self, event):
        """
        Handle key press events with custom behavior.
        Implements special handling for Return, Tab, and Ctrl+X.

        Args:
            event: Key event to handle
        """
        if event.key() == Qt.Key_Return:
            self.handleReturn()
        elif event.key() == Qt.Key_Tab:
            self.handleTab()
        elif event.key() == Qt.Key_X and event.modifiers() & Qt.ControlModifier:
            if not self.textCursor().hasSelection():
                self.cut_line()
                event.accept()
                return
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def cut_line(self):
        """
        Cut the current line to clipboard.
        If no text is selected, cuts the entire current line.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()

        if cursor.hasSelection():
            self.cut()
            cursor.endEditBlock()
            return

        # Select and cut the current line
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)

        # Handle newline character
        if cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor):
            text = cursor.selectedText()
        else:
            text = cursor.selectedText()

        # Copy to clipboard and delete
        QApplication.clipboard().setText(text)
        cursor.removeSelectedText()

        # Clean up end of document
        if cursor.atEnd():
            cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.EndOfLine)

        cursor.endEditBlock()

    def handleReturn(self):
        """
        Handle Return key press with smart indentation.
        Maintains current indentation level and adds extra indent when needed.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()

        block = cursor.block()
        text = block.text()

        current_indent = self.getLineIndentation(text)
        cursor.insertText('\n')
        cursor.insertText(current_indent)

        if self.shouldAddExtraIndent(text):
            cursor.insertText('\t')

        cursor.endEditBlock()

    def handleTab(self):
        """
        Handle Tab key press.
        Implements block indentation for selected text or inserts tab at cursor.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()

        if cursor.hasSelection():
            self.indentSelection()
        else:
            cursor.insertText('\t')

        cursor.endEditBlock()

    def indentSelection(self):
        """
        Indent or unindent the selected text.
        Adds tab to the start of each selected line.
        """
        cursor = self.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.StartOfBlock)
        cursor.beginEditBlock()

        while cursor.position() < end:
            cursor.insertText('\t')
            cursor.movePosition(QTextCursor.NextBlock)

        cursor.endEditBlock()

    def format_verilog(self):
        """
        Format the entire document using the Verilog formatter.
        Preserves scroll position during formatting.
        """
        cursor = self.textCursor()
        cursor.beginEditBlock()

        scrollbar = self.verticalScrollBar()
        scroll_pos = scrollbar.value()

        formatted_text = format_verilog(self.toPlainText())
        self.setPlainText(formatted_text)

        scrollbar.setValue(scroll_pos)

        cursor.endEditBlock()

    def insertFromMimeData(self, source):
        """
        Handle paste operations with proper indentation.
        Maintains indentation for multi-line paste operations.

        Args:
            source: Mime data containing the text to paste
        """
        if source.hasText():
            cursor = self.textCursor()
            cursor.beginEditBlock()

            current_indent = self.getLineIndentation(cursor.block().text())
            text = source.text()
            lines = text.split('\n')

            # Handle multi-line paste
            if len(lines) > 1:
                indented_text = []
                for i, line in enumerate(lines):
                    if line.strip():
                        if i == 0:
                            indented_text.append(line)
                        else:
                            line_indent = self.getLineIndentation(line)
                            indented_text.append(current_indent + line)
                    else:
                        indented_text.append('')
                source.setText('\n'.join(indented_text))

            cursor.endEditBlock()

        super().insertFromMimeData(source)