# MIT License
#
# Copyright (c) 2022 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
#
# evalie - a toy evaluator using
# shunting-yard algorithm.
# ------
# github.com/ferhatgec/evalie
#

import math


class evalie:
    def __init__(self):
        self.precedence = {
            '+': 2,
            '-': 2,
            '*': 3,
            '/': 3,
            '!': 4,
            '^': 4,
            '%': 4
        }

        self.left = 0
        self.right = 0
        self.op = ''

        self.stack = self.evalie_values()

        self.pi = str(math.pi)
        self.e = str(math.e)
        self.tau = str(math.tau)
        self.golden_ratio = str(1.618033988749895)

    class evalie_values:
        def __init__(self):
            self.values = []
            self.operators = []

    @staticmethod
    def check_none(val):
        return val if val is not None else -1

    def get_precedence(self, ch) -> int:
        return self.check_none(self.precedence.get(ch))

    def perform(self):
        if self.left is None:
            self.left = 0

        if self.right is None:
            self.right = 0

        match self.op:
            case '+':
                return self.left + self.right

            case '-':
                return self.right - self.left

            case '*':
                return self.left * self.right

            case '/':
                return self.right / self.left

            case '^':
                return self.right ** self.left

            case '!':
                return float(math.factorial(int(self.left)))

            case '%':
                return self.right % self.left

    def pop(self, data):
        if type(data) == float:
            data = [data]
            return data.pop()

        if len(data) > 0:
            val = data.pop()
            return val

    def precalc(self, data: str):
        return data.replace('pi', self.pi) \
            .replace('π', self.pi) \
            .replace('e', self.e) \
            .replace('tau', self.tau) \
            .replace('τ', self.tau) \
            .replace('phi', self.golden_ratio) \
            .replace('φ', self.golden_ratio) \
            .replace('mod', '%')\
            .replace('+', ' + ')\
            .replace('-', ' - ')\
            .replace('/', ' / ')\
            .replace('*', ' * ')

    def clear(self):
        self.left = self.right = 0
        self.op = 0
        self.stack = self.evalie_values()

    def eval(self, data):
        data = self.precalc(data)

        i = 0

        while i < len(data):
            match data[i]:
                case ' ':
                    i += 1
                    continue

                case '(':
                    self.stack.operators.append(data[i])

                case ')':
                    while len(self.stack.operators) != 0 and self.stack.operators[-1] != '(':
                        self.left = self.pop(self.stack.values)
                        self.right = self.pop(self.stack.values)
                        self.op = self.pop(self.stack.operators)

                        self.stack.values.append(self.perform())

                    self.pop(self.stack.operators)

                case _ if data[i].isdigit() or (data[i] == '-' and self.left > 0 and self.right == 0):
                    value = ''

                    while i < len(data) and (data[i].isdigit() or data[i] == '.' or data[i] == '-'):
                        value += data[i]
                        i += 1

                    value = float(value)
                    self.stack.values.append(value)
                    i -= 1

                case _ as arg:
                    while (len(self.stack.operators) != 0
                           and self.get_precedence(self.stack.operators[-1]) >=
                           self.get_precedence(arg)):
                        self.left = self.pop(self.stack.values)

                        if self.stack.operators[-1] != '!':
                            self.right = self.pop(self.stack.values)

                        self.op = self.pop(self.stack.operators)

                        self.stack.values.append(self.perform())

                    self.stack.operators.append(data[i])

            i += 1

        while len(self.stack.operators) != 0:
            self.left = self.pop(self.stack.values)
            self.right = self.pop(self.stack.values)
            self.op = self.pop(self.stack.operators)

            self.stack.values = self.perform()

        if type(self.stack.values) == float:
            self.stack.values = [self.stack.values]

        if type(self.stack.values) == list and len(self.stack.values) > 0:
            return self.stack.values[-1]