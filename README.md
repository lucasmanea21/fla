# Simple Regex-to-DFA Tool

A Python script that turns regular expressions into DFA’s and checks if words match.

## Project Structure

```
.
├── postfix-to-nfa.py   # Main script with everything in one file
├── tests.json          # List of regexes and test cases
└── README.md           # This file
```

- **postfix-to-nfa.py**

  - `regex_to_postfix` — converts an infix regex (with `|`, `*`, `+`, `?` and implicit concatenation) into postfix form.
  - `postfix_to_nfa` — builds a Thompson NFA from the postfix.
  - `convert_nfa_to_dfa` — does subset-construction to get a DFA.
  - `simulate_dfa` — runs the DFA on an input string to accept or reject.
  - In the `__main__` block it loads `tests.json`, builds DFAs for each regex, and prints OK/FAIL for each test string.

- **tests.json**
  - An array of objects `{ name, regex, test_strings }`.
  - Each `test_strings` is a list of `{ input, expected }` pairs.

---

## How to Run

1. Make sure you have **Python 3** installed.
2. From the project directory, run:
   ```bash
   python postfix-to-nfa.py
   ```
3. You’ll see output like:
   ```
   === R1: /a*/ ===
     '': expected=True, got=True -> OK
     'a': expected=True, got=True -> OK
   …
   ```

---
