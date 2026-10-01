import re
import sys

sys.setrecursionlimit(1000000)


class ExpressionError(Exception):
    pass


class Parser:
    def __init__(self, text, get_variable):
        self.text = text
        self.get_variable = get_variable
        self.tokens = re.findall(r"\d+|[A-Za-z_][A-Za-z0-9_]*|[+\-*()]", text)
        self.position = 0

        joined = "".join(self.tokens)
        original = re.sub(r"\s+", "", text)
        if joined != original:
            raise ExpressionError

    def current(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def expression(self):
        value = self.term()
        while self.current() in ("+", "-"):
            operator = self.current()
            self.position += 1
            right = self.term()
            if operator == "+":
                value += right
            else:
                value -= right
        return value

    def term(self):
        value = self.factor()
        while self.current() == "*":
            self.position += 1
            value *= self.factor()
        return value

    def factor(self):
        token = self.current()

        if token is None:
            raise ExpressionError

        if token.isdigit():
            self.position += 1
            return int(token)

        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            self.position += 1
            return self.get_variable(token)

        if token == "(":
            self.position += 1
            value = self.expression()
            if self.current() != ")":
                raise ExpressionError
            self.position += 1
            return value

        raise ExpressionError

    def parse(self):
        value = self.expression()
        if self.current() is not None:
            raise ExpressionError
        return value


def main():
    try:
        v = int(input())
        definitions = {}

        for _ in range(v):
            line = input()
            if "=" not in line:
                print("INVALID")
                return

            name, expression = line.split("=", 1)
            name = name.strip()
            expression = expression.strip()

            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
                print("INVALID")
                return

            definitions[name] = expression

        target = input().strip()
        memo = {}
        visiting = set()

        def get_variable(name):
            if name in memo:
                return memo[name]
            if name not in definitions:
                raise ExpressionError
            if name in visiting:
                raise RuntimeError

            visiting.add(name)
            value = Parser(definitions[name], get_variable).parse()
            visiting.remove(name)
            memo[name] = value
            return value

        answer = Parser(target, get_variable).parse()
        print(answer)

    except RuntimeError:
        print("CYCLE")
    except (ValueError, ExpressionError, EOFError, RecursionError):
        print("INVALID")


if __name__ == "__main__":
    main()
