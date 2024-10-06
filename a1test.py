import os
from typing import Union, List, Optional



alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
funky_chars = ["(", ")", ".", "\\"]
all_valid_chars = var_chars + funky_chars
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """


    if s and (s[0] in alphabet_chars or s[0] == '_'): 
        return True
    return False


def is_valid_var_name(s: str) -> bool:
    """
    :param s: Candidate input variable name
    :return: True if the variable name starts with a character,
    and contains only characters and digits. Returns False otherwise.
    """
    if s[0] not in alphabet_chars:
        return False
    else:
        if len(s) == 0:
            #print(s)
            return True
    for char in s:
        if char not in var_chars:
            return False

    return True


def var(s): ## Start from first char, end at last char which a valid var name would end at.
    firstNonVar = 0
    for x in range(len(s)):
        if s[x] in funky_chars:
            firstNonVar = x
    while not is_valid_var_name(s[:firstNonVar]):
        firstNonVar -= 1
        if firstNonVar <= 0:
            return False
        if is_valid_var_name(s[:firstNonVar]):
            return firstNonVar

    return False

    
def l_expr(s): # <lambda_expr>::= '\' <var> '.' <expr> | '\' <var> <paren_expr> 
    print("<l_expr>: \t" + s)
    for x in range(len(s)):
        if s[x] == "\\": ## finding '\'
            endOfVar = var(s[x+1:len(s)]) + x + 1 ## finding <var> 
            if endOfVar != False:
                currentVar = s[x+1:x+endOfVar]
                return "\\" + currentVar + expr(s[x+endOfVar+1:]) ## recursing to <expr>
                
            else: 
                print("Couldn't find variable in lambda expression statement ")
                return False
        elif s[x] == " ":
            continue
        else:
            print("Expected '\\', got" + s[x]) ## at position x
            return False    
    
def findLastParen(s):
    id = s.rfind(")")
    if id == -1:
        print("Cant find parentehsis")
        return False
    else:
        return id

def findFirstNonSpace(s):
    for i, char in enumerate(s):
        if char != ' ':
            return i
    return 0

def p_expr(s):
    firstNonSpaceIndex = findFirstNonSpace(s)
    print("<p_expr>: \t" + s[firstNonSpaceIndex:])
    lastParen = findLastParen(s)
    for x in range(firstNonSpaceIndex,len(s)):
        if s[x] == ".":
            print("Period at position:", x)
            return "." + expr(s[x+1:])
        elif s[x] == "(" and lastParen != False:
            return "(" + expr(s[x+1:lastParen]) + ")"
    print("<p_expr> is returning nothing! input: ", s)    
    return "" ## need to handle this

def expr(s):
    print("<expr>: \t" + s)
    for x in range(len(s)):
        if s[x] == "\\":
            return l_expr(s[x:])
        elif s[x] == "(" or s[x] == ".":
            lastp = findLastParen(s) + 1
            return p_expr(s[x:lastp])
        elif s[x] == " ":
            continue
        else:
            return s
        
    return ""

s= "\\x (\\y (x y))"

print(expr(s))

