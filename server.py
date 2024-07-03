import sys; #used to get argv 
import cgi; #used to parse Multipart FormData 
import os;
import json;
import random;

#web server parts 
from http.server import HTTPServer, BaseHTTPRequestHandler;

#use to parse URL and extract form data for GET req
from urllib.parse import urlparse;

#use the Physics file functions 
import Physics;

# Import the Table object from game.py
from game import createTB

#handler for web server - handles GET and POST
class MyHandler(BaseHTTPRequestHandler):
    table = None;
    p1_name = None;
    p2_name = None;
    game_name = None;
    game = None;
    curPlayer = None;
    current_player_name = None;
    

    lowBalls= [];
    highBalls = [];
    cueFound = None;
    eight_found = None;

    assignedBalls = False;
    p1_balls = [];
    p2_balls = [];
    playerWon = None;
    player1Assigned = None
    player2Assigned = None

    def do_GET(self):

        #parse the URL to get path and from data 
        parsed = urlparse(self.path);

        #check if the web page matches the list 
        if parsed.path in [ '/main.html']:

            #retreive HTML file
            fp = open("."+self.path);
            content = fp.read();
            MyHandler.playerWon = None;

            #generrate the handlers 
            self.send_response(200);   #Keep it 200 
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length" , len(content));
            self.end_headers();

            #send it to browser 
            self.wfile.write(bytes(content, "utf-8"));

            #remeber to close it  
            fp.close();

        elif parsed.path in ['/script.js']:  # Handle request for script.js
            #retreive HTML file
            fp = open("./script.js");
            content = fp.read();

            self.send_response(200)
            self.send_header("Content-type", "text/js")
            self.send_header("Content-length", len(content))
            self.end_headers()

            self.wfile.write(bytes(content, "utf-8"))
            fp.close()
        elif parsed.path in ["/info"]:
            
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "applications/json" );
            self.end_headers();
        
            data = [MyHandler.curPlayer, MyHandler.player1Assigned, MyHandler.player2Assigned, MyHandler.playerWon, MyHandler.p1_balls, MyHandler.p2_balls]
            print("We are here, current: ",MyHandler.curPlayer)
            print("Assigned P1: ", MyHandler.player1Assigned)
            print("Assigned P2: ", MyHandler.player2Assigned)
            print("Winner of the game: ", MyHandler.playerWon)

            data_json = json.dumps(data)

            self.wfile.write(bytes(data_json,"utf8"));

        elif parsed.path.startswith('/table'):

            try:
                fp = open("."+parsed.path, 'rb')
                content = fp.read()

                self.send_response(200)
                self.send_header("Content-type", "image/svg+xml")
                self.send_header("Content-length", len(content))
                self.end_headers()

                self.wfile.write(content)
                fp.close()

            except FileNotFoundError:
                printf("ERROR: File not found!");
                self.send_response( 404 );
                self.end_headers();
                self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

    def do_POST(self):
        # Parse the URL to get the path
        parsed = urlparse(self.path);

        # Check if the path matches '/display.html'
        if parsed.path in ['/start_game']:     
            # Parse the form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 
                'CONTENT_TYPE': self.headers['Content-Type']}
            );

            # Delete existing table.svg file (if any)
            for file in os.listdir('.'):
                if file.startswith("table-") and file.endswith(".svg"):
                    os.remove(file)

            # Retrieve form data for game name, player 1 name, and player 2 name
            MyHandler.game_name = str(form.getvalue("gameName"))
            MyHandler.p1_name = str(form.getvalue("player1Name"))
            MyHandler.p2_name = str(form.getvalue("player2Name"))

            # Randomize players
            MyHandler.curPlayer = random.randrange(0, 1)

            self.db = Physics.Database(reset=True)
            self.db.createDB()

            # Create the game object
            MyHandler.game = Physics.Game(gameName=MyHandler.game_name, player1Name=MyHandler.p1_name, player2Name=MyHandler.p2_name)

            MyHandler.table = Physics.Table()

            # Import the Table object from game.py
            MyHandler.table = createTB(MyHandler.table);

            # Random current player 
            MyHandler.curPlayer = random.choice([0, 1]);

            # Determine the current player's name
            MyHandler.current_player_name = MyHandler.p1_name if MyHandler.curPlayer == 0 else MyHandler.p2_name  

            # # Generate HTML content for display.html 
            
            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
            <script src="script.js"></script>
            <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                flex-direction: column;
                margin: 0;
                font-family: Georgia, serif;
                background-color: #f4f4f4;
            }
            .current-player {
                margin-bottom: 5px;
                font-size: 25px;
                margin: 10px;
                padding: 10px;
                background-color: #115d25;
                color: white;
                border-radius: 5px;
            }
            .player-names {
                display: flex;
                font-size: 25px;
                width: 100%;
                justify-content: space-between;
                padding: 0 20px;
                margin-top: -15px;
            }
            .player-names span {
                padding: 5px;
            }
            svg {
                max-width: 100%;
                max-height: 100%;
            }
            </style>
            <title>Game Table</title>
            </head>
            <body>
            """

            # Add current player at the top
            html_content += f'<div class="current-player">Current Player: {MyHandler.current_player_name}</div>'

            # Add player names above the SVG
            html_content += f'<div class="player-names"><span>P1: {MyHandler.p2_name}</span><span>P2: {MyHandler.p1_name}</span></div>'
            #html_content += f'<div class="player-names"><span>{MyHandler.player2Assigned}</span><span>{MyHandler.player1Assigned}</span></div>'

            # Add the SVG
            html_content += MyHandler.table.svg()

            html_content += """
            </body>
            </html>
            """
        
            # Send HTML response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html_content))
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
    
        # Check if the path matches '/script.js'
        elif parsed.path in ['/shoot.html']:

            for file in os.listdir('.'):
                if file.startswith("table") and file.endswith(".svg"):
                    os.remove(file)

            # Parse the form data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            print("Received data from JavaScript:", post_data)

            # Process the received data
            received_data = json.loads(post_data)

            print("Received data from JavaScript:", received_data)

            svg_list= []

            # Calling the shoot function 
            MyHandler.table, svg_list, MyHandler.cue_found, MyHandler.eight_found, MyHandler.lowBalls, MyHandler.highBalls = MyHandler.game.shoot(MyHandler.game_name,MyHandler.current_player_name,MyHandler.table, (-1 * float(received_data["vel_x"])),(-1 * float(received_data["vel_y"])))

            # Print the lists of low and high balls
            print("Low balls:", MyHandler.lowBalls)
            print("High balls:", MyHandler.highBalls)
            print("Que ball: ", MyHandler.cue_found)
            
            # Determine the current player's name
            MyHandler.current_player_name = MyHandler.p1_name if MyHandler.curPlayer == 0 else MyHandler.p2_name
            print("Current_player_name: ", MyHandler.current_player_name)

            if MyHandler.eight_found == False:

                if MyHandler.player1Assigned == "High":
                    MyHandler.p1_balls = MyHandler.highBalls
                    MyHandler.p2_balls = MyHandler.lowBalls
                else:
                    MyHandler.p1_balls = MyHandler.lowBalls
                    MyHandler.p2_balls =  MyHandler.highBalls

                if MyHandler.curPlayer == 0:
                    
                    if len(MyHandler.p1_balls) == 0:
                        MyHandler.playerWon = MyHandler.p1_name
                    else:
                        MyHandler.playerWon = MyHandler.p2_name
                else:

                    if len(MyHandler.p2_balls) == 0:
                        MyHandler.playerWon = MyHandler.p2_name
                    else:
                        MyHandler.playerWon = MyHandler.p1_name
            
            # if MyHandler.eight_found == True:
            #     # Check if the 8 ball is pocketed before shooting all assigned balls
            #     if ((MyHandler.player1Assigned == "High" and MyHandler.p1_balls != MyHandler.highBalls) or
            #         (MyHandler.player1Assigned == "Low" and MyHandler.p1_balls != MyHandler.lowBalls)):
            #         MyHandler.playerWon = MyHandler.p2_name  # Player 2 wins
            #     elif ((MyHandler.player2Assigned == "High" and MyHandler.p2_balls != MyHandler.highBalls) or
            #         (MyHandler.player2Assigned == "Low" and MyHandler.p2_balls != MyHandler.lowBalls)):
            #         MyHandler.playerWon = MyHandler.p1_name  # Player 1 wins
            #     elif (MyHandler.player1Assigned == "High" and len(MyHandler.p1_balls) > 0):
            #         MyHandler.playerWon = MyHandler.p2_name  # Player 2 wins if Player 1 has assigned balls remaining
            #     elif (MyHandler.player1Assigned == "Low" and len(MyHandler.p1_balls) > 0):
            #         MyHandler.playerWon = MyHandler.p2_name  # Player 2 wins if Player 1 has assigned balls remaining
            #     elif (MyHandler.player2Assigned == "High" and len(MyHandler.p2_balls) > 0):
            #         MyHandler.playerWon = MyHandler.p1_name  # Player 1 wins if Player 2 has assigned balls remaining
            #     elif (MyHandler.player2Assigned == "Low" and len(MyHandler.p2_balls) > 0):
            #         MyHandler.playerWon = MyHandler.p1_name  # Player 1 wins if Player 2 has assigned balls remaining
            #     else:
            #         MyHandler.playerWon = None; 

            if MyHandler.assignedBalls == False:
                if len(MyHandler.highBalls) == 7 and len(MyHandler.lowBalls) == 7:
                    MyHandler.player1Assigned = None # was none
                    MyHandler.player2Assigned = None
                    
                    if MyHandler.curPlayer == 0:
                        MyHandler.curPlayer = 1
                    else:
                        MyHandler.curPlayer = 0
                
                elif MyHandler.curPlayer == 0:
                    if len(MyHandler.highBalls) > len(MyHandler.lowBalls):
                        MyHandler.player1Assigned = "Low"
                        MyHandler.p1_balls = MyHandler.lowBalls

                        MyHandler.player2Assigned = "High"
                        MyHandler.p2_balls =  MyHandler.highBalls
                    elif len(MyHandler.highBalls) < len(MyHandler.lowBalls):
                        MyHandler.player1Assigned = "High"
                        MyHandler.p1_balls = MyHandler.highBalls

                        MyHandler.player2Assigned = "Low"
                        MyHandler.p2_balls =  MyHandler.lowBalls
                    else:
                        MyHandler.player1Assigned = "High"
                        MyHandler.p1_balls = MyHandler.highBalls

                        MyHandler.player2Assigned = "Low"
                        MyHandler.p2_balls =  MyHandler.lowBalls
                    
                    MyHandler.assignedBalls = True
                    MyHandler.curPlayer = 0
                    
                elif MyHandler.curPlayer == 1:
                    if len(MyHandler.highBalls) > len(MyHandler.lowBalls):
                        MyHandler.player2Assigned = "Low"
                        MyHandler.p2_balls = MyHandler.lowBalls
                        MyHandler.player1Assigned = "High"
                        MyHandler.p1_balls = MyHandler.highBalls
                    elif len(MyHandler.highBalls) < len(MyHandler.lowBalls):
                        MyHandler.player2Assigned = "High"
                        MyHandler.p2_balls = MyHandler.highBalls
                        MyHandler.player1Assigned = "Low"
                        MyHandler.p1_balls = MyHandler.lowBalls
                    else:
                        MyHandler.player1Assigned = "Low"
                        MyHandler.p1_balls = MyHandler.lowBalls
                        MyHandler.player2Assigned = "High"
                        MyHandler.p2_balls = MyHandler.highBalls
                    
                    MyHandler.assignedBalls = True
                    MyHandler.curPlayer = 1

            else:
                if MyHandler.curPlayer == 0:
                    if MyHandler.player1Assigned == "High":
                        if len(MyHandler.highBalls) == len(MyHandler.p1_balls):
                            MyHandler.curPlayer = 1
                            MyHandler.p2_balls = MyHandler.lowBalls
                        else:
                            MyHandler.p1_balls = MyHandler.highBalls
                            MyHandler.p2_balls = MyHandler.lowBalls
                    else:
                        if len(MyHandler.lowBalls) == len(MyHandler.p1_balls):
                            MyHandler.curPlayer = 1
                            MyHandler.p2_balls = MyHandler.highBalls
                        else:
                            MyHandler.p1_balls = MyHandler.lowBalls
                            MyHandler.p2_balls = MyHandler.highBalls

                else:
                    if MyHandler.player2Assigned == "High":
                        if len(MyHandler.highBalls) == len(MyHandler.p2_balls):
                            MyHandler.curPlayer = 0
                            MyHandler.p1_balls = MyHandler.lowBalls
                        else:
                            MyHandler.p2_balls = MyHandler.highBalls
                            MyHandler.p1_balls = MyHandler.lowBalls
                    else:
                        if len(MyHandler.lowBalls) == len(MyHandler.p2_balls):
                            MyHandler.curPlayer = 0
                            MyHandler.p1_balls = MyHandler.highBalls
                        else:
                            MyHandler.p1_balls = MyHandler.highBalls
                            MyHandler.p2_balls = MyHandler.lowBalls
                
            # Send a success response
            self.send_response(200)
            self.send_header("Content-type", "applications/json")
            self.end_headers()

            # Allows to store JSON data directly into a file
            svg_list_json = json.dumps(svg_list)
        
            self.wfile.write(bytes(svg_list_json,"utf8"));
        
        elif parsed.path == '/switch_player':
            print("Entered switch player")
            print("Current player name : " + str(MyHandler.current_player_name))
            # Switch the current player
            if MyHandler.current_player_name == MyHandler.p1_name:
                MyHandler.current_player_name = MyHandler.p2_name
            else:
                MyHandler.current_player_name = MyHandler.p1_name
            print("New current player: ",MyHandler.current_player_name)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(MyHandler.current_player_name, "utf-8"))

        else:
            # Return 404 response for paths other than '/display.html'
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"));

if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1])), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();
