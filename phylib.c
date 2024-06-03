#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h> 

#include "phylib.h"

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{

    /*Allocate memory for new object*/
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    /*Check if memory allocation was successful*/
    if (new_object == NULL)
    {
        printf("New still ball: no memory allocated\n");
        return NULL;
    }

    /*Set type of object to PHYLIB_STILL_BALL*/
    new_object->type = PHYLIB_STILL_BALL;

    /*Transform information to structure*/
    new_object->obj.still_ball.number = number;
    new_object->obj.still_ball.pos = *pos;

    /*Return a pointer to phylib_object*/
    return new_object;
}

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{

    /*Allocate memory for new object*/
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    /*Check if memory allocation was successful*/
    if (new_object == NULL)
    {
        printf("New rolling ball: no memory allocated\n");
        return NULL;
    }

    /*Set type of object to PHYLIB_ROLLING_BALL*/
    new_object->type = PHYLIB_ROLLING_BALL;

    /*Transform information to structure*/
    new_object->obj.rolling_ball.number = number;
    new_object->obj.rolling_ball.pos = *pos;
    new_object->obj.rolling_ball.vel = *vel;
    new_object->obj.rolling_ball.acc = *acc;

    /*Returns a pointer to phylib_object*/
    return new_object;
}

phylib_object *phylib_new_hole(phylib_coord *pos)
{

    /*Allocate memory for new object*/
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    /*Check if memory allocation was successful*/
    if (new_object == NULL)
    {
        printf("New hole: no memory allocated\n");
        return NULL;
    }

    /*Set type of object to PHYLIB_ROLLING_BALL*/
    new_object->type = PHYLIB_HOLE;

    /*Transform information to structure*/
    new_object->obj.hole.pos = *pos;

    /*Returns a pointer to phylib_object*/
    return new_object;
}

phylib_object *phylib_new_hcushion(double y)
{

    /*Allocate memory for new object*/
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    /*Check if memory allocation was successful*/
    if (new_object == NULL)
    {
        printf("New hcushion: no memory allocated\n");
        return NULL;
    }

    /*Set type of object to PHYLIB_ROLLING_BALL*/
    new_object->type = PHYLIB_HCUSHION;

    /*Transform information to structure*/
    new_object->obj.hcushion.y = y;

    /*Returns a pointer to phylib_object*/
    return new_object;
}

phylib_object *phylib_new_vcushion(double x)
{
    /*Allocate memory for new object*/
    phylib_object *new_object = (phylib_object *)malloc(sizeof(phylib_object));

    /*Check if memory allocation was successful*/
    if (new_object == NULL)
    {
        printf("New hcushion: no memory allocated\n");
        return NULL;
    }

    /*Set type of object to PHYLIB_ROLLING_BALL*/
    new_object->type = PHYLIB_VCUSHION;

    /*Transform information to structure*/
    new_object->obj.vcushion.x = x;

    /*Returns a pointer to phylib_object*/
    return new_object;
}

phylib_table *phylib_new_table(void)
{

    /*Allocate memory for the new table*/
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));

    /*Check if memory allocation was successful*/
    if (new_table == NULL)
    {
        fprintf(stderr, "Error: Failed to allocate memory for new table\n");
        return NULL;
    }

    /*Set time to 0.0*/
    new_table->time = 0.0;

    /*Initialize object pointers to NULL*/
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        new_table->object[i] = NULL;
    }

    /*Create and add elements to the array*/

    /*Horizontal cushion at 0.0 and table length*/
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    /*Verticle cushion at 0.0 and table length*/
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    /*Create holes at 4 corners. This is where the cushion meets*/
    // Top left
    new_table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    // top right
    new_table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    // Bottom left
    new_table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    // Bottom right
    new_table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});

    /*2 holes between top and bottom holes*/
    new_table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    new_table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    /*Return pointer to phylib_table*/
    return new_table;
}

void phylib_copy_object(phylib_object **dest, phylib_object **src)
{

    // Check if src is NULL
    if (*src == NULL)
    {
        printf("scr is Null\n");
        *dest = NULL;
        return;
    }

    // Allocate memory for new phylib_object
    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    // Check if memory allocation is successful
    if (*dest == NULL)
    {
        printf("Memory allocation failed for phylib_copy_object\n");
        exit(EXIT_FAILURE);
    }

    // Copy the content from src to dest using memory
    memcpy(*dest, *src, sizeof(phylib_object));
}

phylib_table *phylib_copy_table(phylib_table *table)
{

    // Check if input table is NULL
    if (table == NULL)
    {
        return NULL;
    }

    // Allocate memory for new phylib table
    phylib_table *copy_table = (phylib_table *)malloc(sizeof(phylib_table));

    // Check if memory allocation was successful
    if (copy_table == NULL)
    {
        printf("Memory allocation failed in phylib_copy_table.\n");
        exit(EXIT_FAILURE);
    }

    // Copy contents from input table to copy_table
    memcpy(copy_table, table, sizeof(phylib_table));

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        copy_table->object[i] = NULL;

        if (table->object[i] != NULL)
        {
            phylib_copy_object(&copy_table->object[i], &table->object[i]);
            
        }
    }


    // Return address of copy_table
    return copy_table;
}

void phylib_add_object(phylib_table *table, phylib_object *object)
{

    // Check if input table or object is null
    if (table == NULL || object == NULL)
    {
        printf("Invalid input in phylib_add_object.\n");
        return;
    }

    // Iterate through array and assign address of object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }
    }

    // If no NULL pointers
    printf("Object array is full in phylib_add_object.\n");
}

void phylib_free_table(phylib_table *table)
{

    // Check if input table is NULL
    if (table == NULL)
    {
        printf("Invalid input in phylib_free_memory.\n");
        return;
    }

    // Free every pointer in object array
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }

    // Free the table
    free(table);
}

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{

    // Calculate difference between two coordinates
    phylib_coord result;

    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;

    return result;
}

double phylib_length(phylib_coord c)
{

    // Calculate length of cordinate c using Phytagorean thearom
    double length_squared = c.x * c.x + c.y * c.y;

    double result = sqrt(length_squared);

    // Return square root of length_squared
    return result;
}

double phylib_dot_product(phylib_coord a, phylib_coord b)
{

    // Calculate dot product between two coordinates
    double dot_product = a.x * b.x + a.y * b.y;

    // Return the dot product
    return dot_product;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{

    // Check if object is a PHYLIB_ROLLING_BALL
    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        printf("Object is not a rolling ball in phylib_distance.\n");
        return -1.0;
    }

    // Extract the position of rolling ball
    phylib_coord ball_position = obj1->obj.rolling_ball.pos;

    // Calculate the distance based on type of object2
    switch (obj2->type)
    {

    // For a rolling and still ball
    case PHYLIB_STILL_BALL:
    {
        phylib_coord pos = obj2->obj.still_ball.pos;
        double distance = phylib_length(phylib_sub(ball_position, pos));
        return distance - PHYLIB_BALL_DIAMETER;
    }

    case PHYLIB_ROLLING_BALL:
    {
        // Calculate distance between centers of 2 balls
        phylib_coord ball2_position = obj2->obj.rolling_ball.pos;
        double distance = phylib_length(phylib_sub(ball_position, ball2_position));
        return distance - PHYLIB_BALL_DIAMETER;
    }

    // For hole
    case PHYLIB_HOLE:
    {
        // Calculate distance between ball and hall
        phylib_coord hole_position = obj2->obj.hole.pos;
        double distance = phylib_length(phylib_sub(ball_position, hole_position));
        return distance - PHYLIB_HOLE_RADIUS;
    }

    // For horizontal cusion
    case PHYLIB_HCUSHION:
    {
        // Calculate distance between ball and horizontal cushion
        double distance = fabs(ball_position.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
        return distance;
    }

    // For vertical cushion
    case PHYLIB_VCUSHION:
    {
        // Calculate distance between ball and vertical cushion
        double distance = fabs(ball_position.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
        return distance;
    }

    // Default
    default:
        return -1.0;
        break;
    }
}

void phylib_roll(phylib_object *new, phylib_object *old, double time)
{

    // Check if both objects are PHYLIB_ROLLING_BALL
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL)
    {
        printf("New or old is not a rolling ball, phylib_roll\n");
        return;
    }

    // Calculate new x position using equation
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x *time + 0.5 * old->obj.rolling_ball.acc.x *time *time;

    // Calculate new y position using equation
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y *time + 0.5 * old->obj.rolling_ball.acc.y *time *time;

    // Calculate new x velocity
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x *time;

    // Check if x velocity changes sign, if so update acceleration
    if ((old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x) < 0)
    {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    // Calculate new y velocity
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y *time;

    // Check if y velocity changes sign, if so update acceleration
    if ((old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y) < 0)
    {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

unsigned char phylib_stopped(phylib_object *object)
{

    // Check if object is ROLLING_BALL
    if (object->type != PHYLIB_ROLLING_BALL)
    {
        printf("Object is not rolling in phylib_stopped.\n");
        return 0;
    }

    // Calculate speed of rolling ball
    double speed_ball = sqrt(pow(object->obj.rolling_ball.vel.x, 2) + pow(object->obj.rolling_ball.vel.y, 2));

    // Check if ball has stopped based on PHYLIB_VEL_EPSILON
    if (speed_ball < PHYLIB_VEL_EPSILON)
    {

        // Set velocities and accelerations to zero
        object->obj.rolling_ball.vel.x = 0.0;
        object->obj.rolling_ball.vel.y = 0.0;
        object->obj.rolling_ball.acc.x = 0.0;
        object->obj.rolling_ball.acc.y = 0.0;

        // convert rolling ball to still ball
        object->type = PHYLIB_STILL_BALL;
        return 1;
    }

    // Ball hasn't stopped
    return 0;
}

void phylib_bounce(phylib_object **a, phylib_object **b)
{

    // Check if both objects are PHYLIB_ROLLING_BALL
    if ((*a)->type != PHYLIB_ROLLING_BALL)
    {
        printf("In phylib_bounce, object a must be rolling.\n");
        return;
    }

    // Variables
    phylib_coord r_ab;  //delta position
    phylib_coord v_rel;  //relative velocity
    phylib_coord n;    //normal vector 
    double v_rel_n;    //relative velocity normal
    double speed_obj_a;
    double speed_obj_b;

    switch ((*b)->type)
    {
    case PHYLIB_HCUSHION:
        // Case 1: b is a HCUSHION
        (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
        (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
        break;

    case PHYLIB_VCUSHION:
        // Case 2: b is a VCUSION
        (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
        (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
        break;

    case PHYLIB_HOLE:
        // Case 3: b is a HOLE
        free(*a);
        *a = NULL;
        break;

    case PHYLIB_STILL_BALL:
        // Case 4: b is a STILL_BALL
        // Upgrade the STILL_BALL to a ROLLING_BALL
        (*b)->type = PHYLIB_ROLLING_BALL;
        (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = 0.0;
        (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.acc.y = 0.0;
        (*b)->obj.rolling_ball.pos.x = (*b)->obj.still_ball.pos.x;
        (*b)->obj.rolling_ball.pos.y = (*b)->obj.still_ball.pos.y;

    case PHYLIB_ROLLING_BALL:
        // Case 5: b is a ROLLING_BALL

        // Compute position of a with respect to b
        r_ab.x = (*a)->obj.rolling_ball.pos.x - (*b)->obj.rolling_ball.pos.x;
        r_ab.y = (*a)->obj.rolling_ball.pos.y - (*b)->obj.rolling_ball.pos.y;

        // Compute relative velocity of a with respect to b
        v_rel.x = (*a)->obj.rolling_ball.vel.x - (*b)->obj.rolling_ball.vel.x;
        v_rel.y = (*a)->obj.rolling_ball.vel.y - (*b)->obj.rolling_ball.vel.y;

        // Compute normal vector
        double length_r_ab = phylib_length(r_ab);
        n.x = r_ab.x / length_r_ab;
        n.y = r_ab.y / length_r_ab;

        // Calculate the dot product
        v_rel_n = phylib_dot_product(v_rel, n);

        // Update velocities
        (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
        (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
        (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
        (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

        // Compute speeds
        speed_obj_a = sqrt(pow((*a)->obj.rolling_ball.vel.x, 2) + pow((*a)->obj.rolling_ball.vel.y, 2));
        speed_obj_b = sqrt(pow((*b)->obj.rolling_ball.vel.x, 2) + pow((*b)->obj.rolling_ball.vel.y, 2));

        if (speed_obj_a > PHYLIB_VEL_EPSILON)
        {
            // Set acceleration of ball a
            double drag_obj_a = -PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.x = drag_obj_a * (*a)->obj.rolling_ball.vel.x / speed_obj_a;
            (*a)->obj.rolling_ball.acc.y = drag_obj_a * (*a)->obj.rolling_ball.vel.y / speed_obj_a;
        }

        if (speed_obj_b > PHYLIB_VEL_EPSILON)
        {
            // Set acceleration of ball b
            double drag_obj_b = -PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.x = drag_obj_b * (*b)->obj.rolling_ball.vel.x / speed_obj_b;
            (*b)->obj.rolling_ball.acc.y = drag_obj_b * (*b)->obj.rolling_ball.vel.y / speed_obj_b;
        }

        break;

    default:
        printf("Unknown object type, phylib_bounce.\n");
        break;
    }
}

unsigned char phylib_rolling(phylib_table *t)
{

    unsigned char rollingBallsCount = 0;

    // Iterate through objects in table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i)
    {

        // Check if object exists and is rolling
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL)
        {
            rollingBallsCount++;
        }
    }

    return rollingBallsCount;
}

phylib_table *phylib_segment(phylib_table *table)
{

    // Check if there are any rolling balls
    if (phylib_rolling(table) == 0)
    {
        //printf("There are no rolling balls, phylib_segment.\n");
        return NULL;
    }

    // Create copy of table
    phylib_table *segTable = phylib_copy_table(table);

    // Initialize time
    double segTime = PHYLIB_SIM_RATE;

    // Loop over time
    while (segTime < PHYLIB_MAX_TIME)
    {
        // Loop over objects
        for (int k = 0; k < PHYLIB_MAX_OBJECTS; ++k)
        {
            // Check if object is a rolling ball
            if (segTable->object[k] != NULL && segTable->object[k]->type == PHYLIB_ROLLING_BALL)
            {
                // Update rolling ball's position and velocity after rolling
                phylib_roll(segTable->object[k], table->object[k], segTime);
            }
        }

        // Nested loop for collisions
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
            {
                if (i != j && segTable->object[i] != NULL && segTable->object[i]->type == PHYLIB_ROLLING_BALL && segTable->object[j] != NULL)
                {
                    double distance = phylib_distance(segTable->object[i], segTable->object[j]);

                    // Check if distance is less than 0
                    if (distance < 0.0)
                    {
                        // Apply bounce function
                        phylib_bounce(&segTable->object[i], &segTable->object[j]);
                        
                        //Increment time 
                        segTable->time += segTime;
                        return segTable;
                    }
                }
            }

            // Check if any rolling ball has stopped after collisions
            if (segTable->object[i] != NULL && segTable->object[i]->type == PHYLIB_ROLLING_BALL && phylib_stopped(segTable->object[i]))
            {
                //Increment time
                segTable->time += segTime;

                //Return table 
                return segTable;
            }
        }
        // Increment the time
        segTime += PHYLIB_SIM_RATE;
    }

    //Return the table
    return segTable;
}

char *phylib_object_string( phylib_object *object ) {
    static char string[80];
    if (object==NULL) {
        snprintf( string, 80, "NULL;" );
        return string;
    }

    switch (object->type) {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
        break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
        break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
        break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
        break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
        break;
    }
    return string;
}
