import phylib;
import sqlite3; 
import os;

from math import sqrt, floor;
import random;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

FRAME_INTERVAL = 0.01;

# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """<line x1="0" x2="0" y2="0" y1="0" stroke="black"/>
</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;

    # add an svg method here
    def svg(self):
        """
        Generates the SVG representation of the StillBall.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])

################################################################################

class RollingBall(phylib.phylib_object):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number, position (x,y), velocity (x,y), 
        and acceleration (x,y) as arguments.
        """

        #Call phylib_object with appropriate parameters
        phylib.phylib_object.__init__(  self,
                                        phylib.PHYLIB_ROLLING_BALL,
                                        number,
                                        pos,
                                        vel,
                                        acc,
                                        0.0, 0.0)
        
        #set class to rolling ball 
        self.__class__=RollingBall;

    # add an svg method here
    def svg(self):
        """
        Generates the SVG representation of the RollingBall.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % ( self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])

################################################################################

class Hole(phylib.phylib_object):
    """
    Hole class.
    """

    def __init__(self,pos):
        """
        Constructor function, requires position (x,y) as arguments.
        """
        #Call phylib_object with appropriate parameters
        phylib.phylib_object.__init__(  self,
                                        phylib.PHYLIB_HOLE,
                                        0,
                                        pos,
                                        None,
                                        None,
                                        0.0, 0.0)

        # Set the class of the object to Hole
        self.__class__ = Hole
        
        # add an svg method here
    def svg(self):
        """
        Generates the SVG representation of the Hole.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)

################################################################################
class HCushion(phylib.phylib_object):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y-coordinate as argument.
        """

        # Call the phylib_object constructor with appropriate parameters
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,
                                      None,
                                      None,
                                      None,
                                      0.0, y)
      
        # Set the class of the object to HCushion
        self.__class__ = HCushion

    # add an svg method here
    def svg(self):
        """
        Generates the SVG representation of the HCushion.
        """
        
        if self.obj.hcushion.y == 0.0:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        else:
            return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (2700)

################################################################################

class VCushion(phylib.phylib_object):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires x-coordinate as argument.
        """

        # Call the phylib_object constructor with appropriate parameters
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,
                                      None,
                                      None,
                                      None,
                                      x, 0.0)
      
        # Set the class of the object to VCushion
        self.__class__ = VCushion

    # add an svg method here
    def svg(self):
        """
        Generates the SVG representation of the VCushion.
        """
        if self.obj.vcushion.x == 0.0:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        else:
            return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (1350)

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg(self):
        """
        Generates the SVG representation of the table and its objects.
        """
        svg_string = HEADER # Assuming HEADER is defined somewhere
        for obj in self: 
            if obj:
                svg_string += obj.svg()  # Assuming obj has a svg method
        svg_string += FOOTER  # Assuming FOOTER is defined somewhere
        return svg_string

    # roll method provided to us 
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall(   ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                        ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

###############################################################################
    
class Database():
    
    def __init__(self, reset=False):
        if(reset==True):
            if os.path.exists('phylib.db'):
                os.remove('phylib.db')
        Database.conn = sqlite3.connect('phylib.db')

    def createDB(self):

        # create database file if it doesn't exist and connect to it
        Database.conn = sqlite3.connect( 'phylib.db' ); #.connect command here is unique to sqlite

        curs = Database.conn.cursor();

        # Table represents a Ball at a specific instance in time
        curs.execute ("""CREATE TABLE IF NOT EXISTS Ball 
                        (BALLID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        BALLNO      INTEGER NOT NULL,
                        XPOS        FLOAT NOT NULL,
                        YPOS        FLOAT NOT NULL,
                        XVEL        FLOAT,
                        YVEL        FLOAT );""");

        # Table represents a Table at a specific instance in time
        curs.execute ("""CREATE TABLE IF NOT EXISTS TTable 
                        (TABLEID    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        TIME        FLOAT NOT NULL );""");

        # Table connects balls to their tables joining TABLEID OF TTable 
        curs.execute("""CREATE TABLE IF NOT EXISTS BallTable 
                        (BALLID      INTEGER NOT NULL,
                        TABLEID      INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball,
                        FOREIGN KEY (TABLEID) REFERENCES TTable);""");

        # Each row in this table represents a shot in a game of pool
        curs.execute("""CREATE TABLE IF NOT EXISTS Shot
                        (SHOTID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID    INTEGER NOT NULL,
                        GAMEID      INTEGER NOT NULL,
                    
                        FOREIGN KEY (PLAYERID) REFERENCES Player,
                        FOREIGN KEY (GAMEID) REFERENCES Game);""");

        #This table connects table snapshots to tables by joining the TABLEID of TTable 
        curs.execute("""CREATE TABLE IF NOT EXISTS TableShot
                        (TABLEID    INTEGER NOT NULL,
                        SHOTID      INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES BallTable,
                        FOREIGN KEY (SHOTID) REFERENCES Shot);""");
        
        # This table connects GAMEIDs to GAMENAMEs
        curs.execute("""CREATE TABLE IF NOT EXISTS Game 
                        (GAMEID     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMENAME    VARCHAR(64) NOT NULL ); """);
        
        #This table connects PLAYERIDs to GAMEIDs and PLAYERNAMES
        curs.execute("""CREATE TABLE IF NOT EXISTS Player
                        (PLAYERID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID      INTEGER NOT NULL,
                        PLAYERNAME  VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES Game);""");

        curs.close();
        Database.conn.commit();

    # This method should return a Table object (from A2)
    def readTable(self, tableID):

        # Create a new table object
        table = Table()

        # Get a cursor for the database connection
        conn = sqlite3.connect('phylib.db')
        cursor = Database.conn.cursor()

        # Retrieve ball attributes based on the table ID using an inner join
        data = cursor.execute("""SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL 
                             FROM BallTable
                             INNER JOIN Ball ON BallTable.BALLID = Ball.BALLID
                             WHERE BallTable.TABLEID = ?;
                          """, (tableID + 1,))

        # Fetch all rows of data containing ball attributes
        rows = data.fetchall()

        if not rows:
            return None

        # Add each row of data into the table class based on whether it is a still or rolling ball
        for row in rows:
            ball_no, xpos, ypos, xvel, yvel = row
            pos = Coordinate(xpos,ypos)

            # Check if the ball is a still ball (no velocity)
            if xvel is None and yvel is None:
                table += StillBall(ball_no, pos)
            else:
                # Calculate the speed and acc for RollingBall
                vel = Coordinate(xvel, yvel)
                speed = sqrt(vel.x ** 2 + vel.y ** 2)

                if speed > VEL_EPSILON:
                    acc_x = (-1 * vel.x) / speed * DRAG
                    acc_y = (-1 * vel.y) / speed * DRAG
                    acc = Coordinate(acc_x, acc_y)

                    # Instantiate the RollingBall
                    table += RollingBall(ball_no, pos, vel, acc)

        # Retrieve the time for our table from the database
        cursor.execute("""SELECT TIME 
                             FROM TTable
                             WHERE TTable.TABLEID = ?;""", (tableID + 1,))
        timeRow = cursor.fetchone()[0]


        # Add the time to the table
        table.time = timeRow

        # Commit the changes to the database and close the cursor
        Database.conn.commit()
        cursor.close()

        # Return the populated table object
        return table

        
    def writeTable(self, table):
        # Create a cursor object
        cur = Database.conn.cursor()

        try:
            # Insert the table time into TTable
            cur.execute("""INSERT INTO TTable (TIME) VALUES (?)""", (table.time,))

            # Retrieve the table ID using the time
            cur.execute("""SELECT TABLEID FROM TTable WHERE TTable.TIME = ?""", (table.time,))
            table_id = cur.fetchone()[0]

            # Loop through the table and add the velocities if it is a RollingBall, else not adding them to our tables
            for obj in table:
                if isinstance(obj, RollingBall):
                    cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                               VALUES (?, ?, ?, ?, ?)""",
                            (obj.obj.rolling_ball.number, obj.obj.rolling_ball.pos.x,
                             obj.obj.rolling_ball.pos.y, obj.obj.rolling_ball.vel.x,
                             obj.obj.rolling_ball.vel.y))
                elif isinstance(obj, StillBall):
                    cur.execute("""INSERT INTO Ball (BALLNO, XPOS, YPOS)
                               VALUES (?, ?, ?)""",
                            (obj.obj.still_ball.number, obj.obj.still_ball.pos.x,
                             obj.obj.still_ball.pos.y))
                elif isinstance(obj, Hole) or isinstance(obj, HCushion) or isinstance(obj, VCushion):
                    # Skip holes and cushions as they are fixed objects
                    continue

                # Add the ball ID and table ID so they are related to each other
                if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                    ball_id = cur.lastrowid
                    cur.execute("""INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?)""", (ball_id, table_id))

            # Close the cursor
            cur.close()

            # Commit the changes
            Database.conn.commit()

        finally:
            # Return the table ID
            return table_id -1

    def getGame(self, gameID):
        cur = Database.conn.cursor()

        # Retrieve game details from the database based on gameID
        cur.execute("""SELECT g.gameName, p1.playerName, p2.playerName
                       FROM Game g
                       JOIN Player p1 ON g.gameID = p1.gameID
                       JOIN Player p2 ON g.gameID = p2.gameID
                       WHERE g.gameID = ?""", (gameID,))
        game_data = cur.fetchone()

        if game_data is None:
            return None

        gameName, player1Name, player2Name = game_data

        # Fetch table object based on gameID
        cur.execute("""SELECT ts.tableID
                       FROM TableShot ts
                       JOIN Shot s ON ts.shotID = s.shotID
                       WHERE s.gameID = ?""", (gameID,))
        tableID = cur.fetchone()[0]

        # Fetch table object based on tableID (You need to implement this)
        table = self.getTable(tableID)

        conn.close()
        Database.conn.commit()

        return [gameName, player1Name, player2Name]
        # return gameID, gameName, player1Name, player2Name, table

    def setGame(self,gameName, player1Name,player2Name):
        """
        Create a new game record in the database.
        """
        # Placeholder for creating a new game record in the database
        curs = Database.conn.cursor()

        # Insert game name into Game table
        curs.execute("""INSERT 
                        INTO Game (GAMENAME) 
                        VALUES (?)""", (gameName,))
        
        # Get gameID
        dataID = curs.execute("""SELECT GAMEID 
                            FROM Game 
                            WHERE GAMENAME = ?""" , (gameName,))

        gameID = dataID.fetchone()[0]

        # Insert player names into Player table
        curs.execute("""INSERT 
                        INTO Player (GAMEID, PLAYERNAME) 
                        VALUES (?, ?)""", (gameID, player1Name,))

        curs.execute("""INSERT 
                        INTO Player (GAMEID, PLAYERNAME) 
                        VALUES (?, ?)""", (gameID, player2Name,))

        curs.close()
        Database.conn.commit

    def recordTableShot(self, shot, table):
        # Record the table snapshot in the database.

        curs = Database.conn.cursor()
        
        # Incrementing shot and table IDs by 1 as they might be zero-based
        new_tableID = table + 1
        new_shotID = shot + 1

        # Insert the TABLEID and SHOTID into the TableShot table
        curs.execute("""INSERT 
                        INTO TableShot (TABLEID, SHOTID) 
                        VALUES (?, ?)""", (new_tableID, new_shotID,));

        curs.close()
        Database.conn.commit()

    def registerShot(self, gameName, playerName):
        cursor = Database.conn.cursor()

        # Get the game ID from the game name
        data = cursor.execute("""SELECT GAMEID FROM Game WHERE GAMENAME = ?""", (gameName,))
        game_id = data.fetchone()[0]

        # Get the player ID
        data = cursor.execute("""SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?""", (playerName,))
        player_id = data.fetchone()[0]

        # Registering a new shot based on player ID and game ID
        cursor.execute("""INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)""", (player_id, game_id))

        # Getting the shot ID
        data = cursor.execute("""SELECT SHOTID FROM Shot WHERE PLAYERID = ?""", (player_id,))
        shot_id = data.fetchone()[0]

        cursor.close()
        Database.conn.commit()

        return shot_id - 1

    def tableShot(self, shotID, tableID):
        cursor = Database.conn.cursor()

        id_table = table_id + 1
        id_shot = shot_id + 1

        # Adds the shot to the table in the database relating the shot to the table
        cursor.execute("""INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)""", (id_table, id_shot))

        cursor.close()
        Database.conn.commit()

    # This method calls commit and then closes the conn 
    def close(self):
        Database.conn.commit();
        Database.conn.close();

################################################################################
class Game():

    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        
        db = Database()

        if isinstance(gameID, int) and gameName is None and player1Name is None and player2Name is None:
            # If only gameID is given and it's an integer, retrieve game details from the database
            self.gameId = gameID
            self.gameName, self.player1Name, self.player2Name = db.getGame(self.gameId)

        elif gameID is None and isinstance(gameName, str) and isinstance(player1Name, str) and isinstance(player2Name, str):
            # If no gameID is provided but names are given, add a new game to the database
            self.gameName, self.player1Name, self.player2Name = gameName, player1Name, player2Name
            self.gameId = db.setGame(gameName, player1Name, player2Name)

        else:
            # Raise TypeError if invalid data types are passed to the constructor
            raise TypeError("Invalid data types passed to Game constructor.")

        db.close()

    def shoot(self, gameName, playerName, table, xvel, yvel):
       
        # Get player ID from playerName using database methods
        db = Database()

        # New shot is made by a player
        shot_id = db.registerShot(gameName, playerName)

        # Find the object representing the cue ball (number 0) in the table.
        for obj in table:
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                cue_ball = obj

                # Set the type attribute of the cue ball to ROLLING_BALL
                cue_ball.type = phylib.PHYLIB_ROLLING_BALL

                # Set the position of the rolling ball to match the cue ball
                cue_ball.obj.rolling_ball.pos.x = cue_ball.obj.still_ball.pos.x
                cue_ball.obj.rolling_ball.pos.y = cue_ball.obj.still_ball.pos.y

                # Set the initial velocity of the rolling ball
                cue_ball.obj.rolling_ball.vel.x = xvel
                cue_ball.obj.rolling_ball.vel.y = yvel

                # Calculate speed and acceleration for RollingBall
                speed = sqrt((xvel * xvel) + (yvel * yvel))

                # Calculate acceleration based on drag
                xacc = (-1 * xvel) / speed * DRAG
                yacc = (-1 * yvel) / speed * DRAG

                # Set acceleration attributes
                cue_ball.obj.rolling_ball.acc.x = xacc
                cue_ball.obj.rolling_ball.acc.y = yacc

                # Set the number of the cue ball to 0
                cue_ball.obj.rolling_ball.number = 0        

        copy = None;
        svg_list = []
        # Start loop for segment simulation
        while table:
            # Call the segment method to simulate the next segment
            copy = table
            start = table.time
            table = table.segment()

            # Check if the segment simulation is finished
            if table is None:
                break

            end = table.time 
            # Calculate the length of the segment (in seconds)
            finalTime = end - start

            # Calculate the number of frames in the segment
            finalTime = int(floor(finalTime / FRAME_INTERVAL))

            # Loop over each frame
            for i in range(finalTime):
                # Simulate the next frame using the roll method
                frame = i * FRAME_INTERVAL
                newTable = copy.roll(frame)

                # Set the time of the returned table
                newTable.time = start + frame

                #append new tables
                svg_list.append(newTable.svg())

        # Initialize a variable to track whether the cue ball (number 0) is found

        cue_found = False
        eight_found = False

        lowBalls = []
        highBalls = []

        # Iterate through each object in the table copy
        for obj in copy:
            # Check if the object is a StillBall and its number is 0
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 0:
                cue_found = True;
            if isinstance(obj, StillBall) and obj.obj.still_ball.number == 8:
                eight_found = True;
            if isinstance(obj, StillBall) and obj.obj.still_ball.number > 0 and obj.obj.still_ball.number <= 7:
                lowBalls.append(obj.obj.still_ball.number);
            if isinstance(obj, StillBall) and obj.obj.still_ball.number > 8:
                highBalls.append(obj.obj.still_ball.number);
        # If the cue ball is not found in the table copy
        if cue_found == False:
            # Add a new cue ball to the table copy at a random position near the center
            copy += StillBall(0, Coordinate(TABLE_WIDTH/2.0 + random.uniform(-3.0,3.0),
                                TABLE_LENGTH-TABLE_WIDTH/2.0))
        
        # Append the SVG representation of the table copy to the SVG list
        svg_list.append(copy.svg())

        # Return a list containing the updated table copy and the SVG list
        return[copy, svg_list, cue_found, eight_found, lowBalls, highBalls]
    
