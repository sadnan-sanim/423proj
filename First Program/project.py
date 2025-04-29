import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

initial_zpos=2.0
distanceCovered=0.0
movementSpeed=0.01
speed_increment=0.0001
max_speed= 0.25
coins= []
coinCount= 0
trees = []
tree_spacing = 8.5  # Distance between trees
max_tree_distance = 50.0  # How far ahead trees are generated
day_time = 0.0
day_speed = 0.001  # Speed of time change
debris = []
debris_spawn_distance = 30.0
debris_spacing = 3.0
game_over = False
score=0
# Window size
width, height = 800, 600

# Player position
player_x, player_z = 0.0, 2.0
player_size = 0.2
move_speed = 0.2

# Bullet count
bullets = 5

# Road and pavement dimensions
road_segment_length = 4.0
road_width = 5.3
num_segments = 10
visible_range = 60.0

# Road/pavement and vehicle data
segments = []
vehicles = []

# Vehicle parameters
vehicle_size = 0.4
vehicle_speed = 2

# Mouse coordinates
mouse_x, mouse_y = 0, 0

def init():
    glClearColor(0.1, 0.1, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.4, 100)
    glMatrixMode(GL_MODELVIEW)

    for i in range(num_segments):
        segments.append({
            "z_position": i * road_segment_length,
            "active": True,
            "vehicle_present": False
        })



def spawn_vehicle():
    side = random.choice(["left", "right"])

    eligible_segments = [s for s in segments if s["z_position"] > player_z and not s["vehicle_present"]]
    if not eligible_segments:
        return

    segment = random.choice(eligible_segments)
    z_position = segment["z_position"]
    segment["vehicle_present"] = True

    if side == "left":
        x_position = -road_width / 2 + vehicle_size / 2
        direction = "right"
    else:
        x_position = road_width / 2 - vehicle_size / 2
        direction = "left"

    speed = random.uniform(0.005, 0.01)

    vehicles.append({
        "x_position": x_position,
        "z_position": z_position,
        "direction": direction,
        "speed": speed
    })

def update_road():
    global segments, vehicles, player_x, player_z, game_over

    if game_over:
        return  # Stop updating if the game is over

    # Remove road segments that are too far behind
    if segments[0]["z_position"] + road_segment_length < player_z - visible_range:
        segments.pop(0)

    # Add new road segments ahead
    if segments[-1]["z_position"] < player_z + visible_range:
        segments.append({
            "z_position": segments[-1]["z_position"] + road_segment_length,
            "active": True,
            "vehicle_present": False
        })

    # Spawn vehicles randomly
    if random.random() < 0.02:
        spawn_vehicle()

    # Spawn coins randomly
    if random.random() < 0.03:
        spawn_coin_batch()

    # Update vehicle positions
    for vehicle in vehicles:
        if vehicle["direction"] == "left":
            vehicle["x_position"] -= vehicle["speed"]
        else:
            vehicle["x_position"] += vehicle["speed"]

    # Remove vehicles that are out of bounds
    vehicles = [v for v in vehicles if (-road_width / 2 - vehicle_size) <= v["x_position"] <= (road_width / 2 + vehicle_size)]

    # Update segment vehicle flags
    for segment in segments:
        segment["vehicle_present"] = any(
            abs(v["z_position"] - segment["z_position"]) < 0.01 for v in vehicles
        )

    # Check for collision with the player
    for vehicle in vehicles:
        if abs(vehicle["x_position"] - player_x) < (vehicle_size / 2 + player_size / 2) and \
           abs(vehicle["z_position"] - player_z) < (vehicle_size / 2 + player_size / 2):
            print("Game Over! The player was hit by a car.")
            game_over = True  # Set the game_over flag
            return  # Stop further updates
        
def draw_starting():
    glPushMatrix()
    glColor3f(48/255,93/255,75/255)
    glRotatef(-90,1,0,0)
    glTranslatef(-3,0,0)
    glBegin(GL_QUADS)
    glVertex3f(0,200,0)
    glVertex3f(0,0,0)
    glVertex3f(800,0,0)
    glVertex3f(200,0,0)
    glEnd()
    glPopMatrix()
def draw_road():
    draw_starting()
    glPushMatrix()
    for segment in segments:
        is_road = int(segment["z_position"] / road_segment_length) % 2 == 0

        if is_road:
            glColor3f(36/255,33/255,42/255)  # Road color
        else:
            glColor3f(48/255,93/255,75/255)  # Grass color

        # Draw road or grass
        glBegin(GL_QUADS)
        glVertex3f(-road_width / 2, -0.05, segment["z_position"])
        glVertex3f(road_width / 2, -0.05, segment["z_position"])
        glVertex3f(road_width / 2, -0.05, segment["z_position"] + road_segment_length)
        glVertex3f(-road_width / 2, -0.05, segment["z_position"] + road_segment_length)
        glEnd()

        # Draw dashed white road markings across
        if is_road:
            glColor3f(1.0, 1.0, 1.0)  # White color
            mark_width = 0.6           # Width of each mark
            mark_thickness = 0.1       # Thickness in Z direction
            mark_gap = 0.7             # Gap between marks

            start_x = -road_width / 2 + mark_gap  # start a bit inside
            end_x = road_width / 2 - mark_width - mark_gap  # end a bit inside

            x = start_x
            while x <= end_x:
                glBegin(GL_QUADS)
                glVertex3f(x, -0.04, segment["z_position"] + road_segment_length / 2 - mark_thickness / 2)
                glVertex3f(x + mark_width, -0.04, segment["z_position"] + road_segment_length / 2 - mark_thickness / 2)
                glVertex3f(x + mark_width, -0.04, segment["z_position"] + road_segment_length / 2 + mark_thickness / 2)
                glVertex3f(x, -0.04, segment["z_position"] + road_segment_length / 2 + mark_thickness / 2)
                glEnd()

                x += mark_width + mark_gap
    glPopMatrix()



def draw_player():
    glPushMatrix()
    glTranslatef(player_x, 0.0, player_z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 1.0, 1.0)
    glutSolidCone(0.1,0.4,32,32)
    glPopMatrix()
    # player head
    glPushMatrix()
    glTranslatef(player_x,0.4,player_z)
    glColor3f(1,1,1)
    glutSolidSphere(0.080,32,32)
    glPopMatrix()
    # hat
    glPushMatrix()
    glTranslate(player_x,0.40,player_z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(200/255,54/255,67/255)
    glutSolidCone(0.08,0.25,32,32)
    # glutSolidOctahedron()
    glPopMatrix()

def rgbconv(r,g,b):
    return (r/255,g/255,b/255)
def draw_circle(x, y, z, radius, slices=30):
    glBegin(GL_POLYGON)
    for i in range(slices):
        angle = 2 * math.pi * i / slices
        glVertex3f(x + radius * math.cos(angle), y, z + radius * math.sin(angle))
    glEnd()
def draw_wheel(x, y, z, radius, rotation_angle):
    # Rotate the wheel to the desired orientation
    glPushMatrix()
    glTranslatef(x, y, z)  # Move to the wheel position
    glColor3f(36/255, 75/255, 117/255)
    glRotatef(rotation_angle, 1, 0, 0)  # Rotate around the Y-axis (you can adjust axes as needed)
    draw_circle(0, 0, 0, radius)  # Draw the circle at the origin of the rotated position
    glPopMatrix()
def draw_vehicles():
    for vehicle in vehicles:
        sf=0.09
        glPushMatrix()
        glTranslatef(vehicle["x_position"], 0.0, vehicle["z_position"])
        # mainbody
        
        glColor3f( 189/255,  67/255, 54/255)
        glTranslatef(0.0,0,0.0)
        glScalef(2,1.0,0.79)
        glutSolidCube(0.4)
        glPopMatrix()
        # left part
        
        glPushMatrix()
        glTranslatef(vehicle["x_position"], 0.0, vehicle["z_position"])
        glColor3f(210/255, 209/255, 185/255)
        glTranslatef(0,0.34,0)
        glScalef(1.5,1.0,0.79)
        glutSolidCube(0.25)
        glPopMatrix()
        
        wheel_radius = 0.1
        wheel_offset = 0.2  # Adjust the position as needed
        wheel_rotation = 90
        draw_wheel(vehicle["x_position"] - wheel_offset, 0.03, vehicle["z_position"] - 0.35, wheel_radius, wheel_rotation)
        # Rear right wheel
        draw_wheel(vehicle["x_position"] + wheel_offset, 0.03, vehicle["z_position"] - 0.35, wheel_radius, wheel_rotation)

import random

def draw_trees():
    for tree in trees:
        glPushMatrix()
        glTranslatef(tree["x"], 0.0, tree["z"])

        # Draw trunk
        glColor3f(76/255, 44/255, 44/255)  # Brown
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0)
        glScalef(0.2, 3.0, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()

        # Draw leaves
        glColor3f(22/255, 113/255, 126/255)  # Green
        glTranslatef(0.0, 1.75, 0.0)  # Move to top of trunk

        num_fronds = 12
        frond_length = 1.5

        for i in range(num_fronds):
            glPushMatrix()

            # Random downward tilt between 20 to 45 degrees
            downward_tilt = random.uniform(40, 45)

            # Rotate downward first (X axis)
            glRotatef(downward_tilt, 1, 0, 0)

            # Then rotate around the trunk (Y axis)
            glRotatef((360 / num_fronds) * i, 0, 1, 0)

            glScalef(0.1, 0.1, frond_length)
            glutSolidSphere(1.0, 6, 6)

            glPopMatrix()

        glPopMatrix()



def update_trees():
    global trees

    # Find farthest z among existing trees
    farthest_z = max([tree["z"] for tree in trees], default=player_z)

    # Keep generating trees ahead
    while farthest_z < player_z + max_tree_distance:
        farthest_z += tree_spacing

        trees.append({
            "x": -road_width / 2 - 1.0,
            "z": farthest_z
        })
        trees.append({
            "x": road_width / 2 + 1.0,
            "z": farthest_z
        })

    # Remove trees that are too far behind
    trees = [tree for tree in trees if tree["z"] > player_z - 10.0]

def draw_desert_ground():
    glPushMatrix()
    glColor3f(191/255,116/255,100/255)  # Sandy color
    glBegin(GL_QUADS)
    glVertex3f(-100.0, -0.06, player_z - 50.0)
    glVertex3f(100.0, -0.06, player_z - 50.0)
    glVertex3f(100.0, -0.06, player_z + 200.0)
    glVertex3f(-100.0, -0.06, player_z + 200.0)
    glEnd()
    glPopMatrix()




def draw_sunset():
    glPushMatrix()
    glDisable(GL_LIGHTING)

    # Sun position based on visible road range
    sunset_distance = player_z + visible_range + 2.0  # small offset ahead to make it look on the horizon

    # Draw background sky (orange to purple)
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.5, 0.2)   # Bottom color (orange)
    glVertex3f(-100, -1.0, sunset_distance)
    glVertex3f(100, -1.0, sunset_distance)
    glColor3f(0.6, 0.0, 0.6)  # Top color (purple-ish)
    glVertex3f(100, 40.0, sunset_distance)
    glVertex3f(-100, 40.0, sunset_distance)
    glEnd()

    # Draw the sun
    glColor3f(254/255,212/255,153/255)  # Yellow
    glTranslatef(0.0, 1.0, sunset_distance - 0.5)  # (10 units high)
    glutSolidSphere(5.0, 32, 32) 

    glPopMatrix()
def draw_mountain(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(3.0, 3.0, 1.0)

    glDisable(GL_DEPTH_TEST)  # <-- temporarily disable depth test

    # Base layer - top lightest
    glColor3f(102/255, 49/255, 8/255)
    glBegin(GL_TRIANGLES)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glEnd()

    # Middle layer - medium
    glColor3f(93/255, 45/255, 8/255)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.8, 0.0, 0.01)
    glVertex3f(0.8, 0.0, 0.01)
    glVertex3f(0.0, 0.8, 0.01)
    glEnd()

    # Top layer - darkest
    glColor3f(79/255, 45/255, 8/255)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.5, 0.0, 0.02)
    glVertex3f(0.5, 0.0, 0.02)
    glVertex3f(0.0, 0.5, 0.02)
    glEnd()

    glEnable(GL_DEPTH_TEST)  # <-- re-enable depth test

    glPopMatrix()




def draw_mountain_range():
    global player_x,player_y
    spacing = 5
    z_base = player_z + 50  # far in the background

    for i in range(-100, 101, spacing):
        
        if i >5 or i<-5:
            draw_mountain(i, 0.0, z_base )  # slight z jitter for depth
        
# def draw_sunset():
#     global day_time

#     glPushMatrix()
#     glDisable(GL_LIGHTING)

#     # Animate sky color
#     sky_r = 0.2 + 0.8 * abs(math.sin(day_time))
#     sky_g = 0.4 + 0.4 * abs(math.sin(day_time))
#     sky_b = 0.8 * abs(math.cos(day_time))

#     sunset_distance = player_z + 60.0

#     glBegin(GL_QUADS)
#     glColor3f(sky_r, sky_g, sky_b)  # Bottom
#     glVertex3f(-100, -1.0, sunset_distance)
#     glVertex3f(100, -1.0, sunset_distance)

#     glColor3f(sky_r * 0.5, sky_g * 0.5, sky_b * 0.5)  # Top
#     glVertex3f(100, 40.0, sunset_distance)
#     glVertex3f(-100, 40.0, sunset_distance)
#     glEnd()

#     # Draw the sun/moon
#     if sky_b > 0.5:  # Daytime
#         glColor3f(1.0, 1.0, 0.0)  # Sun: yellow
#     else:
#         glColor3f(1.0, 1.0, 1.0)  # Moon: white

#     glTranslatef(0.0, 10.0, sunset_distance - 0.5)
#     glutSolidSphere(2.5, 32, 32)

#     glEnable(GL_LIGHTING)
#     glPopMatrix()

#     # Update time
#     day_time += day_speed
#     if day_time > 2 * math.pi:
#         day_time -= 2 * math.pi

def draw_debris():
    for d in debris:
        glPushMatrix()
        glTranslatef(d["x"], 0.0, d["z"])

        if d["type"] == "rock":
            glColor3f(0.3, 0.3, 0.3)
            glutSolidSphere(d["size"], 8, 8)
        elif d["type"] == "bone":
            glColor3f(102/255,51/255,0/255)
            glScalef(0.1, 0.1, 0.5)
            glutSolidCube(d["size"] * 10)

        glPopMatrix()

def update_debris():
    global debris

    farthest_z = max([d["z"] for d in debris], default=player_z)

    while farthest_z < player_z + debris_spawn_distance:
        farthest_z += debris_spacing

        # Random left or right side
        side = random.choice([-1, 1])
        x_pos = side * random.uniform(3.0, 15.0)

        debris.append({
            "x": x_pos,
            "z": farthest_z,
            "size": random.uniform(0.1, 0.9),
            "type": random.choice(["rock", "bone"])
        })

    # Remove debris that went too far behind
    debris = [d for d in debris if d["z"] > player_z - 10.0]

def draw_mouse_coords():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, 10)
    coord_text = f"Mouse: ({mouse_x}, {mouse_y})"
    for ch in coord_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def fire_bullet():
    global bullets, vehicles, game_over


    # Find the nearest vehicle directly ahead (small x-axis difference)
    closest_vehicle = None
    min_distance = float('inf')

    for vehicle in vehicles:
        # Check if vehicle is roughly in the same lane (small x-difference allowed)
        if abs(vehicle["x_position"] - player_x) < 0.5:
            # Check if vehicle is ahead of the player
            if vehicle["z_position"] > player_z:
                distance = vehicle["z_position"] - player_z
                if distance < min_distance:
                    min_distance = distance
                    closest_vehicle = vehicle

    if closest_vehicle:
        vehicles.remove(closest_vehicle)  # Remove the hit vehicle
        print("Shot a car!")
    else:
        print("Missed! No car ahead!")

    bullets -= 1  # Always reduce a bullet after shooting
    print(f"Bullets left: {bullets}")

    # Check if bullets are finished
    if bullets == 0:
        print("No bullets left!")
        


def mouse_motion(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = height - y  # Flip Y to match OpenGL's bottom-left origin
    glutPostRedisplay()
def draw_distance():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)
    distance_text = f"Distance: {int(distanceCovered)}"
    glRasterPos2f(10, height - 30)
    for ch in distance_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_score():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(1.0, 1.0, 0.0)
    score_text = f"Score: {score}"
    glRasterPos2f(10, height - 50)
    for ch in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_game_over():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)  # Set up orthographic projection

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Black background
    glDisable(GL_DEPTH_TEST)
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(width, 0)
    glVertex2f(width, height)
    glVertex2f(0, height)
    glEnd()

    # "YOU DIED" - Red text
    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(width // 2 - 50, height // 2 + 10)
    for c in "YOU DIED":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    # "PRESS R TO RESTART" - White text
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(width // 2 - 90, height // 2 - 20)
    for c in "PRESS R TO RESTART":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def spawn_coin_batch():
    eligible_segments = [s for s in segments if s["z_position"] > player_z + 5 and not s["vehicle_present"]]
    if not eligible_segments:
        return

    segment = random.choice(eligible_segments)

    batch_size = random.randint(2, 5)
    gap = 0.5  # gap between coins on Z-axis

    # Fixed x position across the batch (random horizontal lane on road)
    x_pos = random.uniform(-road_width / 2 + 0.5, road_width / 2 - 0.5)
    z_start = segment["z_position"] + random.uniform(0, road_segment_length)

    for i in range(batch_size):
        z = z_start + i * gap 
        coins.append({
            "x": x_pos,
            "z": z,
            "collected": False
        })

def draw_coins():
    for coin in coins:
        if not coin["collected"]:
            glPushMatrix()
            glTranslatef(coin["x"], 0.2, coin["z"])
            glColor3f(1.0, 0.84, 0.0)
            glutSolidSphere(0.1, 16, 16)
            glPopMatrix()

def coin_collision():
    global coinCount
    for coin in coins:
        if not coin["collected"]:
            if abs(player_x - coin["x"]) < 0.25 and abs(player_z - coin["z"]) < 0.25:
                coin["collected"] = True
                coinCount += 1
                print(f"Coins collected: {coinCount}")

def display():
    global game_over,initial_zpos,distanceCovered,score,player_z,movementSpeed,vehicle_speed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if game_over:
        draw_game_over()
        glutSwapBuffers()
        return 

    distanceCovered=player_z-initial_zpos
    player_z+=movementSpeed
    movementSpeed=min(movementSpeed+speed_increment,max_speed)
    score=int(distanceCovered/10)
    # vehicle_speed+=speed_increment
    # vehicle_speed=min(vehicle_speed,1)
    if game_over:
        # Display "Game Over" message
        glColor3f(1.0, 0.0, 0.0)  # Red color
        glRasterPos2f(-0.2, 0.0)  # Position the text
        for ch in "GAME OVER":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
        glutSwapBuffers()
        return  # Stop further rendering

    cam_x = player_x
    cam_y = 1
    cam_z = player_z - 5
    gluLookAt(cam_x, cam_y, cam_z,
              player_x, 0.0, player_z,
              0.0, 1.0, 0.0)

    draw_sunset()
    draw_mountain_range()
    draw_desert_ground()
    update_debris()
    draw_debris()
    update_trees()
    draw_trees()

    update_road()
    draw_road()
    draw_vehicles()
    draw_player()
    draw_coins()
    coin_collision()
    draw_mouse_coords()
    draw_distance()
    draw_score()
    glutSwapBuffers()



def keyboard(key, x, y):
    global player_x, player_z, bullets, game_over, vehicles, distanceCovered, initial_zpos, move_speed, movementSpeed, speed_increment, segments,coinCount
    key = key.decode("utf-8").lower()

    if game_over and key == 'r':
        player_x = 0.0
        player_z = initial_zpos
        bullets = 5
        movementSpeed = 0.01
        speed_increment = 0.0001
        vehicles.clear()
        distanceCovered = 0
        game_over = False
        coinCount=50
        trees.clear()
        update_trees()
        segments.clear()
        for i in range(num_segments):
            segments.append({
                "z_position": i * road_segment_length,
                "active": True,
                "vehicle_present": False
            })

        return

    if not game_over:
        if key == 'w':
            player_z += move_speed
        elif key == 'a':
            player_x += move_speed
            # Clamp player inside left boundary
            if player_x < -road_width / 2 + player_size / 2:
                player_x = -road_width / 2 + player_size / 2
        elif key == 'd':
            player_x -= move_speed
            # Clamp player inside right boundary
            if player_x > road_width / 2 - player_size / 2:
                player_x = road_width / 2 - player_size / 2
        elif key == ' ' and bullets > 0:
            fire_bullet()
        # Powerup 1: Increase bullet count by 1 (key: J)
        elif key == 'j':
            if coinCount >= 5:
                bullets += 1
                coinCount -= 5
                print("Powerup Activated: +1 Bullet")
            else:
                print("Not enough coins for Bullet Powerup!")

        # Powerup 2: Halve movement speed (key: K)
        elif key == 'k':
            if coinCount >= 10:
                movementSpeed = movementSpeed / 2
                coinCount -= 10
                print("Powerup Activated: Halved Speed")
            else:
                print("Not enough coins for Slowdown Powerup!")

        # Powerup 3: Bomb - Destroy vehicles in range (key: L)
        elif key == 'l':
            if coinCount >= 20:
                bomb_radius = 10.0  # Define radius around player
                vehicles[:] = [v for v in vehicles if math.hypot(v["x_position"] - player_x, v["z_position"] - player_z) > bomb_radius]
                coinCount -= 20
                print("Powerup Activated: Bomb!")
            else:
                print("Not enough coins for Bomb Powerup!")


    glutPostRedisplay()



def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"Crossy Game 3D with Vehicles - PyOpenGL")

    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(display)
    glutPassiveMotionFunc(mouse_motion)
    glutMainLoop()


main()