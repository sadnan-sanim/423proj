import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Window size
width, height = 800, 600

# Player position
player_x, player_z = 0.0, 2.0
player_size = 0.2
move_speed = 0.2

# Bullet count
bullets = 5

# Road and pavement dimensions
road_segment_length = 2.0
road_width = 7.0
num_segments = 20
visible_range = 10.0

# Road/pavement and vehicle data
segments = []
vehicles = []

# Vehicle parameters
vehicle_size = 0.5


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
    vehicles = [v for v in vehicles if -road_width <= v["x_position"] <= road_width]

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
    elif key == 'd':
        player_x += move_speed
    elif key == ' ' and bullets > 0:
        bullets -= 1
        print("Used bullet! Remaining:", bullets)

    glutPostRedisplay()

def sadnan_gay():
    
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
