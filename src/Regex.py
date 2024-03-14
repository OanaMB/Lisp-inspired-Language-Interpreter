from dataclasses import dataclass
from .NFA import NFA
# import the English alphabet
from string import ascii_lowercase as asc_low
from string import ascii_uppercase as asc_up

EPSILON = ''

class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError('the thompson method of the Regex class should never be called')
# you should extend this class with the type constructors of regular expressions and overwrite the 'thompson' method
# with the specific nfa patterns. for example, parse_regex('ab').thompson() should return something like:

# >(0) --a--> (1) -epsilon-> (2) --b--> ((3))

# extra hint: you can implement each subtype of regex as a @dataclass extending Regex

# class that tackles the concatenation (represented by "." in implementation) syntactic sugar 
@dataclass
class Concat(Regex):
    def __init__(self, nfa1: Regex, nfa2: Regex):
        self.nfa1 = nfa1
        self.nfa2 = nfa2
   
    def thompson(self) -> NFA[int]:
        nfa1 = self.nfa1.thompson()
        nfa2 = self.nfa2.thompson()
        
        nfa1 = nfa1.remap_states(lambda state: state + len(nfa2.K))
        
        S = nfa1.S.union(nfa2.S)
        K = nfa1.K.union(nfa2.K)
        dict = {**nfa1.d,**nfa2.d}
        q0 = nfa2.q0
        f = nfa1.F
        
        for i in nfa2.F:
            dict[(i, EPSILON)] = {nfa1.q0}
        
        return NFA(S,K,q0,dict,f)

# class that tackles the | syntactic sugar      
@dataclass   
class Union(Regex):
    def __init__(self, nfa1: Regex, nfa2: Regex):
        self.nfa1 = nfa1
        self.nfa2 = nfa2
        
    def thompson(self) -> NFA[int]:
        nfa1 = self.nfa1.thompson()
        nfa2 = self.nfa2.thompson()
        
        nfa1 = nfa1.remap_states(lambda state: state + 2 + len(nfa2.K))
        nfa2 = nfa2.remap_states(lambda state: state + 2)
        
        S = nfa1.S.union(nfa2.S)
        K = nfa1.K.union(nfa2.K)
        K = K.union({0,1})
        dict = {**nfa1.d,**nfa2.d}
        q0 = 0
        f = {1}

        dict[(q0,EPSILON)] = {nfa1.q0, nfa2.q0}
        for i in nfa1.F:
            dict[(i,EPSILON)] = f
        for i in nfa2.F:
            dict[(i,EPSILON)] = f
            
        return NFA(S,K,q0,dict,f)

# class that tackles the * syntactic sugar     
@dataclass  
class KleeneStar(Regex):
    def __init__(self, nfa : Regex):
        self.nfa = nfa
        
    def thompson(self) -> NFA[int]:
        nfa = self.nfa.thompson()
        nfa = nfa.remap_states(lambda state: state + 2)
        
        K = nfa.K.union({0,1})
        dict = nfa.d
        q0 = 0
        f = {1}
        
        dict[(q0, EPSILON)] = {nfa.q0, 1}
        
        for i in nfa.F:
            dict[(i, EPSILON)] = {nfa.q0, 1}
            
        return NFA(nfa.S,K,q0,dict,f)
        
# class that tackles the + syntactic sugar     
@dataclass  
class Plus(Regex):
    def __init__(self, nfa : Regex):
        self.nfa = nfa
        
    def thompson(self) -> NFA[int]:
        nfa = self.nfa.thompson()
        nfa = nfa.remap_states(lambda state: state + 2)
        
        K = nfa.K.union({0,1})
        dict = nfa.d
        q0 = 0
        f = {1}
        
        dict[(q0, EPSILON)] = {nfa.q0}
        
        for i in nfa.F:
            dict[(i, EPSILON)] = {nfa.q0, 1}
            
        return NFA(nfa.S,K,q0,dict,f)

# class that tackles the ? sintactic sugar   
@dataclass  
class OneNone(Regex):
    def __init__(self, nfa : Regex):
        self.nfa = nfa
        
    def thompson(self) -> NFA[int]:
        nfa = self.nfa.thompson()
        nfa = nfa.remap_states(lambda state: state + 2)
        K = nfa.K.union({0,1})
        dict = nfa.d
        q0 = 0
        f = {1}
        
        dict[(q0, EPSILON)] = {nfa.q0, 1}
        
        for i in nfa.F:
            dict[(i, EPSILON)] = {1}
            
        return NFA(nfa.S,K,q0,dict,f)

# class that tackles the [a-z] syntactic sugar   
@dataclass  
class SmallLetter(Regex):
      
    def thompson(self) -> NFA[int]:
        S = set(asc_low)
        K = {0,1}
        q0 = 0
        dict = {}
        f = {1}
        
        for i in S:
            dict[(0,i)] = {1}
            
        return NFA(S,K,q0,dict,f)

# class that tackles the [A-Z] syntactic sugar        
@dataclass  
class BigLetter(Regex):
        
    def thompson(self) -> NFA[int]:
        S = set(asc_up)
        K = {0,1}
        q0 = 0
        dict = {}
        f = {1}
        
        for i in S:
            dict[(0,i)] = {1}
            
        return NFA(S,K,q0,dict,f)
    
# class that tackles the [0-9] syntactic sugar    
@dataclass  
class Number(Regex):
      
    def thompson(self) -> NFA[int]:
        S = {'0','1','2','3','4','5','6','7','8','9'}
        K = {0,1}
        q0 = 0
        dict = {}
        f = {1}
        
        for i in S:
            dict[(0,i)] = {1}
            
        return NFA(S,K,q0,dict,f)
        
# class that adds a character to the nfa     
@dataclass  
class Character(Regex):
    def __init__(self, character:str, index: int):
        self.character = character
        self.index = index
        
    def thompson(self) -> NFA[int]:
       S = {self.character}
       #print(S)
       dict = {}
       dict[(0,self.character)] = {1}
       return NFA(S,{0,1},0,dict,{1})
    
def parse_regex(regex: str) -> Regex:
    # create a Regex object by parsing the string

    # you can define additional classes and functions to help with the parsing process

    # the checker will call this function, then the thompson method of the generated object. the resulting NFA's
    # behaviour will be checked using your implementation form stage 1
    
    # stack to store characters
    characters = []
    # stack to store operators
    operators = []
    
    # while there is a string with the regex, go through each character
    # and, depending on what it is, create Regex objects
    # since the concatenation operator is not represented in the string, we add "."
    # in the operator stack in different cases of concatenation
    i = 0
    while i < len(regex):
        # in case of space, ignore it
        if regex[i] == ' ':
            i += 1
            continue
        # in case of /, it means the next character will be put in the object
        elif regex[i] == '\\':
            i += 1
            characters.append(Character(regex[i], i))
            
            # check for concatenation
            if i + 1 < len(regex) and regex[i+1] not in ['|','*','+','?', ')', ' ']:
                operators.append(".")
        
        # a paranthesis is opened, we put it in the stack of operators
        elif regex[i] == '(':
            operators.append(regex[i])
            
        # a paranthesis is closed, we execute every operation in the paranthesis until we meet "("   
        elif regex[i] == ')':
            while(operators[-1]!='('):
                if operators[-1] in ['|','.']:
                    operand1 = characters.pop()
                    operand2 = characters.pop()
                    operator = operators.pop()
                    characters.append(applyOperationTwoOperands(operand1,operand2,operator))
                else:
                    operand = characters.pop()
                    operator = operators.pop()
                    characters.append(applyOperationOneOperand(operand,operator))    
                
            operators.pop()
            # check for concatenation
            if i + 1 < len(regex) and regex[i+1] not in ['|','*','+','?', ')', ' ']:
                operators.append(".")
            
        # in case of "[", it means that we can have any of the characters in the list represented:[a-z],[A-Z],[0-9]   
        elif regex[i] == '[':
            i += 1
            if regex[i].isdigit():
                characters.append(Number())
            if regex[i].islower():
                characters.append(SmallLetter())
            if regex[i].isupper():
                characters.append(BigLetter())
            i += 3
            # check for concatenation
            if i + 1 < len(regex) and regex[i+1] not in ['|','*','+','?', ')', ' ']:
                operators.append(".")
                
        # we execute one of the three operations on the last operand in the stack if we meet them
        elif regex[i] in ['*','+','?']:
                operand = characters.pop()
                characters.append(applyOperationOneOperand(operand,regex[i]))
                # check for concatenation
                if i + 1 < len(regex) and regex[i+1] not in ['|','*','+','?', ')', ' ']:
                    operators.append(".")
        
        # we check if there are operators with bigger precedence before executing union,
        # and then we execute the union  
        elif regex[i] == '|':
            while operators and precedence(regex[i]) <= precedence(operators[-1]):

                if operators[-1] in ['|','.']:
                    operand1 = characters.pop()
                    operand2 = characters.pop()
                    operator = operators.pop()
                    characters.append(applyOperationTwoOperands(operand1,operand2,operator))
                    
                else:
                    operand = characters.pop()
                    operator = operators.pop()
                    characters.append(applyOperationOneOperand(operand,operator))
                
            
            operators.append(regex[i])
            
        else:
            # we add the character that is not one of the above
            characters.append(Character(regex[i], i))           
            if i + 1 < len(regex) and regex[i+1] not in ['|','*','+','?', ')', ' ']:
                operators.append(".") 
        i+=1
    
    # if there are more operators left in the stack, we execute the operations, 
    # so that in the operand stack it only remains the result, one regex        
    while operators:
        if operators[-1] in ['|','.']:
            operand1 = characters.pop()
            operand2 = characters.pop()
            operator = operators.pop()
            characters.append(applyOperationTwoOperands(operand1,operand2,operator))
        else:
            operand = characters.pop()
            operator = operators.pop()
            characters.append(applyOperationOneOperand(operand,operator))
    
    # in case there are still more that one operands in the stack we concatenate them 
    # (there could be cases where a space, that we initially ignored, is put between different parts of the string)    
    while len(characters) >= 2:
        operand1 = characters.pop()
        operand2 = characters.pop()
        characters.append(applyOperationTwoOperands(operand1,operand2,"."))
          
    return characters.pop()
    
    
# function that sets the precedence of operators    
def precedence(operator: str) -> int:

    if operator == '*' or operator == '+' or operator == '?':
        return 3
    if operator == '.':
        return 2
    if operator == '|':
        return 1
    
    return 0

# function that executes a postfix operation
def applyOperationOneOperand(operand: Regex, operator: str) -> Regex:
    if operator == '*':
        return KleeneStar(operand)
    if operator == '+':
        return Plus(operand)
    if operator == '?':
        return OneNone(operand)
   
# function that executes an infix operation   
def applyOperationTwoOperands(operand1: Regex, operand2:Regex, operator: str) -> Regex:
   
    if operator == '|':
        return Union(operand1,operand2)
    if operator == '.':
        return Concat(operand1,operand2)
    