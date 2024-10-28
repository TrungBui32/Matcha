from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize


class LineNumberArea(QWidget):
    """
    A custom widget that displays line numbers alongside the text editor.
    This widget is designed to be a child of the editor and manages its own
    painting and sizing based on the editor's content.

    The actual painting logic is delegated to the editor to ensure proper
    synchronization with the editor's content and scrolling position.
    """

    def __init__(self, editor):
        """
        Initialize the line number area widget.

        Args:
            editor: The parent text editor widget that this line number area
                   will be attached to. The editor must implement lineNumberAreaWidth()
                   and lineNumberAreaPaintEvent() methods.
        """
        super().__init__(editor)
        self.editor = editor  # Store reference to parent editor for size and paint calculations

    def sizeHint(self):
        """
        Provide the recommended size for the line number area.

        The width is calculated by the editor based on the number of digits
        needed for the highest line number. The height is managed automatically
        by the editor's layout.

        Returns:
            QSize: Recommended size with calculated width and unconstrained height (0)
        """
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        """
        Handle the painting of line numbers.

        Delegates the actual painting to the editor to ensure proper synchronization
        with the editor's content, scrolling, and viewport transformations.

        Args:
            event: QPaintEvent containing the region that needs to be repainted
        """
        self.editor.lineNumberAreaPaintEvent(event)