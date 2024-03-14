from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file
        epsilon_closure = set()
        
        # initialize list that stores states that need to be analyzed in order to find the next states
        states_to_be_analyzed = [state]
        # initialize list that stores states that are analyzed
        states_that_are_analized = []
      
        while states_to_be_analyzed:
            current_state = states_to_be_analyzed[0]
            
            # add current_state in the epsilon_closure
            epsilon_closure.add(current_state)
            states_to_be_analyzed.pop(0)
            key = (current_state, EPSILON) 
            
            # if we find the entry of (current_state, epsilon), then we add all the next states
            # in the list of unanalyzed states
            if key in self.d.keys():
                for elem in self.d[key]:
                    if elem not in states_that_are_analized:
                        states_to_be_analyzed.append(elem)
            states_that_are_analized.append(current_state)
            
        return epsilon_closure

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm
        e_closures = {}
        for st in self.K:
            e_closures[st] = self.epsilon_closure(st)
          
        # initialize the elements of the dfa
        # initialize set of states with the sink state
        new_K = {frozenset("S")}
        # the initial state is the e-closure of the nfa initial state
        new_q0 = frozenset(e_closures[self.q0])
        # intialize dictionary
        new_d = {}
        # initialize final state
        new_F = set()
            
        # initialize list that stores states that need to be analyzed in order to
        # find the next states; we start with the state that contains the initial state of the NFA
        states_to_be_analyzed = []
        states_to_be_analyzed.append(e_closures[self.q0])
        
        # for every tuple of sink state and character, the next state will be sink
        for character in self.S:
            new_d[(frozenset("S"), character)] =  frozenset("S")
        
        while states_to_be_analyzed:
            current_state = states_to_be_analyzed[0]
            
            # if the current state contains a state of the nfa that is accepted as a final state
            # then the current state is a final state for our new dfa
            if self.F.intersection(current_state):
                # the final state is the set of e-closures
                new_F.add(frozenset(current_state))
            
            # analize all the combinations of state and character of the alphabet
            for character in self.S:
                # create the next state that our current state will go into with the respective transition
                next_state = set()
                
                # go through all the states of the initial nfa that are present in the current state
                # next_state will result in a reunion of all the states that the states in current_state go to
                for state in current_state:
                    key = (state, character)
                    
                    # if we have an entry in the dictionary on this (state,character), 
                    # we combine all the e-closures of the states that this transition goes to
                    if key in self.d.keys():                   
                        for i in self.d[key]:
                            set_closure = e_closures[i]
                            next_state.update(set_closure)
                
                # add in dictionary and check if next_state is empty, if it is, we go in sink state
                if not next_state:
                    new_d[(frozenset(current_state), character)] =  frozenset("S")   
                else:
                    new_d[(frozenset(current_state), character)] = frozenset(next_state)    
                
                # if we haven't analyzed the next_state we put it in the list of states_to_be_analyzed
                if next_state and next_state != current_state and next_state not in new_K:
                    states_to_be_analyzed.append(next_state)
                    
            # add the current state in the set of states of the dfa  
            new_K.add(frozenset(current_state))
            states_to_be_analyzed.pop(0)
            
        dfa = DFA (self.S, new_K, new_q0, new_d, new_F)
        
        #print(dfa)
        return dfa

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.  
        new_K = set()
        new_d = {}
        new_F = set()
        
        for state in self.K:
            new_K.add(f(state))
        for state in self.F:
            new_F.add(f(state))
        for key, value in self.d.items():
            new_d[(f(key[0]), key[1])] = {f(x) for x in value}
        
        nfa = NFA(self.S,new_K,f(self.q0),new_d,new_F)
        return nfa
