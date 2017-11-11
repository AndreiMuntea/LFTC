

class FiniteAutomata:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        FiniteAutomata._validate_automata(states, alphabet, initial_state, final_states, transitions)

        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

    @staticmethod
    def _validate_automata(states, alphabet, initial_state, final_states, transitions):
        if not isinstance(states, list):
            raise ValueError("States should be given as a list!")

        if not isinstance(alphabet, list):
            raise ValueError("Alphabet should be given as a list!")

        if not isinstance(initial_state, str):
            raise ValueError("Initial state should be a string")

        if not isinstance(final_states, list):
            raise ValueError("Final states should be given as a list")

        if not isinstance(transitions, dict):
            raise ValueError("Transitions should be given as a dictionary")

        if initial_state not in states:
            raise ValueError("Initial state should be a valid state")

        if len(final_states) is 0:
            raise ValueError("There should be at least one final state")

        if len(final_states) != len(set(final_states)):
            raise ValueError("Final states shouldn't repeat")

        for t in transitions:
            if t not in states:
                raise ValueError("Invalid state {0}".format(t))

            for delta in transitions[t]:
                if delta not in alphabet:
                    raise ValueError("Invalid alphabet symbol {0}".format(delta))
                for tran in transitions[t][delta]:
                    if tran not in states:
                        raise ValueError("Invalid state {0}".format(tran))

    def __str__(self):
        ret_value = "States: [" + ", ".join(self.states) + "]\n"
        ret_value += "Alphabet: [" + ", ".join(self.alphabet) + "]\n"
        ret_value += "Initial state: " + self.initial_state + "\n"
        ret_value += "Final states: [" + ", ".join(self.final_states) + "]\n"
        ret_value += "Delta: \n"

        for t in self.transitions:
            ret_value += t + ":\n"
            for delta in self.transitions[t]:
                ret_value += "\t" + delta + " -> "
                ret_value += ", ".join(self.transitions[t][delta])
                ret_value += "\n"
        return ret_value
