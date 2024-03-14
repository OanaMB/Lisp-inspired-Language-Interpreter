from sys import argv
from .Lexer import Lexer
from .DFA import DFA
from .NFA import NFA
from .Regex import parse_regex

def replace_innermost_lambda_body(expression, new_body):
    
        if expression['type'] == 'LAMBDA':
            expression['body'] = replace_innermost_lambda_body(expression['body'], new_body)
            return expression
        else:
            return new_body
    

def inlocuire(lambda_function,key,value):
    
    for el in lambda_function["elements"]:
        if 'value' in el and el['value'] == key:
            del el['value']
            if value["type"] == "LAMBDA":
                el['type'] = value['type']
                el['id'] = value['id']
                el['body'] = value['body']
                el['value'] = value['value']
                
            else:
                el['type'] = value['type']
                el['elements'] = value['elements']
                                 
        elif el['type'] == 'LIST':
            inlocuire(el,key,value)
    
def inlocuire2(el,key,value):
        if 'value' in el and el['value'] == key:
            del el['value']
            if value["type"] == "LAMBDA":
                el['type'] = value['type']
                el['id'] = value['id']
                el['body'] = value['body']
                el['value'] = value['value']
                
            else:
                el['type'] = value['type']
                el['elements'] = value['elements']
                                 
        elif el['type'] == 'LIST':
            inlocuire(el,key,value)
            
def add_lambda(lambdas):
    lambda_function = lambdas[0]
    lambda_values = {}

    for element in lambdas[1:]:
            id = lambda_function["id"]
            lambda_values[id] = element
            lambda_function = lambda_function["body"]
            
    lambda_function_copy = lambda_function
            
    if lambda_function["type"] == "LAMBDA":       
        while lambda_function["type"] == "LAMBDA":
            lambda_function = lambda_function["body"]
            
    # print("func", lambda_function)
    # print("values", lambda_values)
    

    for key, value in lambda_values.items():
        if lambda_function["type"] == "LIST":
            inlocuire(lambda_function,key,value)
        if lambda_function["type"] == "ID" or lambda_function["type"] == "LAMBDA":
            inlocuire2(lambda_function,key,value)
    # print("\n")  
    # print("\n")     
    # print("func2", lambda_function)
    # print("\n")  
    # print("\n")
    
   
    ok = 0 
    interpreted_result = ""    
    #print("lambda:",lambda_function)   
    #print('\n')
    if lambda_function["type"] == "LIST":
        interpreted_result, ok = interpreter.evaluate_list(lambda_function["elements"])
    else:
        lista = {"type": "LIST", "elements" : [lambda_function]}
        #print(lista)
        interpreted_result, ok = interpreter.evaluate_list(lista["elements"])
    # print("interpreted_result",interpreted_result) 
    # print(ok)   
    
        
    #print("interpret_result", interpreted_result)
    if ok == 1:
        
        # print(interpreted_result)
        # print('\n')
        
        
        interpreted_result = flatten_list2(interpreted_result)
        interpreted_result = interpreted_result[::-1]
        
        #print("interpreted_result",interpreted_result) 
        
        #print("interpret_result", interpreted_result)
        count = 0
        lambdas = []
        
        for el in interpreted_result:
            if isinstance(el,dict):
                count += 1
                lambdas.append(el)
                
        # for i in lambdas:
        #     print(i)       
        
        new_function = ""
        if count >= 2:
            interpreted_result = [item for item in interpreted_result if not isinstance(item, dict)]
            new_function = add_lambda(lambdas)
            print("new function",new_function) 
            
            interpreted_result.insert(0, new_function)
            
            #interpreted_result = interpret_lambda(interpreter,interpreted_result)    
            
    #print("interpret_result", interpreted_result)
    interpreted_result = interpret_lambda(interpreter,interpreted_result) 

    if isinstance(interpreted_result, list):
        interpreted_result = parse_list(interpreted_result)
    elif isinstance(str(interpreted_result), str):
        interpreted_result = parse_id(interpreted_result)
    elif isinstance(int(interpreted_result), int):
        interpreted_result = parse_number(interpreted_result)
        
    lambda_function_copy = replace_innermost_lambda_body(lambda_function_copy, interpreted_result)
    return lambda_function_copy
        
def interpret_lambda(interpreter,interpreted_result):
        
        #print("interpret_result", interpreted_result)
        lambda_function = interpreted_result[0]
        lambda_values = {}
 
        for element in interpreted_result[1:]:

            id = lambda_function["id"]
            lambda_values[id] = element
            lambda_function = lambda_function["body"]
            
        for key, value in lambda_values.items():
               
                if isinstance(value, list):
                    value = parse_list(value)
                elif isinstance(str(value), str):
                    value = parse_id(value)
                elif isinstance(int(value), int):
                    value = parse_number(value)
                    
                if lambda_function["type"] == "LIST":
                    inlocuire(lambda_function,key,value)
                    interpreted_result, ok = interpreter.evaluate_list(lambda_function["elements"])
                elif lambda_function["type"] == "NUMBER" or lambda_function["type"] == "ID":
                    if 'value' in lambda_function and lambda_function['value'] == key:
                            del lambda_function['value']
                            lambda_function['type'] = value['type']
                            lambda_function['value'] = value['value']
                            interpreted_result = value['value']
        return interpreted_result
        
def parse_list(input_list):
    parsed_list = {
        'type': 'LIST',
        'elements': [{'type': 'NUMBER', 'value': str(item)} for item in input_list]
    }
    return parsed_list

def parse_number(input_number):
    return {"type": "NUMBER", "value" : input_number}

def parse_id(input_number):
    return {"type": "ID", "value" : input_number}

def transform_list(lst):
    result = '( '
    for item in lst:
        if isinstance(item, list):
            result += transform_list(item)
        else:
            result += item
        result += ' '
    result = result.rstrip() + ' )'
    return result

def flatten_list2(lst):
    result = []
    if len(lst) == 2:
        result.append(lst[1])
        result.extend(flatten_list2(lst[0]))
    elif isinstance(lst, dict):
        result.append(lst)
       
    return result
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0

    def get_next_token(self):
        while self.current_index < len(self.tokens):
        
            self.current_index += 1
            if self.current_index == len(self.tokens):
                return self.current_index
            
            token_type, token_value = self.tokens[self.current_index]
            if token_type == "SPACE" or token_type == "NEWLINE" or token_type == "TAB":        
                continue
            else:
                return
            
        
    def eat(self, expected_type):
        token_type, token_value = self.tokens[self.current_index]
        if token_type == expected_type:
            self.get_next_token()  
            return token_value
        else:
            raise SyntaxError(f"Expected {expected_type}, got {token_type}")
        
    def parse_list(self):
        elements = []
        self.eat("OPEN_PAR")
        elements = self.parse_elements()
        self.eat("CLOSED_PAR")
        return {'type': 'LIST', 'elements': elements}
    
    def parse_elements(self):
        elements = []
        while (self.tokens[self.current_index][0] == "NUMBER" or 
              self.tokens[self.current_index][0] == "EMPTY" or 
              self.tokens[self.current_index][0] == "OPEN_PAR" or 
              self.tokens[self.current_index][0] == "ID" or
              self.tokens[self.current_index][0] == "SUM" or
              self.tokens[self.current_index][0] == "CONCAT" or
              self.tokens[self.current_index][0] == "LAMBDA"):
            elements.append(self.parse_atom())
        return elements
    
    def parse_atom(self):
        if self.tokens[self.current_index][0] == "OPEN_PAR":
            return self.parse_list()
        if self.tokens[self.current_index][0] == "NUMBER":
            return self.parse_number()
        if self.tokens[self.current_index][0] == "EMPTY":
            return self.parse_empty_list()
        if self.tokens[self.current_index][0] == "ID":
            return self.parse_id()
        if self.tokens[self.current_index][0] == "SUM":
            return self.parse_plus()
        if self.tokens[self.current_index][0] == "CONCAT":
            return self.parse_concatenation()
        if self.tokens[self.current_index][0] == "LAMBDA":
            self.eat("LAMBDA")
            return self.parse_lambda()
    
    def parse_number(self):
        return {"type": "NUMBER", "value" : self.eat("NUMBER")}
    
    def parse_empty_list(self):
        return {"type": "EMPTY", "value" : self.eat("EMPTY")}
    
    def parse_id(self):
        return {"type": "ID", "value" : self.eat("ID")}
    
    def parse_plus(self):
        return {"type": "SUM", "value" : self.eat("SUM")}
    
    def parse_concatenation(self):
        return {"type": "CONCAT", "value" : self.eat("CONCAT")}
    
    def parse_lambda(self):
        id = self.eat("ID")
        self.eat("DESP")
        return {"type": "LAMBDA", "id" : id, "body" : self.parse_atom(), "value" : {}}
    
    
class Interpreter:
    def __init__(self):
        pass
       
    def evaluate_concat(self, list):
        
        result = []
        if list["type"] == "LIST":
            for element in list["elements"]:
                if element["type"] == "NUMBER":
                    result.append(element["value"])
                    
                if element["type"] == "LIST":
                    for el in element["elements"]:
                        if el["type"] == "NUMBER" or el["type"] == "EMPTY":
                            result.append(el["value"])
                        if el["type"] == "LIST":
                            values, ok = self.evaluate_list(el["elements"])
                            if (len(list(str(result))) > 1):
                                result.append("( " + ' '.join(str(e) for e in values) + " )")
                            else:
                                result.append(values)      
                                                           
        return result
     
    def evaluate_list(self, elements):
        result = []
        ok = 0
    
        for element in elements:
            #print("element", element)
            
            if element["type"] == "LAMBDA":
                result.append(element)
                ok = 1
                
            if element["type"] == "NUMBER" or element["type"] == "EMPTY" or element["type"] == "ID":
                result.append(element["value"])
               
            if element["type"] == "LIST":
                values = ""
                if ok == 1:
                    values, ok = self.evaluate_list(element["elements"])
                    ok = 1
                else:
                    values, ok = self.evaluate_list(element["elements"])
                result.append(values)
                    
            if element["type"] == "CONCAT":
                # evaluam lista
                result = self.evaluate_concat(elements[1])
                break
            
            if element["type"] == "SUM":
                operands = ""
                
                if ok == 1:
                    operands, ok = self.evaluate_list(elements[1]["elements"])
                    ok = 1
                else:
                    operands, ok = self.evaluate_list(elements[1]["elements"])
                
                if ok == 1:
                    operands = interpret_lambda(interpreter,operands)
                    ok = 0
                    
                suma = 0
                for element in operands:
                    if isinstance(element, list):
                        suma += sum(int(x) for x in element)
                    elif element == '()':
                        suma += 0
                    else:
                        suma += int(element)
                        
                return suma, ok
            
        return result, ok

def main():
    if len(argv) != 2:
        return
    filename = argv[1]
    # TODO implementarea interpretor L (bonus)
    f = open(filename, "r")
    command = f.read().rstrip("\n")
    spec = [("SPACE", "\\ "), 
            ("NEWLINE", "\n"), 
            ("TAB", "\t"), 
            ("SUM", r"\+"), 
            ("CONCAT", r"\+\+"), 
            ("NUMBER", "[1-9][0-9]*|0"), 
            ("LAMBDA", "lambda"), 
            ("ID", "[a-z]|[A-Z]"), 
            ("DESP", ":"), 
            ("EMPTY", r"\(\)"), 
            ("OPEN_PAR", r'\('), 
            ("CLOSED_PAR", r'\)')]
    lexer = Lexer(spec)
    lexeme = lexer.lex(command)
   
    parser = Parser(lexeme)
    result = parser.parse_list()
   
    interpreted_result, ok = interpreter.evaluate_list(result["elements"])
    
   
    if ok == 1:
        interpreted_result = flatten_list2(interpreted_result)
        interpreted_result = interpreted_result[::-1]
        count = 0
        lambdas = []
        
        #print(interpreted_result)
        
        for el in interpreted_result:
            if isinstance(el,dict):
                count += 1
                lambdas.append(el)
        new_function = ""
        #print(count)
        if count >= 2:
            interpreted_result = [item for item in interpreted_result if not isinstance(item, dict)]
            new_function = add_lambda(lambdas)
            interpreted_result.insert(0, new_function)

        interpreted_result = interpret_lambda(interpreter,interpreted_result)
        if isinstance(interpreted_result, list):
            result = transform_list(interpreted_result)
            print(result)
        else:
            print(interpreted_result)
    else:
        if isinstance(interpreted_result, list):
            result = transform_list(interpreted_result)
            print(result)
        else:
            print(interpreted_result)  
            
    # {'type': 'LIST', 'elements':        
    #     [{'type': 'LIST', 'elements': 
    #         [{'type': 'LAMBDA', 'body': 
    #             {'type': 'LAMBDA', 'id': 'y', 'body': 
    #                 {'type': 'ID', 'value': 'x'}, 'value': {}}, 'value': {}, 'id': 'x'}, 
    #         {'type': 'LAMBDA', 'body': 
    #             {'type': 'LAMBDA', 'id': 'y', 'body': 
    #                 {'type': 'ID', 'value': 'y'}, 'value': {}}, 'value': {}, 'id': 'x'}]}, 
    #     {'type': 'LAMBDA', 'body': 
    #         {'type': 'LAMBDA', 'id': 'y', 'body': 
    #             {'type': 'ID', 'value': 'x'}, 'value': {}}, 'value': {}, 'id': 'x'}]}       
            
if __name__ == '__main__':
    interpreter = Interpreter()
    main()
