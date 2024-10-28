import re


def format_verilog(text):
    """
    Format Verilog code with proper indentation and alignment.
    Handles module declarations, port lists, begin/end blocks, and comments.

    Args:
        text: String containing unformatted Verilog code

    Returns:
        str: Formatted Verilog code with consistent indentation and spacing
    """
    # Split input into lines for processing
    lines = text.split('\n')
    formatted_lines = []
    indent_level = 0  # Track current indentation level
    in_module = False  # Track if we're inside a module declaration

    # Define keywords that affect indentation levels
    indent_keywords = ['begin']  # Keywords that increase indentation
    unindent_keywords = ['end', 'endcase', 'endfunction', 'endtask']  # Keywords that decrease indentation

    # Process each line of code
    for i, line in enumerate(lines):
        # Handle empty lines
        if not line.strip():
            # Preserve module-level indentation for empty lines within modules
            formatted_lines.append('\t' if in_module else '')
            continue

        # Split line into code and comment parts
        # Preserve comments while formatting code
        code_part = line
        comment_part = ''
        if '//' in line:
            parts = line.split('//', 1)
            code_part = parts[0]
            comment_part = '//' + parts[1]

        # Remove leading/trailing whitespace from code
        stripped_code = code_part.strip()

        # Handle module declaration start
        if stripped_code.startswith('module'):
            in_module = True
            formatted_lines.append(stripped_code)
            continue

        # Handle module declaration end
        if stripped_code == 'endmodule':
            in_module = False
            formatted_lines.append(stripped_code)  # endmodule is never indented
            continue

        # Adjust indentation level for unindenting keywords
        if any(stripped_code.startswith(keyword) for keyword in unindent_keywords):
            indent_level = max(0, indent_level - 1)

        # Special handling for else statements
        # Reduce indent level to match the corresponding if statement
        if stripped_code.startswith('else'):
            indent_level = max(0, indent_level - 1)

        # Calculate proper indentation
        indent = '\t' * indent_level
        # Add extra indentation for module contents
        if in_module and not stripped_code.startswith('endmodule'):
            indent = '\t' + indent

        # Combine indentation with code
        formatted_line = indent + stripped_code

        # Handle comment restoration
        if comment_part:
            if in_module:
                # Inside modules, align comments with tabs
                formatted_line = formatted_line.rstrip() + '\t' + comment_part.strip()
            else:
                # Outside modules, keep comments close to code
                formatted_line = stripped_code.rstrip() + comment_part.strip()

        formatted_lines.append(formatted_line)

        # Check for keywords that increase indentation
        if any(keyword in stripped_code for keyword in indent_keywords):
            indent_level += 1

    # Join formatted lines back into text
    formatted_text = '\n'.join(formatted_lines)

    def format_module_ports(match):
        """
        Format module port declarations with proper alignment and indentation.
        Helper function for regex substitution.

        Args:
            match: Regex match object containing module name and port list

        Returns:
            str: Formatted module declaration with aligned ports
        """
        module_name = match.group(1)  # Extract module name
        ports = match.group(2)  # Extract port list

        # Format each port on its own line with indentation
        port_lines = ['\t' + port.strip() for port in ports.split(',')]

        # Join ports with commas and newlines
        formatted_ports = ',\n'.join(port_lines)

        # Reconstruct module declaration
        return f"module {module_name} (\n{formatted_ports}\n);"

    # Apply module port formatting using regex
    # Matches module declarations and captures name and port list
    formatted_text = re.sub(
        r'module\s+(\w+)\s*\(([\s\S]*?)\);',
        format_module_ports,
        formatted_text
    )

    return formatted_text