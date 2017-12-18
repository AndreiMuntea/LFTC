class State:
    def __init__(self, data, key):
        self.data = data
        self.key = key

    def __eq__(self, other):
        return self.data == other.data

    def __hash__(self):
        return hash(self.key)


class Automaton:
    def __init__(self, start):
        self.start = start
        self.states = {start.key: start}
        self.transitions = []

    def add_state(self, state):
        self.states[state.key] = state

    def add_transition(self, s1, s2, symbol):
        self.transitions.append((s1, symbol, s2))

    def find_state(self, func):
        for state in self.states.values():
            if func(state):
                return state
        return None

    def next(self, state, symbol):
        for t in self.transitions:
            if t[0] == state and t[1] == symbol:
                return t[2]
        return None

    def all_states(self):
        for state in self.states.values():
            yield state
        raise StopIteration
