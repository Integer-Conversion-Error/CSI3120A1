import os
from typing import Union, List, Optional

# from sklearn import tree

alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
funky_chars = ["(", ")", ".", "\\"]
all_valid_chars = var_chars + funky_chars
avc = var_chars + ["\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"
own_valid_examples_fp = "./own_valid_ex.txt"
own_invalid_examples_fp = "./own_invalid_examples.txt"

recursionLevel = 0
parCount = 0
tokenArr = []
invalidFlag = False
errorMsg = []

def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]: # type: ignore
    """
    Reads lines from a given file path and returns them as a list of strings with leading and trailing
    whitespaces removed.
    :param fp: File path of the .txt file.
    :return: A list of stripped strings, each representing a line from the file.
    """
    with open(fp, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def handleTokens():
    """
    Appends closing parentheses to `tokenArr` until `parCount` reaches zero.
    This function is used when balancing parentheses during token handling.
    """
    while parCount > 0:
        tokenArr.append(")")

class Node:
    """
    Represents a node in a parse tree.
    Attributes:
        elem: A list of strings representing the content of the node.
        children: A list of child nodes representing sub-expressions.
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []

    def add_child_node(self, node: 'Node') -> None:
        """
        Adds a child node to the current node.
        :param node: The child node to be added.
        """
        self.children.append(node)

class ParseTree:
    """
    Represents a full parse tree with nodes.
    Attributes:
        root: The root node of the tree.
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        """
        Recursively prints the parse tree starting from the given node.
        :param node: The current node to print from. Defaults to the root if None.
        :param level: The current level of indentation for pretty printing.
        """
        if node is None:
            node = self.root

        print("\t" * level + str(node.elem))
        for child in node.children:
            self.print_tree(child, level + 1)

def findLastParen(s):
    """
    Finds the index of the last closing parenthesis in the string.
    :param s: The input string.
    :return: The index of the last closing parenthesis, or False if not found.
    """
    id = s.rfind(")")
    if id == -1:
        return False
    else:
        return id

def findFirstParen(s):
    """
    Finds the index of the first unmatched closing parenthesis in the string.
    :param s: The input string.
    :return: The index of the first unmatched closing parenthesis, or False if not found.
    """
    x = 0
    opening = 0
    while x < len(s):
        if s[x] == "(":
            opening += 1
        if s[x] == ")" and opening > 1:
            opening -= 1
        elif s[x] == ")":
            return x
        x += 1
    return False

def findFirstNonSpace(s):
    """
    Finds the index of the first non-space character in a string.
    :param s: The input string.
    :return: The index of the first non-space character, or False if the string is empty.
    """
    for i, char in enumerate(s):
        if char != ' ':
            return i
    return False

def handleAbstraction(s):
    """
    Converts dot notation in a string representing lambda expressions into parentheses for better parsing.
    This function ensures proper nesting of lambda expressions.
    :param s: The input string.
    :return: A transformed string with dot notation replaced by parentheses.
    """
    new_s = ""
    absCount = 0
    for char in s:
        if char == ".":
            new_s += "(" 
            absCount += 1
        else:
            new_s += char
    while absCount > 0: 
        absCount -= 1
        new_s += ")"
    new_s = new_s.replace("( ", "(")
    return new_s

def is_valid_var_name(s: str) -> bool:
    """
    Checks if a given string is a valid variable name.
    A valid variable starts with an alphabetic character and may contain alphanumeric characters.
    :param s: Candidate input variable name.
    :return: True if the variable name is valid, False otherwise.
    """
    if len(s) == 0:
        return False
    if s[0] not in alphabet_chars:
        return False
    for char in s[1:]:
        if char not in var_chars or char == ' ':
            return False
    return True

def var_idx(s: str):
    """
    Finds the index of the last character of a valid variable in a string.
    :param s: The input string.
    :return: The index of the last character of the valid variable, or False if not found.
    """
    last_valid_index = -1
    for i in range(1, len(s) + 1):
        try:
            if is_valid_var_name(s[:i]) or s[i] == " ":
                last_valid_index = i - 1
            else:
                break
        except IndexError:
            break
    if last_valid_index == -1:
        last_valid_index = False
    return last_valid_index

def var(s):
    """
    Parses a valid variable or expression from a string.
    Recursively checks if there are further expressions after the variable.
    :param s: The input string containing the potential variable.
    :return: The parsed variable or expression.
    """
    firstNonSpaceIndex = findFirstNonSpace(s)
    if is_valid_var_name(s):
        return s
    for x in range(firstNonSpaceIndex, len(s)):
        if is_valid_var_name(s[:x]):
            for y in range(x, len(s) + 1):
                if is_valid_var_name(s[:y-1]) and not is_valid_var_name(s[x:y]):
                    return s[:y-1] + "_" + expr(s[y-1:])
    print("Outside of VAR block!")
    return s

def bool_var(s):
    """
    Checks if a string can be parsed as a valid variable.
    :param s: The input string.
    :return: True if the string is a valid variable, False otherwise.
    """
    if is_valid_var_name(s):
        return True
    for x in range(len(s)):
        if is_valid_var_name(s[:x]):
            for y in range(x, len(s) + 1):
                if is_valid_var_name(s[0:y-1]) and not is_valid_var_name(s[x:y]):
                    return True
    return False

def l_expr(s):
    """
    Parses a lambda expression from the input string according to the grammar.
    Handles expressions of the form '\\' <var> '.' <expr>.
    :param s: The input string representing a lambda expression.
    :return: The parsed lambda expression as a string if valid, or an empty string in case of errors.
    """
    global errorMsg
    for x in range(len(s)):
        if s[x] == "\\":  # Finding the '\' (lambda symbol)
            endOfVar = var_idx(s[x+1:len(s)]) + x + 1  # Finding <var>
            if endOfVar != False:
                currentVar = s[x+1:x+endOfVar+1]
                if bool_var(currentVar) and expr(s[x+endOfVar+1:]) != "":
                    return  "\_" + currentVar + "_" + expr(s[x+endOfVar+1:])
                if not bool_var(currentVar):
                    ermesg = "Expected variable in lambda expression at position " + str(x + 1) + ", Received: " + currentVar + ": " + s
                    errorMsg.append(ermesg)
                    return ""  # Handle error gracefully
                if expr(s[x+endOfVar+1:]) == "":
                    ermesg = "Missing expression in lambda expression at position " + str(x + 1) + ": " + s
                    errorMsg.append(ermesg)
                    return ""  # Handle error gracefully
            else:
                ermesg = "Couldn't find variable in lambda expression statement"
                errorMsg.append(ermesg)
                return ""  # Handle error gracefully
        elif s[x] == " ":
            continue
        else:
            errorMsg.append("Expected '\\', got " + s[x])  # Expected a lambda symbol, got something else
            return ""  # Handle error gracefully

def bool_l_expr(s):
    """
    Checks if the given string can be parsed as a valid lambda expression.
    :param s: The input string.
    :return: True if the string represents a valid lambda expression, False otherwise.
    """
    global errorMsg
    for x in range(len(s)):
        if s[x] == "\\":  # Finding '\'
            endOfVar = var_idx(s[x+1:len(s)]) + x + 1  # Finding <var>
            if endOfVar != False:
                currentVar = s[x+1:x+endOfVar+1]
                if bool_var(currentVar):
                    return True
                else:
                    return False
            else:
                return False
        elif s[x] == " ":
            continue
        else:
            return False

def p_expr(s):
    """
    Parses a parenthesized expression from the input string.
    Handles cases such as (a), (a b), (a (b)), etc.
    :param s: The input string.
    :return: The parsed parenthesized expression if valid, or an empty string in case of errors.
    """
    global errorMsg
    firstParen = findFirstParen(s)
    for x in range(len(s)):
        if firstParen == False:
            ermesg = 'Missing end bracket'
            errorMsg.append(ermesg)
            return ""
        if s[x] == "(" and firstParen != False:
            if is_leaf(s[x+1:firstParen]):
                return "(_" + var(s[x+1:firstParen]) + "_)" + expr(s[firstParen + 1:])
            elif expr(s[x+1:firstParen]) != "":
                return "(_" + expr(s[x+1:firstParen]) + "_)" + expr(s[firstParen+1:])
            elif expr(s[x+1:firstParen]) == "":
                ermesg = 'Expected expression in parentheses'
                errorMsg.append(ermesg)
                return ""
    ermesg = "<p_expr> is returning nothing! input: " + s
    errorMsg.append(ermesg)
    return ""

def bool_p_expr(s):
    """
    Checks if the given string can be parsed as a valid parenthesized expression.
    :param s: The input string.
    :return: True if the string represents a valid parenthesized expression, False otherwise.
    """
    firstNonSpaceIndex = findFirstNonSpace(s)
    lastParen = findLastParen(s)
    if s == "()":
        return False
    for x in range(len(s)):
        if s[x] == ".":
            return True
        elif s[x] == "(" and lastParen != False:
            return True
    return False

def is_leaf(s):
    """
    Checks if the given string is a leaf node, meaning it contains no nested expressions.
    :param s: The input string.
    :return: True if the string is a leaf node, False otherwise.
    """
    for char in s:
        if char in funky_chars:
            return False
    if s == "":
        return False
    return True

def expr(s):
    """
    Recursively parses the input string as a general expression.
    Handles lambda expressions, variables, and parenthesized expressions.
    :param s: The input string.
    :return: The parsed expression as a string, or an empty string if the expression is invalid.
    """
    for x in range(len(s)):
        if s[x] == "\\":
            if bool_l_expr(s[x:]):
                return l_expr(s[x:])
            else:
                errorMsg.append("Invalid lambda expression: " + s)
                return ""
        elif s[x] == "(" or s[x] == ".":
            lastp = findLastParen(s) + 1
            if bool_p_expr(s[x:lastp]):
                return p_expr(s[x:lastp])
            elif findLastParen(s) < 0:
                errorMsg.append("Missing closing parentheses")
                return ""
            else:
                errorMsg.append("Invalid parentheses expression: " + s)
                return ""
        elif s[x] == " " or s[x] == ")":
            return expr(s[x+1:])
        # elif s[x] == ".":
        #     checkforperiod = bool_var(s[x+1:])
        #     if not checkforperiod:
        #         return 
        #     return 
        elif s[x] in alphabet_chars:
            if bool_var(s[x:]):
                return var(s[x:])
            elif bool_var(s):
                return s
            else:
                return ""
        elif s[x] not in all_valid_chars:
            ermesg = 'Invalid character ' + s[x] + ' in ' + s
            errorMsg.append(ermesg)
            return ""
        else:
            return ""
    if invalidFlag:
        return False
    return ""

def parse_tokens(s_: str, association_type: Optional[str] = None) -> Union[List[str], bool]:
    """
    Tokenizes and parses the given string based on lambda calculus rules.
    Converts valid strings into a list of tokens, including variables and parentheses.
    :param s_: The input string.
    :param association_type: If not None, add brackets to make expressions non-ambiguous.
    :return: A list of tokens if the input is valid, or False otherwise.
    """
    global errorMsg
    s = handleAbstraction(s_)
    s_despaced = ""
    r_despaced = ""
    recurring_stuff = expr(s)
    if recurring_stuff == False:
        tokenArr = False
        return tokenArr
    recurring_stuff = recurring_stuff.replace(")(", ")_(")

    for item in s.split(" "):
        s_despaced += item

    for item in recurring_stuff.split("_"):
        if item != "" and item != " ":
            r_despaced += item
    r_despaced = r_despaced.replace(" ", "")
    if s_despaced != r_despaced:
        tokenArr = False
        print(s_despaced)
        for msg in errorMsg:
            print(msg)
        print("\n")
    elif recurring_stuff != "":
        tokenArr = recurring_stuff.split("_")
    else:
        tokenArr = False
    errorMsg = []
    return tokenArr

def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None: # type: ignore
    """
    Reads each line from a .txt file, checks its validity, and prints the tokenized output.
    In case of an invalid line, error messages are printed.
    :param fp: The file path of the lines to parse.
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string '{l}' is '{'_'.join(tokens)}'")
    if len(valid_lines) == len(lines):
        print("All lines are valid")

def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None: # type: ignore
    """
    Reads each line from a .txt file, tokenizes it, and constructs a parse tree from the tokens.
    Prints the parse tree using the print_tree() method.
    :param fp: The file path of the lines to parse.
    """
    lines = read_lines_from_txt(fp)
    #print(parse_tokens(lines[0]))
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()

def add_associativity(s_: List[str], association_type: str = "left") -> List[str]:
    """
    Adds parentheses to a list of tokens to make expressions non-ambiguous.
    :param s_: A list of string tokens.
    :param association_type: A string indicating associativity ('left' or 'right').
    :return: A list of strings with added parentheses.
    """
    s = s_[:]
    return []

def matchParantheses(tokens):
    """
    Finds the indices of matching parentheses in a list of tokens.
    :param tokens: A list of tokens.
    :return: A tuple with the indices of the first matching parentheses, or (-1, -1) if not found.
    """
    first_index = -1
    for i, token in enumerate(tokens):
        if token == '(':
            first_index = i
            break

    if first_index == -1:
        return -1, -1

    open_count = 0
    for index in range(first_index, len(tokens)):
        token = tokens[index]
        if token == '(':
            open_count += 1
        elif token == ')':
            open_count -= 1
        if open_count == 0:
            return first_index, index

    return -1, -1

def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    Recursively builds a parse tree from a list of tokens.
    :param tokens: A list of token strings.
    :param node: A Node object.
    :return: A node with children corresponding to the parsed tokens.
    """
    if len(tokens) == 1:
        return Node(tokens)
    elif not node:
        node = build_parse_tree_rec(tokens, Node(tokens))
    else:
        index = 0
        while index < len(tokens):
            if len(tokens[index]) == 1 and tokens[index] in alphabet_chars:
                node.add_child_node(Node(tokens[index]))
                index += 1
            elif len(tokens[index]) > 1:
                node.add_child_node(Node(tokens[index]))
                index += 1
            elif tokens[index] == "(":
                openingBracketIndex, closingBracketIndex = matchParantheses(tokens)
                if closingBracketIndex < index and closingBracketIndex != -1:
                    closingBracketIndex += index
                #if closingBracketIndex == -1:
                    #print(tokens)
                if closingBracketIndex < index:
                    closingBracketIndex += index
                else:
                    node.add_child_node(Node(tokens[index]))
                    node.add_child_node(build_parse_tree_rec(tokens[index + 1: closingBracketIndex]))
                    node.add_child_node(Node(tokens[closingBracketIndex]))
                    index = closingBracketIndex + 1
            elif tokens[index] == "\\":
                node.add_child_node(Node(tokens[index]))
                index += 1
                node.add_child_node(Node(tokens[index]))
                index += 1
            else:
                index += 1
            
    return node

def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Builds a complete parse tree from a list of tokens.
    :param tokens: List of tokens representing the parsed input.
    :return: A ParseTree object with the parsed tokens.
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt

if __name__ == "__main__":
    print("\n\nChecking valid examples...")
    read_lines_from_txt_check_validity(valid_examples_fp)
    read_lines_from_txt_output_parse_tree(valid_examples_fp)

    print("\n\nChecking custom valid examples...")
    read_lines_from_txt_check_validity(own_valid_examples_fp)
    read_lines_from_txt_output_parse_tree(own_valid_examples_fp)

    print("Checking invalid examples...")
    read_lines_from_txt_check_validity(invalid_examples_fp)
    print("Checking own invalid examples...")
    read_lines_from_txt_check_validity(own_invalid_examples_fp)