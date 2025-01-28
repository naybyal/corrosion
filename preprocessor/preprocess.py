import clang.cindex

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