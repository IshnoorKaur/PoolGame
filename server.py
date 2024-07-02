import sys; #used to get argv 
import cgi; #used to parse Multipart FormData 
import os;

#web server parts 
from http.server import HTTPServer, BaseHTTPRequestHandler;

#use to parse URL and extract form data for GET req
from urllib.parse import urlparse, parse_qsl;

#use the Physics file functions 
import Physics;

#need the sqrt from math 
from math import sqrt

#handler for web server - handles GET and POST
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        #parse the URL to get path and from data 
        parsed = urlparse(self.path);

        #check if the web page matches the list 
        if parsed.path in [ '/shoot.html']:

            #retreive HTML file
            fp = open("."+self.path);
            content = fp.read();

            #generrate the handlers 
            self.send_response(200);   #Keep it 200 
            self.send_header("Content-type", "text/html");
            self.send_header("Content-length" , len(content));
            self.end_headers();

            #send it to browser 
            self.wfile.write(bytes(content, "utf-8"));

            #remeber to close it  
            fp.close();

        #
        elif parsed.path.startswith('/table-'):

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
        if parsed.path in ['/display.html']:
            # Parse the form data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 
                'CONTENT_TYPE': self.headers['Content-Type']}
            );

            # Delete existing table-?.svg files (if any)
            for filename in os.listdir('.'):
                if filename.startswith('table-') and filename.endswith('.svg'):
                    os.remove(filename)


            # Retrieve data for Still Ball
            stillb_number = int(form.getvalue('sb_number'));
            stillb_x = float(form.getvalue('sb_x'));
            stillb_y = float(form.getvalue('sb_y'));
        
            # Retrieve data for Rolling Ball
            rollb_number = int(form.getvalue("rb_number"))
            rollb_x = float(form.getvalue('rb_x'));
            rollb_y = float(form.getvalue('rb_y'));
            rollb_dx = float(form.getvalue('rb_dx'));
            rollb_dy = float(form.getvalue('rb_dy'));

            # Create a Physics Table object       
            table = Physics.Table();

            # Create a Coordinate object for Still Ball position
            pos = Physics.Coordinate(stillb_x, stillb_y);

            # Create a StillBall object
            still_b = Physics.StillBall(stillb_number, pos);

            # Create a Coordinate object for Rolling Ball position and velocity
            pos = Physics.Coordinate(rollb_x, rollb_y);
            vel = Physics.Coordinate(rollb_dx, rollb_dy);

            # Calculate speed and acceleration for Rolling Ball
            speed = sqrt(vel.x**2 + vel.y**2);
            acc_x = (-1 * vel.x)/speed * Physics.DRAG;
            acc_y = (-1 * vel.y)/speed * Physics.DRAG;
            acc = Physics.Coordinate(acc_x, acc_y);

            # Create a RollingBall object
            roll_b = Physics.RollingBall(rollb_number, pos, vel, acc);

            # Add Still Ball and Rolling Ball to the table
            table += still_b;
            table += roll_b;

            count = 0; 

            # Save the table-?.svg file
            file = open("table-%d.svg" % (count), "w");
            file.write(table.svg());

            count += 1;

            # Generate HTML content for display.html

            html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Display SVG Images</title>
            </head>
            <body>
                <h1>Phylib Webserver Application</h1>
                <img src="/table-0.svg" alt ="Table 0"/>\n

            """
            # Iterate through table segments and generate SVG images
            while table: 
                table = table.segment()
                if table: 
                    file = open("table-%d.svg" % (count), "w")
                    file.write(table.svg());
                    html_content += """<img src="/table-%d.svg" alt ="Table %s"/>\n""" %(count, count)
                count += 1
            
            # Add Back button to return to shoot.html
            html_content += """
                            <a href="/shoot.html">
                                <button>Back</button>
                            </a>
                         </body>
                      </html>
                    """

            # Send HTML response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(html_content))
            self.end_headers()
            self.wfile.write(bytes(html_content, "utf-8"))
    
        else:
            # Return 404 response for paths other than '/display.html'
            self.send_response(404);
            self.end_headers();
            self.wfile.write(bytes("404: %s not found" % self.path, "utf-8"));


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1])), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();