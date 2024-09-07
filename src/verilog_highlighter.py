from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor


class VerilogHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.highlighting_rules = []

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "module", "endmodule", "input", "output", "wire", "reg", "always", "begin", "end",
            "if", "else", "case", "endcase", "for", "while", "function", "endfunction",
            "task", "endtask", "assign", "posedge", "negedge"
        ]
        for keyword in keywords:
            pattern = QRegExp("\\b" + keyword + "\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))
        number_pattern = QRegExp("\\b[0-9]+\\b")
        self.highlighting_rules.append((number_pattern, number_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#608B4E"))
        comment_pattern = QRegExp("//[^\n]*")
        self.highlighting_rules.append((comment_pattern, comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
