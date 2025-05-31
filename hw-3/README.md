### Description

This project allows you to define and work with context-free grammars (CFGs) in Python. It can print grammar rules, generate example strings, show derivation steps, test string membership, and check special patterns like aⁿbⁿcⁿ.

### How to run

- Requires **Python 3**
- Run:
  ```
  python cfg.py
  ```

### Features

- Define any CFG by specifying non-terminals, terminals, start symbol, and rules
- Print the grammar in a readable format
- Generate random strings from the grammar (up to 10 characters)
- Show leftmost derivation steps for a given string
- Test if a string is in the CFG language
- Check if a string matches the pattern aⁿbⁿcⁿ (n ≥ 1)

### Example output

```
Printing CFG:
non-terminals: S
terminals: a, b
start symbol: S
production rules:
S → aSb | ε

Task 2 - strings
''
'ab'
'aabb'
'aabbaa'
'aaabbb'
...

Task 3 - derivation
S -> aSb -> aaSbb -> aabb

Task 4 - membership check
'': True
'ab': True
'aabb': True
'aaabbb': True
'aba': False
'aab': False

Task 5 - recognizer for a^n b^n c^n
'abc': True
'aabbcc': True
'aaabbbccc': True
'aaabbccc': False
'aabbbcc': False
'': False
```
