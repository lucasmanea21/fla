import random

class CFG:
    def __init__(self, non_terminals, terminals, start_symbol, rules):
        self.non_terminals = set(non_terminals)
        self.terminals = set(terminals)
        self.start_symbol = start_symbol
        self.rules = dict(rules)

    def print_cfg(self):
        print("Printing CFG: ")
        print("non-terminals:", ", ".join(sorted(self.non_terminals)))
        print("terminals:", ", ".join(sorted(self.terminals)))
        print("start symbol:", self.start_symbol)
        print("production rules:")
        
        for nt in sorted(self.rules):
            rhs_list = []
            for prod in self.rules[nt]:
                if prod:
                    rhs = "".join(prod)
                else:
                    rhs = "ε"
                rhs_list.append(rhs)
                
        print(f"  {nt} → {' | '.join(rhs_list)}")

    # string generator (random, up to max_length)
    def generate_string(self, symbol=None, max_length=10):
        if symbol is None:
            symbol = self.start_symbol
        if max_length <= 0:
            return ''
        productions = self.rules.get(symbol, [[symbol]])
        prod = random.choice(productions)
        
        result = ''
        for sym in prod:
            if sym in self.non_terminals:
                result += self.generate_string(sym, max_length - len(result))
            else:
                result += sym
            if len(result) >= max_length:
                break
        return result
    

    def generate_strings(self, n=10, max_length=10):
        generated = set()
        tries = 0
        while len(generated) < n and tries < 100:
            s = self.generate_string(self.start_symbol, max_length)
            if len(s) <= max_length:
                generated.add(s)
            tries += 1
        return list(generated)


    def leftmost_derivation(self, target, current=None, steps=None):
        if current is None:
            current = self.start_symbol
        if steps is None:
            steps = [current]
        if current == target:
            return steps
    
        for i, sym in enumerate(current):
            if sym in self.non_terminals:
                for prod in self.rules[sym]:
                    next_string = current[:i] + ''.join(prod) + current[i+1:]
                    if len(next_string) > len(target):
                        continue
                    res = self.leftmost_derivation(target, next_string, steps + [next_string])
                    if res:
                        return res
                break
        return None


    def is_in_language(self, s, symbol=None):
        if symbol is None:
            symbol = self.start_symbol

        def helper(sub, sym):
            if sym not in self.non_terminals:
                return sub == sym
            for prod in self.rules[sym]:
                if not prod:
                    if sub == '':
                        return True
                    continue
                
                
                if len(prod) == 3 and prod[0] in self.terminals and prod[2] in self.terminals and prod[1] in self.non_terminals:
                    if len(sub) >= 2 and sub[0] == prod[0] and sub[-1] == prod[2]:
                        if helper(sub[1:-1], prod[1]):
                            return True
                elif len(prod) == 1 and prod[0] in self.terminals:
                    if sub == prod[0]:
                        return True
                elif not prod:
                    if sub == '':
                        return True
            return False
        
        return helper(s, symbol)


    @staticmethod
    def is_anbncn(s):
        n = len(s) // 3
        if n < 1 or len(s) != 3 * n:
            return False
        
        if s[:n] == 'a' * n and s[n:2*n] == 'b' * n and s[2*n:] == 'c' * n:
            return True
        return False


if __name__ == "__main__":
    non_terminals = {'S'}
    
    terminals = {'a', 'b'}
    start_symbol = 'S'
    rules = {
        'S': [['a', 'S', 'b'], []]  
    }

    task = CFG(non_terminals, terminals, start_symbol, rules)

    
    task.print_cfg()


    print("\nTask 2 - strings")
    strings = task.generate_strings()
    for s in strings:
        print(repr(s))

    print("\nTask 3 - derivation")
    steps = task.leftmost_derivation("aabb")
    if steps:
        print(" -> ".join(steps))
    else:
        print("no derivation")

    print("\nTask 4 - membership check")
    test_strings = ["", "ab", "aabb", "aaabbb", "aba", "aab"]
    for ts in test_strings:
        print(f"{ts!r}: {task.is_in_language(ts)}")

    print("\nTask 5 - recognizer for a^n b^n c^n")
    bonus_tests = ["abc", "aabbcc", "aaabbbccc", "aaabbccc", "aabbbcc", ""]
    for bt in bonus_tests:
        print(f"{bt!r}: {CFG.is_anbncn(bt)}")
