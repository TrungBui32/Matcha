# config.py

class EditorConfig:
    """
    Main configuration class for the Verilog editor.
    Contains all settings related to appearance, behavior, and functionality.
    """

    def __init__(self):
        # Editor settings - Basic editor appearance and behavior configuration
        self.editor = {
            'font_family': 'Consolas',  # Monospace font optimized for coding
            'font_size': 11,  # Default font size in points
            'tab_size': 4,  # Number of spaces for each tab
            'auto_indent': True,  # Automatically indent new lines
            'line_numbers': True,  # Show line numbers in the gutter
            'highlight_current_line': True,  # Highlight the line where cursor is
            'show_whitespace': False,  # Show whitespace characters
            'word_wrap': False,  # Wrap long lines to window width
            'auto_brackets': True  # Automatically complete brackets/parentheses
        }

        # Theme colors - VSCode-like dark theme for syntax highlighting and UI elements
        self.theme = {
            # Base colors for the editor interface
            'background': "#1E1E1E",  # Main editor background
            'foreground': "#D4D4D4",  # Default text color
            'current_line': "#282828",  # Background color of current line
            'selection': "#264F78",  # Background color of selected text

            # Syntax highlighting colors for different Verilog elements
            'module_keyword': "#4EC9B0",  # Color for module-related keywords
            'module_name': "#9CDCFE",  # Color for module names in declarations
            'instance_name': "#4FC1FF",  # Color for module instance names
            'keywords': "#569CD6",  # Color for general Verilog keywords
            'types': "#4EC9B0",  # Color for data type declarations
            'storage': "#569CD6",  # Color for storage modifiers
            'special_keywords': "#C586C0",  # Color for edge triggers and special terms
            'operators': "#D4D4D4",  # Color for operators and symbols
            'numbers': "#B5CEA8",  # Color for numerical values
            'parameters': "#4FC1FF",  # Color for parameter declarations
            'strings': "#CE9178",  # Color for string literals
            'comments': "#608B4E",  # Color for all types of comments
            'ports': "#9CDCFE",  # Color for port declarations

            # UI element colors for editor components
            'line_numbers': "#858585",  # Color of line number text
            'line_number_bg': "#1E1E1E",  # Background color of line number area
            'fold_marker': "#D4D4D4",  # Color of code folding indicators
            'indent_guide': "#404040",  # Color of indentation guide lines
            'scrollbar': "#424242",  # Color of scrollbar
            'scrollbar_hover': "#4E4E4E",  # Color of scrollbar when hovered
            'matching_bracket': "#646464",  # Color for matching bracket highlights

            # Status and diagnostic colors
            'error': "#F14C4C",  # Color for error indicators
            'warning': "#CCA700",  # Color for warning indicators
            'info': "#3794FF",  # Color for information indicators

            # Version control and diff colors
            'added': "#587C0C",  # Color for added lines in diff
            'modified': "#1B81A8",  # Color for modified lines in diff
            'deleted': "#94151B",  # Color for deleted lines in diff

            # Search highlighting colors
            'find_match': "#515C6A",  # Color for found search matches
            'find_match_active': "#613214"  # Color for currently selected match
        }

        # Formatter settings - Code formatting and style preferences
        self.formatting = {
            'use_tabs': True,  # Use tabs instead of spaces
            'tab_size': 4,  # Size of tabs in spaces
            'spaces_around_operators': True,  # Add spaces around operators
            'spaces_within_parentheses': False,  # No spaces inside parentheses
            'align_port_definitions': True,  # Align port definitions vertically
            'align_assignments': True,  # Align consecutive assignments
            'preserve_blank_lines': True,  # Keep user-added blank lines
            'max_blank_lines': 2,  # Maximum consecutive blank lines
            'indent_case_statements': True,  # Indent inside case blocks
            'line_length_limit': 120,  # Maximum characters per line
            'always_expand_module_ports': True  # One port per line in declarations
        }

        # Keyboard shortcuts - Mapping of editor actions to key combinations
        self.keybindings = {
            'format': 'Ctrl+Shift+F',  # Format current document
            'save': 'Ctrl+S',  # Save current file
            'save_as': 'Ctrl+Shift+S',  # Save file with new name
            'new': 'Ctrl+N',  # Create new file
            'open': 'Ctrl+O',  # Open existing file
            'find': 'Ctrl+F',  # Open find dialog
            'replace': 'Ctrl+H',  # Open find and replace dialog
            'goto_line': 'Ctrl+G',  # Jump to specific line
            'comment': 'Ctrl+/',  # Toggle line comment
            'fold': 'Ctrl+Shift+[',  # Collapse code region
            'unfold': 'Ctrl+Shift+]',  # Expand code region
            'indent': 'Tab',  # Increase indentation
            'unindent': 'Shift+Tab'  # Decrease indentation
        }

        # Verilog-specific settings - Language-specific features and syntax
        self.verilog = {
            # Keyword lists for syntax highlighting
            'module_keywords': [
                'module', 'endmodule', 'begin', 'end',
                'function', 'endfunction', 'task', 'endtask'
            ],
            'conditional_keywords': [
                'if', 'else', 'case', 'endcase', 'default'
            ],
            'loop_keywords': [
                'for', 'while', 'repeat', 'forever'
            ],
            'type_keywords': [
                'wire', 'reg', 'integer', 'real', 'time',
                'realtime', 'parameter', 'localparam'
            ],
            'port_keywords': [
                'input', 'output', 'inout'
            ],
            'edge_keywords': [
                'posedge', 'negedge'
            ],

            # Auto-completion configuration
            'enable_autocomplete': True,  # Enable code completion
            'autocomplete_delay': 500,  # Delay before showing suggestions (ms)
            'min_chars_for_completion': 2,  # Min characters to trigger completion

            # Predefined code snippets for common constructs
            'snippets': {
                'always': 'always @(posedge clk or posedge rst) begin\n\tend',
                'module': 'module ${1:name} (\n\t${2:ports}\n);\n\nendmodule',
                'if': 'if (${1:condition}) begin\n\t${2}\nend',
                'case': 'case (${1:expression})\n\t${2}\nendcase'
            }
        }

        # File handling settings - File management and backup configuration
        self.file = {
            'default_extension': '.v',  # Default file extension
            'backup_enabled': True,  # Enable automatic backups
            'backup_directory': '.backup',  # Directory for backup files
            'auto_save': True,  # Enable automatic saving
            'auto_save_interval': 300,  # Time between auto-saves (seconds)
            'file_associations': {  # Map file extensions to languages
                '.v': 'Verilog',
                '.sv': 'SystemVerilog'
            }
        }