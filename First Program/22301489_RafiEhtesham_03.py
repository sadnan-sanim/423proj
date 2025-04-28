from OpenGL.GL import *
from OpenGL.GLUT import *  # Import all GLUT functions
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18  # Explicitly import the font
from OpenGL.GLU import *
from math import *
import random

last_camera_coords = None
# Camera-related variables
camera_pos = (0,500,500)
first_person_mode = False  # Flag to indicate if the camera is in first-person mode
cheat_mode = False  # Flag to indicate if cheat mode is activated
gun_follow_mode = False  # Flag to indicate if the gun follows the camera

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423

game_over = False  # Flag to indicate if the game is over
life_remaining = 5
score = 0
bullets_missed = 0

player_pos = (0, 0, 0)  # Player position
player_angle = 0  # Player angle
player_fall_angle = 0  # Player fall angle
player_rotate_speed = 10  # Player rotation speed
player_speed = 30  # Player speed
gun_barrel_length = 80  # Length of the gun barrel


bullet_speed = 10 # Bullet speed
bullet_height = 100 # Bullet height
bullet_pos = player_pos  # Bullet position
bullet_angle = player_angle  # Bullet angle
bullets = []  # List to store bullet positions and angles

enemies = []  # List to store enemy positions
enemy_radius = 50  # Radius of the enemy for collision detection
enemy_speed = 0.15  # Speed at which enemies move toward the player
time_elapsed = 0  # Tracks the elapsed time for pulsing

def spawn_enemy():
    """
    Spawns a new enemy at a random position within the grid.
    """
    x = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
    y = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
    z = 50  # Fixed height for enemies
    enemies.append({'pos': (x, y, z)})

def initialize_enemies():
    """
    Initializes the grid with 5 enemies.
    """
    global enemies
    existing_enemies = len(enemies)
    for _ in range(5-existing_enemies):
        spawn_enemy()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
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

def draw_shapes():
    drawPlayer()
    drawEnemies()
    drawBullets()

def drawPlayer():
    global player_pos, player_fall_angle, game_over, player_angle

    glPushMatrix()  # Save the current matrix state

    x, y, z = player_pos  # Unpack player position
    glTranslatef(x, y, z)  # Move to the position of the player
    glRotatef(180, 0, 0, 1)  # Rotate to align with the player's direction
    glRotatef(player_angle, 0, 0, 1)  # Rotate to align with the player's direction
    if game_over:
        glRotatef(player_fall_angle, 0, 1, 0)

    glColor3f(0, 0.4, 0)
    glTranslatef(0, 0, 100)  
    glScalef(0.5, 1, 2)  # Scale the cube to make it a cuboid (2x width, 1x height, 1x depth)
    glutSolidCube(50) # Take cube size as the parameter
    glScalef(2, 1, 0.5)
    glTranslatef(0, 0, -100)
    
    glColor3f(0, 0, 1)
    glTranslatef(0, 10, 50)
    glRotatef(180, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glRotatef(-180, 0, 1, 0)  # parameters are: angle, x, y, z
    glTranslatef(0, -10, -50)
    glTranslatef(0, -10, 50)
    glRotatef(180, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glRotatef(-180, 0, 1, 0)  # parameters are: angle, x, y, z
    glTranslatef(0, 10, -50)
    
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 165) 
    gluSphere(gluNewQuadric(), 15, 10, 10)  # parameters are: quadric, radius, slices, stacks
    glTranslatef(0, 0, -165) 
    
    glColor3f(1, 0.8, 0.6)  # Skin color (light peach)
    glTranslatef(0, 30, 125)
    glRotatef(-90, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    glTranslatef(0, -30, -125)
    glTranslatef(0, -30, 125)
    glRotatef(-90, 0, 1, 0)  # parameters are: angle, x, y, z
    gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    glTranslatef(0, 30, -125)

    glColor3f(0.5, 0.5, 0.5)  # Gray color for the gun
    glTranslatef(0, 0, 125)  # Move to the position of the gun
    glRotatef(-90, 0, 1, 0)  # Rotate to align with the gun direction
    glScalef(1, 1, 2)  # Scale the cylinder to make it look like a gun barrel
    gluCylinder(gluNewQuadric(), 10, 3, 40, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glScalef(1, 1, 0.5)  # Scale the cylinder to make it look like a gun barrel
    glRotatef(90, 0, 1, 0)  # Rotate back to original orientation
    glTranslatef(0, 0, -125)  # Move back to the original position

    glPopMatrix()  # Restore the previous matrix state

def drawEnemies():
    global enemies, time_elapsed, enemy_radius

    scale_factor = 1 + 0.2 * sin(time_elapsed)  # Oscillates between 0.8 and 1.2

    for enemy in enemies:
        glPushMatrix()  # Save the current matrix state

        x, y, z = enemy['pos']  # Extract enemy position
        glTranslatef(x, y, z)  # Move to the position of the enemy
        glScalef(scale_factor, scale_factor, scale_factor)  # Scale the enemy for pulsing effect
        glColor3f(1, 0, 0)  # Red color for the enemy
        glutSolidSphere(enemy_radius, 10, 10)  # Draw the main body of the enemy
        glColor3f(0, 0, 0)  # Black color for the enemy's detail
        glTranslatef(0, 0, 75)  # Adjust position for the detail
        glutSolidSphere(enemy_radius//2 , 10, 10)  # Draw the detail
        glTranslatef(0, 0, -75)  # Move back to the original position
        
        glPopMatrix()  # Restore the previous matrix state

def drawBullets():
    global bullets
    # Draw each bullet
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
        glRotatef(bullet['angle'], 0, 0, 1)  # Rotate to align with the bullet's direction
        glColor3f(1, 0, 0)  # Red color for the bullet
        glutSolidCube(10)  # Draw a cube with size 20
        glPopMatrix()

def is_enemy_in_line_of_sight(player_pos, player_angle, enemy_pos, tolerance=1):
    """
    Checks if an enemy is in the player's line of sight.
    :param player_pos: Position of the player (x, y, z)
    :param player_angle: Angle of the player's gun
    :param enemy_pos: Position of the enemy (x, y, z)
    :param tolerance: Angle tolerance for line of sight (in degrees)
    :return: True if the enemy is in line of sight, False otherwise
    """
    # Calculate the direction vector of the gun
    gun_dx = cos(radians(player_angle))
    gun_dy = sin(radians(player_angle))

    # Calculate the vector from the player to the enemy
    enemy_dx = enemy_pos[0] - player_pos[0]
    enemy_dy = enemy_pos[1] - player_pos[1]

    # Normalize the enemy vector
    distance = sqrt(enemy_dx**2 + enemy_dy**2)
    if distance == 0:
        return False  # Enemy is at the same position as the player
    enemy_dx /= distance
    enemy_dy /= distance

    # Calculate the dot product between the gun direction and the enemy direction
    dot_product = gun_dx * enemy_dx + gun_dy * enemy_dy

    # Calculate the angle between the two vectors
    angle = degrees(acos(dot_product))

    # Check if the angle is within the tolerance
    return abs(angle) <= tolerance

def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global camera_pos, life_remaining, score, bullets_missed, player_pos, player_angle, player_speed, player_rotate_speed, cheat_mode, gun_follow_mode, game_over, first_person_mode
    # # Move forward (W key)
    if key == b'w':  
        dx = player_speed * cos(radians(player_angle))  # Change in x based on angle
        dy = player_speed * sin(radians(player_angle))  # Change in y based on angle
        if -GRID_LENGTH <= player_pos[0] + dx <= GRID_LENGTH and -GRID_LENGTH <= player_pos[1] + dy <= GRID_LENGTH:
            player_pos = (player_pos[0] + dx, player_pos[1] + dy, player_pos[2])  # Update position
            # print(f"Player moved forward to {player_pos}")

    # # Move backward (S key)
    if key == b's':
        dx = player_speed * cos(radians(player_angle))  # Change in x based on angle
        dy = player_speed * sin(radians(player_angle))  # Change in y based on angle
        if -GRID_LENGTH <= player_pos[0] - dx <= GRID_LENGTH and -GRID_LENGTH <= player_pos[1] - dy <= GRID_LENGTH:
            player_pos = (player_pos[0] - dx, player_pos[1] - dy, player_pos[2])  # Update position
            # print(f"Player moved backward to {player_pos}")

    # # Rotate gun left (A key)
    if key == b'a':
        player_angle += player_rotate_speed
        # camera_pos = (camera_pos[0], camera_pos[1] + 10, camera_pos[2])  # Move camera backward

    # # Rotate gun right (D key)
    if key == b'd':
        player_angle -= player_rotate_speed
        # camera_pos = (camera_pos[0], camera_pos[1] - 10, camera_pos[2])  # Move camera backward

    # # Toggle cheat mode (C key)
    if key == b'c':
        cheat_mode = not cheat_mode  # Toggle cheat mode
        if cheat_mode:
            print("Cheat mode activated!")
        else:
            print("Cheat mode deactivated!")
    
    # # Toggle cheat vision (V key)
    if key == b'v':
        if cheat_mode and first_person_mode:
            gun_follow_mode = not gun_follow_mode  # Toggle gun-following mode
            if gun_follow_mode:
                print("Gun-following mode activated!")
            else:
                print("Gun-following mode deactivated!")


    # # Reset the game if R key is pressed
    if key == b'r':
        
        """Resets the game state to its initial values."""
        global game_over, life_remaining, score, bullets_missed
        
        game_over = False  # Reset game over flag
        cheat_mode = False  # Reset cheat mode flag 
        life_remaining = 5  # Reset life remaining
        score = 0  # Reset score
        bullets_missed = 0  # Reset missed bullets
        player_pos = (0, 0, 0)  # Reset player position
        player_angle = 0  # Reset player angle
        player_speed = 10  # Reset player speed
        player_rotate_speed = 10  # Reset player rotation speed
        bullets.clear()  # Clear bullets list
        enemies.clear()  # Clear enemies list
        initialize_enemies()  # Reinitialize enemies
        print("Game restarted!")
        
def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, first_person_mode
    if not first_person_mode:
        x, y, z = camera_pos
        # Move camera up (UP arrow key)
        if key == GLUT_KEY_UP:
            z += 10  # Small angle decrement for smooth movement

        # # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN:
            z -= 10  # Small angle increment for smooth movement

        # moving camera left (LEFT arrow key)
        if key == GLUT_KEY_LEFT:
            angle = -1  # Angle decrement for rotation to the left
            x = x * cos(radians(angle)) - y * sin(radians(angle))
            y = x * sin(radians(angle)) + y * cos(radians(angle))
            
        # moving camera right (RIGHT arrow key)
        if key == GLUT_KEY_RIGHT:
            angle = 1  # Angle increment for rotation
            x = x * cos(radians(angle)) - y * sin(radians(angle))
            y = x * sin(radians(angle)) + y * cos(radians(angle))

        camera_pos = (x, y, z)

def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global player_pos, player_angle, bullets, bullet_height, bullet_speed, camera_pos, gun_barrel_length, first_person_mode, fovY

        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Calculate the bullet's initial position at the tip of the gun nozzle
        bullet_x = player_pos[0] + gun_barrel_length * cos(radians(player_angle))
        bullet_y = player_pos[1] + gun_barrel_length * sin(radians(player_angle))
        bullet_z = bullet_height  # Same height as the gun nozzle

        # Create a new bullet with the correct position and angle
        bullet = {
            'pos': (bullet_x, bullet_y, bullet_z),  # Start at the gun nozzle
            'angle': player_angle  # Use the player's angle for the bullet
        }
        bullets.append(bullet)

    # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode  # Toggle first-person mode
        if first_person_mode:
            fovY = 90  # Narrower field of view for first-person mode
            print("First-person mode activated")
        else:
            fovY = 120
            camera_pos = (0, 500, 500)  # Reset camera position for third-person mode
            print("Third-person mode activated")

def check_aabb_collision_2d(pos1, size1, pos2, size2):
    """
    Checks for axis-aligned bounding box (AABB) collision between two objects in 2D (ignoring z-axis).
    :param pos1: Position of the first object (x, y, z)
    :param size1: Size (radius or half-width) of the first object
    :param pos2: Position of the second object (x, y, z)
    :param size2: Size (radius or half-width) of the second object
    :return: True if the objects collide in 2D, False otherwise
    """
    return (
        abs(pos1[0] - pos2[0]) <= size1 + size2 and  # Check overlap in x-axis
        abs(pos1[1] - pos2[1]) <= size1 + size2      # Check overlap in y-axis
    )


def update():
    """
    Handles all game logic, such as player movement, bullet updates, enemy movement,
    collision detection, and score updates.
    """
    global bullets, enemies, life_remaining, score, bullets_missed, time_elapsed, player_pos, player_angle, player_speed, player_rotate_speed, game_over, first_person_mode, camera_pos, cheat_mode, gun_follow_mode, player_fall_angle
    
    if game_over:
        if player_fall_angle < 90:
            player_fall_angle += 2
        return

    time_elapsed += 0.05  # Increment time elapsed

    # Cheat mode logic
    if cheat_mode:
        # Continuously rotate the gun
        player_angle += player_rotate_speed * 0.25 # Rotate the gun slowly

        # Check for enemies in line of sight
        for enemy in enemies:
            if is_enemy_in_line_of_sight(player_pos, player_angle, enemy['pos']):
                # Fire a bullet toward the enemy
                bullet_x = player_pos[0] + gun_barrel_length * cos(radians(player_angle))
                bullet_y = player_pos[1] + gun_barrel_length * sin(radians(player_angle))
                bullet_z = bullet_height  # Same height as the gun nozzle

                bullet = {
                    'pos': (bullet_x, bullet_y, bullet_z),  # Start at the gun nozzle
                    'angle': player_angle  # Use the player's angle for the bullet
                }
                bullets.append(bullet)
                break  # Fire only one bullet per frame

    # Update bullets
    for bullet in bullets:
        # Move the bullet forward
        bullet['pos'] = (
            bullet['pos'][0] + bullet_speed * cos(radians(bullet['angle'])),
            bullet['pos'][1] + bullet_speed * sin(radians(bullet['angle'])),
            bullet['pos'][2]
        )

        # Check if the bullet goes out of bounds
        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][1]) > GRID_LENGTH:
            bullets.remove(bullet)  # Remove the bullet
            bullets_missed += 1  # Increment the missed bullets counter
            print(f"Bullet missed! Total missed: {bullets_missed}")

            # Check if the game is over
            if bullets_missed >= 10:
                game_over = True
                print("Game Over! You missed too many bullets.")
                return  # Stop further updates


    # Check for collisions between bullets and enemies
    for bullet in bullets[:]:  # Iterate over a copy of the bullets list
        for enemy in enemies[:]:  # Iterate over a copy of the enemies list
            if check_aabb_collision_2d(bullet['pos'], 10, enemy['pos'], enemy_radius):  # Bullet size = 10
                # print(f"Collision detected! Bullet: {bullet['pos']}, Enemy: {enemy['pos']}")
                bullets.remove(bullet)  # Remove the bullet
                enemies.remove(enemy)  # Remove the enemy
                score += 1  # Increment the score
                # print(f"Enemy hit! Score: {score}")
                break  # Exit the inner loop after handling the collision

    # Check for collisions between the player and enemies
    for enemy in enemies[:]:
        if check_aabb_collision_2d(player_pos, 25, enemy['pos'], enemy_radius):  # Player size = 25
            print(f"Player collided with enemy at {enemy['pos']}")
            enemies.remove(enemy)  # Remove the enemy
            life_remaining -= 1  # Decrement life
            print(f"Life remaining: {life_remaining}")

            # Check if the game is over
            if life_remaining <= 0:
                game_over = True
                print("Game Over! You ran out of lives.")
                return  # Stop further updates
    
    # Move enemies toward the player
    for enemy in enemies:
        ex, ey, ez = enemy['pos']  # Enemy position
        px, py, pz = player_pos  # Player position

        # Calculate direction vector from enemy to player
        dx = px - ex
        dy = py - ey
        dz = pz - ez

        # Normalize the direction vector
        distance = sqrt(dx**2 + dy**2 + dz**2)
        if distance > 0:  # Avoid division by zero
            dx /= distance
            dy /= distance
            dz /= distance

        # Update enemy position
        enemy['pos'] = (
            ex + dx * enemy_speed,
            ey + dy * enemy_speed,
            ez + dz * enemy_speed
        )
    
    initialize_enemies()  # Initialize enemies

def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    global first_person_mode, player_pos, player_angle, gun_follow_mode, cheat_mode, camera_pos, last_camera_coords
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if first_person_mode:
        # First-person mode: Position the camera at the player's head
        head_offset = 200  # Height of the player's head
        shoulder_offset = -25  # Offset to the right shoulder
        backward_offset = 75  # Offset to move the camera slightly behind
        x, y, z = player_pos

        # Calculate the right direction vector based on the player's angle
        right_x = -sin(radians(player_angle)) * shoulder_offset
        right_y = cos(radians(player_angle)) * shoulder_offset

        # Calculate the backward direction vector based on the player's angle
        backward_x = -cos(radians(player_angle)) * backward_offset
        backward_y = -sin(radians(player_angle)) * backward_offset

        camera_x = x + gun_barrel_length * cos(radians(player_angle)) * 0.25 + right_x + backward_x
        camera_y = y + gun_barrel_length * sin(radians(player_angle)) * 0.25 + right_y + backward_y
        camera_z = z + head_offset
        
    
        # Freeze camera rotation if gun_follow_mode is active
        if first_person_mode and gun_follow_mode:
            gluLookAt(last_camera_coords[0], last_camera_coords[1], last_camera_coords[2],  # Camera position
                    last_camera_coords[3], last_camera_coords[4], last_camera_coords[5],  # Look-at target
                    0, 0, 1)
        else:
            look_at_x = camera_x + cos(radians(player_angle))
            look_at_y = camera_y + sin(radians(player_angle))
            last_camera_coords = (camera_x, camera_y, camera_z, look_at_x, look_at_y, camera_z)
            gluLookAt(camera_x, camera_y, camera_z,  # Camera position
                    look_at_x, look_at_y, camera_z,  # Look-at target
                    0, 0, 1)  # Up vector (z-axis)
        
        # print(f"Camera position: {camera_x}, {camera_y}, {camera_z}")
        # print(f"Camera look-at: {look_at_x}, {look_at_y}, {camera_z}")
    else:
        # Third-person mode: Default camera position
        x, y, z = camera_pos
        gluLookAt(x, y, z,  # Camera position
                  0, 0, 0,  # Look-at target
                  0, 0, 1)  # Up vector (z-axis)

def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    update()
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """

    global game_over

    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw the grid (game floor)
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, 100):
        for j in range(-GRID_LENGTH, GRID_LENGTH, 100):
            if (i + j) % 200 == 0:
                glColor3f(1, 1, 1)  # Gray color
            else:
                glColor3f(0.7, 0.5, 0.95)  # Darker gray color
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)
    glEnd()

    # Drawing the walls of the game
    wall_height = 100
    glBegin(GL_QUADS)
    glColor3f(0, 0, 1)  # Blue color / Top Wall
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    glColor3f(0, 1, 1)  # Cyan color / Left Wall
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    glColor3f(1, 1, 0)  # Yellow color / Bottom Wall
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)  

    glColor3f(1, 0, 1)  # Magenta color / Right Wall
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)

    glEnd()
    

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"Player Life Remaining: {life_remaining}")
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Player Bullet Missed: {bullets_missed}")

    # Check if the game is over
    if game_over:
        draw_text(400, 750, "GAME OVER", font=GLUT_BITMAP_HELVETICA_18)
        draw_text(400, 710, "Press R to Restart", font=GLUT_BITMAP_HELVETICA_18)
        drawPlayer()
    else:
        draw_shapes()

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