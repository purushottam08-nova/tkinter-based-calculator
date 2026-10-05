class CalculatorLogic:
    def __init__(self):
        self.current = "0"
        self.previous = None
        self.operator = None
        self.reset_display = False

    def input_number(self, number):
        if self.current == "0" or self.reset_display:
            self.current = number
            self.reset_display = False
        else:
            self.current += number

        return self.current

    def input_decimal(self):
        if self.reset_display:
            self.current = "0."
            self.reset_display = False
        elif "." not in self.current:
            self.current += "."

        return self.current

    def set_operator(self, operator):
        if self.current == "":
            return self.current

        if self.previous is not None and self.operator is not None and not self.reset_display:
            self.calculate()

        self.previous = float(self.current)
        self.operator = operator
        self.reset_display = True

        return self.current

    def calculate(self):
        if self.previous is None or self.operator is None:
            return self.current

        current = float(self.current)

        try:
            if self.operator == "+":
                result = self.previous + current
            elif self.operator == "-":
                result = self.previous - current
            elif self.operator == "×":
                result = self.previous * current
            elif self.operator == "÷":
                if current == 0:
                    raise ZeroDivisionError
                result = self.previous / current
            else:
                return self.current

            self.current = self.format_result(result)
            self.previous = None
            self.operator = None
            self.reset_display = True

            return self.current

        except ZeroDivisionError:
            self.current = "Error"
            self.previous = None
            self.operator = None
            self.reset_display = True
            return self.current

    def clear(self):
        self.current = "0"
        self.previous = None
        self.operator = None
        self.reset_display = False
        return self.current

    def backspace(self):
        if self.current == "Error" or self.reset_display:
            return self.current

        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"

        return self.current

    def toggle_sign(self):
        if self.current == "0" or self.current == "Error":
            return self.current

        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current

        return self.current

    def percentage(self):
        if self.current == "Error":
            return self.current

        try:
            self.current = self.format_result(float(self.current) / 100)
        except ValueError:
            self.current = "Error"

        return self.current

    @staticmethod
    def format_result(result):
        if result == int(result):
            return str(int(result))

        return str(round(result, 10))