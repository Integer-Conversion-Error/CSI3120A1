import os
from typing import Union, List, Optional

#from sklearn import tree



alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
funky_chars = ["(", ")", ".", "\\"]
all_valid_chars = var_chars + funky_chars
avc = var_chars + ["\\"]
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"

recursionLevel = 0
parCount = 0
tokenArr = []
invalidFlag = False
errorMsg = []

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
            node = self.root  

        print("\t" * level + str(node.elem))

        for child in node.children:
            self.print_tree(child, level + 1)

def findLastParen(s):
    id = s.rfind(")")
    if id == -1:
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
            opening -= 1
        elif s[x] == ")":
            return x
        x += 1

    return False

def findFirstNonSpace(s):
    for i, char in enumerate(s):
        if char != ' ':
            return i
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

def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with an alphabetic character,
    contains only alphabetic characters and digits, and has no spaces.
    Returns False otherwise.
    """
    if len(s) == 0: #empty string
        return False  

    if s[0] not in alphabet_chars: # nonalpha first char
        return False

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
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<var>:  \t" + s[firstNonSpaceIndex:])
    if is_valid_var_name(s):
        return s
    for x in range(firstNonSpaceIndex,len(s)):
        if is_valid_var_name(s[:x]):
            for y in range(x,len(s) + 1):
                if is_valid_var_name(s[:y-1]) and not is_valid_var_name(s[x:y]):
                    return s[:y-1] + "_"+ expr(s[y-1:])
    print("Outside of VAR block! ")
    return s 

def bool_var(s):
    if is_valid_var_name(s):
        return True
    for x in range(len(s)):
        if is_valid_var_name(s[:x]):
            for y in range(x,len(s) + 1):
                if is_valid_var_name(s[0:y-1]) and not is_valid_var_name(s[x:y]):
                    return True
    return False 

def l_expr(s): # <lambda_expr>::= '\' <var> '.' <expr> | '\' <var> <paren_expr> | '\' <var> <expr>
    global errorMsg
    #print("<l_expr>: \t" + s[findFirstNonSpace(s):])
    for x in range(len(s)):
        if s[x] == "\\": ## finding '\'
            endOfVar = var_idx(s[x+1:len(s)]) + x + 1 ## finding <var> 
            if endOfVar != False : 
                currentVar = s[x+1:x+endOfVar+1]
                if bool_var(currentVar) and expr(s[x+endOfVar+1:]) != "":
                    return  "\_" + currentVar +"_"+expr(s[x+endOfVar+1:]) ## recursing to <expr> add \?
                if not bool_var(currentVar):
                    ermesg = str("Expected variable in lambda expression at position" + str(x + 1) + ", Recieved:" + currentVar + ": " + s)
                    errorMsg.append(ermesg)
                    return "" #False
                if expr(s[x+endOfVar+1:]) == "": #not !=
                    ermesg = str("Missing expression in lambda expression at position " + str(x + 1)+ ": " + s)
                    errorMsg.append(ermesg)
                    return "" # False                             
            else: 
                ermesg = "Couldn't find variable in lambda expression statement "
                errorMsg.append(ermesg)
                return "" # L_False
        elif s[x] == " ":
            continue
        else:
            errorMsg+= "Expected '\\', got" + s[x] ## at position x
            return ""     #L_False
        
def bool_l_expr(s): # <lambda_expr>::= '\' <var> '.' <expr> | '\' <var> <paren_expr> 
    global errorMsg
    for x in range(len(s)):
        if s[x] == "\\": ## finding '\'
            endOfVar = var_idx(s[x+1:len(s)]) + x + 1 ## finding <var> 
            if endOfVar != False :
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
    global errorMsg
    #print("<p_expr>: \t" + s[findFirstNonSpace(s):])
    firstParen = findFirstParen(s) ## means we have left association
    for x in range(len(s)):
        if firstParen == False:
            ermesg = 'Missing end bracket' #at position ' + str(len(s))
            errorMsg.append(ermesg)
            return ""
        if s[x] == "(" and firstParen != False :
            if is_leaf(s[x+1:firstParen]):
                return "(_" + var(s[x+1:firstParen]) + "_)" + expr(s[firstParen + 1:]) ## (a)(b)(c)(d)
            elif expr(s[x+1:firstParen]) != "":
                return "(_" + expr(s[x+1:firstParen]) + "_)" + expr(s[firstParen+1:]) ## (a (b)) (bcd)
            elif expr(s[x+1:firstParen]) == "":
                ermesg = 'Expected expression in parantheses' #at ' + str(x+1)
                errorMsg.append(ermesg)
                return ""
    ermesg ="<p_expr> is returning nothing! input: " + s
    errorMsg.append(ermesg)
    return "" ## need to handle this ?

def bool_p_expr(s):
    firstNonSpaceIndex = findFirstNonSpace(s)
    #print("<bool_p_expr>: \t" + s[firstNonSpaceIndex:])
    lastParen = findLastParen(s)
    if s == "()": 
        return False 
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
    if s == "":
        return False
    return True

def expr(s):
    #print("<expr>: \t" + s)
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
                errorMsg.append("Missing closing parentheses ")
                return ""
            else:
                errorMsg.append("Invalid parantheses expression: "+s)
                return ""
        elif s[x] == " " or s[x] == ")":
            return expr(s[x+1:])
        elif s[x] in alphabet_chars:
            if bool_var(s[x:]):
                return var(s[x:])
            elif bool_var(s):
                return s
            else:
                return ""
        elif s[x] not in all_valid_chars:
            ermesg = 'Invalid character ' + s[x] +' in ' + s
            errorMsg.append(ermesg)
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
    global errorMsg
    s = handleAbstraction(s_)
    s_despaced = ""
    r_despaced = ""
    recurring_stuff = expr(s)
    if recurring_stuff == False:
        tokenArr = False
        return tokenArr
    recurring_stuff = recurring_stuff.replace(")(",")_(")

    for item in s.split(" "):
        s_despaced += item

    for item in recurring_stuff.split("_"):
        if item != "" and item != " ":
            r_despaced += item
    r_despaced = r_despaced.replace(" ","")
    if s_despaced != r_despaced:
        tokenArr = False
        #print("\nERROR - PARSE MISMATCH: ",s,s_despaced,r_despaced) ## comment this out!
        for msg in errorMsg:
            print(msg)
        print("\n") ## make into for loop to print individual error msgs
    
    elif recurring_stuff != "":
        tokenArr = recurring_stuff.split("_") 
        
        
    else:
        tokenArr = False
    errorMsg = []         
    return tokenArr

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


# This function finds the most outer bracket for a string list
def findLastBracket(lst):
    # Iterate through the list in reverse order
    for i in range(len(lst) - 1, -1, -1):
        # Check if the string contains a closing parenthesis
        if ')' in lst[i]:
            # Find the index of the last closing parenthesis in the string
            return i
    # Return -1 if no closing parenthesis is found
    return -1





# This function recursivly builds a tree from a string list "tokens"
def build_parse_tree_rec(tokens: List[str], node: Optional[Node] = None) -> Node:
    """
    An inner recursive inner function to build a parse tree
    :param tokens: A list of token strings
    :param node: A Node object
    :return: a node with children whose tokens are variables, parenthesis, slashes, or the inner part of an expression
    """
    
    if(len(tokens) == 1):
        return Node(tokens)
    
    # If there is no root node
    elif not node:
        node = build_parse_tree_rec(tokens, Node(tokens))

    else:
        index = 0
        while(index < len(tokens)):

            # If the token is a variable name with a length equal to 1
            if len(tokens[index]) == 1 and tokens[0] in alphabet_chars: 
                node.add_child_node(Node(tokens[index]))
                index = index + 1
                
            # If the token is a variable name with a length greater than 1
            elif len(tokens[index]) > 1:                           
                node.add_child_node(Node(tokens[index]))
                index = index + 1
                
            # If the token is a opening bracket
            elif tokens[index] == "(":
                closingBracketIndex = findLastBracket(tokens)
                # If a closing bracket is not found
                if closingBracketIndex == -1:
                    print("No closing bracket found")
                    print(tokens)
                else:
                    node.add_child_node(Node(tokens[index]))
                    node.add_child_node(build_parse_tree_rec(tokens[index + 1: closingBracketIndex]))
                    node.add_child_node(Node(tokens[closingBracketIndex]))  
                    index = closingBracketIndex + 1
                                     
            # If the token is a lambda sign("\")
            elif tokens[0] == "\\":
                node.add_child_node(Node(tokens[index]))
                # Adding variable that goes along with lambda
                index = index + 1
                node.add_child_node(Node(tokens[index]))
                index = index + 1
            
            else:
                print("Token " + tokens[index] + "not accounted for in if statements")
                print(tokens)
    
    return node

def build_parse_tree(tokens: List[str]) -> ParseTree:
    """
    Build a parse tree from a list of tokens
    :param tokens: List of tokens
    :return: parse tree
    """
    pt = ParseTree(build_parse_tree_rec(tokens))
    return pt


if __name__ == "__main__":

    string = "\_x_(_\_y_(_x_y_)_)"
    newLst = string.rsplit("_")
    
    #tokenTree = build_parse_tree(newLst)
    #tokenTree.print_tree()
    
    # print("\n\nChecking valid examples...")
    # read_lines_from_txt_check_validity(valid_examples_fp)
    # #read_lines_from_txt_output_parse_tree(valid_examples_fp)

    # print("Checking invalid examples...")
    # read_lines_from_txt_check_validity(invalid_examples_fp)