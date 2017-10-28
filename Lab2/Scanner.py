import json
from Token import *
from Lexer import *
from InternalProgramForm import *


def load_data(json_file):
    with open(json_file) as file:
        data = json.load(file)
    return data["codes"], data["rules"]


def get_tokens(rules):
    tokens = []
    for r in rules:
        objects = []
        for fl in rules[r]['followup']:
            objects.append((fl, rules[fl]['values']))
        tokens.append(Token(rules[r]['values'], r, objects))
    return tokens


def build_internal_program_form(codes, lexer):
    internal_program_form = InternalProgramForm(codes)

    for t in lexer.tokens():
        print(t[0], '-', t[1].get_name())
        internal_program_form.insert_token(t[1].get_name(), t[0])

    return internal_program_form


def setup():
    codes, rules = load_data("codes.json")
    tokens = get_tokens(rules)
    lexer = Lexer("program.txt", tokens)
    return build_internal_program_form(codes, lexer)


if __name__ == '__main__':
    try:
        ifp = setup()
        print(ifp.get_tokens())
    except ValueError as v:
        print("[LEXER ERROR]", v)
