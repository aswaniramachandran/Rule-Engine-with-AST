
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

    def to_dict(self):
        """Convert the Node to a dictionary format for easier serialization."""
        return {
            'node_type': self.node_type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

def create_rule(rule_string):
    """Create an AST from the rule string."""
    if not rule_string:
        raise ValueError("Rule string cannot be empty.")

    tokens = tokenize_rule(rule_string)

    if not tokens:
        raise ValueError("No valid tokens found in the rule string.")

    ast = parse_tokens(tokens)

    if ast is None:
        raise ValueError("Failed to create an AST from the tokens.")

    return ast

def tokenize_rule(rule_string):
    """Tokenize the rule string into logical components."""
    token_pattern = r"(\s+AND\s+|\s+OR\s+|\(|\)|\w+\s*[<>=!]+\s*\"[^\"]*\"|\w+\s*[<>=!]+\s*'[^']*'|\w+\s*[<>=!]+\s*\d+)"
    tokens = re.split(token_pattern, rule_string)
    tokens = [token.strip() for token in tokens if token.strip()]
    return tokens

def parse_tokens(tokens):
    """Recursively parses tokens into an AST."""
    output = []
    operators = []

    def precedence(op):
        if op == 'AND':
            return 2
        if op == 'OR':
            return 1
        return 0

    def apply_operator():
        """Helper function to apply operator and construct AST."""
        if len(output) < 2:
            raise ValueError("Not enough operands to apply operator.")
        
        right = output.pop()
        left = output.pop()
        op = operators.pop()
        output.append(Node('operator', value=op, left=left, right=right))

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == '(':
            operators.append(token)

        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator()
            if operators and operators[-1] == '(':
                operators.pop()  # Remove the '(' from the stack

        elif token in ('AND', 'OR'):
            while operators and precedence(operators[-1]) >= precedence(token):
                apply_operator()
            operators.append(token)

        else:
            match = re.match(r"(\w+)\s*([<>=!]+)\s*(\"[^\"]*\"|'[^']*'|\d+)", token)
            if match:
                field, op, val = match.groups()
                if val.startswith("\"") and val.endswith("\""):
                    val = val.strip("\"")  # Remove double quotes
                elif val.startswith("'") and val.endswith("'"):
                    val = val.strip("'")  # Remove single quotes
                else:
                    val = int(val)  # Convert to int if it's a number
                output.append(Node('operand', value={'field': field, 'operator': op, 'value': val}))
            else:
                raise ValueError(f"Invalid token: {token}")

        # Debug prints
        print(f"Current token: {token}")
        print(f"Operators stack: {operators}")
        print(f"Output stack: {output}")

        i += 1

    while operators:
        apply_operator()

    return output[0] if output else None

def evaluate_rule(ast, data):
    """Evaluate an AST against provided data."""
    if not ast or not data:
        raise ValueError("AST or data cannot be empty.")

    if ast.node_type == 'operand':
        field = ast.value['field']
        op = ast.value['operator']
        val = ast.value['value']
        field_value = data.get(field)

        if field_value is None:
            raise ValueError(f"Missing field '{field}' in provided data.")

        if isinstance(field_value, str) and isinstance(val, str):
            if op == '=':
                return field_value == val
            elif op == '!=':
                return field_value != val
        elif isinstance(field_value, int) and isinstance(val, int):
            if op == '>':
                return field_value > val
            elif op == '<':
                return field_value < val
            elif op == '=':
                return field_value == val
            elif op == '!=':
                return field_value != val
    elif ast.node_type == 'operator':
        if ast.value == 'AND':
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == 'OR':
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)

    return False

def combine_rules(rules):
    """Combine multiple ASTs into a single AST using AND operator."""
    if not rules:
        raise ValueError("No rules provided to combine.")
    
    combined_rule = None
    for rule in rules:
        print(f"Processing rule: {rule}")  # Debugging line
        if rule is not None:
            if combined_rule is None:
                combined_rule = rule
            else:
                combined_rule = Node('operator', 'AND', combined_rule, rule)
        else:
            raise ValueError("Encountered a None rule while combining.")

    print(f"Combined rule: {combined_rule}")  # Debugging line
    return combined_rule

def reconstruct_ast(ast_data):
    """Reconstruct the AST from serialized data."""
    if not ast_data:
        return None

    node_type = ast_data.get('node_type')
    value = ast_data.get('value')
    left = reconstruct_ast(ast_data.get('left'))
    right = reconstruct_ast(ast_data.get('right'))

    return Node(node_type, value=value, left=left, right=right)

