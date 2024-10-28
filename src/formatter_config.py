class VerilogFormatterConfig:
    """
    Configuration class for Verilog code formatting.
    Controls how the formatter handles indentation, spacing, alignment, and other formatting rules.
    All settings can be customized through kwargs during initialization.
    """

    def __init__(self, **kwargs):
        """
        Initialize formatter configuration with customizable settings.

        Args:
            **kwargs: Keyword arguments to override default settings.
        """
        # Indentation settings
        self.indent_size = kwargs.get('indent_size', 2)  # Number of spaces per indent level
        self.use_tabs = kwargs.get('use_tabs', False)  # Use tabs instead of spaces for indentation
        self.indent_case = kwargs.get('indent_case', True)  # Indent contents inside case statements

        # Spacing settings - Control whitespace insertion
        self.spaces_around_operators = kwargs.get('spaces_around_operators',
                                                  True)  # Add spaces around operators (e.g., a + b)
        self.spaces_within_parentheses = kwargs.get('spaces_within_parentheses', False)  # Add spaces inside parentheses
        self.spaces_after_comma = kwargs.get('spaces_after_comma', True)  # Add space after commas in lists
        self.align_port_definitions = kwargs.get('align_port_definitions', True)  # Align port definitions in columns

        # Line breaking settings
        self.max_line_length = kwargs.get('max_line_length', 80)  # Maximum characters per line before wrapping
        self.newline_after_begin = kwargs.get('newline_after_begin', True)  # Add newline after 'begin' keyword
        self.newline_after_port = kwargs.get('newline_after_port', True)  # Add newline after each port declaration

        # Comment handling settings
        self.preserve_comment_position = kwargs.get('preserve_comment_position',
                                                    True)  # Keep comments at original position
        self.min_spaces_before_inline_comment = kwargs.get(  # Minimum spaces between code and inline comment
            'min_spaces_before_inline_comment', 2)

        # Code alignment settings
        self.align_assignments = kwargs.get('align_assignments', False)  # Align consecutive assignment operators
        self.align_module_ports = kwargs.get('align_module_ports', True)  # Align module port declarations

        # Keyword formatting
        self.uppercase_keywords = kwargs.get('uppercase_keywords', False)  # Convert keywords to uppercase

        # Keywords that affect indentation levels
        # Keywords that increase indent level for following lines
        self.indent_after_keywords = kwargs.get('indent_after_keywords', [
            'begin', 'case', 'casex', 'casez', 'module', 'function', 'task'
        ])

        # Keywords that decrease indent level for current and following lines
        self.unindent_keywords = kwargs.get('unindent_keywords', [
            'end', 'endcase', 'endmodule', 'endfunction', 'endtask'
        ])

        # Keywords that require special indentation handling
        self.special_indent_keywords = kwargs.get('special_indent_keywords', [
            'else', 'end else'  # These might need different indentation rules
        ])

        # Operator spacing rules
        # Dictionary defining space requirements before and after each operator
        # Tuple format: (space_before, space_after)
        self.operator_spacing = kwargs.get('operator_spacing', {
            '<=': (True, True),  # Non-blocking assignment
            '>=': (True, True),  # Greater than or equal
            '==': (True, True),  # Equality comparison
            '!=': (True, True),  # Inequality comparison
            '&&': (True, True),  # Logical AND
            '||': (True, True),  # Logical OR
            '&': (True, True),  # Bitwise AND
            '|': (True, True),  # Bitwise OR
            '^': (True, True),  # Bitwise XOR
            '+': (True, True),  # Addition
            '-': (True, True),  # Subtraction
            '*': (True, True),  # Multiplication
            '/': (True, True),  # Division
            '=': (True, True),  # Blocking assignment
            '<': (True, True),  # Less than
            '>': (True, True),  # Greater than
        })
