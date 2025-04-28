from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random
# TASK-1
day=False

wind_dir=1.0
rain_speed=10
trans=0.0
target=0.0

num_drop=random.randint(700,1000)
rainDrops=[]
# populates the raindrops array with random x,y coordinates
for i in range(num_drop):
    rainDrops.append([random.randint(0,1500),random.randint(400,800)])
print(rainDrops)
def myInit():

    glColor3f(0.2, 0.5, 0.4)
    glPointSize(10.0)
    gluOrtho2D(0, 1500, 0, 800)

def house():
    glBegin(GL_QUADS)
    glColor3f(255 / 255, 171 / 255, 91 / 255)
    glVertex2f(0, 0)
    glVertex2f(0, 400.0)
    glVertex2f(1500, 400)
    glVertex2f(1500, 0)
    glEnd()

    # house body
    glBegin(GL_QUADS)
    glColor3f(0, 135 / 255, 158 / 255)
    glVertex2f(500, 100)
    glVertex2f(500, 300)
    glVertex2f(1000, 300)
    glVertex2f(1000, 100)
    glEnd()
    # house roof
    glBegin(GL_TRIANGLES)
    glColor3f(0, 48 / 255, 146 / 255)
    glVertex2f(450, 300)
    glVertex2f(750, 400)
    glVertex2f(1050, 300)
    glEnd()
#     house door
    glBegin(GL_QUADS)
    glColor3f(80/255,75/255,56/255)
    glVertex2f(700,100)
    glVertex2f(800,100)
    glVertex2f(800,250)
    glVertex2f(700,250)
    glEnd()
#     house window1
    glBegin(GL_QUADS)
    glColor(1,242/255,219/255)
    glVertex2f(600,200)
    glVertex2f(650,200)
    glVertex2f(650,250)
    glVertex2f(600,250)
    glEnd()
# house winddow2
    glBegin(GL_QUADS)
    glColor3f(1, 242 / 255, 219 / 255)
    glVertex2f(850, 200)
    glVertex2f(900,200)
    glVertex2f(900,250)
    glVertex2f(850,250)
    glEnd()

# window bar
    glBegin(GL_LINES)
    glColor3f(0,0,0)
    glVertex2f(600,225)
    glVertex2f(650,225)
    glVertex2f(625,200)
    glVertex2f(625,250)
    glVertex2f(850,225)
    glVertex2f(900,225)
    glVertex2f(875,200)
    glVertex2f(875,250)
    glEnd()
    glBegin(GL_POINTS)

    glVertex2f(775,175)
    glEnd()
# is used to draw the rain lines for rainfall effect
def rainLines():
    glColor3f(0.5, 0.5, 1)
    glLineWidth(2.0)
    glBegin(GL_LINES)


    for coord in rainDrops:
        x,y=coord
        glVertex2f(x,y)
        glVertex2f(x+wind_dir*4,y-15)
    glEnd()
# rainFall() is used to animate the rainfall animation using the timer function and glutPostRedisplay, it also randomly resets the raindrop when 0 is created

def rainFall(value):
    global rainDrops
    for drop in rainDrops:
        drop[1]-=rain_speed
        drop[0]+=wind_dir*2
        if drop[1]<0:
            # print("reached reached")
            drop[0]=random.randint(0,1500)
            drop[1]=random.randint(0,800)
            # print(drop)
    glutPostRedisplay()
    glutTimerFunc(30,rainFall,0)
def specialKeys(key,x,y):
    global wind_dir
    print(wind_dir)
    if key==GLUT_KEY_LEFT:
        if wind_dir>=-20.0:
            wind_dir-=0.5
        else:

            wind_dir=-20.0
    elif key==GLUT_KEY_RIGHT:
        if wind_dir<=20.0:
            wind_dir+=  0.5
        else:
            wind_dir==20.0
    elif key==GLUT_KEY_DOWN:
        wind_dir=0

def display():
    global trans
    r=(0.53*trans)
    g=(0.81*trans)
    b=(0.98*trans)
    glClearColor(r,g,b,0)
    glClear(GL_COLOR_BUFFER_BIT)

    house()
    rainLines()
    glFlush()

def update_transition(value):
    global trans,target
    if trans<target:
        trans+=0.2
        print(trans)
        if trans > target:
            trans=target
    elif trans>target:
        trans-=0.2
        if trans<target:
            trans=target
    glutPostRedisplay()
    glutTimerFunc(30,update_transition,0)

def keyboardListener(key,x,y):
    global target
    if key==b'd':
        target=1.0
        print("day")
    elif key==b'n':
        target=0.0
        print('night')



glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(1500, 800)
glutInitWindowPosition(200, 175)
glutCreateWindow(b"TASK-1")
myInit()
glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeys)
glutTimerFunc(30,update_transition,0)
glutTimerFunc(30,rainFall,0)

glutMainLoop()




##########################################################################################################################################################
# task-2
# balls = []
# speed = 1.5
# blink = False
# stationary = False
# # This the Ball object created
# class Ball:
#     def __init__(self, x, y, color, dirx, diry):
#         self.x = x
#         self.y = y
#         self.color = color
#         self.originalColor=color.copy()
#
#         self.dirx = dirx
#         self.diry = diry
# # Initialize the orthogonal region and the background color of the task
# def myInit():
#     glClearColor(0,0,0,0)
#     gluOrtho2D(0,1600,0,900)
# # makes the ball move along with the timer function
# def updateBallPosition(value):
#     global balls, speed, stationary
#     if not stationary:
#         for ball in balls:
#             ball.x+=speed*ball.dirx
#             ball.y+=speed*ball.diry
#             if ball.x<=0:
#                 ball.dirx= - ball.dirx
#             elif ball.x>=1600:
#                 ball.dirx= ball.dirx*-1
#             if ball.y<=0 or ball.y>=900:
#                 ball.diry= ball.diry*-1
#     glutPostRedisplay()
#     glutTimerFunc(16,updateBallPosition,0)
# # blinking feature is implemented by checking for the color of the ball objects
# # if the object.color is black, it is changed to it original color, if not it is changed to black
# #  this change is animated over multiple frames with the timer function
# def blinkingBalls(value):
#     global balls, blink
#     if blink:
#         for ball in balls:
#
#             if ball.color!=[0.0,0.0,0.0]:
#                 ball.color=[0.0,0.0,0.0]
#             elif ball.color==[0.0,0.0,0.0]:
#                 ball.color=ball.originalColor
#     glutPostRedisplay()
#     glutTimerFunc(200,blinkingBalls,0)
# # draws the ball from the balls array which saves its coordinate position
#
# def display():
#     glClear(GL_COLOR_BUFFER_BIT)
#     glPointSize(10.0)
#     for ball in balls:
#         glColor3f(*ball.color)
#         glBegin(GL_POINTS)
#         glVertex2f(ball.x,ball.y)
#         glEnd()
#     glFlush()
#
#
# def keyboardListener(key,x,y):
#     global speed, stationary
#     if key==b' ':
#         stationary= not stationary
# def specialKeyListener(key,x,y):
#     global speed
#     if key==GLUT_KEY_UP:
#         speed+=0.1
#     elif key== GLUT_KEY_DOWN:
#         speed=max(0.1,speed-0.1)
#
#
# # right btn creates balls which move in a random direction set using a random integer generated then divided by 100
# # this random change is proportionally multiplied to the dirx and diry which is constantly updated by the update function
# def mouseListener(btn,state,x,y):
#     global balls,blink
#     y=900-y
#     if btn==GLUT_RIGHT_BUTTON and state==GLUT_DOWN:
#         color=[random.random() for i in range(3)]
#         dirx=random.randint(-100,100)/80
#         diry=random.randint(-100,100)/80
#         balls.append(Ball(x,y,color,dirx,diry))
#     elif btn==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
#         blink= not blink
#
#
# # main initialization and settings
# glutInit()
# glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
# glutInitWindowSize(1600,900)
# glutInitWindowPosition(0, 0)
# glutCreateWindow(b"TASK2")
# myInit()
# glutDisplayFunc(display)
# glutMouseFunc(mouseListener)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
# glutTimerFunc(16,updateBallPosition,0)
# glutTimerFunc(200,blinkingBalls,0)
# glutMainLoop()
