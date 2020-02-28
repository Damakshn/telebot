import re
import operator as op


class GenericCommand:

    def __init__(self, *args, **kwargs):
        self.input_error = ""
    
    def run(self, user_input):
        self.check_errors(user_input)
        if self.input_error:
            return self.input_error
        return self.main(self.parse_command_args(user_input))
    
    def check_errors(self, user_input):
        pass

    def parse_command_args(self, user_input):
        return user_input
    
    def main(self, command_args):
        return ""

class CalcCommand(GenericCommand):
    """
    def refine_user_input(self, user_input):
        self.refined_input = user_input.replace(" ", "")
    
    def check_raw_input(self, user_input):
        operator_pattern = "[\+\-\*\/]"
        operator_without_operands = f"^{operator_pattern}|{operator_pattern}$|{operator_pattern}{operator_pattern}"
        if not expression_string:
            return "Выражение не задано"
        if not re.match(operator_pattern, expression_string):
            return "Нет ни одного арифметического оператора"
        if re.match(operator_without_operands, expression_string):
            return "Оператор без операндов"
        return ""
    """

    def check_errors(self, user_input):
        refined_string = user_input.replace(" ", "")
        operator_pattern = "[\+\-\*\/]"
        operator_without_operands = f"^{operator_pattern}|{operator_pattern}$|{operator_pattern}{operator_pattern}"
        if not refined_string:
            self.input_error = "Выражение не задано"
        elif not re.search(operator_pattern, refined_string):
            self.input_error = "Нет ни одного арифметического оператора"
        elif re.search(operator_without_operands, refined_string):
            self.input_error = "Оператор без операндов"

    def parse_command_args(self, user_input):
        return re.findall("\d+|[\+\-\*\/]", user_input)
    
    def evaluate(self, tokenized_expression):
        values = []
        operators = []

        def is_operator(token):
            return (token in ("+", "-", "*", "/"))

        def precedence(operator):
            if operator in ("+", "-"):
                return 0
            if operator in ("*", "/"):
                return 1

        def to_digit(token):
            try:
                return int(token)
            except:
                return float(token)

        def evaluate_last():
            actions = {
                "+": op.add,
                "-": op.sub,
                "*": op.mul,
                "/": op.truediv
            }
            operand2 = values.pop()
            operand1 = values.pop()
            operator = operators.pop()
            action = actions[operator]
            new_value = action(operand1, operand2)
            values.append(new_value)

        for token in tokenized_expression:
            if is_operator(token):
                if operators and precedence(token) <= precedence(operators[-1]):
                    evaluate_last()
                    operators.append(token)
                else:
                    operators.append(token)
            else:
                values.append(to_digit(token))

        while operators:
            evaluate_last()

        return f"Получилось {values[0]}"
    
    def main(self, command_args):
        try:
            return self.evaluate(command_args)
        except ZeroDivisionError:
            return "Ошибка - попытка деления на ноль"


class CityGameCommand(GenericCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_cities = kwargs["cities"]
        self.used_cities = set()
        # ToDo время на час от текущего
        self.expiration_time = None
        self.bot_last_city = ""
    
    def check_errors(self, user_input):
        if re.search("[a-zA-Z\d]", user_input):
            self.input_error = "Латиницу и цифры использовать нельзя"
        elif self.bot_last_city:
            last_letter = self.bot_last_city[-1].capitalize()
            if not user_input.startswith(last_letter):
                self.input_error = f"Новый город должен начинаться на букву {last_letter}"
    
    def main(self, command_args):
        return self.play(command_args)
    
    def play(self, city_from_user):
        if city_from_user in self.used_cities:
            return "Такой город уже был! Ты проиграл!"
        self.used_cities.add(city_from_user)
        if city_from_user in self.bot_cities:
            self.bot_cities.remove(city_from_user)
        letter = city_from_user[-1].capitalize()
        available_cities = [city for city in self.bot_cities if city.startswith(letter)]
        if not available_cities:
            return f"Я не знаю городов на букву {letter}, ты победил!"
        next_city = available_cities[0]
        self.bot_last_city = next_city
        self.used_cities.add(next_city)
        self.bot_cities.remove(next_city)
        return next_city
   