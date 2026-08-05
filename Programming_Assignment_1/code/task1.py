"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

# START EDITING HERE
# You can use this space to define any helper functions that you need

# END EDITING HERE
class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.result = np.zeros(num_arms)
        # END EDITING HERE

    def give_pull(self):
        # START EDITING HERE
        t = np.sum(self.counts)
        log_val = math.log(t+1)
        for i in range (self.num_arms):
            exploration = np.sqrt(2 *log_val / (self.counts[i] + 1e-7))
            self.result[i] = self.values[i] + exploration
        ls = list(self.result)
        return ls.index(max(ls))
        # END EDITING HERE  
        
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        # copied from given get_reward in Eps_Greedy function
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.ones(num_arms)* 0.5
        self.c = 0
        # END EDITING HERE
    
    def kl_divergence(self,p,q):
        if p==0:
            p=1e-6
        elif p==1:
            p=1-1e-6
        elif q==0:
            q=1e-6
        elif q==1:
            q=1-1e-6
        divergence = p*math.log(p/q) + (1-p)*math.log((1-p)/(1-q))
        return divergence

    
    def klucb_max_val(self, arm):
        t = np.sum(self.counts)
        val = (math.log(t+1) + self.c*math.log(math.log(t+1)))/(self.counts[arm])
        low = self.values[arm]
        high = 1
        while high-low > 1e-3:
            mid = (high+low)/2
            kl_val = self.kl_divergence(self.values[arm],mid)
            if kl_val <  val:
                low = mid
            else:
                high = mid
        
        return (low+high)/2


    def give_pull(self):
        # START EDITING HERE
        result = []
        for i in range (self.num_arms):
            if (self.counts[i]==0):
                return i
        for i in range (self.num_arms):
            result.append(self.klucb_max_val(i))
        return result.index(max(result))

        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE

class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.success = np.zeros(num_arms)
        self.failure = np.zeros(num_arms)
        self.result = np.zeros(num_arms)
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        for i in range (self.num_arms):
            self.result[i] = np.random.beta(self.success[i]+1, self.failure[i]+1)
        ls = list(self.result)
        return ls.index(max(ls))
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        if (reward == 1):
            self.success[arm_index]+=1
        else:
            self.failure[arm_index]+=1
        # END EDITING HERE
