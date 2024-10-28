# project_explorer.py
from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import QDir


class ProjectExplorer(QTreeView):
    """
    A file system explorer widget specifically designed for HDL projects.
    Displays a tree view of Verilog (*.v) and SystemVerilog (*.sv) files,
    allowing easy navigation and file selection within a project directory.

    Inherits from QTreeView to provide a hierarchical view of the file system.
    """

    def __init__(self, parent=None):
        """
        Initialize the project explorer widget.

        Args:
            parent: Parent widget that will handle file opening requests.
                   Must implement a load_file(path) method.
        """
        super().__init__(parent)
        self.parent = parent  # Store parent reference for file opening callbacks
        self.setup_model()  # Initialize the file system model

    def setup_model(self):
        """
        Configure the file system model and view settings.

        Sets up:
        - File system model with HDL file filters
        - Root directory path
        - Visible columns
        - Click handling
        """
        # Create and configure the file system model
        self.model = QFileSystemModel()
        # Set the root directory to start browsing from
        self.model.setRootPath(QDir.currentPath())

        # Configure file filters to show only Verilog files
        self.model.setNameFilters(['*.v', '*.sv'])  # Show only .v and .sv files
        self.model.setNameFilterDisables(False)  # Hide (rather than disable) non-matching files

        # Connect model to view and set initial root path
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QDir.currentPath()))

        # Hide all columns except the file name column
        # This removes size, type, and date modified columns
        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)

        # Connect file selection handler
        self.clicked.connect(self.on_file_clicked)

    def on_file_clicked(self, index):
        """
        Handle file selection in the project explorer.

        When a file is clicked, requests the parent widget to load it.
        Ignores clicks on directories.

        Args:
            index: QModelIndex of the clicked item in the tree view
        """
        path = self.model.filePath(index)
        if self.model.isDir(index):
            return  # Ignore directory clicks
        self.parent.load_file(path)  # Request parent to load the selected file

    def set_root_path(self, path):
        """
        Change the root directory displayed in the project explorer.

        Args:
            path: New root directory path to display
        """
        # Update both the model's root path and the view's root index
        self.setRootIndex(self.model.setRootPath(path))