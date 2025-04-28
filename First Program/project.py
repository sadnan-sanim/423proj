import random
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

trees = []
tree_spacing = 2.0   # Distance between trees
max_tree_distance = 50.0  # How far ahead trees are generated
day_time = 0.0
day_speed = 0.001  # Speed of time change
debris = []
debris_spawn_distance = 60.0
debris_spacing = 3.0

# Window size
width, height = 800, 600

# Player position
player_x, player_z = 0.0, 2.0
player_size = 0.2
move_speed = 0.2

# Bullet count
bullets = 5

# Road and pavement dimensions
road_segment_length = 1.0
road_width = 5.0
num_segments = 10
visible_range = 60.0

# Road/pavement and vehicle data
segments = []
vehicles = []

# Vehicle parameters
vehicle_size = 0.4
vehicle_speed = 0.05

# Mouse coordinates
mouse_x, mouse_y = 0, 0

def init():
    glClearColor(0.1, 0.1, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, width / height, 0.1, 100)
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
    global segments, vehicles

    if segments[0]["z_position"] + road_segment_length < player_z - visible_range:
        segments.pop(0)

    if segments[-1]["z_position"] < player_z + visible_range:
        segments.append({
            "z_position": segments[-1]["z_position"] + road_segment_length,
            "active": True,
            "vehicle_present": False
        })

    if random.random() < 0.02:
        spawn_vehicle()

    for vehicle in vehicles:
        if vehicle["direction"] == "left":
            vehicle["x_position"] -= vehicle["speed"]
        else:
            vehicle["x_position"] += vehicle["speed"]

    # Remove vehicles out of bounds
    vehicles = [v for v in vehicles if (-road_width/2 - vehicle_size) <= v["x_position"] <= (road_width/2 + vehicle_size)]

    # Update segment vehicle flags
    for segment in segments:
        segment["vehicle_present"] = any(
            abs(v["z_position"] - segment["z_position"]) < 0.01 for v in vehicles
        )

def draw_road():
    glPushMatrix()
    for segment in segments:
        if int(segment["z_position"] / road_segment_length) % 2 == 0:
            glColor3f(0.5, 0.5, 0.5)
        else:
            glColor3f(0.0, 0.5, 0.0)

        glBegin(GL_QUADS)
        glVertex3f(-road_width / 2, -0.05, segment["z_position"])
        glVertex3f(road_width / 2, -0.05, segment["z_position"])
        glVertex3f(road_width / 2, -0.05, segment["z_position"] + road_segment_length)
        glVertex3f(-road_width / 2, -0.05, segment["z_position"] + road_segment_length)
        glEnd()
    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(player_x, 0.0, player_z)
    glColor3f(1.0, 1.0, 0.0)
    glutSolidCube(player_size)
    glPopMatrix()

def draw_vehicles():
    for vehicle in vehicles:
        glPushMatrix()
        glTranslatef(vehicle["x_position"], 0.0, vehicle["z_position"])
        glColor3f(1.0, 0.0, 0.0)
        glutSolidCube(vehicle_size)
        glPopMatrix()

def draw_trees():
    for tree in trees:
        glPushMatrix()
        glTranslatef(tree["x"], 0.0, tree["z"])

        # Draw trunk
        glColor3f(0.55, 0.27, 0.07)  # Brown
        glPushMatrix()
        glTranslatef(0.0, 0.25, 0.0)
        glScalef(0.1, 0.5, 0.1)
        glutSolidCube(1.0)
        glPopMatrix()

        # Draw leaves
        glColor3f(0.0, 0.8, 0.0)  # Green
        glTranslatef(0.0, 0.6, 0.0)
        glutSolidSphere(0.3, 8, 8)

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
    glColor3f(237/255,201/255,175/255)  # Sandy color
    glBegin(GL_QUADS)
    glVertex3f(-100.0, -0.06, player_z - 50.0)
    glVertex3f(100.0, -0.06, player_z - 50.0)
    glVertex3f(100.0, -0.06, player_z + 200.0)
    glVertex3f(-100.0, -0.06, player_z + 200.0)
    glEnd()
    glPopMatrix()


def draw_mountains():
    glPushMatrix()
    glDisable(GL_LIGHTING)

    mountain_base = player_z + 55  # Near the sunset
    glColor3f(0.4, 0.3, 0.2)  # Brownish

    glBegin(GL_TRIANGLES)
    random.seed(0)  # Fixed seed for consistent mountains

    for i in range(-100, 100, 20):
        peak_x = i + random.randint(-5, 5)
        peak_height = random.uniform(5, 10)

        # Left triangle
        glVertex3f(i, 0.0, mountain_base)
        glVertex3f(i + 20, 0.0, mountain_base)
        glVertex3f(peak_x + 10, peak_height, mountain_base)
    glEnd()

    glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_sunset():
    glPushMatrix()
    glDisable(GL_LIGHTING)

    # Draw background sky (orange to purple)
    sunset_distance = player_z + 60.0
    glBegin(GL_QUADS)
    glColor3f(1.0, 0.5, 0.2)  # Bottom color (orange)
    glVertex3f(-100, -1.0, sunset_distance)
    glVertex3f(100, -1.0, sunset_distance)
    glColor3f(0.6, 0.0, 0.6)  # Top color (purple-ish)
    glVertex3f(100, 40.0, sunset_distance)
    glVertex3f(-100, 40.0, sunset_distance)
    glEnd()

    # Draw the sun
    glColor3f(1.0, 0.9, 0.0)  # Yellow
    glTranslatef(0.0, 10.0, sunset_distance - 0.5)  # Slightly in front
    glutSolidSphere(2.5, 32, 32)

    glPopMatrix()

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
            glColor3f(1.0, 1.0, 1.0)
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
        x_pos = side * random.uniform(6.0, 15.0)

        debris.append({
            "x": x_pos,
            "z": farthest_z,
            "size": random.uniform(0.1, 0.3),
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

def mouse_motion(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = height - y  # Flip Y to match OpenGL's bottom-left origin
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    cam_x = player_x
    cam_y = 1.5
    cam_z = player_z - 4.0

    gluLookAt(cam_x, cam_y, cam_z,
              player_x, 0.0, player_z,
              0.0, 1.0, 0.0)

    draw_sunset()
    # draw_mountains() 
    draw_desert_ground()
    update_debris()
    draw_debris()
    update_trees()
    draw_trees()

    update_road()
    draw_road()
    draw_vehicles()
    draw_player()
    draw_mouse_coords()

    glutSwapBuffers()



def keyboard(key, x, y):
    global player_x, player_z, bullets
    key = key.decode("utf-8").lower()

    if key == 'w':
        player_z += move_speed
    elif key == 's':
        player_z -= move_speed
    elif key == 'a':
        player_x -= move_speed
        # Clamp player inside left boundary
        if player_x < -road_width / 2 + player_size / 2:
            player_x = -road_width / 2 + player_size / 2
    elif key == 'd':
        player_x += move_speed
        # Clamp player inside right boundary
        if player_x > road_width / 2 - player_size / 2:
            player_x = road_width / 2 - player_size / 2
    elif key == ' ' and bullets > 0:
        bullets -= 1
        print("Used bullet! Remaining:", bullets)

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