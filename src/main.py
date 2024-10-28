import sys
from PyQt5.QtWidgets import QApplication
from editor_window import EditorWindow
from config import EditorConfig


def main():
    """
    Main entry point for the HDLPad application.
    Initializes the Qt application, sets up configuration,
    creates the main editor window, and starts the event loop.
    """
    # Initialize Qt application with command line arguments
    # This sets up the core Qt framework and enables command line parameter handling
    app = QApplication(sys.argv)

    # Set application name for settings storage and window titles
    # This name is used by QSettings for storing user preferences
    app.setApplicationName("HDLPad")

    # Create default configuration object
    # EditorConfig contains all settings for editor behavior, appearance, and functionality
    config = EditorConfig()

    # Create and initialize main editor window with configuration
    # EditorWindow is the main application window containing the editor and all UI elements
    editor = EditorWindow(config)

    # Display the main window
    # Window will be shown at the position and size specified in saved settings,
    # or at default values for first-time launch
    editor.show()

    # Start the Qt event loop and exit with its return code
    # This begins processing user input and maintains the application until closed
    # app.exec_() returns an exit code which is passed to sys.exit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    """
    Standard Python idiom to ensure the main() function is only called if
    this script is run directly (not imported as a module).

    This allows the script to be both imported and run directly while
    avoiding unintended execution of the main() function.
    """
    main()