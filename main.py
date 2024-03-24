import pygame
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, FPS, CD
from lines import Point, Circle

pygame.init

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

doExit = False
clock = pygame.time.Clock()
cooldown = 0
grabbedPoints = []
camera = Vector2(0, 0)
mouseVel = pygame.mouse.get_rel()

circles = []

# mainPoint = Point(Vector2(SCREEN_X//2, SCREEN_Y//2), (0, 255, 0))
# xPoint = Point(Vector2(mainPoint.pos.x + 100, mainPoint.pos.y), (255, 0, 0))
# yPoint = Point(Vector2(mainPoint.pos.x, mainPoint.pos.y + 100), (0, 0, 255))
# #updates the mainPoint so that it's relative to the x and y points.
# mainPoint.pos = Vector2(xPoint.pos.x, yPoint.pos.y)
# mainPoint.updateStaticPos()
# print(mainPoint)

# mainCircle = Circle(Vector2(200, 200))

while not doExit:
	delta = clock.tick(FPS)/1000
	screen.fill(BG_COLOR)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True

	#gets mouseVelocity to add to the camera if right click is pressed
	mouseVel = pygame.mouse.get_rel()

	#updates main.py cooldown
	if cooldown > 0:
		cooldown -= delta
	else:
		cooldown = 0

	#creates a new circle at the mouse
	keys = pygame.key.get_pressed()
	if keys[pygame.K_c] and cooldown == 0:
		cooldown = CD
		circles.append(Circle(Vector2(pygame.mouse.get_pos()) - camera))
	
	#moves the camera
	if pygame.mouse.get_pressed(3)[2]:
		camera += mouseVel
	
	#draws and updates all circles
	for i in range(0, len(circles)):
		'''
		More detailed for next line:
		circles = [0, 1, 2]
		as counting through i and len(circles), circles[1] is deleted.
		this leaves the table as:
		circles = [0, 2] but then the max of i is still 2 instead of the now updated 1.
		the following line of code would just not go into the next spot in the table if it doesn't exist anymore.
		'''
		if i < len(circles): # this line prevents the case where a circles is deleted and then i < len(circles) so an index error happens.
			circles[i].update(screen, delta, camera, grabbedPoints)
			#deletes the circle if any of it's points are highlighted and backspace or x is pressed.
			if cooldown == 0 and (keys[pygame.K_BACKSPACE] or keys[pygame.K_x]) and (circles[i].cPoint.highlighted or circles[i].xPoint.highlighted or circles[i].yPoint.highlighted):
				del circles[i]

	pygame.display.flip()
	pygame.mouse.get_rel()
pygame.quit()