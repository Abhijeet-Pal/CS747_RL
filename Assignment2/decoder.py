import argparse
import numpy as np

def read_file_opponent(location):
    with open (location, 'r') as file:
        r_policy = {}
        r_policy['state'] = []
        for data in file:
            st = data.strip()
            st = st.split()
            if (st[0]=='state'):
                continue
            else:
                state = str(st[0])
                # print(state)
                r_policy['state'].append(state)
                r_policy[state] = (float(st[1]), float(st[2]), float(st[3]), float(st[4]))
    return r_policy

def read_file(location):
    value = []
    action = []
    with open (location, 'r') as file:
        for data in file:
            st = data.strip()
            st = st.split()
            # print(st)
            value.append(st[0])
            action.append(st[1])

    return value, action

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--value-policy', type = str, required = True)
    parser.add_argument('--opponent', type = str, required = True)
    args = parser.parse_args()
    location_val = args.value_policy
    # print(location_val)
    location_opp = args.opponent
    value, action = read_file(location_val)
    mdp_opponent = read_file_opponent(location_opp)
    for i in range (len(mdp_opponent['state'])):
        state = mdp_opponent['state'][i]
        print(f'{state} {action[i]} {value[i]}')
