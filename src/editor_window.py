from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QMessageBox,
                             QDockWidget, QUndoStack, QApplication, QVBoxLayout,
                             QWidget, QLabel, QStatusBar)
from PyQt5.QtGui import QIcon, QKeySequence, QFont
from PyQt5.QtCore import Qt, QFileInfo, QSettings, QSize
from verilog_editor import VerilogEditor
from search_widget import SearchWidget
from config import EditorConfig


class EditorWindow(QMainWindow):
    """
    Main window class for the Matcha Verilog Editor application.
    Handles the overall UI layout, menus, file operations, and editor integration.
    Inherits from QMainWindow to provide the main application window framework.
    """

    def __init__(self, config=None):
        """
        Initialize the editor window with configuration settings.

        Args:
            config: Optional EditorConfig instance. If None, creates a new one.
        """
        super().__init__()
        self.config = config or EditorConfig()
        self.current_file = None  # Tracks the currently open file
        self.search_widget = None  # Search/Replace widget reference
        self.initUI()
        self.load_settings()  # Restore previous window state and geometry

    def initUI(self):
        """
        Initialize the user interface components.
        Sets up the main window layout, editor, docks, status bar, and menus.
        """
        # Set window properties
        self.setWindowTitle('Matcha - Verilog Editor')
        self.setGeometry(100, 100, 1200, 800)  # Default window size and position

        # Create and set up the main editor widget
        self.editor = VerilogEditor(self, self.config)
        self.setCentralWidget(self.editor)

        # Track document modifications
        self.editor.document().modificationChanged.connect(self.documentWasModified)

        # Initialize UI components
        self.setup_docks()
        self.setup_status_bar()
        self.create_menu_bar()
        self.apply_theme()

    def setup_docks(self):
        """
        Set up dock widgets for additional functionality.
        Currently includes the search/replace widget in a bottom dock area.
        """
        # Create search dock widget
        self.search_dock = QDockWidget("Search", self)
        self.search_widget = SearchWidget(self.editor)
        self.search_dock.setWidget(self.search_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.search_dock)
        self.search_dock.hide()  # Initially hidden

    def setup_status_bar(self):
        """
        Set up the status bar with cursor position and file information.
        Displays current line/column numbers and active file details.
        """
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)

        # Create status indicators
        self.cursor_position_label = QLabel("Line: 1, Column: 1")
        self.file_info_label = QLabel("No File")

        # Add permanent widgets to status bar
        status_bar.addPermanentWidget(self.cursor_position_label)
        status_bar.addPermanentWidget(self.file_info_label)

        # Update cursor position when it changes
        self.editor.cursorPositionChanged.connect(self.update_cursor_position)

    def create_menu_bar(self):
        """
        Create the application menu bar with File, Edit, and View menus.
        Sets up all menu actions with shortcuts and icons.
        """
        menubar = self.menuBar()

        # File menu - New, Open, Save, Save As, Exit
        file_menu = menubar.addMenu('&File')
        new_action = self.create_action('&New',
                                        self.config.keybindings['new'],
                                        'Create new file',
                                        self.new_file,
                                        'new')
        open_action = self.create_action('&Open...',
                                         self.config.keybindings['open'],
                                         'Open file',
                                         self.open_file,
                                         'open')
        save_action = self.create_action('&Save',
                                         self.config.keybindings['save'],
                                         'Save file',
                                         self.save_file,
                                         'save')
        save_as_action = self.create_action('Save &As...',
                                            self.config.keybindings['save_as'],
                                            'Save file as',
                                            self.save_file_as,
                                            'save-as')

        file_menu.addActions([new_action, open_action, save_action, save_as_action])
        file_menu.addSeparator()
        file_menu.addAction(self.create_action('E&xit', 'Alt+F4', 'Exit application', self.close, 'exit'))

        # Edit menu - Undo, Redo, Find/Replace, Format
        edit_menu = menubar.addMenu('&Edit')

        # Undo/Redo actions
        self.undo_action = QAction('&Undo', self)
        self.undo_action.setShortcut('Ctrl+Z')
        self.undo_action.triggered.connect(self.editor.undo)
        self.undo_action.setEnabled(self.editor.document().isUndoAvailable())
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction('&Redo', self)
        self.redo_action.setShortcut('Ctrl+Shift+Z')
        self.redo_action.triggered.connect(self.editor.redo)
        self.redo_action.setEnabled(self.editor.document().isRedoAvailable())
        edit_menu.addAction(self.redo_action)

        # Connect undo/redo availability signals
        self.editor.document().undoAvailable.connect(self.undo_action.setEnabled)
        self.editor.document().redoAvailable.connect(self.redo_action.setEnabled)

        edit_menu.addSeparator()

        # Find/Replace and Format actions
        find_action = self.create_action('&Find/Replace',
                                         self.config.keybindings['find'],
                                         'Find and replace text',
                                         self.show_search,
                                         'find')
        edit_menu.addAction(find_action)
        edit_menu.addSeparator()

        format_action = self.create_action('&Format Code',
                                           self.config.keybindings.get('format', 'Ctrl+Shift+F'),
                                           'Format Verilog code',
                                           self.format_code,
                                           'format')
        edit_menu.addAction(format_action)

        # View menu - Toggle dock widgets
        view_menu = menubar.addMenu('&View')
        view_menu.addAction(self.search_dock.toggleViewAction())

    def create_action(self, text, shortcut, status_tip, callback, icon_name=None):
        """
        Helper method to create QAction objects with consistent styling.

        Args:
            text: Action text in menu
            shortcut: Keyboard shortcut
            status_tip: Status bar tooltip
            callback: Function to call when triggered
            icon_name: Optional icon resource name

        Returns:
            QAction: Configured action object
        """
        action = QAction(text, self)
        if icon_name and hasattr(QIcon, icon_name):
            action.setIcon(QIcon(f":/icons/{icon_name}.png"))
        action.setShortcut(shortcut)
        action.setStatusTip(status_tip)
        action.triggered.connect(callback)
        return action

    def apply_theme(self):
        """
        Apply the configured theme colors to the window components.
        Uses colors defined in the config.theme dictionary.
        """
        if self.config.theme.get('background'):
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {self.config.theme['background']};
                    color: {self.config.theme['foreground']};
                }}
                QMenuBar {{
                    background-color: {self.config.theme['background']};
                    color: {self.config.theme['foreground']};
                }}
                QStatusBar {{
                    background-color: {self.config.theme['background']};
                    color: {self.config.theme['foreground']};
                }}
            """)

    def documentWasModified(self):
        """
        Handle document modification events.
        Updates window title and undo/redo state.
        """
        self.update_title()
        self.undo_action.setEnabled(self.editor.document().isUndoAvailable())
        self.redo_action.setEnabled(self.editor.document().isRedoAvailable())

    def new_file(self):
        """
        Create a new empty file.
        Prompts to save current file if modified.
        """
        if self.maybe_save():
            self.editor.clear()
            self.current_file = None
            self.editor.document().setModified(False)
            self.editor.document().clearUndoRedoStacks()
            self.update_title()
            self.update_file_info()

    def open_file(self):
        """
        Open an existing file via file dialog.
        Prompts to save current file if modified.
        """
        if self.maybe_save():
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(
                self, "Open Verilog File", "",
                "Verilog Files (*.v *.sv);;All Files (*)", options=options)
            if fileName:
                self.load_file(fileName)

    def load_file(self, fileName):
        """
        Load content from specified file into editor.

        Args:
            fileName: Path to file to load
        """
        try:
            with open(fileName, 'r') as f:
                self.editor.setPlainText(f.read())
            self.current_file = fileName
            self.editor.document().setModified(False)
            self.editor.document().clearUndoRedoStacks()
            self.update_title()
            self.update_file_info()
            self.statusBar().showMessage(f'Loaded {fileName}', 2000)
            self.add_to_recent_files(fileName)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load file: {str(e)}")

    def save_file(self):
        """
        Save the current file.
        If file has no name, prompts for save location.

        Returns:
            bool: True if save was successful, False otherwise
        """
        if self.current_file:
            return self.save_file_as(self.current_file)
        return self.save_file_as()

    def save_file_as(self, fileName=None):
        """
        Save the current file with a new name.

        Args:
            fileName: Optional path to save to. If None, shows save dialog.

        Returns:
            bool: True if save was successful, False otherwise
        """
        if not fileName:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(
                self, "Save Verilog File", "",
                "Verilog Files (*.v *.sv);;All Files (*)", options=options)
        if fileName:
            try:
                with open(fileName, 'w') as f:
                    f.write(self.editor.toPlainText())
                self.current_file = fileName
                self.editor.document().setModified(False)
                self.update_title()
                self.update_file_info()
                self.statusBar().showMessage(f'Saved {fileName}', 2000)
                self.add_to_recent_files(fileName)
                return True
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
        return False

    def maybe_save(self):
        """
        Check if current file needs saving and prompt user if needed.

        Returns:
            bool: True if operation can proceed, False if cancelled
        """
        if not self.editor.document().isModified():
            return True

        ret = QMessageBox.warning(self, "Matcha",
                                  "The document has been modified.\nDo you want to save your changes?",
                                  QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

        if ret == QMessageBox.Save:
            return self.save_file()
        elif ret == QMessageBox.Cancel:
            return False
        return True

    def update_title(self):
        """
        Update window title to reflect current file and modification state.
        Format: "Matcha - [filename][*]"
        """
        title = "Matcha - "
        if self.current_file:
            title += QFileInfo(self.current_file).fileName()
        else:
            title += "Untitled"
        if self.editor.document().isModified():
            title += "*"
        self.setWindowTitle(title)

    def update_file_info(self):
        """
        Update file information display in status bar.
        Shows filename and path for current file.
        """
        if self.current_file:
            file_info = QFileInfo(self.current_file)
            self.file_info_label.setText(f"{file_info.fileName()} - {file_info.path()}")
        else:
            self.file_info_label.setText("No File")

    def update_cursor_position(self):
        """
        Update cursor position display in status bar.
        Shows current line and column numbers (1-based).
        """
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.cursor_position_label.setText(f"Line: {line}, Column: {column}")

    def show_search(self):
        """
        Show the search/replace dock widget and focus search input.
        """
        self.search_dock.show()
        self.search_widget.focusSearchInput()

    def format_code(self):
        """
        Format the current Verilog code using configured formatter.
        """
        try:
            cursor = self.editor.textCursor()
            cursor.beginEditBlock()  # Group formatting as single undo operation

            self.editor.format_verilog()

            cursor.endEditBlock()
            self.statusBar().showMessage('Code formatted successfully', 2000)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not format code: {str(e)}")

    def add_to_recent_files(self, fileName):
        """
        Add a file to the recent files list in application settings.
        Maintains a list of up to 10 most recently accessed files.

        Args:
            fileName: Path of file to add to recent list
        """
        settings = QSettings('Matcha', 'RecentFiles')
        files = settings.value('recentFileList', [])

        # Remove if exists and add to front
        if fileName in files:
            files.remove(fileName)
        files.insert(0, fileName)
        del files[10:]  # Keep only 10 most recent

        settings.setValue('recentFileList', files)

    def load_settings(self):
        """
        Load saved application settings.
        Restores window geometry and state from previous session.
        """
        settings = QSettings('Matcha', 'EditorWindow')

        # Restore window geometry (size and position)
        geometry = settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)

        # Restore window state (dock positions, toolbar positions, etc.)
        state = settings.value('windowState')
        if state:
            self.restoreState(state)

    def closeEvent(self, event):
        """
        Handle application close event.
        Prompts to save unsaved changes and saves window state.

        Args:
            event: QCloseEvent to accept or ignore based on user action
        """
        if self.maybe_save():
            # Save window state and geometry for next session
            settings = QSettings('Matcha', 'EditorWindow')
            settings.setValue('geometry', self.saveGeometry())
            settings.setValue('windowState', self.saveState())
            event.accept()
        else:
            event.ignore()  # Cancel close if user cancels save