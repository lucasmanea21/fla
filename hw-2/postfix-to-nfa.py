import json

def regex_to_postfix(regex):
    precedence = {'|':1, '·':2, '*':3, '+':3, '?':3}
    right_associative = {'*', '+', '?'}
    
    def is_symbol(c):
        return c not in precedence and c not in {'(', ')'}
    
    output = []    
    stack = []    
    last_was_symbol = False
    
    for c in regex:
        # two symbols
        if (is_symbol(c) or c == '(') and last_was_symbol:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence['·']:
                output.append(stack.pop())
            
            stack.append('·')
        
        if c in precedence:
            # it's an operator
            while stack and stack[-1] != '(':
                top = stack[-1]
                if (precedence[top] > precedence[c]) or \
                   (precedence[top] == precedence[c] and c not in right_associative):
                    output.append(stack.pop())
                else:
                    break
            stack.append(c)
            last_was_symbol = c in {'*', '+', '?'}
        elif c == '(':
            stack.append(c)
            last_was_symbol = False
        elif c == ')':
            # pop until "("
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # pop "("
            last_was_symbol = True
        else:
            # normal symbol
            output.append(c)
            last_was_symbol = True
        
    while stack:
        output.append(stack.pop())
        
    return ''.join(output)

def postfix_to_nfa(postfix):
    state_count = 0
    transitions = []  
    stack = []        

    def new_state():
        nonlocal state_count
        name = f"q{state_count}"
        state_count += 1
        return name

  
    for i, c in enumerate(postfix):
        if c == '*':
            if len(stack) < 1:
                raise ValueError(f"'*' at position {i} needs one operand")
            s, t = stack.pop()
            s0, t0 = new_state(), new_state()
            transitions += [
                (s0, 'ε', s), (s0, 'ε', t0),
                (t, 'ε', s), (t, 'ε', t0),
            ]
            stack.append((s0, t0))
        elif c == '+':
            if len(stack) < 1:
                raise ValueError(f"'+' at position {i} needs one operand")
            s, t = stack.pop()
            transitions.append((t, 'ε', s))
            stack.append((s, t))

        elif c == '?':
            if len(stack) < 1:
                raise ValueError(f"'?' at position {i} needs one operand")
            s, t = stack.pop()
            s0, t0 = new_state(), new_state()

            transitions += [
                (s0, 'ε', s), (s0, 'ε', t0),
                (t,  'ε', t0),
            ]
            stack.append((s0, t0))

        elif c in ('.','·'):
            if len(stack) < 2:
                raise ValueError(f"concat '{c}' at position {i} needs two operands")
            s2, t2 = stack.pop()
            s1, t1 = stack.pop()
            transitions.append((t1, 'ε', s2))
            stack.append((s1, t2))

        elif c in ('|','^'):
            if len(stack) < 2:
                raise ValueError(f"union '{c}' at position {i} needs two operands")
            s2, t2 = stack.pop()
            s1, t1 = stack.pop()
            s0, t0 = new_state(), new_state()
            transitions += [
                (s0, 'ε', s1), (s0, 'ε', s2),
                (t1, 'ε', t0), (t2, 'ε', t0),
            ]
            stack.append((s0, t0))

        else:
            # literal
            s0, t0 = new_state(), new_state()
            transitions.append((s0, c, t0))
            stack.append((s0, t0))

    if len(stack) != 1:
        raise ValueError(f"Invalid postfix: {len(stack)} fragments remain")
    start, accept = stack.pop()

    # assemble NFA dict
    states = set()
    for s, sym, t in transitions:
        states.add(s)
        states.add(t)
    trans_dict = {s: {} for s in states}
    for (s, sym, t) in transitions:
        trans_dict[s].setdefault(sym, set()).add(t)
    operators = {'ε','.','·','|','^','*'}
    alphabet = {sym for _, sym, _ in transitions if sym not in operators}

    return {
        'states': states,
        'alphabet': alphabet,
        'transitions': trans_dict,
        'start': start,
        'accept': {accept}
    }


def convert_nfa_to_dfa(nfa):
    alphabet = nfa['alphabet']
    trans_nfa = nfa['transitions']
    q0 = nfa['start']
    F = nfa['accept']

    def epsilon_closure(T):
        stack = list(T)
        closure = set(T)
        while stack:
            u = stack.pop()
            for v in trans_nfa.get(u, {}).get('ε', ()):
                if v not in closure:
                    closure.add(v)
                    stack.append(v)
        return closure

    def move(T, a):
        result = set()
        for u in T:
            result |= trans_nfa.get(u, {}).get(a, set())
        return result

    start_cl = frozenset(epsilon_closure({q0}))
    d_states = [start_cl]
    d_trans = {}
    d_accept = set()

    for D in d_states:
        if F & D:
            d_accept.add(D)
        for a in alphabet:
            U = frozenset(epsilon_closure(move(D, a)))
            if not U:
                continue
            d_trans.setdefault(D, {})[a] = U
            if U not in d_states:
                d_states.append(U)

    return {
        'states': d_states,
        'alphabet': alphabet,
        'transitions': d_trans,
        'start': start_cl,
        'accept': d_accept
    }


def simulate_dfa(dfa, word):
    current = dfa['start']
    for c in word:
        # invalid symbol
        if c not in dfa['alphabet']:
            return False
        current = dfa['transitions'].get(current, {}).get(c)
        if current is None:
            return False
    return current in dfa['accept']


def print_nfa(nfa):
    print('States:', nfa['states'])
    print('Alphabet:', nfa['alphabet'])
    print('Start:', nfa['start'])
    print('Accept:', nfa['accept'])
    print('Transitions:')
    for s, m in nfa['transitions'].items():
        for sym, tgt in m.items():
            print(f"  {s} --{sym}--> {tgt}")

if __name__=='__main__':
    with open('tests.json') as f:
        tests = json.load(f)
    for reg in tests:
        name = reg['name']
        regex = reg['regex']
        # convert to postfix, NFA, DFA
        postfix = regex_to_postfix(regex)
        nfa = postfix_to_nfa(postfix)
        
        # print_nfa(nfa)
        
        dfa = convert_nfa_to_dfa(nfa)
        
        # print(dfa)
        # print(f"=== {name}: /{regex}/ ===")
    
        print(f"=== {name}: /{regex}/ ===")
        for case in reg['test_strings']:
            input = case['input']
            expected = case['expected']
            got = simulate_dfa(dfa, input)
            status = 'OK' if got==expected else 'FAIL'
            print(f"  {input!r}: expected={expected}, got={got} -> {status}")
        print()
