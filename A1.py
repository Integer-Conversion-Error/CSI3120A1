import os
from typing import Union, List, Optional



alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
funky_chars = ["(", ")", ".", "\\"]
all_valid_chars = var_chars + funky_chars
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]: # type: ignore
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """

    with open(fp, 'r') as file:

        lines = [line.strip() for line in file.readlines()]
        
    return lines


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """


    if s and (s[0] in alphabet_chars or s[0] == '_'): ##if s and (s[0].isalpha() or s[0] == '_') and s.isidentifier():
        return True
    return False


class Node:
    """
    Nodes in a parse tree
    Attributes:
        elem: a list of strings
        children: a list of child nodes
    """
    def __init__(self, elem: List[str] = None):
        self.elem = elem
        self.children = []


    def add_child_node(self, node: 'Node') -> None:
        self.children.append(node)


class ParseTree:
    """
    A full parse tree, with nodes
    Attributes:
        root: the root of the tree
    """
    def __init__(self, root):
        self.root = root

    def print_tree(self, node: Optional[Node] = None, level: int = 0) -> None:
        if node is None:
            node = self.root  # Start from the root if no node is passed

        # Print the node's elem at the current level, indented based on the level
        print("\t" * level + str(node.elem))

        # Recursively print all child nodes, increasing the level for indentation
        for child in node.children:
            self.print_tree(child, level + 1)



def parse_tokens(s_: str, association_type: Optional[str] = None) -> Union[List[str], bool]:
    """
    Gets the final tokens for valid strings as a list of strings, only for valid syntax,
    where tokens are (no whitespace included)
    \\ values for lambdas
    valid variable names
    opening and closing parenthesis
    Note that dots are replaced with corresponding parenthesis

    :param s_: the input string
    :param association_type: If not None, add brackets to make expressions non-ambiguous
    :return: A List of tokens (strings) if a valid input, otherwise False
    """
    ##is_valid_var_name(s: str) 
    openP = 0
    closedP = 0
    abstractionCount = 0
    lambdaFlag = 0
    proto_token = ""
    s = s_[:]  #  Don't modify the original input string
    post_tokens = []
    pre_tokens = s.split(" ")
    for pre_token in pre_tokens:
        for char_token in pre_token:
            if char_token == "(": ## Parentheses Case 1
                post_tokens.append(char_token)
            elif char_token == ")": ## Parentheses Case 2
                post_tokens.append(char_token)
            elif char_token == "\\": ## Lambda Case
                post_tokens.append(char_token) 
                lambdaFlag += 1
            elif char_token in var_chars or char_token == "_": ## Variable Case
                proto_token += char_token
            elif char_token == ".":
                post_tokens.append("(")
                abstractionCount += 1

        if proto_token != "" and lambdaFlag > 0:
            post_tokens.append(proto_token)
            proto_token = ""
            lambdaFlag -= 1
        else:
            print(post_tokens)
            post_tokens = False
            return post_tokens
    
    for x in range(abstractionCount):
        post_tokens.append(")")
    
    for token in post_tokens: 
        print(token)
        if  "(" == token:
            openP += 1
        if ")" == token:
            closedP += 1
    print(post_tokens)
    if closedP != openP:
        print("Parentheses Error! ")
        post_tokens = False
    else: 
        print("Good Parentheses! ")
            

    print("_____________________EndLine___________________________")
    # TODO

    return post_tokens


def read_lines_from_txt_check_validity(fp: [str, os.PathLike]) -> None: # type: ignore
    """
    Reads each line from a .txt file, and then
    parses each string  to yield a tokenized list of strings for printing, joined by _ characters
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param lines: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    valid_lines = []
    #print(parse_tokens(lines[0]))
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            valid_lines.append(l)
            print(f"The tokenized string for input string {l} is {'_'.join(tokens)}")
    if len(valid_lines) == len(lines):
        print(f"All lines are valid")



def read_lines_from_txt_output_parse_tree(fp: [str, os.PathLike]) -> None: # type: ignore
    """
    Reads each line from a .txt file, and then
    parses each string to yield a tokenized output string, to be used in constructing a parse tree. The
    parse tree should call print_tree() to print its content to the console.
    In the case of a non-valid line, the corresponding error message is printed (not necessarily within
    this function, but possibly within the parse_tokens function).
    :param fp: The file path of the lines to parse
    """
    lines = read_lines_from_txt(fp)
    for l in lines:
        tokens = parse_tokens(l)
        if tokens:
            print("\n")
            parse_tree2 = build_parse_tree(tokens)
            parse_tree2.print_tree()


def add_associativity(s_: List[str], association_type: str = "left") -> List[str]:
    """
    :param s_: A list of string tokens
    :param association_type: a string in [`left`, `right`]
    :return: List of strings, with added parenthesis that disambiguates the original expression
    """

    # TODO Optional
    s = s_[:]  # Don't modify original string
    return []




def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """

    #TODO



    return Node()


def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    print("\n\nChecking valid examples...")


    lines = read_lines_from_txt(invalid_examples_fp)
    valid_lines = []
    print(parse_tokens(lines[1]))
    # read_lines_from_txt_check_validity(valid_examples_fp)
    # read_lines_from_txt_output_parse_tree(valid_examples_fp)

    # print("Checking invalid examples...")
    # read_lines_from_txt_check_validity(invalid_examples_fp)
    
    # # Optional
    # print("\n\nAssociation Examples:")
    # sample = ["a", "b", "c"]
    # print("Right association")
    # associated_sample_r = add_associativity(sample, association_type="right")
    # print(associated_sample_r)
    # print("Left association")
    # associated_sample_l = add_associativity(sample, association_type="left")
    # print(associated_sample_l)
