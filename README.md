# CS 4392 Project 1
Exploring different programming languages.

## How to solve
The board is represented as a completely disconnected graph.
Every iteration, calculate the edges between the holes.
An edge exists between an empty hole and every non-empty hole that is 2 away from it.
Each edge represents a move.
Test all possible moves, and for each move, calculate the resulting edge set.
Use the move that produces the graph that has the least number of edges (i.e., the least number of moves possible from that board).
Repeat this process until the board has no more edges (no more moves).
