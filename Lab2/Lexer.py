class Lexer:
    def __init__(self, file_name, tokens_list):
        self.__file_name = file_name
        self.__tokens = tokens_list

    def __lines(self):
        with open(self.__file_name) as f:
            for line in f:
                yield line

    def __get_tokens(self, line):
        pos = 0
        while pos < len(line):
            match = None
            tp = None
            for tok in self.__tokens:
                m = tok.get_rule().match(line[pos:])
                if m is not None:
                    match = m.groupdict()[tok.get_name()]
                    tp = tok
                    break
            if match is None:
                raise ValueError("Nothing matches line: '" + line[:-1] + "'")
            pos += len(match)
            yield (match, tp)

    def tokens(self):
        for line in self.__lines():
            for tok in self.__get_tokens(line):
                yield tok
