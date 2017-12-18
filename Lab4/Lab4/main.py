from LR0 import *


def main():
    productions = {
        'K': [Production('K', ['S'])],
        'S': [Production('S', ["A","B"]), Production('S', ['D', 'B'])],
        'A': [Production('A', ["B", "D"]), Production('S', ['a'])],
        'B': [Production('B', ["b"]), Production('B', ['c'])],
        'D': [Production('D', ["d"])]
    }

    terminals = ['a','b','c','d']
    non_terminals = ['K', 'S', 'A', 'B', 'D' ]
    g = Grammar(productions, 'K', terminals, non_terminals)

    c = LR0(g)
    (err, out) = c.parse("?(x>5){O(5)}")
    for p in out:
        print(p)


if __name__ == '__main__':
    main()
