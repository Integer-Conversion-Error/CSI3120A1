import os
from typing import Union, List, Optional



alphabet_chars = list("abcdefghijklmnopqrstuvwxyz") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
numeric_chars = list("0123456789")
var_chars = alphabet_chars + numeric_chars
funky_chars = ["(", ")", ".", "\\", " "]
all_valid_chars = var_chars + funky_chars
valid_examples_fp = "./valid_examples.txt"
invalid_examples_fp = "./invalid_examples.txt"



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
            print(s)
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

    

s ="\\x (\\y (x y))"
print(var(s))