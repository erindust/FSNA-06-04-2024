import ast

def extract_docstrings(file_path,output_file):
    with open(file_path,"r") as file:
        # read the content of the python program
        file_content = file.read()

    # parse the file content into an AST
    tree = ast.parse(file_content)

    # List to hold all docstrings
    docstring = []

    # Define a visitor class to traverse the AST
    class DocstringVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self,node):
            if ast.get_docstring(node):
                docstring.append(ast.get_docstring(node))
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            if ast.get_docstring(node):
                docstring.append(ast.get_docstring(node))
            self.generic_visit(node)

        def visit_Module(self, node):
            if ast.get_docstring(node):
                docstring.append(ast.get_docstring(node))
            self.generic_visit(node)

    # Create an instance of the visitor and visit the AST
    visitor = DocstringVisitor()
    visitor.visit(tree)

    with open(output_file,"w") as out_file:
        for docstring in docstring:
            out_file.write(docstring + "\n\n")


if __name__ == "__main__":
    input_file_path = "test_flaskr.py"
    output_file_path = "test_flaskr_docstrings.txt"
    extract_docstrings(input_file_path,output_file_path)
    print(f"Docstrings have been written to {output_file_path}")


