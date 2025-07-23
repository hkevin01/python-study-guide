#!/usr/bin/env python3
"""
HTML Code Syntax Fixer
Fixes malformed HTML syntax highlighting and duplicate class attributes
"""

import re
import os
import sys
from pathlib import Path

class HTMLCodeFixer:
    def __init__(self):
        # Define syntax highlighting mappings
        self.syntax_classes = {
            'comment': '#5c6370',
            'string': '#98c379',
            'keyword': '#c678dd',
            'function': '#61afef',
            'number': '#d19a66',
            'operator': '#56b6c2',
            'builtin': '#e06c75',
            'decorator': '#e5c07b'
        }
        
        # Python keywords
        self.keywords = [
            'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except',
            'finally', 'with', 'as', 'import', 'from', 'return', 'yield', 'break',
            'continue', 'pass', 'raise', 'assert', 'lambda', 'and', 'or', 'not',
            'in', 'is', 'True', 'False', 'None', 'self', 'super', 'global', 'nonlocal',
            'async', 'await', 'match', 'case'
        ]
        
        # Built-in functions
        self.builtins = [
            'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict',
            'set', 'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr',
            'setattr', 'delattr', 'open', 'file', 'input', 'sum', 'min', 'max',
            'sorted', 'reversed', 'enumerate', 'zip', 'map', 'filter', 'all', 'any'
        ]

    def fix_duplicate_classes(self, html_content):
        """Fix duplicate class attributes like class=class="py-string">"""
        # Pattern to match duplicate class attributes
        pattern = r'class=class="([^"]+)">([^<]*)'
        
        def replace_duplicate(match):
            class_name = match.group(1)
            content = match.group(2)
            
            # Map old class names to new ones
            class_mapping = {
                'py-comment': 'comment',
                'py-string': 'string',
                'py-keyword': 'keyword',
                'py-function': 'function',
                'py-number': 'number',
                'py-operator': 'operator',
                'py-builtin': 'builtin',
                'py-decorator': 'decorator'
            }
            
            new_class = class_mapping.get(class_name, class_name)
            return f'<span class="{new_class}">{content}</span>'
        
        return re.sub(pattern, replace_duplicate, html_content)

    def highlight_python_code(self, code):
        """Apply proper syntax highlighting to Python code"""
        if not code.strip():
            return code
        
        # Escape HTML entities
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Track what's already highlighted to avoid double highlighting
        highlighted_ranges = []
        
        def add_span(match, class_name, offset=0):
            start = match.start() + offset
            end = match.end() + offset
            # Check if this range is already highlighted
            for r_start, r_end in highlighted_ranges:
                if start >= r_start and end <= r_end:
                    return None
            highlighted_ranges.append((start, end))
            return (start, end, f'<span class="{class_name}">{match.group()}</span>')
        
        replacements = []
        
        # Highlight strings (both single and double quotes, including multi-line)
        string_pattern = r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
        for match in re.finditer(string_pattern, code):
            result = add_span(match, 'string')
            if result:
                replacements.append(result)
        
        # Highlight comments
        comment_pattern = r'#[^\n]*'
        for match in re.finditer(comment_pattern, code):
            result = add_span(match, 'comment')
            if result:
                replacements.append(result)
        
        # Highlight numbers
        number_pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(number_pattern, code):
            result = add_span(match, 'number')
            if result:
                replacements.append(result)
        
        # Highlight decorators
        decorator_pattern = r'@\w+'
        for match in re.finditer(decorator_pattern, code):
            result = add_span(match, 'decorator')
            if result:
                replacements.append(result)
        
        # Highlight keywords
        for keyword in self.keywords:
            pattern = rf'\b{keyword}\b'
            for match in re.finditer(pattern, code):
                result = add_span(match, 'keyword')
                if result:
                    replacements.append(result)
        
        # Highlight built-in functions
        for builtin in self.builtins:
            pattern = rf'\b{builtin}\b(?=\s*\()'
            for match in re.finditer(pattern, code):
                result = add_span(match, 'builtin')
                if result:
                    replacements.append(result)
        
        # Highlight function and class definitions
        func_pattern = r'(?:def|class)\s+(\w+)'
        for match in re.finditer(func_pattern, code):
            # Highlight the function/class name
            name_start = match.start(1)
            name_end = match.end(1)
            result = (name_start, name_end, f'<span class="function">{match.group(1)}</span>')
            replacements.append(result)
        
        # Apply replacements in reverse order to maintain positions
        replacements.sort(key=lambda x: x[0], reverse=True)
        for start, end, replacement in replacements:
            code = code[:start] + replacement + code[end:]
        
        return code

    def fix_pre_code_blocks(self, html_content):
        """Fix all <pre><code> blocks in the HTML"""
        def fix_code_block(match):
            code_content = match.group(1)
            
            # Remove existing span tags to start fresh
            code_content = re.sub(r'<span[^>]*>', '', code_content)
            code_content = re.sub(r'</span>', '', code_content)
            
            # Apply syntax highlighting
            highlighted = self.highlight_python_code(code_content)
            
            return f'<pre><code>{highlighted}</code></pre>'
        
        # Pattern to match pre code blocks
        pattern = r'<pre><code>(.*?)</code></pre>'
        return re.sub(pattern, fix_code_block, html_content, flags=re.DOTALL)

    def generate_css(self):
        """Generate CSS for syntax highlighting"""
        css = """/* Syntax Highlighting */
"""
        for class_name, color in self.syntax_classes.items():
            if class_name == 'comment':
                css += f'.{class_name} {{ color: {color}; font-style: italic; }}\n'
            elif class_name == 'function':
                css += f'.{class_name} {{ color: {color}; font-weight: bold; }}\n'
            else:
                css += f'.{class_name} {{ color: {color}; }}\n'
        
        return css

    def process_file(self, input_file, output_file=None):
        """Process a single HTML file"""
        if output_file is None:
            output_file = input_file.replace('.html', '_fixed.html')
        
        print(f"Processing {input_file}...")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix duplicate class attributes
            content = self.fix_duplicate_classes(content)
            
            # Fix pre code blocks
            content = self.fix_pre_code_blocks(content)
            
            # Update or add CSS
            css = self.generate_css()
            if '<style>' in content:
                # Replace existing syntax highlighting CSS
                content = re.sub(
                    r'/\* Syntax Highlighting \*/.*?(?=/\*|</style>)',
                    css,
                    content,
                    flags=re.DOTALL
                )
            else:
                # Add CSS to head
                content = content.replace('</head>', f'<style>\n{css}</style>\n</head>')
            
            # Write fixed content
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ Fixed HTML saved to {output_file}")
            
            # Generate report
            self.generate_report(input_file, output_file)
            
        except Exception as e:
            print(f"✗ Error processing file: {e}")
            return False
        
        return True

    def generate_report(self, input_file, output_file):
        """Generate a report of changes made"""
        report_file = output_file.replace('.html', '_report.txt')
        
        with open(input_file, 'r', encoding='utf-8') as f:
            original = f.read()
        
        with open(output_file, 'r', encoding='utf-8') as f:
            fixed = f.read()
        
        # Count fixes
        duplicate_fixes = len(re.findall(r'class=class=', original))
        
        report = f"""HTML Code Fix Report
===================
Input File: {input_file}
Output File: {output_file}
Date: {os.path.getmtime(output_file)}

Fixes Applied:
- Duplicate class attributes fixed: {duplicate_fixes}
- Code blocks processed: {len(re.findall(r'<pre><code>', original))}
- File size: {len(original)} → {len(fixed)} bytes

CSS Classes Used:
"""
        
        for class_name in self.syntax_classes:
            count = len(re.findall(f'class="{class_name}"', fixed))
            report += f"- .{class_name}: {count} occurrences\n"
        
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"📊 Report saved to {report_file}")

def main():
    """Main function"""
    fixer = HTMLCodeFixer()
    
    if len(sys.argv) < 2:
        print("Usage: python fix_html_syntax.py <input_file.html> [output_file.html]")
        print("\nExample:")
        print("  python fix_html_syntax.py python-study.html")
        print("  python fix_html_syntax.py python-study.html fixed-study.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)
    
    if fixer.process_file(input_file, output_file):
        print("\n✅ HTML syntax fixing completed successfully!")
    else:
        print("\n❌ HTML syntax fixing failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()