import random
import string
import copy

from FiniteAutomata import *
from Grammar import *


class Converter:
    @staticmethod
    def automata_to_grammar(automata):
        non_terminals = copy.deepcopy(automata.states)
        terminals = copy.deepcopy(automata.alphabet)
        empty_string = "epsilon"
        start_symbol = automata.initial_state
        productions = dict()

        for s in automata.states:
            productions[s] = list()

        if automata.initial_state in automata.final_states:
            productions[start_symbol].append([empty_string])

        for t in automata.transitions:
            for d in automata.transitions[t]:
                for state in automata.transitions[t][d]:
                    if state in automata.final_states:
                        productions[t].append([d])
                    productions[t].append([d, state])

        return Grammar(terminals, non_terminals, start_symbol, empty_string, productions)

    @staticmethod
    def grammar_to_automata(grammar):
        states = copy.deepcopy(grammar.non_terminals)
        alphabet = copy.deepcopy(grammar.terminals)
        initial_state = grammar.start_symbol
        f = Converter._create_final_state(states)
        states.append(f)
        final_states = [f]
        transitions = dict()

        if Converter._check_if_initial_state_is_final(grammar.empty_string, grammar.start_symbol, grammar.productions):
            final_states.append(initial_state)

        for production in grammar.productions:
            transitions[production] = dict()
            for exp in grammar.productions[production]:
                if len(exp) == 1:
                    # This should happen only in initial state
                    if exp[0] == grammar.empty_string:
                        continue
                    else:
                        if exp[0] not in transitions[production]:
                            transitions[production][exp[0]] = list()
                        transitions[production][exp[0]].append(f)
                else:
                    if exp[0] not in transitions[production]:
                        transitions[production][exp[0]] = list()
                    transitions[production][exp[0]].append(exp[1])

        return FiniteAutomata(states, alphabet, initial_state, final_states, transitions)

    @staticmethod
    def _check_if_initial_state_is_final(empty_string, start_symbol, productions):
        for t in productions[start_symbol]:
            if len(t) is 1 and t[0] == empty_string:
                return True
        return False

    @staticmethod
    def _create_final_state(states):
        s = "FINAL_STATE"
        while s in states:
            s = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return s
