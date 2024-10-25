# import re

# class Node:
#     def __init__(self, node_type, value=None, left=None, right=None):
#         self.node_type = node_type 
#         self.value = value  
#         self.left = left  
#         self.right = right  

#     def __repr__(self):
#         if self.node_type == 'operator':
#             return f"Node(type={self.node_type}, value={self.value}, left={self.left}, right={self.right})"
#         return f"Node(type={self.node_type}, value={self.value})"

# def create_rule(rule_string):
#     tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\(|\))', rule_string)
#     tokens = [token.strip() for token in tokens if token.strip()]
#     return parse_tokens(tokens)

# def parse_tokens(tokens):
#     """Recursively parses tokens into an AST."""
#     if not tokens:
#         return None
    
#     while '(' in tokens:
#         open_idx = tokens.index('(')
#         close_idx = tokens.index(')', open_idx)
#         if close_idx == -1:
#             raise ValueError("Unmatched opening parenthesis found")
#         sub_ast = parse_tokens(tokens[open_idx + 1:close_idx])
#         tokens = tokens[:open_idx] + [sub_ast] + tokens[close_idx + 1:]

#     for operator in ['OR', 'AND']:
#         if operator in tokens:
#             idx = tokens.index(operator)
#             left = parse_tokens(tokens[:idx])
#             right = parse_tokens(tokens[idx + 1:])
#             return Node('operator', operator, left, right)

#     if len(tokens) == 1:
#         condition = tokens[0]
#         field, op, val = re.split(r'(\s*[<>=]+\s*)', condition.strip())
#         return Node('operand', value={'field': field.strip(), 'operator': op.strip(), 'value': int(val.strip())})

#     return None

# def evaluate_rule(ast, data):
#     """Evaluates the AST based on the provided data."""
#     if ast is None:  # Check if AST is None
#         raise ValueError("AST is None")

#     if ast.node_type == 'operand':
#         field = ast.value['field']
#         op = ast.value['operator']
#         val = ast.value['value']
#         if op == '>':
#             return data.get(field) > val
#         elif op == '<':
#             return data.get(field) < val
#         elif op == '=':
#             return data.get(field) == val
#     elif ast.node_type == 'operator':
#         if ast.value == 'AND':
#             return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
#         elif ast.value == 'OR':
#             return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
    
#     return False

# def combine_rules(rules, operator='AND'):
#     """Combines multiple AST rules into a single one using the given operator."""
#     combined_ast = rules[0]
#     for rule in rules[1:]:
#         combined_ast = Node('operator', operator, combined_ast, rule)
#     return combined_ast

# def reconstruct_ast(ast_data):
#     """Convert a dictionary representation of the AST back into Node structure."""
#     if ast_data['node_type'] == 'operand':
#         return Node('operand', value=ast_data['value'])
#     elif ast_data['node_type'] == 'operator':
#         left = reconstruct_ast(ast_data['left'])  
#         right = reconstruct_ast(ast_data['right'])
#         return Node('operator', ast_data['value'], left, right)
#     return None

# # Example usage
# if __name__ == "__main__":
#     try:
#         rule = create_rule("salary > 50000 OR (experience > 5 AND location = 'NY')")
#         print("AST Representation:", rule)

#         sample_data = {
#             'salary': 60000,
#             'experience': 4,
#             'location': 'NY'
#         }
        
#         result = evaluate_rule(rule, sample_data)
#         print("Evaluation Result:", result)

#     except ValueError as ve:
#         print("Error:", ve)


















import re

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type 
        self.value = value  
        self.left = left  
        self.right = right  

    def __repr__(self):
        if self.node_type == 'operator':
            return f"Node(type={self.node_type}, value={self.value}, left={self.left}, right={self.right})"
        return f"Node(type={self.node_type}, value={self.value})"

def create_rule(rule_string):
    tokens = re.split(r'(\s+AND\s+|\s+OR\s+|\(|\))', rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]
    return parse_tokens(tokens)

def parse_tokens(tokens):
    """Recursively parses tokens into an AST."""
    if not tokens:
        return None

    # Handle parentheses
    while '(' in tokens:
        open_idx = tokens.index('(')
        close_idx = tokens.index(')', open_idx)
        if close_idx == -1:
            raise ValueError("Unmatched opening parenthesis found")
        sub_ast = parse_tokens(tokens[open_idx + 1:close_idx])
        tokens = tokens[:open_idx] + [sub_ast] + tokens[close_idx + 1:]

    # Handle OR and AND operators
    for operator in ['OR', 'AND']:
        if operator in tokens:
            idx = tokens.index(operator)
            left = parse_tokens(tokens[:idx])
            right = parse_tokens(tokens[idx + 1:])
            return Node('operator', operator, left, right)

    # Handle operands (conditions)
    if len(tokens) == 1:
        condition = tokens[0]
        field, op, val = re.split(r'(\s*[<>=]+\s*)', condition.strip())
        val = val.strip()

        # Check if val is numeric or a string
        if val.isdigit():
            val = int(val)
        elif (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
            val = val[1:-1]  # Remove the quotes around string values
        else:
            raise ValueError(f"Unsupported value format: {val}")
        
        return Node('operand', value={'field': field.strip(), 'operator': op.strip(), 'value': val})

    return None

def evaluate_rule(ast, data):
    """Evaluates the AST based on the provided data."""
    if ast is None:
        raise ValueError("AST is None")

    if ast.node_type == 'operand':
        field = ast.value['field']
        op = ast.value['operator']
        val = ast.value['value']
        
        if field not in data:
            raise KeyError(f"Field '{field}' not found in the data")

        if op == '>':
            return data.get(field) > val
        elif op == '<':
            return data.get(field) < val
        elif op == '=':
            return data.get(field) == val

    elif ast.node_type == 'operator':
        if ast.value == 'AND':
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == 'OR':
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
    
    return False

def combine_rules(rules, operator='AND'):
    """Combines multiple AST rules into a single one using the given operator."""
    combined_ast = rules[0]
    for rule in rules[1:]:
        combined_ast = Node('operator', operator, combined_ast, rule)
    return combined_ast

def reconstruct_ast(ast_data):
    """Convert a dictionary representation of the AST back into Node structure."""
    if ast_data['node_type'] == 'operand':
        return Node('operand', value=ast_data['value'])
    elif ast_data['node_type'] == 'operator':
        left = reconstruct_ast(ast_data['left'])
        right = reconstruct_ast(ast_data['right'])
        return Node('operator', ast_data['value'], left, right)
    return None

# Example usage
if __name__ == "__main__":
    try:
        rule = create_rule("(age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing') AND (salary > 50000 OR experience > 5)")
        print("AST Representation:", rule)

        sample_data = {
            'age': 35,
            'department': 'Sales',
            'salary': 60000,
            'experience': 4
        }
        
        result = evaluate_rule(rule, sample_data)
        print("Evaluation Result:", result)

    except ValueError as ve:
        print("Error:", ve)
