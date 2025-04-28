from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# player_rotation = 0
camera_pos = (0, 500, 500)
fovY = 120
GRID_LENGTH = 600
player_pos = [0, 0]
gun_angle = 0
first_person = False
cheat_mode = False
cheat_vision = False

enemies = []
bullets = []
score = 0
lives = 5
missed = 0
game_over = False
player_speed = 10
bullet_speed = 20
ENEMY_SPEED = 0.3
BULLET_SIZE = 10
enemy_counter = 0

def resetGame():
    global bullets, enemies, score, lives, missed, player_pos, gun_angle, game_over
    print()
    bullets.clear()
    enemies.clear()
    score = 0
    lives = 5
    missed = 0
    player_pos = [0, 0]
    gun_angle = 0

    game_over = False

    targeted_enemy_ids.clear()
    enemySpawn()

def enemySpawn():
    global enemy_counter
    while len(enemies) < 5:
        x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        if math.hypot(x - player_pos[0], y - player_pos[1]) > 150:
            enemies.append({
                'id': enemy_counter,
                'x': x,
                'y': y,
                'pulse': 1.0,
                'dir': 0.02
            })
            enemy_counter += 1


def enemyUpdate():
    global lives, game_over
    for e in enemies[:]:
        dx = player_pos[0] - e['x']
        dy = player_pos[1] - e['y']
        dist = math.hypot(dx, dy)
        if dist < 30:
            enemies.remove(e)

            lives -= 1
            print('Remaining Player Life:',lives)
            enemySpawn()
            if lives <= 0:
                game_over = True
                enemies.clear()
            continue
        if dist > 0:
            e['x'] += ENEMY_SPEED * dx / dist
            e['y'] += ENEMY_SPEED * dy / dist
        e['pulse'] += e['dir']
        if e['pulse'] > 1.4 or e['pulse'] < 0.8:
            e['dir'] *= -1

def bulletUpdate():
    global bullets, score, missed, game_over
    for bullet in bullets[:]:
        bullet['x'] += bullet['dx']
        bullet['y'] += bullet['dy']
        bullet['z'] += bullet['dz']
        hit = False
        for enemy in enemies[:]:

            dist = math.sqrt(
                (bullet['x'] - enemy['x'])**2 +
                (bullet['y'] - enemy['y'])**2 +
                (bullet['z'] - 100)**2
            )
            if dist < 45:
                targeted_enemy_ids.discard(enemy['id'])
                enemies.remove(enemy)
                enemySpawn()
                score += 10
                bullets.remove(bullet)
                hit = True
                break

        if not hit and (abs(bullet['x']) > GRID_LENGTH or abs(bullet['y']) > GRID_LENGTH or bullet['z'] < 0 or bullet['z'] > 200):
            bullets.remove(bullet)

            missed += 1
            print("Bullet missed:",missed)
            if missed >= 10:
                game_over = True

targeted_enemy_ids = set() 
# tracks tagetd enmy
def cheating():
    global gun_angle, bullets, targeted_enemy_ids
    if not cheat_mode or game_over:
        return

    gun_angle = (gun_angle + 2) % 360

    angle_fixed = (gun_angle + 90) % 360

    for enemy in enemies:
        if enemy['id'] in targeted_enemy_ids:
            continue

        dx = enemy['x'] - player_pos[0]
        dy = enemy['y'] - player_pos[1]
        angle_to_enemy = math.degrees(math.atan2(dy, dx)) % 360
        distance = math.hypot(dx, dy)
        angle_diff = abs((angle_to_enemy - angle_fixed + 180) % 360 - 180)

        if angle_diff < 10:
            norm_dx = dx / distance
            norm_dy = dy / distance
            bullets.append({
                'x': player_pos[0] + norm_dx * 40,
                'y': player_pos[1] + norm_dy * 40,
                'z': 95,
                'dx': norm_dx * bullet_speed,
                'dy': norm_dy * bullet_speed,
                'dz': 0,
                'target_id': enemy['id']  # bullet tag
            })
            targeted_enemy_ids.add(enemy['id'])

            break


def keyboardListener(key, x, y):
    global gun_angle, cheat_mode, cheat_vision, player_pos, game_over, first_person
    angle_fixed=gun_angle+90
    if game_over and key == b'r':
        resetGame()
        return
    if game_over: return

    if key == b'w':
        player_pos[0] += math.cos(math.radians(angle_fixed)) * player_speed
        player_pos[1] += math.sin(math.radians(angle_fixed)) * player_speed
    if key == b's':
        player_pos[0] -= math.cos(math.radians(angle_fixed)) * player_speed
        player_pos[1] -= math.sin(math.radians(angle_fixed)) * player_speed

    if key == b'a':

        gun_angle = (gun_angle + 5) % 360

    if key == b'd':

        gun_angle = (gun_angle - 5) % 360

    if key == b'c': cheat_mode = not cheat_mode
    if key == b'v' and cheat_mode:
        cheat_vision = not cheat_vision
        first_person = not first_person

def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos

    if key == GLUT_KEY_UP:
        cz += 20
    if key == GLUT_KEY_DOWN:
        cz -= 20


    if key == GLUT_KEY_LEFT:
        angle = 5
        old_cx, old_cy = cx, cy
        cx = old_cx * math.cos(math.radians(angle)) - old_cy * math.sin(math.radians(angle))
        cy = old_cx * math.sin(math.radians(angle)) + old_cy * math.cos(math.radians(angle))

    if key == GLUT_KEY_RIGHT:
        angle = -5
        old_cx, old_cy = cx, cy
        cx = old_cx * math.cos(math.radians(angle)) - old_cy * math.sin(math.radians(angle))
        cy = old_cx * math.sin(math.radians(angle)) + old_cy * math.cos(math.radians(angle))

    camera_pos = (cx, cy, cz)


def mouseListener(button, state, x, y):
    global bullets, game_over, first_person
    if game_over: return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rad = math.radians(gun_angle + 90)
        print("Player Bullet Fired!")
        bullets.append({
            'x': player_pos[0] + math.cos(rad) * 40,
            'y': player_pos[1] + math.sin(rad) * 40,
            'z': 95,
            'dx': math.cos(rad) * bullet_speed,
            'dy': math.sin(rad) * bullet_speed,
            'dz': 0
        })
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def drawCuboid(width, height, depth):
    w, h, d = width / 2, height / 2, depth / 2
    glBegin(GL_QUADS)
    glColor3f(0.2, .48, .32)
    for f in [((1,1,1),(-w,-h,d),(w,-h,d),(w,h,d),(-w,h,d)),
              ((1,1,1),(-w,-h,-d),(-w,h,-d),(w,h,-d),(w,-h,-d)),
              ((1,1,1),(-w,h,-d),(-w,h,d),(w,h,d),(w,h,-d)),
              ((1,1,1),(-w,-h,-d),(w,-h,-d),(w,-h,d),(-w,-h,d)),
              ((1,1,1),(w,-h,-d),(w,h,-d),(w,h,d),(w,-h,d)),
              ((1,1,1),(-w,-h,-d),(-w,-h,d),(-w,h,d),(-w,h,-d))]:
        for v in f[1:]:
            glVertex3f(*v)
    glEnd()

def draw_shapes():
    glPushMatrix()
    glRotatef(gun_angle, 0, 0, 1)
    glTranslatef(0, 0, 70)
    drawCuboid(70, 60, 70)
    glTranslatef(0, 0, 60)
    glColor3f(0, 1, 1)
    gluSphere(gluNewQuadric(), 30, 10, 10)
    glColor3f(235/255, 210/255, 157/255)
    glTranslatef(22, 26, -35)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 4, 40, 50, 50)
    glColor3f(63/255, 72/255, 74/255)
    glTranslatef(-22, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 4, 50, 50, 50)
    glColor3f(235/255, 210/255, 157/255)
    glTranslatef(-22, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 4, 40, 50, 50)
    glColor3f(25/255, 42/255, 230/255)
    glTranslatef(40, 60, -20)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 7, 35, 50, 50)
    glTranslatef(-35, 0, 0)
    gluCylinder(gluNewQuadric(), 15, 7, 35, 50, 50)
    glPopMatrix()

def draw_enemies():
    for e in enemies:
        glPushMatrix()
        glTranslatef(e['x'], e['y'], 55)
        glColor3f(1, 0, 0)
        glutSolidSphere(45 * e['pulse'], 10, 10)
        glTranslatef(0, 5, 25)
        glColor3f(0, 0, 0)
        glutSolidSphere(35 * e['pulse'], 20, 20)
        glPopMatrix()

def setupCamera():
    global fovY
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    px, py = player_pos

    if first_person:
        fovY=120
        camera_forward = 40
        camera_height = 125
        look_distance = 100
        angle_fix=gun_angle+90

        cam_x = px + math.cos(math.radians(angle_fix)) * camera_forward
        cam_y = py + math.sin(math.radians(angle_fix)) * camera_forward


        look_x = cam_x + math.cos(math.radians(angle_fix)) * look_distance
        look_y = cam_y + math.sin(math.radians(angle_fix)) * look_distance

        gluLookAt(cam_x, cam_y, camera_height,
                  look_x, look_y, camera_height,
                  0, 0, 1)


    else:
        fovY=120
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 0, 1)

def idle():
    enemyUpdate()
    bulletUpdate()
    cheating()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    # Grid
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, 40):
        for j in range(-GRID_LENGTH, GRID_LENGTH, 40):
            glColor3f(1.0, 1.0, 1.0) if (i + j) % 80 == 0 else glColor3f(1.0, 0.85, 0.6)
            glVertex3f(i, j, 0)
            glVertex3f(i + 40, j, 0)
            glVertex3f(i + 40, j + 40, 0)
            glVertex3f(i, j + 40, 0)
    glEnd()
    # wallll
    wall_height = 100
    glBegin(GL_QUADS)

    glColor3f(0, 0, 1)  #blue
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    glColor3f(0, 1, 1)  #cyan
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    glColor3f(0, 1, 0)  #gren
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    glColor3f(1, 1, 1)  #white
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)

    glEnd()

    # texts
    glColor3f(1, 1, 1)
    draw_text(10, 770, f"Score: {score}")
    draw_text(10, 740, f"Lives: {lives}")
    draw_text(10, 710, f"Missed: {missed}/10")
    if cheat_mode:
        glColor3f(1, 1, 1)
        draw_text(10, 680, "CHEAT MODE: ON", GLUT_BITMAP_HELVETICA_12)
    if cheat_vision:
        glColor3f(1, 1, 1)
        draw_text(10, 650, "CHEAT VISION: ON", GLUT_BITMAP_HELVETICA_12)
    if game_over:
        glColor3f(0, 0, 0)  # Black color
        draw_text(300, 300, "GAME OVER - Press R to restart", GLUT_BITMAP_TIMES_ROMAN_24)
    glColor3f(1, 0, 0)
    for bullet in bullets:
        glPushMatrix()
        glTranslatef(bullet['x'], bullet['y'], bullet['z'])
        glutSolidCube(BULLET_SIZE)
        glPopMatrix()
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 0)
    if game_over:
        glRotatef(90, 1, 0, 0)
    draw_shapes()
    glPopMatrix()
    draw_enemies()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1000, 800)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Bullet Frenzy - 3D Shooting Game")
glEnable(GL_DEPTH_TEST)
glClearColor(0.1, 0.1, 0.1, 1.0)
resetGame()
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(idle)
glutMainLoop()
