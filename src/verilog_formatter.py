import re


def format_verilog(text):
    lines = text.split('\n')
    formatted_lines = []
    indent_level = 0
    indent_size = 2

    # Keywords that increase indent
    indent_keywords = ['module', 'begin', 'case', 'function', 'task', 'generate', 'if', 'else']

    # Keywords that decrease indent
    unindent_keywords = ['end', 'endmodule', 'endcase', 'endfunction', 'endtask', 'endgenerate']

    for line in lines:
        # Strip leading and trailing whitespace
        stripped_line = line.strip()

        # Check for unindenting keywords
        if any(line.strip().startswith(keyword) for keyword in unindent_keywords):
            indent_level = max(0, indent_level - 1)

        # Add the formatted line
        if stripped_line:
            formatted_lines.append(' ' * (indent_level * indent_size) + stripped_line)
        else:
            formatted_lines.append('')

        # Check for indenting keywords
        if any(re.search(r'\b' + keyword + r'\b', stripped_line) for keyword in indent_keywords):
            indent_level += 1

    return '\n'.join(formatted_lines)