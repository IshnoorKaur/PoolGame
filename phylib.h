#ifndef PHYLIB_H
#define PHYLIB_H

/*Constants*/
#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2 * PHYLIB_BALL_RADIUS)

#define PHYLIB_HOLE_RADIUS (2 * PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0)                   // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH / 2.0) // mm

#define PHYLIB_SIM_RATE (0.0001)                        // s
#define PHYLIB_VEL_EPSILON (0.01)                       // mm/s

#define PHYLIB_DRAG (150.0)                             //mm/s^2
#define PHYLIB_MAX_TIME (600)                          // s

#define PHYLIB_MAX_OBJECTS (26)

/*enum for object types*/
typedef enum
{
    PHYLIB_STILL_BALL = 0,
    PHYLIB_ROLLING_BALL = 1,
    PHYLIB_HOLE = 2,
    PHYLIB_HCUSHION = 3,
    PHYLIB_VCUSHION = 4,
} phylib_obj;

/*Structure for 2D coordinates*/
typedef struct
{
    double x;
    double y;
} phylib_coord;

/*Structure for still ball*/
typedef struct
{
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

/*Structure for rolling ball*/
typedef struct
{
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc;
} phylib_rolling_ball;

/*Structure for hole*/
typedef struct
{
    phylib_coord pos;
} phylib_hole;

/*Structure for horizontal cushion*/
typedef struct
{
    double y;
} phylib_hcushion;

/*Structure for vertical cushion*/
typedef struct
{
    double x;
} phylib_vcushion;

/*Union to store any of the above structures*/
typedef union
{
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

/*Structure to represent a generic object*/
typedef struct
{
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

/*Structure for the table*/
typedef struct
{
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

/*Function Prototypes*/

/*Part 1*/
/*Creates a new still ball*/
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos);

/*Creates a new rolling ball*/
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc);

/*Creates a new hole*/
phylib_object *phylib_new_hole(phylib_coord *pos);

/*Creates a new horizontal cushion object*/
phylib_object *phylib_new_hcushion(double y);

/*Creates a new verticle cushion object*/
phylib_object *phylib_new_vcushion(double x);

/*Creates a new table object*/
phylib_table *phylib_new_table(void);


/*Part 2*/

/*Copies an object from src to a new memory location pointed by dest.*/
void phylib_copy_object( phylib_object **dest, phylib_object **src );

/*Creates a copy of the table.*/
phylib_table *phylib_copy_table( phylib_table *table );

/*Adds an object to the array of objects of given table.*/
void phylib_add_object( phylib_table *table, phylib_object *object );

/*Frees object arrays of a table.*/
void phylib_free_table( phylib_table *table );

/*Calculates the difference between 2 coordinates.*/
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 );

/*Calculates length of coodinate c using pythagorean thearom.*/
double phylib_length( phylib_coord c );

/*Calculates dot product between two coordinates.*/
double phylib_dot_product( phylib_coord a, phylib_coord b );

/*Calculates the distance between two objects.*/
double phylib_distance( phylib_object *obj1, phylib_object *obj2 );


/*Part 3*/

/*Update rolling ball's position and velocity after rolling for given time.*/
void phylib_roll( phylib_object *new, phylib_object *old, double time );

/*Check if rolling ball has stopped.*/
unsigned char phylib_stopped( phylib_object *object );

/*Handles collision of two objects.*/
void phylib_bounce( phylib_object **a, phylib_object **b );

/*Counts the number of rolling balls on table.*/
unsigned char phylib_rolling( phylib_table *t );

/*Creates copies of input table and then iterates over time and rolling balls, updating their positions and velocities.*/
phylib_table *phylib_segment( phylib_table *table );


/*New function added A2*/
char *phylib_object_string( phylib_object *object );

#endif /* PHYLIB_H */
