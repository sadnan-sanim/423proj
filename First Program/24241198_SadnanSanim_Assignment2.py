from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

x1,x2,x3,x4 = 20,50,135,165 # diamond catcher
y1,y2 = 10,40
cat_width=x4-x1
cat_height=y2-y1
cat_speed=10

white = (1.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)
cat_color = white

diamond_palette = [
(1.0, 0.0, 0.0),(0.0, 1.0, 0.0),(0.0, 0.0, 1.0),(1.0, 1.0, 0.0),(1.0, 0.0, 1.0),(0.0, 1.0, 1.0),(0.8, 1.0, 0.0),(1.0, 0.498, 0.314),(1.0, 0.627, 0.537),(1.0, 0.078, 0.576)]

diamond_arr=[]
falling=None
diamond_speed=2

score=0

width=600
height=900

pause_flag = False
gameover_flag = False
restart_flag = False

def draw_points(x,y) :
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    zone = -1
    if abs(dx) > abs(dy):
        if dx > 0:
            if dy > 0:
                zone = 0
            else:
                zone = 7
        else:
            if dy > 0:
                zone = 3
            else:
                zone = 4
    else:
        if dy > 0:
            if dx > 0:
                zone = 1
            else:
                zone = 2
        else:
            if dx > 0:
                zone = 6
            else:
                zone = 5
    return zone

def convert(original_zone,x,y):
    if (original_zone == 0):
        return x,y
    elif (original_zone == 1):
        return y,x
    elif (original_zone == 2):
        return -y,x
    elif (original_zone == 3):
        return -x,y
    elif (original_zone == 4):
        return -x,-y
    elif (original_zone == 5):
        return -y,-x
    elif (original_zone == 6):
        return -y,x
    elif (original_zone == 7):
        return x,-y

def convert_original(original_zone,x,y):
    if (original_zone == 0):
        return x,y
    elif (original_zone == 1):
        return y,x
    elif (original_zone == 2):
        return -y,-x
    elif (original_zone == 3):
        return -x,y
    elif (original_zone == 4):
        return -x,-y
    elif (original_zone == 5):
        return -y,-x
    elif (original_zone == 6):
        return y,-x
    elif (original_zone == 7):
        return x,-y

def midpoint(zone,x0,y0, x1,y1):
    dx = x1-x0
    dy = y1-y0
    d = (2*dy) - dx
    forE = 2*dy
    forNE = 2*(dy-dx)
    x = x0
    y = y0
    while (x < x1):
        org_x, org_y = convert_original(zone,x,y)
        draw_points(org_x,org_y)
        if (d<=0):
            x += 1
            d += forE
        else:
            x += 1
            y += 1
            d += forNE
def eightWaySym(x0,y0,x1,y1):
    zone = find_zone(x0,y0,x1,y1)
    conv_x0, conv_y0 = convert(zone,x0,y0)
    conv_x1, conv_y1 = convert(zone,x1,y1)
    midpoint(zone,conv_x0,conv_y0,conv_x1,conv_y1)
def draw_catcher():
    global x1,x2,x3,x4,y1,y2
    glColor3fv(cat_color)
    eightWaySym(x2,y1,x3,y1)
    eightWaySym(x1,y2,x2,y1)
    eightWaySym(x3,y1,x4,y2)
    eightWaySym(x1,y2,x4,y2)

def left_arrow():
    glColor3f(0.0,1.0,1.0)
    eightWaySym(20,850,100,850)
    eightWaySym(40,865,20,850)
    eightWaySym(40,835,20,850)

def cross():
    glColor3f(1.0,0.0,0.0)
    eightWaySym(500,825,550,865)
    eightWaySym(500,865,550,825)
def play():
    glColor3f(1.0,1.0,0.0)
    eightWaySym(290,870,290,820)
    eightWaySym(310,870,310,820)
def pause():
    glColor3f(1.0,1.0,0.0)
    eightWaySym(297,870,297,820)
    eightWaySym(297,870,310,845)
    eightWaySym(297,820,310,845)
def animation():
    global pause_flag,gameover_flag
    if (pause_flag == False and gameover_flag==False):
        glutPostRedisplay()
# screen setup 
def iterate():
    glViewport(0,0,600,900)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0,600,0.0,900,0.0,1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
def specialKeyListener(key,x,y):
    global x1,x2,x3,x4,cat_speed,pause_flag
    if (not pause_flag and gameover_flag==False):
        if (key==GLUT_KEY_RIGHT):
            if (x1<600) and (x2<=600) and (x3<600) and (x4<600) :
                x1 += cat_speed
                x2 += cat_speed
                x3 += cat_speed
                x4 += cat_speed
        if (key==GLUT_KEY_LEFT):
            if (x1>0) and (x2>0) and (x3>0) and (x4>0) :
                x1 -= cat_speed
                x2 -= cat_speed
                x3 -= cat_speed
                x4 -= cat_speed
    glutPostRedisplay()

def mouseListener(button,state,x,y):
    global pause_flag,x1,x2,x3,x4,score,restart_flag,gameover_flag
    new_y=height-y
    pause_count=0
    if (button==GLUT_LEFT_BUTTON) and (state==GLUT_DOWN):
            #pause
            if(290<=x<=310) and (820<=new_y<=870):
                pause_count+=1

            if(pause_count%2 !=0):
                pause_flag = True
                print(f"Pause Score: {score}")
            if(pause_count%2 ==0):
                pause_flag = False
                #restart
            if (20<=x<=100) and (845<=new_y<=855):
                restart_flag=True
                print("Starting Over")
                #terminate
            if (500<=x<=575) and (840<=new_y<=880):
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()

def create_diamond():
    diamond_y=800
    diamond_x=random.randint(25,525)
    diamond_color=random.choice(diamond_palette)
    diamond_arr.append([diamond_x,diamond_y,diamond_color])
def draw_diamond(x,y,color):
    glColor3fv(color)
    eightWaySym(x,y,x+15,y+15)
    eightWaySym(x-15,y+15,x,y)
    eightWaySym(x,y+30,x+15,y+15)
    eightWaySym(x,y+30,x-15,y+15)


def mainloop(value):
    global score, cat_color, x1, x2, x3, x4, y1, y2, gameover_flag, restart_flag, pause_flag, falling, diamond_speed
    bar_x = (x1 + x4) / 2

    if restart_flag:
        score = 0
        cat_color = white
        x1 = 20
        x2 = 50
        x3 = 135
        x4 = 165
        gameover_flag = False
        diamond_speed=2
        diamond_arr.clear()
        for i in range(10):
            create_diamond()

        falling = None
        restart_flag = False
    elif not gameover_flag and not pause_flag:
        if not falling:
            if diamond_arr:
                falling = diamond_arr.pop(0)
        if falling:
            diamond_x, diamond_y, diamond_color = falling
            diamond_y -= diamond_speed
            falling = [diamond_x, diamond_y, diamond_color]

            if diamond_y <= cat_height and abs(diamond_x - bar_x) < cat_width / 2:
                score += 1
                print(f"Score: {score}")
                falling = None
                if score >= 1:
                    diamond_speed += 0.25
                    create_diamond()

            elif diamond_y < 0:
                gameover_flag = True
                diamond_speed = 2
                falling = None
                cat_color = red
                if gameover_flag:
                    pause_flag = True
                    cat_color = red
                    print(f"Game Over! Your final score: {score}")

    glutPostRedisplay()
    glutTimerFunc(10, mainloop, 0)


def showScreen() :
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_catcher()
    left_arrow()
    cross()
    if falling:
        xi,yi,color=falling
        draw_diamond(xi,yi,color)
    if (pause_flag==True):
        pause()

    else:
        play()
    glutSwapBuffers()

for i in range(10):
    create_diamond()
glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(width,height)
glutInitWindowPosition(500,0)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(animation)
glutTimerFunc(10, mainloop, 0)
glutMainLoop()