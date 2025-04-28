from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Camera-related variables
camera_pos = (0, 500, 500)

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423
player_pos = [0, 0]
first_person=False
enemies=[]
cheat_mode=False
bullets=[]
score = 0
lives=5
missed=0
game_over=False
def reset_game():
    global bullets, enemies, score, lives, missed, player_pos, gun_angle, game_over, cheat_last_fire_angle
    bullets.clear()
    enemies.clear()
    score = 0
    lives = 5
    missed = 0
    player_pos = [0, 0]
    gun_angle = 0
    game_over = False
    cheat_last_fire_angle = None
    spawn_enemies()
def spawn_enemies():
    while len(enemies) < 5:
        x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        if math.hypot(x - player_pos[0], y - player_pos[1]) > 100:
            enemies.append({'x': x, 'y': y, 'pulse': 1.0, 'dir': 0.02})
def draw_enemies():
    for e in enemies:
        glPushMatrix()
        glTranslatef(e['x'], e['y'], 10)
        glColor3f(1, 0, 0)
        glutSolidSphere(10 * e['pulse'], 10, 10)
        glTranslatef(0, 0, 20)
        glutSolidSphere(10 * e['pulse'], 10, 10)
        glTranslatef(0, 0, 15)
        glColor3f(0, 0, 0)
        glutSolidSphere(6 * e['pulse'], 10, 10)
        glPopMatrix()
def update_enemies():
    global lives, game_over
    for e in enemies[:]:
        dx = player_pos[0] - e['x']
        dy = player_pos[1] - e['y']
        dist = math.hypot(dx, dy)
        if dist < 20:
            enemies.remove(e)
            lives -= 1
            spawn_enemies()
            if lives <= 0:
                game_over = True
            continue
        if dist > 0:
            e['x'] += 5 * dx / dist
            e['y'] += 5 * dy / dist
        e['pulse'] += e['dir']
        if e['pulse'] > 1.4 or e['pulse'] < 0.8:
            e['dir'] *= -1

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def drawCuboid(width, height, depth):
    w = width / 2
    h = height / 2
    d = depth / 2
    glBegin(GL_QUADS)

    # Front face
    glVertex3f(-w, -h, d)
    glVertex3f(w, -h, d)
    glVertex3f(w, h, d)
    glVertex3f(-w, h, d)

    # Back face
    glVertex3f(-w, -h, -d)
    glVertex3f(-w, h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, -h, -d)

    # Top face
    glVertex3f(-w, h, -d)
    glVertex3f(-w, h, d)
    glVertex3f(w, h, d)
    glVertex3f(w, h, -d)

    # Bottom face
    glVertex3f(-w, -h, -d)
    glVertex3f(w, -h, -d)
    glVertex3f(w, -h, d)
    glVertex3f(-w, -h, d)

    # Right face
    glVertex3f(w, -h, -d)
    glVertex3f(w, h, -d)
    glVertex3f(w, h, d)
    glVertex3f(w, -h, d)

    # Left face
    glVertex3f(-w, -h, -d)
    glVertex3f(-w, -h, d)
    glVertex3f(-w, h, d)
    glVertex3f(-w, h, -d)

    glEnd()

def draw_shapes():
    glPushMatrix()  # Save the current matrix state
    glColor3f(0.2, .48, .32)
    glTranslatef(0, 0, 70)
    drawCuboid(70,60,70)  # Take cube size as the parameter
    glTranslatef(0, 0, 60)
    glColor3f(0, 1, 0)
    # glutSolidCube(60)

    # glColor3f(1, 1, 0)
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10,
    #             10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100)
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    glColor3f(0, 1, 1)
    glTranslatef(0,0, 0)
    gluSphere(gluNewQuadric(), 30, 10, 10)
    # parameters are: quadric, radius, slices, stacks

    glColor3f(235/255, 210/255, 157/255)
    glTranslatef(22,26,-35)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(),10,4,40,50,50)


    glColor3f(63/255, 72/255, 74/255)
    glTranslatef(-22, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 4, 50, 50, 50)

    glColor3f(235/255, 210/255, 157/255)
    glTranslatef(-22,0,0)


    gluCylinder(gluNewQuadric(), 10, 4, 40, 50, 50)
    glColor3f(25/255, 42/255, 230/255)
    glTranslatef(40, 60, -20)
    glRotate(-90,1,0,0)
    gluCylinder(gluNewQuadric(), 15, 7, 35, 50, 50)
    glTranslatef(-35, 0, 0)

    gluCylinder(gluNewQuadric(), 15, 7, 35, 50, 50)

    glPopMatrix()  # Restore the previous matrix state


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos
    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        y+=20

    # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        y-=20

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        x -= 20  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        x += 20  # Small angle increment for smooth movement

    camera_pos = (x, y, z)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    # # Left mouse button fires a bullet
    # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

    # # Right mouse button toggles camera tracking mode
    # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    px, py = player_pos
    if first_person:
        look_x = px + math.cos(math.radians(gun_angle)) * 100
        look_y = py + math.sin(math.radians(gun_angle)) * 100
        gluLookAt(px, py, 35, look_x, look_y, 35, 0, 0, 1)
    else:
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 0, 1)

def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # # Draw a random points
    # glPointSize(20)
    # glBegin(GL_POINTS)
    # glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # glEnd()

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, 40):
        for j in range(-GRID_LENGTH, GRID_LENGTH, 40):
            if (i + j) % 80 == 0:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(1.9, 0.85, 0.6)
            glVertex3f(i, j, 0)
            glVertex3f(i + 40, j, 0)
            glVertex3f(i + 40, j + 40, 0)
            glVertex3f(i, j + 40, 0)
    glEnd()
    wall_colors = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0)]
    wall_pos = [(-GRID_LENGTH, 0), (GRID_LENGTH, 0), (0, -GRID_LENGTH), (0, GRID_LENGTH)]
    for color, pos in zip(wall_colors, wall_pos):
        glColor3f(*color)
        glPushMatrix()
        glTranslatef(pos[0], pos[1], 100)
        glScalef(10, 10, 200)
        glutSolidCube(1)
        glPopMatrix()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")

    draw_shapes()
    draw_enemies()
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop


if __name__ == "__main__":
    main()
