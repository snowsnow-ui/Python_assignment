import re


class InvalidFormatError(Exception):
    pass


class UnknownVariableError(Exception):
    pass


class DivisionByZeroError(Exception):
    pass


class UnsupportedOperatorError(Exception):
    pass


def get_value(value, variables):
    if re.fullmatch(r"[+-]?(\d+(\.\d*)?|\.\d+)", value):
        return float(value)

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
        if value not in variables:
            raise UnknownVariableError
        return variables[value]

    raise InvalidFormatError


def calculate(line, variables):
    parts = line.split()

    if len(parts) == 1:
        return get_value(parts[0], variables)

    if len(parts) != 3:
        raise InvalidFormatError

    left = get_value(parts[0], variables)
    operator = parts[1]
    right = get_value(parts[2], variables)

    if operator not in ["+", "-", "*", "/", "%"]:
        raise UnsupportedOperatorError

    if operator in ["/", "%"] and right == 0:
        raise DivisionByZeroError

    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        return left / right
    return left % right


def show(value):
    if value.is_integer():
        return int(value)
    return value


def main():
    variables = {}

    while True:
        try:
            line = input().strip()
        except EOFError:
            break

        if line.lower() == "quit":
            break

        try:
            assignment = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)", line)

            if assignment:
                name = assignment.group(1)
                expression = assignment.group(2)
                variables[name] = calculate(expression, variables)
            else:
                result = calculate(line, variables)
                print(show(result))

        except InvalidFormatError:
            print("InvalidFormatError")
        except UnknownVariableError:
            print("UnknownVariableError")
        except DivisionByZeroError:
            print("DivisionByZeroError")
        except UnsupportedOperatorError:
            print("UnsupportedOperatorError")


if __name__ == "__main__":
    main()
