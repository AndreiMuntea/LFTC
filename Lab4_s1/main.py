from LR0 import *

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




def main():
    try:
        ifp = setup()
        print(ifp.get_tokens())

        productions = {
            'K': [Production('K', ["IF"])],
            "IF": [Production("IF", [CODE_IF, CODE_OPEN_BRACKET, 'COND', CODE_CLOSED_BRACKET, CODE_OPEN_CURLY_BRACKET, 'STATEMENT', CODE_CLOSED_CURLY_BRACKET])],
            'COND': [Production('COND', ['COND_M', 'OPERATOR', 'COND_M'])],
            'COND_M': [Production('COND_M', [CODE_IDENTIFIER]), Production('COND_M', [CODE_CONSTANT])],
            'OPERATOR': [Production('OPERATOR', [CODE_OPERATOR_GREATER]), Production('OPERATOR', [CODE_OPERATOR_GREATER_OR_EQUAL]), Production('OPERATOR', [CODE_OPERATOR_SMALLER]), Production('OPERATOR', [CODE_OPERATOR_SMALLER_OR_EQUAL]), Production('OPERATOR', [CODE_OPERATOR_EQUAL]), Production('OPERATOR', [CODE_OPERATOR_DIFFERENT])],
            'STATEMENT': [Production('STATEMENT', ["READ"]), Production('STATEMENT', ["WRITE"])],
            'READ': [Production('READ', [CODE_READ, CODE_OPEN_BRACKET, CODE_IDENTIFIER, CODE_CLOSED_BRACKET])],
            'WRITE': [Production('WRITE', [CODE_WRITE, CODE_OPEN_BRACKET, 'COND_M', CODE_CLOSED_BRACKET])],
        }

        terminals = [CODE_READ, CODE_WRITE, CODE_IF, CODE_OPEN_BRACKET, CODE_CLOSED_BRACKET, CODE_OPEN_CURLY_BRACKET, CODE_CLOSED_CURLY_BRACKET, CODE_OPERATOR_EQUAL, CODE_OPERATOR_GREATER, CODE_OPERATOR_GREATER_OR_EQUAL, CODE_OPERATOR_SMALLER, CODE_OPERATOR_SMALLER_OR_EQUAL, CODE_OPERATOR_DIFFERENT]
        non_terminals = ['K', 'COND', 'COND_M', 'OPERATOR', 'STATEMENT', "IF", "READ", "WRITE"]
        g = Grammar(productions, 'K', terminals, non_terminals)

        c = LR0(g)

        seq = []
        for fp in ifp.get_tokens():
            seq.append(fp[1])
        print(seq)

        (err, out) = c.parse(seq)
        print("EROAREA ESTE ", err)
        for p in out:
            print(p)

    except Exception as v:
        print("[ERROR]", v)


if __name__ == '__main__':
    main()
