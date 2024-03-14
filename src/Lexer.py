from .DFA import DFA
from .NFA import NFA
from .Regex import parse_regex
import sys
from typing import Union, FrozenSet

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        # initialisation should convert the specification to a dfa which will be used in the lex method
        # the specification is a list of pairs (TOKEN_NAME:REGEX)
        self.info = {}
        
        # create the big nfa that is to be transformed in a dfa
        S = set()
        K = {0}
        q0 = 0
        dict = {(q0,EPSILON) : set()}
        F = set()
        final_state_last_nfa = 0
        
        for tup in spec:
            token_name, regex = tup
            nfa = parse_regex(regex).thompson()
            nfa = nfa.remap_states(lambda state: state + final_state_last_nfa + 1)
            for i in nfa.F:
                self.info[i] = token_name
            
            # add it in the big nfa
            S = S.union(nfa.S)
            K = K.union(nfa.K)
            dict[(q0,EPSILON)].add(nfa.q0)
            
            for key, value in nfa.d.items():
                dict[key] = value
            F = F.union(nfa.F)
            final_state_last_nfa = max(list(K))
            
        nfa_big = NFA(S,K,q0,dict,F)     
        self.dfa = nfa_big.subset_construction()
        
    def lex(self, word: str) -> list[tuple[str, str]] | None:
        # this method splits the lexer into tokens based on the specification and the rules described in the lecture
        # the result is a list of tokens in the form (TOKEN_NAME:MATCHED_STRING)

        # if an error occurs and the lexing fails, you should return none # todo: maybe add error messages as a task
    
        longest_accepted_word = ''
        longest_token_id = ''
        current_character = ''
        accepted_word = ''
        lexemes = []
        index = 0
        index_global = 0 
        lines = 0
        word_initial = word
        current_state = self.dfa.q0
        
        while index < len(word):
            current_character = word[index]
            accepted_word += current_character 
           
            if current_character not in self.dfa.S:
                return [("", f"No viable alternative at character {index_global}, line {lines}")]
             
            current_key_tuple = (current_state, current_character) 
            current_state = self.dfa.d[current_key_tuple]
        
            if current_state in self.dfa.F:
                
                min_index = sys.maxsize
                for elem in current_state:
                    if elem in self.info.keys() and elem < min_index:
                        longest_accepted_word = accepted_word
                        longest_token_id = self.info[elem]
                        min_index = elem
                index += 1
                index_global += 1
                         
            elif current_state == frozenset('S'):
                
                if not longest_accepted_word:
                    return [("", f"No viable alternative at character {index_global}, line {lines}")]
                         
                lexemes.append((longest_token_id, longest_accepted_word))
                current_character = '' 
                accepted_word = ''
                
                n = len(longest_accepted_word)
                m = len(word_initial) - len(word)
                index_global = word_initial.find(longest_accepted_word, m) + n
                
                if longest_accepted_word == "\n":
                    lines += 1
                    index_global = 0

                word = word[n:]
                index = 0
                longest_accepted_word = ''
                longest_token_id = ''
                current_state = self.dfa.q0
            
            else:
                index += 1
                index_global += 1 
                        
        if current_state in self.dfa.F or current_state == frozenset('S'):
            lexemes.append((longest_token_id, longest_accepted_word))
        else:
            return [("", f"No viable alternative at character EOF, line {lines}")]
        
        return lexemes