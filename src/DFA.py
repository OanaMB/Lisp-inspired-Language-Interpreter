from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]

    def accept(self, word: str) -> bool:
        # simulate the dfa on the given word. return true if the dfa accepts the word, false otherwise
        # if the word is null and the initial state is also a final state
        # we accept the word, if the initial state is not final state, we do not accept
        if not word and (self.q0 in self.F):
            return True
        if not word:
            return False
        
        # initialize current state
        current_state = self.q0
        
        while word:
            # analize the current first character in the word
            current_character = word[0]
            # if the character is not in the alphabet of the dfa, then word is not acepted
            if current_character not in self.S:
                return False
            current_key_tuple = (current_state, current_character)
            
            # for the transition in the dictionary of (current_state, current_character), 
            # we remove the character that was just analyzed and we move in the next state
            word = word[1:]
            current_state = self.d[current_key_tuple]
            
        if current_state in self.F:
            return True
        else:
            return False

    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        # optional, but might be useful for subset construction and the lexer to avoid state name conflicts.
        # this method generates a new dfa, with renamed state labels, while keeping the overall structure of the
        # automaton.

        # for example, given this dfa:

        # > (0) -a,b-> (1) ----a----> ((2))
        #               \-b-> (3) <-a,b-/
        #                   /     ⬉
        #                   \-a,b-/

        # applying the x -> x+2 function would create the following dfa:

        # > (2) -a,b-> (3) ----a----> ((4))
        #               \-b-> (5) <-a,b-/
        #                   /     ⬉
        #                   \-a,b-/

        new_K = set()
        new_d = {}
        new_F = set()
        
        for state in self.K:
            new_K.add(f(state))
        for state in self.F:
            new_F.add(f(state))
        for key, value in self.d.items():
            new_d[(f(key[0]), key[1])] = f(value)
        
        dfa = DFA(self.S,new_K,f(self.q0),new_d,new_F)
        return dfa
