import pygame
import math
import random
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, FPS, COOLDOWNVAL

pygame.init

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

doExit = False
clock = pygame.time.Clock()
cooldown = 0 #cooldown (in dt) between actions.
globalGrabbed = False #a boolean to tell if the one thing that can be grabbed has been grabbed or not.
camera = Vector2(0, 0) #global relative camera position

class Point:
    def __init__(self, name, pos, center, color = (255, 255, 255)):
        self.pos = pos
        self.storedRelPos = self.pos - center #relative position to the center point (as inputed with center)
        self.name = name
        self.color = color
        self.size = 2
        self.grabbed = False #grabbed by mouse
        self.highlighted = False #close enough to be grabbed by mouse

    def update(self, screen, center, camera):
        global globalGrabbed
        mouse = Vector2(pygame.mouse.get_pos())
        if math.dist(mouse, self.pos + camera) < 5 and globalGrabbed == False: #if this point is in range of the mouse and the mouse isn't already holding something:
            self.size = 5 #make it bigger
            self.highlighted = True #"highlight" it
            if pygame.mouse.get_pressed(3)[0] == True and self.grabbed == False: #if clicked on: (The self.grabbed == False is to prevent this being called every frame)
                self.grabbed = True
                globalGrabbed = True
        else:
            self.highlighted = self.grabbed #to make sure it's only highlighted if it's grabbed
            self.size = 2 #default size

        if self.grabbed:
            if self.name == "center":
                mouse = Vector2(0, 0)
            self.pos = mouse - camera #updates the position if it's grabbed to be the mouse pos. the -camera fixes some problems with the p1 and p2. But it's still super jank
            if pygame.mouse.get_pressed(3)[0] == False: #only if it was grabbed and then left click was false, would it mean that left click was released
                self.grabbed = False #disables grabbed
                self.storedRelPos = self.pos - center #updates relative pos
                globalGrabbed = False #disables the global grabbed
                print(self.storedRelPos)
                # print("was released")

        pygame.draw.circle(screen, self.color, self.pos + camera, self.size) #draws the point to the screen

class Circle:
    def __init__(self, center, iterations : int = 10):
        #defines points
        self.center = Point("center", center, Vector2(0, 0), (0, 255, 0))
        self.p1 = Point("p1", self.center.pos + Vector2(100, 0), self.center.pos, (255, 0, 0))
        self.p2 = Point("p2", self.center.pos + Vector2(0, 100), self.center.pos, (0, 0, 255))

        #defines x and y relative lengths for the ellipse
        self.xLen = abs(self.p2.pos.x - self.p1.pos.x)
        self.yLen = abs(self.p2.pos.y - self.p1.pos.y)
        #the number of points on the ellipse
        self.iterations = iterations

    def update(self, screen, camera):
        self.center.pos = Vector2(self.p2.pos.x, self.p1.pos.y) #resets center position based on p1 and p2
        #updates relatives x and y lengths
        self.xLen = abs(self.p2.pos.x - self.p1.pos.x)
        self.yLen = abs(self.p2.pos.y - self.p1.pos.y)
        

        global cooldown
        keys=pygame.key.get_pressed()
        if keys[pygame.K_f] and (self.p1.highlighted or self.p2.highlighted or self.center.highlighted) and cooldown == 0:
            #if f is pressed and any of the points are highlighted, it will be flipped.
            cooldown = COOLDOWNVAL
            temp = self.p1.pos
            self.p1.pos = self.p2.pos
            self.p2.pos = temp

        mouse = Vector2(pygame.mouse.get_pos())
        if self.p1.grabbed: #handles updating the p1 if it's grabbed
            p1Rel = mouse - self.p1.pos
            self.p1.pos = p1Rel + mouse
            self.p2.storedRelPos = self.p2.pos - self.center.pos
        elif self.p2.grabbed: #handles updating the p2 if it's grabbed
            p2Rel = mouse - self.p2.pos
            self.p2.pos = p2Rel + mouse
            self.p1.storedRelPos = self.p1.pos - self.center.pos
        if self.center.grabbed: #if the center is grabbed, it doesn't need to move from here, as it's already moved. however, both p1 and p2 need to be updated.
            self.p2.pos = mouse + self.p2.storedRelPos #relative positions are relative to center.
            self.p1.pos = mouse + self.p1.storedRelPos
            print(self.p2.storedRelPos, self.p1.storedRelPos)

        #draws self
        self.draw(screen, camera)
        #updates and draws all points relative to the camera and center.
        self.p1.update(screen, self.center.pos, camera)
        self.p2.update(screen, self.center.pos, camera)
        self.center.update(screen, Vector2(0, 0), camera)


    def draw(self, screen, camera):
        #figures out what  the proper quadrant is based on some trig. Fuck this.
        degree1 = math.degrees(math.atan2(self.p1.pos.y - self.center.pos.y, self.p1.pos.x - self.center.pos.x))
        degree2 = math.degrees(math.atan2(self.p2.pos.y - self.center.pos.y, self.p2.pos.x - self.center.pos.x))
        degree1 += 0 if degree1 >= 0 else 360
        degree2 += 0 if degree2 >= 0 else 360
        minDegrees = degree1 if degree1 < degree2 else degree2
        maxDegrees = degree1 if degree1 > degree2 else degree2
        
        if minDegrees == 0 and maxDegrees == 270:
            minDegrees = 270
            maxDegrees = 360

        #figures out what the proper quadrant it is based on brute force.
        # if self.p1.pos.y >= 0 and self.p2.pos.x >= 0:
        #     minDegrees = 0
        #     maxDegrees = 90
        # elif self.p1.pos.y >= 0 and self.p2.pos.x < 0:
        #     minDegrees = 90
        #     maxDegrees = 180
        # elif self.p1.pos.y < 0 and self.p2.pos.x < 0:
        #     minDegrees = 180
        #     maxDegrees = 270
        # elif self.p1.pos.y < 0 and self.p2.pos.x >= 0:
        #     minDegrees = 270
        #     maxDegrees = 360

        #idk
        if self.p1.grabbed or self.p2.grabbed or self.center.grabbed:
            camera = Vector2(0, 0)

        #loops through all iterations that it needs to place + 1 for that 100%
        for i in range(self.iterations + 1):
            percent = i / self.iterations #percent of i that's already been done/or is currently on.
            angle = math.radians((maxDegrees - minDegrees) * percent + minDegrees) #the angle is somewhere between minDegrees and maxDegrees, interpolated from percent.
            x = math.cos(angle) * self.xLen + self.center.pos.x
            y = math.sin(angle) * self.yLen + self.center.pos.y
        #     pygame.draw.line(screen, (25, 25, 25), (self.p1.x, y), (x, y), 1)
        #     pygame.draw.line(screen, (50, 50, 50), self.center, (x, y), 1)
            pygame.draw.circle(screen, (255, 255, 255), (x, y) + camera, 1)

        # pygame.draw.line(screen, (50, 50, 50), self.p1, self.p2, 2)
        

quarterCircles = []
# oldMousePos = Vector2(pygame.mouse.get_pos())
while not doExit:
    if cooldown > 0:
        cooldown -= delta
    else:
        cooldown = 0

    delta = clock.tick(FPS)/1000
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            doExit = True

    keys=pygame.key.get_pressed()
    if keys[pygame.K_c] and cooldown == 0:
        cooldown = COOLDOWNVAL
        quarterCircles.append(Circle(Vector2(pygame.mouse.get_pos()) - camera))

    if pygame.mouse.get_pressed(3)[2]:
        camera += Vector2(0, 0)#pygame.mouse.get_rel()

    for i in range(len(quarterCircles)):
        quarterCircles[i].update(screen, camera)
        if keys[pygame.K_x] and (quarterCircles[i].p1.highlighted or quarterCircles[i].p2.highlighted or quarterCircles[i].center.highlighted):
            del quarterCircles[i]
            break

    pygame.display.flip()
    pygame.mouse.get_rel()
pygame.quit()