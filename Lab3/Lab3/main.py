import json
from Converter import *

def load_data(json_file):
    with open(json_file) as file:
        data = json.load(file)
    return data


def construct_grammar(json_data):
    try:
        g = Grammar(
            json_data["terminals"],
            json_data["non_terminals"],
            json_data["start_symbol"],
            json_data["empty_string"],
            json_data["productions"]
        )
        return g
    except ValueError as ex:
        print(ex)


def construct_automata(json_data):
    try:
        a = FiniteAutomata(
            json_data["states"],
            json_data["alphabet"],
            json_data["initial_state"],
            json_data["final_states"],
            json_data["transitions"]
        )
        return a
    except ValueError as ex:
        print(ex)


def load_grammar():
    a = load_data("grammar.json")
    grammar = construct_grammar(a)

    automata = Converter.grammar_to_automata(grammar)

    return (grammar, automata)


def load_automata():

    a = load_data("finite_automata.json")
    automata = construct_automata(a)

    grammar = Converter.automata_to_grammar(automata)

    return (grammar, automata)


if __name__ == "__main__":
    #(grammar, automata) = load_grammar()

    (grammar, automata) = load_automata()

    print(grammar)
    print(automata)

