import numpy as np
import argparse
import pulp

def read_file(location):
    numStates = np.zeros(1)
    numActions = np.zeros(1)
    mdptype = np.zeros(1)
    discount = np.zeros(1)
    mdp_dict = {}
    with open (location, 'r') as file:
        for data in file:
            st = data.strip()
            st = st.split()
            if st[0] == 'numStates':
                mdp_dict['numStates'] = int(st[1])
            elif st[0] =='numActions':
                mdp_dict['numActions'] = int(st[1])
                mdp_dict['transition_reward'] = [[[] for i in range (mdp_dict['numActions'])] for j in range (mdp_dict['numStates'])]
            elif st[0] == 'discount':
                mdp_dict['discount'] = float(st[1])
            elif st[0] == 'mdptype':
                mdp_dict['mdptype'] = str(st[1])
            elif st[0] == 'end':
                mdp_dict['end'] = st[1:]
            elif st[0] == 'transition':
                mdp_dict['transition_reward'][int(st[1])][int(st[2])]. append((int (st[3]), float(st[4]), float(st[5])))
    return mdp_dict
        

def find_policy(policy_path):
    policy = []
    with open (policy_path, 'r') as file:
        for data in file:
            st = data.strip()
            st = st.split()
            policy.append(int(st[0]))
    return policy


def val_policy(mdp_dict, policy):

    numStates= mdp_dict['numStates']
    numActions = mdp_dict['numActions']
    transition_reward = mdp_dict['transition_reward']
    discount = mdp_dict['discount']
    value = np.zeros(numStates)
    while True:
        new_value = np.zeros(numStates)

        for s in range(numStates):
            term1 = 0
            term2 = 0
            for j in range(len(transition_reward[s][policy[s]])):    
                s_prime = transition_reward[s][policy[s]][j][0] 
                term1 += transition_reward[s][policy[s]][j][2] * transition_reward[s][policy[s]][j][1]
                term2 += discount * transition_reward[s][policy[s]][j][2] * value[s_prime]
            new_value[s] = term1 + term2
        if np.allclose(new_value, value, rtol=0, atol = 1e-12):
            break
        value = new_value
    return value


def val_iter (mdp_dict):
    numStates= mdp_dict['numStates']
    numActions = mdp_dict['numActions']
    transition_reward = mdp_dict['transition_reward']
    discount = mdp_dict['discount']
    value = np.zeros(numStates)

    while True:
        new_val = np.zeros_like(value)  
        for s in range(numStates):
            max_val = -float('inf') 
            for a in range(numActions):
                expected_reward = 0
                expected_future_value = 0
                for j in range(len(transition_reward[s][a])):
                    s_prime = transition_reward[s][a][j][0]
                    expected_reward += transition_reward[s][a][j][2] * transition_reward[s][a][j][1]
                    expected_future_value += discount * transition_reward[s][a][j][2] * value[s_prime]
                sum = expected_reward +  expected_future_value
                max_val = max(max_val, sum)
            new_val[s] = max_val
        if np.allclose(new_val,value,rtol=0, atol = 1e-10):
            break
        value = new_val

    
    policy = np.zeros(numStates, dtype = int)
    for s in range (numStates):
        max_expec_val = -np.inf
        best_action = None
        for a in range(numActions):
            total_expected_value = 0
            for j in range (len(transition_reward[s][a])):
                s_prime = transition_reward[s][a][j][0]
                total_expected_value += np.sum(transition_reward[s][a][j][2] * transition_reward[s][a][j][1]) + discount * np.sum(transition_reward[s][a][j][2] * new_val[s_prime])
            if total_expected_value > max_expec_val:
                max_expec_val = total_expected_value
                best_action = a
        policy[s] = best_action
    return new_val, policy
 
def hpi_algo(mdp_dict):
    numStates= mdp_dict['numStates']
    numActions = mdp_dict['numActions']
    transition_reward = mdp_dict['transition_reward']
    discount = mdp_dict['discount']
    policy = np.zeros(numStates, dtype= int)
    new_policy = np.zeros(numStates, dtype=int)
    while True:
        value = val_policy(mdp_dict, policy)        
        policy_stable = True
        for s in range(numStates):
            best_action = policy[s]
            max_value = float('-inf')
            for a in range(numActions):
                term1 = 0
                term2 = 0
                for j in range(len(transition_reward[s][a])):
                    s_prime = transition_reward[s][a][j][0]
                    term1 += transition_reward[s][a][j][2] * transition_reward[s][a][j][1]
                    term2 += discount * transition_reward[s][a][j][2] * value[s_prime]    
                total = term1 + term2    
                if total > max_value:
                    max_value = total
                    best_action = a
            if best_action != policy[s]:
                policy_stable = False  
                new_policy[s] = best_action
        if policy_stable:
            break
        policy = new_policy.copy()
    return val_policy(mdp_dict, policy), policy

def lp_algo (mdp_dict):
    numStates= mdp_dict['numStates']
    numActions = mdp_dict['numActions']
    transition_reward = mdp_dict['transition_reward']
    discount = mdp_dict['discount']
    prob = pulp.LpProblem("MDP_Assignment", pulp.LpMinimize)
    value_vars = [pulp.LpVariable(f"value_{i}", lowBound=0) for i in range(numStates)]
    prob += pulp.lpSum(value_vars)
    value = np.array(value_vars)
    for s in range(numStates):
        for a in range(numActions):
            constraint_expr = 0  # Initialize constraint expression
            for j in range(len(transition_reward[s][a])):
                s_prime, reward, prob_sprime = transition_reward[s][a][j]
                constraint_expr += prob_sprime * (reward + discount * value_vars[s_prime])
            prob += value_vars[s] >= constraint_expr
    prob.solve(pulp.apis.PULP_CBC_CMD(msg = False))
    value = np.array([v.varValue for v in value])


    policy = np.zeros(numStates, dtype = int)
    for s in range (numStates):
        max_expec_val = -np.inf
        best_action = None
        for a in range(numActions):
            total_expected_value = 0
            for j in range (len(transition_reward[s][a])):
                s_prime = transition_reward[s][a][j][0]
                total_expected_value += np.sum(transition_reward[s][a][j][2] * transition_reward[s][a][j][1]) + discount * np.sum(transition_reward[s][a][j][2] * value[s_prime])
            if total_expected_value > max_expec_val:
                max_expec_val = total_expected_value
                best_action = a
        policy[s] = best_action
    return value, policy


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mdp', type = str, required = True)
    parser.add_argument('--algorithm', type = str, default = 'vi')
    parser.add_argument('--policy', type = str, required = False)
    args = parser.parse_args()
    mdp_list = read_file(args.mdp)

    if args.policy != None:
        policy = find_policy(args.policy)
        val = val_policy (mdp_list, policy)
        for i in range (len(val)):
            print(f'{val[i]:.6f} {int(policy[i])}')
    else:
        if args.algorithm == 'vi':
            val, policy = val_iter(mdp_list)
            for i in range (len(val)):
                print(f'{val[i]:.6f} {int(policy[i])}')
        elif args.algorithm == 'hpi':
            val, policy = hpi_algo(mdp_list)
            for i in range (len(val)):
                print(f'{val[i]:.6f} {int(policy[i])}')
        elif args.algorithm == 'lp':
            val, policy = lp_algo(mdp_list)
            for i in range (len(val)):
                print(f'{val[i]:.6f} {int(policy[i])}')