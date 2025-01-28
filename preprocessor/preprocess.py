import clang.cindex
import re

def parse_c_code(file_path):
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path)
    elements = []

    def traverse(node):
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            elements.append(("function", node.spelling, node.extent.start.line, node.extent.end.line))
        elif node.kind == clang.cindex.CursorKind.STRUCT_DECL:
            elements.append(("struct", node.spelling, node.extent.start.line, node.extent.end.line))
        for child in node.get_children():
            traverse(child)

    traverse(translation_unit.cursor)
    return elements

def merge_c_files(main_file):
    with open(main_file, "r") as f:
        content = f.read()
    includes = re.findall(r'#include\s+"(.+?)"', content)
    for include in includes:
        with open(include, "r") as f:
            include_content = f.read()
        content = content.replace(f'#include "{include}"', include_content)
    return content