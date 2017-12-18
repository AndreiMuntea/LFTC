import re


class Token:
    def __init__(self, values, name, followup_tokens=None):
        self.__name = name
        self.__values = values
        self.__values_group = Token.__create_groups(values, name)
        self.__rule = re.compile('(^)' + self.__values_group + Token.__get_followup(followup_tokens))

    def get_name(self):
        return self.__name

    def get_values(self):
        return self.__values

    def get_values_as_groups(self):
        return self.__values_group

    def get_rule(self):
        return self.__rule

    @staticmethod
    def __create_groups(objects, group_name):
        group = '(?P<' + group_name + '>'
        for o in objects:
            group += '(' + o + ')' + '|'
        return group[:-1] + ')'

    @staticmethod
    def __get_followup(followup):
        if followup is None or followup == []:
            return ''
        f = '('
        for follow in followup:
            f += '(' + Token.__create_groups(follow[1], follow[0]) + ')' + '|'
        return f[:-1] + ')'

