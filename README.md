# Matcha - Verilog HDL Editor

Matcha is a modern, feature-rich editor specifically designed for Verilog HDL development. It provides a clean, VS Code-inspired interface with powerful editing capabilities tailored for hardware description language development.

## Features

### Code Editing
- Syntax highlighting for Verilog HDL
- Smart auto-indentation
- Line numbering
- Current line highlighting
- Code formatting
- Multiple undo/redo
- Block indentation/unindentation
- Smart line cutting (Ctrl+X without selection)

### Search and Replace
- Find and replace functionality
- Case-sensitive search option
- Whole word matching
- Search result highlighting
- Multi-file search capability
- Search history

### Project Management
- Project explorer for easy file navigation
- File filtering for Verilog (*.v) and SystemVerilog (*.sv) files
- Recent files tracking
- Automatic file backup
- Auto-save functionality

### Interface
- VS Code-inspired dark theme
- Customizable font settings
- Adjustable tab size
- Show/hide whitespace characters
- Word wrap toggle
- Status bar with cursor position and file information

### Configuration
- Customizable editor settings
- Configurable keyboard shortcuts
- Adjustable formatting rules
- Theme customization
- Font selection

## Installation

### Prerequisites
- Python 3.6 or higher
- PyQt5
- Required Python packages (install via pip):
```bash
pip install PyQt5
```

### Running the Application
1. Clone the repository:
```bash
git clone https://github.com/TrungBui32/matcha.git
cd matcha
```

2. Run the editor:
```bash
python main.py
```

## Usage

### Basic Editing
- **New File**: Ctrl+N
- **Open File**: Ctrl+O
- **Save**: Ctrl+S
- **Save As**: Ctrl+Shift+S
- **Find/Replace**: Ctrl+F
- **Format Code**: Ctrl+Shift+F

### Code Navigation
- Use the Project Explorer to browse files
- Line numbers for easy reference
- Quick search with Ctrl+F
- Go to line with Ctrl+G

### Code Formatting
The editor provides automatic code formatting with configurable rules:
- Indentation settings
- Line length limits
- Port alignment
- Comment preservation
- Module structure formatting

### Configuration
Edit the `config.py` file to customize:
```python
class EditorConfig:
    editor = {
        'font_family': 'Consolas',
        'font_size': 11,
        'tab_size': 4,
        'auto_indent': True,
        # ... other settings
    }
```

## File Structure
```
matcha-verilog-editor/
├── main.py                 # Application entry point
├── config.py              # Configuration settings
├── editor_window.py       # Main window implementation
├── verilog_editor.py      # Core editor component
├── verilog_highlighter.py # Syntax highlighting
├── verilog_formatter.py   # Code formatting
├── search_widget.py       # Search functionality
├── project_explorer.py    # File navigation
└── line_number_area.py    # Line numbering widget
```

