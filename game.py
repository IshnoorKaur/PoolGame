import Physics;
import math;
import random;

def nudge():
    return random.uniform( -1.5, 1.5 );

def createTB(table):
#Create a table
#table = Physics.Table();

    # 1 ball
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0,
                Physics.TABLE_WIDTH / 2.0,
                );

    sb = Physics.StillBall( 1, pos );
    table += sb;

    # Row 2
    # 2 ball
    pos = Physics.Coordinate(
                Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 +
                nudge(),
                Physics.TABLE_WIDTH/2.0 - 
                math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                nudge()
                );
    sb = Physics.StillBall( 2, pos );
    table += sb;

    # 14 ball
    pos = Physics.Coordinate(
                Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                nudge(),
                Physics.TABLE_WIDTH/2.0 - 
                math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                nudge()
                );
    sb = Physics.StillBall( 14, pos );
    table += sb;

    # Row 3
    # 13 ball 
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 5.0) + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER*2.0)+10.0) + nudge(),
                );

    sb = Physics.StillBall( 13, pos );
    table += sb;

    # 8 ball
    pos = Physics.Coordinate(
                Physics.TABLE_WIDTH / 2.0 + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 2.0) + 10.0) + nudge() # Adjust as needed for alignment
                );
    sb = Physics.StillBall(8, pos);
    table += sb;

    # 10 ball 
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 2.0)-42.0) + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 2.0) +10.0) + nudge(),
                );

    sb = Physics.StillBall( 10, pos );
    table += sb;

    # Row 4 
    # 6 ball
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * (Physics.BALL_DIAMETER + 50.0 ) + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 3.0) + 20.0) + nudge(),
                );

    sb = Physics.StillBall( 6, pos );
    table += sb;

    # 15 ball
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * (Physics.BALL_DIAMETER - 20.0) + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 3.0) + 20.0) + nudge(),
                );

    sb = Physics.StillBall( 15, pos );
    table += sb;

    # 12 ball
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * (Physics.BALL_DIAMETER - 90.0) + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 3.0) + 20.0) + nudge(),
                );

    sb = Physics.StillBall( 12, pos );
    table += sb;

    # 3 ball
    pos = Physics.Coordinate( 
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * (Physics.BALL_DIAMETER - 160.0) + nudge(),
                Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 3.0) + 20.0) + nudge(),
                );

    sb = Physics.StillBall( 3, pos );
    table += sb;

    # Row 5 
    # 4 ball
    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 4.0) + 25.0) + nudge() # Adjust as needed for alignment
        );
    sb = Physics.StillBall(4, pos)
    table += sb

    # 7 ball
    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 3.0) - 25.0) + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 4.0) + 25.0) + nudge() # Adjust as needed for alignment
        );
    sb = Physics.StillBall(7, pos)
    table += sb

    # 9 ball
    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 2.0) - 40.0) + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 4.0) + 25.0) + nudge() # Adjust as needed for alignment
        );
    sb = Physics.StillBall(9, pos)
    table += sb

    # 11 ball
    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * (Physics.BALL_DIAMETER - 130.0) + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 4.0) + 25.0) + nudge() # Adjust as needed for alignment
        );
    sb = Physics.StillBall(11, pos)
    table += sb

    # 5 ball
    pos = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * (Physics.BALL_DIAMETER - 200.0) + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0)/2.0 * ((Physics.BALL_DIAMETER * 4.0) + 25.0) + nudge() # Adjust as needed for alignment
        );  
    sb = Physics.StillBall(5, pos)
    table += sb

    # cue ball also still
    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + 3.0,
                          Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
    sb  = Physics.StillBall( 0, pos );
    table += sb;


    return table;

#db = Physics.Database(True)
#db.createDB()


#game = Physics.Game(gameName=game_name, player1Name=player1_name, player2Name=player2_name)

if __name__ == "__main__":
    table = Physics.Table()
    table = createTB(table)
    print(table)