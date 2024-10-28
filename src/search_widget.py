from PyQt5.QtWidgets import (QWidget, QGridLayout, QLineEdit, QPushButton,
                             QCheckBox, QLabel, QHBoxLayout, QVBoxLayout,
                             QFrame, QGroupBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QTextDocument


class SearchWidget(QWidget):
    """
    A search and replace widget for the text editor.
    Provides functionality for finding and replacing text with various options.
    Implements a VS Code-like dark theme interface.
    """

    def __init__(self, editor, config=None):
        """
        Initialize the search widget.

        Args:
            editor: The text editor widget this search widget will operate on
            config: Optional configuration object for styling and behavior settings
        """
        super().__init__()
        self.editor = editor
        self.config = config
        self.last_search = ''  # Store the last search term for repeat operations
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface components.
        Creates a layout with search and replace functionality, including:
        - Search input field with navigation buttons
        - Replace input field with replace buttons
        - Search options (case sensitivity, whole word matching)
        - Status indicator for search results
        """
        # Main layout with padding and spacing
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Search group box with custom styling
        search_group = QGroupBox("Search")
        search_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #404040;
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
                color: #D4D4D4;
            }
        """)
        search_layout = QGridLayout()
        search_layout.setSpacing(8)

        # Search input container with custom frame
        search_container = QFrame()
        search_container.setStyleSheet("""
            QFrame {
                border: 1px solid #404040;
                border-radius: 4px;
                background-color: #1E1E1E;
            }
        """)
        search_hbox = QHBoxLayout(search_container)
        search_hbox.setContentsMargins(5, 0, 5, 0)

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Find text...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 5px;
                background-color: transparent;
                color: #D4D4D4;
                selection-background-color: #264F78;
            }
        """)
        self.search_input.returnPressed.connect(self.find_next)
        search_hbox.addWidget(self.search_input)

        # Navigation buttons
        button_layout = QHBoxLayout()
        find_prev_btn = self.create_button("◀", "Find Previous (Shift+F3)", self.find_previous)
        find_next_btn = self.create_button("▶", "Find Next (F3)", self.find_next)
        button_layout.addWidget(find_prev_btn)
        button_layout.addWidget(find_next_btn)

        # Add search components to layout
        search_layout.addWidget(search_container, 0, 0)
        search_layout.addLayout(button_layout, 0, 1)

        # Replace input container
        replace_container = QFrame()
        replace_container.setStyleSheet("""
            QFrame {
                border: 1px solid #404040;
                border-radius: 4px;
                background-color: #1E1E1E;
            }
        """)
        replace_hbox = QHBoxLayout(replace_container)
        replace_hbox.setContentsMargins(5, 0, 5, 0)

        # Replace input field
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace with...")
        self.replace_input.setStyleSheet("""
            QLineEdit {
                border: none;
                padding: 5px;
                background-color: transparent;
                color: #D4D4D4;
                selection-background-color: #264F78;
            }
        """)
        replace_hbox.addWidget(self.replace_input)

        # Replace buttons
        replace_layout = QHBoxLayout()
        replace_btn = self.create_button("Replace", "Replace", self.replace)
        replace_all_btn = self.create_button("Replace All", "Replace All", self.replace_all)
        replace_layout.addWidget(replace_btn)
        replace_layout.addWidget(replace_all_btn)

        # Add replace components to layout
        search_layout.addWidget(replace_container, 1, 0)
        search_layout.addLayout(replace_layout, 1, 1)

        # Search options
        options_layout = QHBoxLayout()

        # Case sensitivity checkbox
        self.case_sensitive = QCheckBox("Match Case")
        self.case_sensitive.setStyleSheet("""
            QCheckBox {
                color: #D4D4D4;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: 1px solid #404040;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
            }
        """)

        # Whole word matching checkbox
        self.whole_words = QCheckBox("Whole Words")
        self.whole_words.setStyleSheet("""
            QCheckBox {
                color: #D4D4D4;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                border: 1px solid #404040;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                background-color: #007ACC;
            }
        """)

        options_layout.addWidget(self.case_sensitive)
        options_layout.addWidget(self.whole_words)
        options_layout.addStretch()

        # Add options to layout
        search_layout.addLayout(options_layout, 2, 0, 1, 2)
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)

        # Status label for search results
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #D4D4D4;
                padding: 5px;
            }
        """)
        main_layout.addWidget(self.status_label)

        main_layout.addStretch()
        self.setLayout(main_layout)

        # Set overall widget style
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
            }
            QPushButton {
                background-color: #0E639C;
                border: none;
                border-radius: 4px;
                color: white;
                padding: 5px 10px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #1177BB;
            }
            QPushButton:pressed {
                background-color: #0D5789;
            }
            QPushButton:disabled {
                background-color: #2D2D2D;
                color: #666666;
            }
        """)

    def create_button(self, text, tooltip, callback):
        """
        Create a styled button with specified text, tooltip, and callback.

        Args:
            text: Button label text
            tooltip: Hover tooltip text
            callback: Function to call when button is clicked

        Returns:
            QPushButton: Configured button instance
        """
        btn = QPushButton(text)
        btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        return btn

    def focusSearchInput(self):
        """
        Focus the search input field and select its contents.
        Called when the search widget is shown.
        """
        self.search_input.setFocus()
        self.search_input.selectAll()

    def find_next(self):
        """
        Find the next occurrence of the search text.
        Wraps around to the beginning of the document if no match is found forward.
        Updates the status label with the search result.
        """
        text = self.search_input.text()
        if not text:
            return

        # Set up search flags based on options
        flags = QTextDocument.FindFlags()
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QTextDocument.FindWholeWords

        cursor = self.editor.textCursor()
        found = self.editor.find(text, flags)

        if not found:
            # Wrap around to beginning
            cursor.movePosition(cursor.Start)
            self.editor.setTextCursor(cursor)
            found = self.editor.find(text, flags)

        # Update status
        if found:
            self.status_label.setText("")
            self.last_search = text
        else:
            self.status_label.setText("No matches found")
            self.status_label.setStyleSheet("color: #F48771;")

    def find_previous(self):
        """
        Find the previous occurrence of the search text.
        Wraps around to the end of the document if no match is found backward.
        Updates the status label with the search result.
        """
        text = self.search_input.text()
        if not text:
            return

        # Set up search flags based on options
        flags = QTextDocument.FindFlags()
        flags |= QTextDocument.FindBackward
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QTextDocument.FindWholeWords

        cursor = self.editor.textCursor()
        found = self.editor.find(text, flags)

        if not found:
            # Wrap around to end
            cursor.movePosition(cursor.End)
            self.editor.setTextCursor(cursor)
            found = self.editor.find(text, flags)

        # Update status
        if found:
            self.status_label.setText("")
            self.last_search = text
        else:
            self.status_label.setText("No matches found")
            self.status_label.setStyleSheet("color: #F48771;")

    def replace(self):
        """
        Replace the current selection with the replacement text.
        Only replaces if text is selected (presumably from a find operation).
        Automatically finds the next match after replacing.
        """
        if self.editor.textCursor().hasSelection():
            self.editor.textCursor().insertText(self.replace_input.text())
            self.find_next()

    def replace_all(self):
        """
        Replace all occurrences of the search text in the document.
        Performs the operation as a single undo/redo operation.
        Updates the status label with the number of replacements made.
        """
        text = self.search_input.text()
        if not text:
            return

        count = 0
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()  # Start compound edit operation

        # Start from beginning of document
        cursor.movePosition(cursor.Start)
        self.editor.setTextCursor(cursor)

        # Replace all occurrences
        while True:
            flags = Qt.FindFlags()
            if self.case_sensitive.isChecked():
                flags |= Qt.CaseSensitive
            if self.whole_words.isChecked():
                flags |= Qt.WholeWords

            found = self.editor.find(text, flags)
            if not found:
                break

            if self.editor.textCursor().hasSelection():
                self.editor.textCursor().insertText(self.replace_input.text())
                count += 1

        cursor.endEditBlock()  # End compound edit operation

        # Update status with results
        if count > 0:
            self.status_label.setText(f"Replaced {count} occurrence(s)")
            self.status_label.setStyleSheet("color: #89D185;")  # Success color
        else:
            self.status_label.setText("No matches found")
            self.status_label.setStyleSheet("color: #F48771;")  # Error color