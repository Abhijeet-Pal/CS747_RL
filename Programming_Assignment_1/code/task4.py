"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the MultiBanditsAlgo class. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, set_pulled, reward): This method is called 
        just after the give_pull method. The method should update the 
        algorithm's internal state based on the arm that was pulled and the 
        reward that was received.
        (The value of arm_index is the same as the one returned by give_pull 
        but set_pulled is the set that is randomly chosen when the pull is 
        requested from the bandit instance.)
"""

import numpy as np

# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE


class MultiBanditsAlgo:
    def __init__(self, num_arms, horizon):
        # You can add any other variables you need here
        self.num_arms = num_arms
        self.horizon = horizon
        self.success1 = np.zeros(num_arms)
        self.failure1 = np.zeros(num_arms)
        self.success2 = np.zeros(num_arms)
        self.failure2 = np.zeros(num_arms)
        self.result = np.zeros(num_arms)
        self.counts1 = 0
        self.counts2 = 0
        # START EDITING HERE
        
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        choice = np.random.randint(2)
        if choice == 0:
            self.counts1+=1
        else:
            self.counts2+=1

        for i in range (self.num_arms):
            self.result[i] = (np.random.beta(self.success1[i]+1,self.failure1[i]+1)+np.random.beta(self.success2[i]+1,self.failure2[i]+1))/2
        ls = list(self.result)
        return ls.index(max(ls))
    
        # END EDITING HERE
    
    def get_reward(self, arm_index, set_pulled, reward):
        # START EDITING HERE
        if set_pulled==0:
                if reward ==1:
                    self.success1[arm_index]+=1
                else:
                    self.failure1[arm_index]+=1
        else:
            if reward ==1:
                self.success2[arm_index]+=1
            else:
                self.failure2[arm_index]+=1

        # END EDITING HERE
