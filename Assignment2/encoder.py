import argparse
import numpy as np

def read_file(location):
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

def get_position(state):
    b1_pos = state[0:2]
    b2_pos = state[2:4]
    r_pos = state[4:6]
    ball_pos = int(state[6:7])
    return [int(b1_pos),int(b2_pos), int(r_pos),int(ball_pos)]

def x_y_pos(element_pos):
    num = int(element_pos)
    x_cor = (num-1)%4
    y_cor = (num-1)//4
    return x_cor, y_cor

def pos(x_cor, y_cor):
    num = 1+ (y_cor * 4 + x_cor)
    return num
def r_new_pos(r_pos_x_old, r_pos_y_old):
    r_new_x = []
    r_new_y = []
    r_new_x.append(r_pos_x_old-1)
    r_new_x.append(r_pos_x_old+1)
    r_new_x.append(r_pos_x_old)
    r_new_x.append(r_pos_x_old)
    r_new_y.append(r_pos_y_old)
    r_new_y.append(r_pos_y_old)
    r_new_y.append(r_pos_y_old-1)
    r_new_y.append(r_pos_y_old+1)
    return r_new_x, r_new_y

def inline(x1,y1,x2,y2,rx,ry):
    if (x1 == x2 == rx and (y1<= ry <= y2 or y2<=ry<=y1 )):
        return True
    elif ((y1 == y2 == ry) and (x1<=rx<=x2 or x2<=rx<=x1)):
        return True
    elif ((x1+y1 == x2+y2 == rx+ry) and (x1<=rx<=x2) and (y1>=ry>=y2)):
        return True
    elif ((x1+y1 == x2+y2 == rx+ry) and (x2<=rx<=x1) and (y1<=ry<=y2)):
        return True
    elif ((x1-y1 == x2-y2 == rx-ry) and (x1<=rx<=x2) and (y1<=ry<=y2)):
        return True
    elif ((x1-y1 == x2-y2 == rx-ry) and (x2<=rx<=x1) and (y2<=ry<=y1)):
        return True
    else:
        return False
def get_state(state_str ,r_policy):
    lis = r_policy['state']
    return lis.index(state_str)



def shoot(state, init_position, r_policy, q, state_encoded):
    b1_pos = init_position[0]
    b2_pos = init_position[1]
    r_pos = init_position[2]
    ball_pos = init_position[3]
    prob_values = r_policy[state]
    r_pos_x_old, r_pos_y_old = x_y_pos(r_pos)
    r_new_x, r_new_y = r_new_pos(r_pos_x_old, r_pos_y_old)
    if ball_pos ==1:
        x1, y1 = x_y_pos(b1_pos)
    else:
        x1, y1 = x_y_pos(b2_pos)
    prob_sum = 0
    prob = 0

    for i in range (len(prob_values)):
        if prob_values[i]<=0:
            continue
        else:
            if (pos(r_new_x[i], r_new_y[i]) == 8 or pos(r_new_x[i], r_new_y[i]) ==12):
                prob =prob_values[i] * 0.5* (q-0.2*(3-x1))
                prob_sum += prob
                # print(f'transition {state_encoded} 9 8192 1 {prob} ')
            else:
                prob=prob_values[i] *(q-0.2*(3-x1))
                prob_sum += prob
                # print(f'transition {state_encoded} 9 8192 1 {prob} ')

                #8192 -- goal
                #8193 -- end
    print (f'transition {state_encoded} 9 8192 1 {prob_sum}')
    print(f'transition {state_encoded} 9 8193 0 {1-prob_sum}')


def passing(state, init_position, r_policy, q, state_encoded):
    b1_pos = init_position[0]
    b2_pos = init_position[1]
    r_pos = init_position[2]
    ball_pos = init_position[3]
    prob_values = r_policy[state]
    r_pos_x_old, r_pos_y_old = x_y_pos(r_pos)
    r_new_x, r_new_y = r_new_pos(r_pos_x_old, r_pos_y_old)

    x1, y1 = x_y_pos(b1_pos)
    x2, y2 = x_y_pos(b2_pos)
    prob = 0
    prob_sum = 0
    if ball_pos == 1:
        after_pass =2
    else:
        after_pass = 1

    for i in range (len(prob_values)):
        if prob_values[i]<=0:
            continue
        else:

            if (inline(x1,y1,x2,y2,r_new_x[i],r_new_y[i])):
                prob = prob_values[i] * 0.5 * (q - 0.1* max( abs(x1-x2) , abs(y1-y2)))
                prob_sum+=prob
                stri=str(b1_pos).zfill(2)+str(b2_pos).zfill(2)+str(pos(r_new_x[i], r_new_y[i])).zfill(2)+str(after_pass)
                state2 = get_state(stri, r_policy)
                print(f'transition {state_encoded} 8 {state2} 0 {prob} ')

            else:
                prob = prob_values[i]  * (q - 0.1* max( abs(x1-x2) , abs(y1-y2)))
                prob_sum+=prob
                stri=str(b1_pos).zfill(2)+str(b2_pos).zfill(2)+str(pos(r_new_x[i], r_new_y[i])).zfill(2)+str(after_pass)
                state2 = get_state(stri, r_policy)
                print(f'transition {state_encoded} 8 {state2} 0 {prob} ')

    print(f'transition {state_encoded} 8 8193 0 {1-prob_sum}')


def move(state, init_position, r_policy, p, q, state_encoded):
    b1_pos = init_position[0]
    b2_pos = init_position[1]
    r_pos = init_position[2]
    ball_pos = init_position[3]
    # print('init_pos', ball_pos)
    prob_values = r_policy[state]
    r_pos_x_old, r_pos_y_old = x_y_pos(r_pos)
    r_new_x, r_new_y = r_new_pos(r_pos_x_old, r_pos_y_old)
    b1_x_old, b1_y_old = x_y_pos(b1_pos)
    b2_x_old , b2_y_old = x_y_pos(b2_pos)
    prob = 0
    prob_sum = 0
    action = [0,1,2,3,4,5,6,7]
    b1_x_new, b1_y_new = r_new_pos(b1_x_old, b1_y_old)
    b2_x_new, b2_y_new = r_new_pos(b2_x_old, b2_y_old)

    for ac in action:
        prob_fail = 0
        if ac<=3:
            move = 1
        else:
            move = 2

        if (ball_pos == 1 and move == 2):
            if (b2_x_new[ac%4] < 0 or b2_x_new[ac%4] >= 4 or b2_y_new[ac%4] < 0 or b2_y_new[ac%4] >= 4):
                print(f'transition {state_encoded} {ac} 8193 0 1')
                continue
            else:
                prob_sum = 0
                for k in range (len(r_new_x)):
                    if prob_values[k]<=0:
                        continue
                    else:

                        st = str(b1_pos).zfill(2) + str(pos(b2_x_new[ac%4], b2_y_new[ac%4])).zfill(2) + str(pos(r_new_x[k], r_new_y[k])).zfill(2) + str(ball_pos)
                        state2 = get_state(st, r_policy)
                        prob_sum+=(1-p)*prob_values[k]
                        print(f'transition {state_encoded} {ac} {state2} 0 {(1-p)*prob_values[k]}')
                print(f'transition {state_encoded} {ac} 8193 0 {1-prob_sum}')
                
        elif (ball_pos==2 and move==1):
                if (b1_x_new[ac%4] < 0 or b1_x_new[ac%4] >= 4 or b1_y_new[ac%4] < 0 or b1_y_new[ac%4] >= 4):
                    print(f'transition {state_encoded} {ac} 8193 0 1')
                    continue
                else:
                    prob_sum=0
                    for k in range (len(r_new_x)):
                        if (prob_values[k] <=0):
                            continue
                        else:
                            st = str(pos(b1_x_new[ac%4], b1_y_new[ac%4])).zfill(2) + str(b2_pos).zfill(2) + str(pos(r_new_x[k], r_new_y[k])).zfill(2) + str(ball_pos)
                            state2 = get_state(st, r_policy)
                            prob_sum+=(1-p)*prob_values[k]
                            print(f'transition {state_encoded} {ac} {state2} 0 {(1-p)*prob_values[k]}')
                    print(f'transition {state_encoded} {ac} 8193 0 {1-prob_sum}')

        elif (ball_pos == 1 and move == 1):
                if (b1_x_new[ac%4] < 0 or b1_x_new[ac%4] >= 4 or b1_y_new[ac%4] < 0 or b1_y_new[ac%4] >= 4):
                    print(f'transition {state_encoded} {ac} 8193 0 1')
                    continue
                else:
                    for k in range (len(r_new_x)):
                        if (prob_values[k] <=0):
                            continue
                        else:

                            if ((r_new_x[k] == b1_x_new[ac%4] and r_new_y[k] == b1_y_new[ac%4]) or ((r_new_x[k] == b1_x_old and r_new_y[k] == b1_y_old) and (b1_x_new[ac%4] == r_pos_x_old and b1_y_new[ac%4] == r_pos_y_old))):
                                prob_fail += ((1-2*p) * 0.5 + 2*p)* prob_values[k]
                                st = str(pos(b1_x_new[ac%4], b1_y_new[ac%4])).zfill(2) + str(b2_pos).zfill(2) + str(pos(r_new_x[k], r_new_y[k])).zfill(2) + str(ball_pos)
                                state2 = get_state(st, r_policy)
                                print(f'transition {state_encoded} {ac} {state2} 0 {0.5*(1-2*p)*prob_values[k]}')
                            else:
                                st =str(pos(b1_x_new[ac%4], b1_y_new[ac%4])).zfill(2) + str(b2_pos).zfill(2) + str(pos(r_new_x[k], r_new_y[k])).zfill(2) + str(ball_pos)
                                state2 = get_state(st, r_policy)
                                print(f'transition {state_encoded} {ac} {state2} 0 {(1-2*p)*prob_values[k]}')
                                prob_fail += 2*p * prob_values[k]
                    print(f'transition {state_encoded} {ac} 8193 0 {prob_fail}')
        
        
        elif (ball_pos == 2 and move == 2):
            if (b2_x_new[ac%4] < 0 or b2_x_new[ac%4] >= 4 or b2_y_new[ac%4] < 0 or b2_y_new[ac%4] >= 4):
                print(f'transition {state_encoded} {ac} 8193 0 1')
                continue
            else:
                for k in range (len(r_new_x)):
                    if (prob_values[k]<=0):
                        continue
                    else:
                        if ((r_new_x[k] == b2_x_new[ac%4] and r_new_y[k] == b2_y_new[ac%4]) or (r_new_x[k] == b2_x_old and r_new_y[k] == b2_y_old and b2_x_new[ac%4] == r_pos_x_old and b2_y_new[ac%4] == r_pos_y_old)):
                            prob_fail += ((1-2*p) * 0.5 + 2*p)* prob_values[k]
                            st =str(b1_pos).zfill(2) + str(pos(b2_x_new[ac%4], b2_y_new[ac%4])).zfill(2) + str(pos(r_new_x[k], r_new_y[k])).zfill(2) + str(ball_pos)
                            state2 = get_state(st, r_policy)
                            print(f'transition {state_encoded} {ac} {state2} 0 {0.5*(1-2*p)*prob_values[k]}')
                        else:
                            st =str(b1_pos).zfill(2) + str(pos(b2_x_new[ac%4], b2_y_new[ac%4])).zfill(2) + str(pos(r_new_x[k], r_new_y[k])).zfill(2) + str(ball_pos)
                            state2 = get_state(st, r_policy)
                            print(f'transition {state_encoded} {ac} {state2} 0 {(1-2*p)*prob_values[k]}')
                            prob_fail += 2*p * prob_values[k]
                print(f'transition {state_encoded} {ac} 8193 0 {prob_fail}')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--opponent', type = str, required = True)
    parser.add_argument('--p', type = float, required = True)
    parser.add_argument('--q', type = float, required = True)
    args = parser.parse_args()

    opponent_file_loc = args.opponent
    p = args.p
    q = args.q
    r_policy = read_file(opponent_file_loc)
    print(f'numStates {8194}')
    print(f'numActions {10}')
    print(f'end 8192 8193')
    # print(len(r_policy['state']))
    for i in range (len(r_policy['state'])):
        state = r_policy['state'][i]
        init_position = get_position(state)
        move(state, init_position, r_policy, p, q, i )
        passing(state, init_position, r_policy, q, i)
        shoot(state, init_position, r_policy, q, i)
    print(f'mdptype episodic')
    print(f'discount {1}')







    
