from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor


class VerilogHighlighter(QSyntaxHighlighter):
    """
    Syntax highlighter for Verilog HDL code.
    Provides real-time syntax highlighting for various Verilog language elements:
    - Keywords and control structures
    - Module declarations and instances
    - Port directions and data types
    - Numbers in various formats
    - Comments (single-line and multi-line)
    - Operators and special characters
    """

    def __init__(self, parent=None, config=None):
        """
        Initialize the Verilog syntax highlighter.

        Args:
            parent: Parent QTextDocument
            config: Configuration object containing theme colors
        """
        super().__init__(parent)
        self.config = config or {}
        self.highlighting_rules = []  # List to store (pattern, format) pairs

        self.init_formats()  # Initialize text formats
        self.init_rules()  # Set up highlighting rules

    def init_formats(self):
        """
        Initialize text formats for different syntax elements.
        Creates QTextCharFormat objects with appropriate colors and styles
        for each type of syntax element.
        """
        # Format for language keywords (if, else, begin, end, etc.)
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(self.config.theme.get('keywords', "#569CD6")))
        self.keyword_format.setFontWeight(QFont.Bold)

        # Format for port direction keywords (input, output, inout)
        self.port_format = QTextCharFormat()
        self.port_format.setForeground(QColor(self.config.theme.get('storage', "#569CD6")))

        # Format for data types (wire, reg, integer, etc.)
        self.type_format = QTextCharFormat()
        self.type_format.setForeground(QColor(self.config.theme.get('types', "#4EC9B0")))

        # Format for numeric literals
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(self.config.theme.get('numbers', "#B5CEA8")))

        # Format for comments (both single-line and multi-line)
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(self.config.theme.get('comments', "#608B4E")))

        # Format for special keywords (posedge, negedge, etc.)
        self.special_format = QTextCharFormat()
        self.special_format.setForeground(QColor(self.config.theme.get('special_keywords', "#C586C0")))

        # Format for operators and brackets
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor(self.config.theme.get('operators', "#D4D4D4")))

    def init_rules(self):
        """
        Initialize syntax highlighting rules using regular expressions.
        Each rule consists of a QRegExp pattern and its corresponding format.
        Rules are processed in order, so more specific rules should come first.
        """
        # Bracket highlighting (all types of brackets)
        self.highlighting_rules.append((
            QRegExp(r'[\[\]{}()]'),
            self.operator_format
        ))

        # Module names and instance names
        # Uses lookahead to avoid including parentheses
        self.highlighting_rules.append((
            QRegExp(r'module\s+(\w+)|(\w+)\s+\w+\s*(?=\()'),
            self.keyword_format
        ))

        # Language keywords
        keywords = [
            'module', 'endmodule', 'timescale',  # Module-related
            'begin', 'end', 'if', 'else',  # Control structures
            'case', 'endcase', 'default',  # Case statements
            'assign', 'always', 'initial',  # Behavioral constructs
            'function', 'endfunction',  # Functions
            'task', 'endtask',  # Tasks
            'parameter', 'localparam'  # Parameters
        ]
        for keyword in keywords:
            pattern = QRegExp('\\b' + keyword + '\\b')  # Word boundaries
            self.highlighting_rules.append((pattern, self.keyword_format))

        # Port direction keywords
        port_keywords = ['input', 'output', 'inout']
        for keyword in port_keywords:
            pattern = QRegExp('\\b' + keyword + '\\b')
            self.highlighting_rules.append((pattern, self.port_format))

        # Data type keywords
        type_keywords = ['wire', 'reg', 'integer', 'real']
        for keyword in type_keywords:
            pattern = QRegExp('\\b' + keyword + '\\b')
            self.highlighting_rules.append((pattern, self.type_format))

        # Special keywords
        special_keywords = ['posedge', 'negedge', 'or']
        for keyword in special_keywords:
            pattern = QRegExp('\\b' + keyword + '\\b')
            self.highlighting_rules.append((pattern, self.special_format))

        # Operators (arithmetic, logical, comparison)
        operators = [
            '=', '==', '!=', '<=', '>=',  # Assignment and comparison
            '&&', r'\|\|',  # Logical AND/OR
            r'\+', '-', r'\*', '/',  # Arithmetic
            r'\^', r'\&', r'\|', '~',  # Bitwise
            '<<', '>>'  # Shifts
        ]
        for operator in operators:
            pattern = QRegExp(operator)
            self.highlighting_rules.append((pattern, self.operator_format))

        # Number formats
        number_patterns = [
            r'\b\d+\'[bB][01_]+\b',  # Binary (e.g., 4'b1010)
            r'\b\d+\'[hH][0-9a-fA-F_]+\b',  # Hexadecimal (e.g., 8'hAB)
            r'\b\d+\'[dD][0-9_]+\b',  # Decimal with base (e.g., 10'd42)
            r'\b\d+\b',  # Simple decimal
            r'\b[0-9]+\.[0-9]+\b'  # Floating point
        ]
        for pattern in number_patterns:
            self.highlighting_rules.append((QRegExp(pattern), self.number_format))

        # Single-line comments
        self.highlighting_rules.append((
            QRegExp(r'//[^\n]*'),
            self.comment_format
        ))

    def highlightBlock(self, text):
        """
        Apply syntax highlighting to a block of text.
        Called automatically by Qt when text needs to be highlighted.

        Args:
            text: Text block to highlight
        """
        # Handle multi-line comments first
        self.handle_multiline_comments(text)

        # Apply all other highlighting rules
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                # Skip highlighting if inside multi-line comment
                if not self.is_in_multiline_comment(index, length):
                    self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

    def handle_multiline_comments(self, text):
        """
        Process multi-line comments in the text block.
        Handles both start and end of multi-line comments,
        maintaining state between blocks.

        Args:
            text: Text block to process
        """
        start = '/*'
        end = '*/'

        # Determine comment start position
        start_index = text.find(start) if self.previousBlockState() != 1 else 0

        while start_index >= 0:
            end_index = text.find(end, start_index)
            if end_index == -1:
                # Comment continues to next block
                self.setFormat(start_index, len(text) - start_index, self.comment_format)
                self.setCurrentBlockState(1)  # Mark block as ending in comment
                break
            else:
                # Comment ends in this block
                length = end_index - start_index + len(end)
                self.setFormat(start_index, length, self.comment_format)
                start_index = text.find(start, start_index + length)

    def is_in_multiline_comment(self, position, length):
        """
        Check if a text range is inside a multi-line comment.

        Args:
            position: Start position to check
            length: Length of text range

        Returns:
            bool: True if the range is within a comment
        """
        return self.format(position) == self.comment_format