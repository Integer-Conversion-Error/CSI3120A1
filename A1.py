import os
from typing import Union, List, Optional

from sklearn import tree



alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
funky_chars = ["(", ")", ".", "\\"]
all_valid_chars = var_chars + funky_chars
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"

recursionLevel = 0
parCount = 0
tokenArr = []
invalidFlag = False

def read_lines_from_txt(fp: [str, os.PathLike]) -> List[str]: # type: ignore
    """
    :param fp: File path of the .txt file.
    :return: The lines of the file path removing trailing whitespaces
    and newline characters.
    """

    with open(fp, 'r') as file:

        lines = [line.strip() for line in file.readlines()]
        
    return lines


def handleTokens():
    while parCount > 0:
        tokenArr.append(")")


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


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with an alphabetic character,
    contains only alphabetic characters and digits, and has no spaces.
    Returns False otherwise.
    """
    if len(s) == 0:
        return False  # Empty string is not a valid variable name

    # First character must be alphabetic (from alphabet_chars)
    if s[0] not in alphabet_chars:
        return False

    # Remaining characters (if any) must be alphanumeric (from var_chars) and not contain spaces
    for char in s[1:]:
        if char not in var_chars or char == ' ':
            return False

    return True


def var_idx(s: str):
    """
    Find the index of the last character of a valid variable in the string.
    :param s: The input string
    :return: The index of the last character of the valid variable, or -1 if no valid variable is found
    """
    last_valid_index = -1

    # Iterate over the string and check each substring as a potential variable
    for i in range(1, len(s) + 1):
        # Check if the current prefix is a valid variable name
        try:
            if is_valid_var_name(s[:i]) or s[i] == " ":
                #print(s[:i])
                last_valid_index = i - 1  # Update the last valid index
            
            else:
                break  # Stop once the current prefix is not valid
        except IndexError:
            print("No var index found! ")
            break
    if last_valid_index == -1:
        last_valid_index = False
    #print(s[last_valid_index])
    return last_valid_index

## get var to show as recurring string, catch case of (a (b c))
def var(s):
    
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<var>:  \t" + s[firstNonSpaceIndex:])
    if is_valid_var_name(s):
        #print("Valid full string:" + s)
        return s
    for x in range(firstNonSpaceIndex,len(s)):
        if is_valid_var_name(s[:x]):
            #print("S is valid var: ", s[:x], " len(s):", len(s),x)
            for y in range(x,len(s) + 1):
                #print("Theres something happening here...",s[x:y], is_valid_var_name(s[x:y]))
                if is_valid_var_name(s[:y-1]) and not is_valid_var_name(s[x:y]):
                    #print(s[:y-1], s[y-1:])
                    return s[:y-1] + "_"+ expr(s[y-1:])
        #elif is_valid_var_name(s):
            
        #print(s[:x])
    return s # will cause infinite recursion

def bool_var(s):
    #print("<bool_var>:  \t" + s)
    if is_valid_var_name(s):
        return True
    for x in range(len(s)):
        if is_valid_var_name(s[:x]):
            #print("S is valid var: ", s[:x], " len(s):", len(s),x)
            for y in range(x,len(s) + 1):
                #print("Theres something happening here...",s[x:y], is_valid_var_name(s[x:y]))
                if is_valid_var_name(s[0:y-1]) and not is_valid_var_name(s[x:y]):
                    return True
    return False # will cause infinite recursion

def l_expr(s): # <lambda_expr>::= '\' <var> '.' <expr> | '\' <var> <paren_expr> 
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<l_expr>: \t" + s[firstNonSpaceIndex:])
    for x in range(len(s)):
        if s[x] == "\\": ## finding '\'
            endOfVar = var_idx(s[x+1:len(s)]) + x + 1 ## finding <var> 
            #print("Checking this for leafness:",s[x+endOfVar:])
            if endOfVar != False : ##  (bool_l_expr(s[x+1:]) or bool_p_expr(s[x+1:])) or something like this : and not is_leaf(s[x+endOfVar+1:])
                currentVar = s[x+1:x+endOfVar+1]
                #print("what lambda is seeing as var: " +currentVar)

                if bool_var(currentVar) and expr(s[x+endOfVar+1:]) != "":
                    return  "\_" + currentVar +"_"+expr(s[x+endOfVar+1:]) ## recursing to <expr> add \?
                elif not bool_var(currentVar):
                    print("Expected variable in lambda expression at position ",x + 1,", Recieved:", currentVar )
                    return "False"
                elif not expr(s[x+endOfVar+1:]) != "":
                    print("Missing expression in lambda expression at position",x + 1 )
                    return "False"
            #elif endOfVar != False and is_leaf(s[x+endOfVar+1:]):
                
            else: 
                print("Couldn't find variable in lambda expression statement ")
                return "L_False"
        elif s[x] == " ":
            continue
        else:
            print("Expected '\\', got" + s[x]) ## at position x
            return "L_False"    
        
def bool_l_expr(s): # <lambda_expr>::= '\' <var> '.' <expr> | '\' <var> <paren_expr> 
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<l_expr>: \t" + s[firstNonSpaceIndex:])
    for x in range(len(s)):
        if s[x] == "\\": ## finding '\'
            endOfVar = var_idx(s[x+1:len(s)]) + x + 1 ## finding <var> 
            if endOfVar != False :
                currentVar = s[x+1:x+endOfVar+1]
                if bool_var(currentVar):
                    return True
                else:
                    print("Expected variable in lambda expression at position ",x + 1,", Recieved:", currentVar )
                    return False
            else: 
                print("Couldn't find variable in lambda expression statement ")
                return False
        elif s[x] == " ":
            continue
        else:
            print("Expected '\\', got " + s[x]) ## at position x
            return False    
    
def findLastParen(s):
    id = s.rfind(")")
    if id == -1:
        #print("Cant find parenthesis in ", s)
        return False
    else:
        return id
    
def findFirstParen(s):
    x = 0
    opening = 0
    while x < len(s):
        if s[x] == "(":
            opening += 1
        if s[x] == ")" and opening > 1:
            #print(s[x], opening)
            opening -= 1
        elif s[x] == ")":
            return x
        x += 1

    return False

def findFirstNonSpace(s):
    for i, char in enumerate(s):
        if char != ' ':
            return i
    #print('Could\'t find nonspace in string ',s)
    return False

def handleAbstraction(s):
    new_s = ""
    absCount = 0
    for char in s:
        if char ==".":
            new_s += "(" 
            absCount += 1
        else:
            new_s += char
    while absCount > 0: 
        absCount -= 1
        new_s += ")"

    new_s = new_s.replace("( ", "(")
    return new_s


def handleAbstractionBetter(s):
    new_s = ""
    absCount = 0
    for x in range(len(s)):
        if s[x] =="." and s[x+1] == " ":
            new_s += "(" 
            absCount += 1
        else:
            new_s += s[x]
    while absCount > 0: 
        absCount -= 1
        new_s += ")"
    return new_s


def p_expr(s): ##  NEEDS FIXING, CATCH CASE OF PARANTHESES WITH NOTHING IN IT LIKE I DID IN L_EXPR
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<p_expr>: \t" + s[firstNonSpaceIndex:])
    lastParen = findFirstParen(s)
    for x in range(len(s)):
        # if s[x] == "."  and not is_leaf(s[x+1:]):
        #     print("Period at position:", x)
        #     return "(_" + expr(s[x+1:]) + "_)" ## true
        if s[x] == "(" and lastParen != False :
            if is_leaf(s[x+1:lastParen]):
                return "(_" + var(s[x+1:lastParen]) + "_)"+ expr(s[lastParen + 1:]) ## true lastParen + 1
            elif expr(s[x+1:lastParen]) != "":
                return "(_" + expr(s[x+1:lastParen]) + "_)" + expr(s[lastParen+1:]) ## lastParen +1
    print("<p_expr> is returning nothing! input: ", s)   #Expected ")" at (some index) 
    return "P_False" ## need to handle this

def bool_p_expr(s):
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<bool_p_expr>: \t" + s[firstNonSpaceIndex:])
    lastParen = findLastParen(s)
    for x in range(len(s)):
        if s[x] == ".":
            return True ## true
        elif s[x] == "(" and lastParen != False:
            return True ## true
    #print("<p_expr> is returning nothing! input: ", s)    
    return False ## need to handle this

def is_leaf(s):
    for char in s:
        if char in funky_chars:
            return False
    return True

def expr(s):
    #print("<expr>: \t" + s)
    for x in range(len(s)):
        if s[x] == "\\":
            if bool_l_expr(s[x:]):
                return l_expr(s[x:])
            else:
                return ""
        elif s[x] == "(" or s[x] == ".":
            lastp = findLastParen(s) + 1
            if bool_p_expr(s[x:lastp]):
                return p_expr(s[x:lastp])
            else:
                return ""
        elif s[x] == " " or s[x] == ")":
            return expr(s[x+1:])
        elif s[x] in alphabet_chars:
            if bool_var(s[x:]):
                #print(var(s[x:]))
                return var(s[x:])
            elif bool_var(s):
                return s
            else:
                return ""
        else:
            return ""
    if invalidFlag:
        return False

    ## BLANK PARANTHESES CASE??    
    return "" # false


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
    s = handleAbstraction(s_)
    s_despaced = ""
    r_despaced = ""
    #print("Pre-Parsing (and pre-abstraction): ",s_)
    recurring_stuff = expr(s)
    if recurring_stuff == False:
        tokenArr = False
        return tokenArr
    #print("Post-Parsing, Delimited: ",recurring_stuff)

    for item in s.split(" "):
        s_despaced += item

    for item in recurring_stuff.split("_"):
        if item != "" and item != " ":
            r_despaced += item
    r_despaced = r_despaced.replace(" ","")
    #r_despaced = r_despaced.replace(")(", ")_(")
    #print(s_despaced,r_despaced)
    if s_despaced != r_despaced:
        tokenArr = False
        print("ERROR - PARSE MISMATCH: ",s,s_despaced,r_despaced,'\n')
    elif recurring_stuff != "":
        tokenArr = recurring_stuff.split("_") 
        
        
    else:
        tokenArr = False
            
    return tokenArr





# s2 = "\\x( a b)"


# print(parse_tokens(s2))

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
            print(f"The tokenized string for input string \'{l}\' is \'{'_'.join(tokens)}\'")
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
    print(parse_tokens(lines[0]))
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


    # lines = read_lines_from_txt(invalid_examples_fp)
    # valid_lines = []
    # print(parse_tokens("\\ x . a b"))

    # # Sample list
    # my_list = ['a', 'b', 'c', 'd', 'e']

    # # Index of the element to be split
    # index_to_split = 2  # splitting 'c'

    # # The two new elements to insert
    # new_element1 = 'x'
    # new_element2 = 'y'

    # # Perform the split
    # my_list[index_to_split:index_to_split + 1] = [new_element1, new_element2]

    # # Print the updated list
    # print(my_list)

    read_lines_from_txt_check_validity(invalid_examples_fp)
    #read_lines_from_txt_output_parse_tree(valid_examples_fp)

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
