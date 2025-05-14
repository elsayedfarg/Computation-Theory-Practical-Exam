from typing import Set, Dict, Tuple, List

class State:
    # __init__ is a special method that is called automatically when you create an object from a class
    def __init__(self, is_final=False):
        self.transitions: Dict[str, Set['State']] = {} # e.g. {'a': {state1, state2}, 'b': {state3}}
        self.epsilon: Set['State'] = set()             # Epsilon (ε) transitions (no input)
        self.is_final = is_final                       # Is this a final/accepting state?

    def add_transition(self, symbol: str, state: 'State'):
        if symbol == '':
            self.epsilon.add(state)
        else:
            if symbol not in self.transitions:
                self.transitions[symbol] = set()
            self.transitions[symbol].add(state)

class NFA:
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end

class DFA:
    def __init__(self, transitions, start_state, accept_states):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states

    def accepts(self, input_str):
        state = self.start_state
        for symbol in input_str:
            state = self.transitions.get((state, symbol))
            if state is None:
                return False
        return state in self.accept_states

def regex_to_dfa(regex: str) -> DFA:
    postfix = to_postfix(regex)
    nfa = postfix_to_nfa(postfix)
    return nfa_to_dfa(nfa)

# Helper functions

def to_postfix(regex: str) -> str:
    precedence = {'*': 3, '.': 2, '|': 1}
    output = []
    stack = []

    # def is_operator(c): return c in precedence or c in '()'

    # Add concatenation operator
    new_regex = ''
    for i, c in enumerate(regex):
        new_regex += c
        if c in 'ab)' and i + 1 < len(regex) and regex[i + 1] in '(ab':
            new_regex += '.'

    for c in new_regex:
        if c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif c in precedence:
            while stack and stack[-1] in precedence and precedence[stack[-1]] >= precedence[c]:
                output.append(stack.pop())
            stack.append(c)
        else:
            output.append(c)

    while stack:
        output.append(stack.pop())
    return ''.join(output)

def postfix_to_nfa(postfix: str) -> NFA:
    stack = []
    for c in postfix:
        if c in 'ab':
            start = State()
            end = State(is_final=True)
            start.add_transition(c, end)
            stack.append(NFA(start, end))
        elif c == '*':
            nfa = stack.pop()
            start = State()
            end = State(is_final=True)
            start.add_transition('', nfa.start)
            start.add_transition('', end)
            nfa.end.add_transition('', nfa.start)
            nfa.end.add_transition('', end)
            nfa.end.is_final = False
            stack.append(NFA(start, end))
        elif c == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.end.add_transition('', nfa2.start)
            nfa1.end.is_final = False
            stack.append(NFA(nfa1.start, nfa2.end))
        elif c == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            start = State()
            end = State(is_final=True)
            start.add_transition('', nfa1.start)
            start.add_transition('', nfa2.start)
            nfa1.end.add_transition('', end)
            nfa2.end.add_transition('', end)
            nfa1.end.is_final = False
            nfa2.end.is_final = False
            stack.append(NFA(start, end))
    return stack.pop()

def epsilon_closure(states: Set[State]) -> Set[State]:
    stack = list(states)
    closure = set(states)
    while stack:
        state = stack.pop()
        for eps_state in state.epsilon:
            if eps_state not in closure:
                closure.add(eps_state)
                stack.append(eps_state)
    return closure

def move(states: Set[State], symbol: str) -> Set[State]:
    result = set()
    for state in states:
        result.update(state.transitions.get(symbol, []))
    return result

def nfa_to_dfa(nfa: NFA) -> DFA:
    start_set = epsilon_closure({nfa.start})
    state_map = {frozenset(start_set): 0}
    unmarked = [start_set]
    transitions = {}
    accept_states = set()
    state_id = 1

    while unmarked:
        current = unmarked.pop()
        current_id = state_map[frozenset(current)]
        for symbol in 'ab':
            target = epsilon_closure(move(current, symbol))
            if not target:
                continue
            frozen = frozenset(target)
            if frozen not in state_map:
                state_map[frozen] = state_id
                unmarked.append(target)
                state_id += 1
            transitions[(current_id, symbol)] = state_map[frozen]
    for states, sid in state_map.items():
        if any(s.is_final for s in states):
            accept_states.add(sid)

    return DFA(transitions, 0, accept_states)

if __name__ == "__main__":
    dfa = regex_to_dfa("(a|b)*abb")
    print("Input: 'aabb'  →", dfa.accepts("aabb"))    # True
    print("Input: 'ababa' →", dfa.accepts("ababa"))   # False
