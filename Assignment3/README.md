# Optimal Cue-stick Control (CS747 Programming Assignment 3)

This repository contains my solution for **Programming Assignment 3** of **CS747: Foundations of Intelligent and Learning Agents** at IIT Bombay.

## Problem Statement

The original assignment specification can be found below

**CS747 Programming Assignment 3 – Optimal Cue-stick Control**  
https://www.cse.iitb.ac.in/~shivaram/teaching/old/cs747-a2023/pa-3/pa-3.html



## Overview

The objective of the assignment was to design an autonomous billiards agent that selects the optimal **cue angle** and **force** to pocket all balls within a limited number of shots. The agent receives the current table state (ball positions) and outputs an action `(angle, force)`.

## Approach

My solution uses:
- Geometric calculations for shot planning.
- Hole selection based on feasible pocketing angles.
- Collision-aware target selection.
- Limited forward simulation using the provided `get_next_state()` utility to evaluate candidate shots.
- Force tuning to improve shot accuracy under stochastic angle noise.
