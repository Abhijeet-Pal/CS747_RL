import os
import sys
import random 
import json
import math
import utils
import time
import config
import numpy
random.seed(73)

class Agent:
    def __init__(self, table_config) -> None:
        self.table_config = table_config
        self.prev_action = None
        self.curr_iter = 0
        self.state_dict = {}
        self.holes =[]
        self.ns = utils.NextState()


    def set_holes(self, holes_x, holes_y, radius):
        for x in holes_x:
            for y in holes_y:
                self.holes.append((x[0], y[0]))
        self.ball_radius = radius


    def action(self, ball_pos=None):
        ## Code you agent here ##
        ## You can access data from config.py for geometry of the table, configuration of the levels, etc.
        ## You are NOT allowed to change the variables of config.py (we will fetch variables from a different file during evaluation)
        ## Do not use any library other than those that are already imported.
        ## Try out different ideas and have fun!
        hole_pos = self.holes
        ball_rad = self.ball_radius
        def distance (ball1, ball2):
            dist = numpy.sqrt((ball1[0]-ball2[0])**2 + (ball1[1] - ball2[1])**2)
            return dist
        def angle (ball,hole):
            angle = -(math.atan2(hole[0]-ball[0], -hole[1]+ball[1]))/numpy.pi
            return angle      
          
        cue_pos = ball_pos['white']
        ball_dist = []
        for type, ball in ball_pos.items():
            if type != 'white' and type !=0:
                ball_dist.append(distance(cue_pos, ball))
        min_dist = numpy.min(ball_dist)

        for type, ball in ball_pos.items():
            if type != 'white' and type != 0:
                if distance(cue_pos, ball) == min_dist:
                    break
    

        dist = []
        for hole in hole_pos:
            dist.append(distance(hole, ball))
        position = numpy.argmin(dist)
        hole = hole_pos[position]

        ang_ch = angle(cue_pos, hole)
        ang_bh = angle(ball, hole)
        ang_cb = angle(cue_pos, ball)
        ball_hole_vec = (numpy.array(hole) - numpy.array(ball))/ distance(ball, hole)

        ang_cb_err = angle(cue_pos,(ball - 1.9*ball_rad* ball_hole_vec))
        ang_diff = ang_ch - ang_bh
        angle_final = ang_cb_err

        if (ang_cb == ang_bh):
            angle_final = ang_bh
        dist_hole_cue = distance(hole, cue_pos)
        force = max(((dist_hole_cue/distance(hole_pos[0], hole_pos[-1])),0.5))
        return angle_final, force
