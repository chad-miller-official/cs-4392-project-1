#!/usr/bin/python

import sys

triangle_num = lambda n : ( n * ( n + 1 ) ) / 2
avg          = lambda a, b : ( a + b ) / 2

def get_x_and_y( n ):
    def get_x( row, n ):
        return row - 1 if n <= triangle_num( row ) - 1 else get_x( row + 1, n )
    
    x = get_x( 0, n )
    y = [ i for i in range( len( neighbors[x] ) ) if neighbors[x][i] == n ][0]
    return ( x, y )

class Move( object ):
    def __init__( self, start, end ):
        global neighbors
        
        self.start  = start
        self.end    = end
        x1, y1      = get_x_and_y( start )
        x2, y2      = get_x_and_y( end )
        self.middle = neighbors[avg( x1, x2 )][avg( y1, y2 )]

class Board( object ):
    def __init__( self, empty, history=[] ):
        global num_holes
        
        self.holes   = [ ( i in empty ) for i in range( num_holes ) ]
        self.history = list( history )
        self.moves   = []
        
        for i in [ i for i in range( len( self.holes ) ) if self.holes[i] ]:
            for j in self.get_two_away_neighbors( i ):
                self.moves.append( Move( j, i ) )
            
    def get_two_away_neighbors( self, n ):
        global neighbors
        
        retval = []
        i, j   = get_x_and_y( n )
        
        try:
            if i - 2 >= 0 and j - 2 >= 0 and not self.holes[neighbors[i - 1][j - 1]] and not self.holes[neighbors[i - 2][j - 2]]:
                retval.append( neighbors[i - 2][j - 2] )
        except:
            pass
    
        try:
            if i - 2 >= 0 and not self.holes[neighbors[i - 1][j]] and not self.holes[neighbors[i - 2][j]]:
                retval.append( neighbors[i - 2][j] )
        except:
            pass
        
        try:
            if j - 2 >= 0 and not self.holes[neighbors[i][j - 1]] and not self.holes[neighbors[i][j - 2]]:
                retval.append( neighbors[i][j - 2] )
        except:
            pass

        try:
            if not self.holes[neighbors[i][j + 1]] and not self.holes[neighbors[i][j + 2]]:
                retval.append( neighbors[i][j + 2] )
        except:
            pass

        try:
            if not self.holes[neighbors[i + 1][j]] and not self.holes[neighbors[i + 2][j]]:
                retval.append( neighbors[i + 2][j] )
        except:
            pass

        try:
            if not self.holes[neighbors[i + 1][j + 1]] and not self.holes[neighbors[i + 2][j + 2]]:
                retval.append( neighbors[i + 2][j + 2] )
        except:
            pass

        return retval
    
    def num_pegs( self ):
        return len( [ h for h in self.holes if not h ] )
    
    def execute_move( self, move ):
        next_holes = [ i for i in range( len( self.holes ) ) if self.holes[i] ] + [move.start] + [move.middle]
        next_holes.remove( move.end )
        next_history = list( self.history ) + [move]
        return Board( next_holes, next_history )

def solve_board( board ):
    global best, best_num_pegs
    
    if board.num_pegs() > best_num_pegs:
        if len( board.moves ) > 0:
            for move in board.moves:
                solve_board( board.execute_move( move ) )
        else:
            best = board
            best_num_pegs = board.num_pegs()

if __name__ == "__main__":
    global size, num_holes, neighbors, best, best_num_pegs
    
    args = sys.argv[1:]
    
    if len( args ) != 2 or args[0] != "-s":
        sys.exit( "Usage: ./Game.py -s [board size]" )
    
    size          = int( args[1] )
    num_holes     = triangle_num( size )
    neighbors     = [ range( triangle_num( i ), triangle_num( i + 1 ) ) for i in range( size ) ]
    best          = Board( [i for i in range( num_holes )] )
    best_num_pegs = best.num_pegs()
    
    for i in range( size ):
        solve_board( Board( [i] ) )
    
    print( str( best.history[0].end + 1 ) + ", " + str( len( best.history ) ) )
    
    for move in best.history:
        print( str( move.start + 1 ) + ", " + str( move.end + 1 ) )
    
