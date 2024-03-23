import pygame
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, FPS, CD
from circle import Point, Circle

pygame.init

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

doExit = False
clock = pygame.time.Clock()
cooldown = 0
grabbedPoints = []
camera = Vector2(0, 0)
mouseVel = pygame.mouse.get_rel()

circles = []
tempPoints = []

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

	mouseVel = pygame.mouse.get_rel()


	if cooldown > 0:
		cooldown -= delta
	else:
		cooldown = 0

	keys = pygame.key.get_pressed()
	if keys[pygame.K_c] and cooldown == 0:
		cooldown = CD
		circles.append(Circle(Vector2(pygame.mouse.get_pos()) - camera))
		# tempPoints.append(Point(Vector2(pygame.mouse.get_pos()) - camera))
		# print(tempPoints[len(tempPoints)-1])
		# print("made a new point!")
		# #append a new circle.
	
	if pygame.mouse.get_pressed(3)[2]:
		camera += mouseVel

	
	# '''
	# So the way that positional stuff is controlled is that for all points other than the mainPoint, their position is just set to the mouse if they are grabbed.
	# When they are released, their position is updated to the world position of the mouse on screen. So, SS -> WS (Screen Space, World Space)

	# A similar setup is happening with the mainPoint. If it's grabbed, then it's position is just set to the mouse.
	# However, all other points have their relative positions stored, and then are moved to their relativePos + mainPoint.pos (mainPoint.pos == mouse)
	# When mainPoint is released though, the other point's staticPosition is updated to reflect that which was shown on screen while mainPoint.grabbed == True.
	# '''
	# for i in range(len(tempPoints)):
	# 	if mainPoint.grabbed:
	# 		tempPoints[i].pos = (tempPoints[i].staticPos - mainPoint.staticPos) + mainPoint.pos #updatees tempPoints to it's relative position before mainPoint was grabbed and adds the mouse (or, mainPoint.pos)
	# 		if not pygame.mouse.get_pressed(3)[0]: #when mainPoint is released. This only happens once.
	# 			tempPoints[i].staticPos = tempPoints[i].pos #updates the static position of the other points.
	# 	tempPoints[i].update(screen, camera, grabbedPoints)

	# #same code as above but for preset points.
	# if mainPoint.grabbed:
	# 	xPoint.pos = (xPoint.staticPos - mainPoint.staticPos) + mainPoint.pos
	# 	yPoint.pos = (yPoint.staticPos - mainPoint.staticPos) + mainPoint.pos
	# 	if not pygame.mouse.get_pressed(3)[0]:
	# 		xPoint.staticPos = xPoint.pos
	# 		yPoint.staticPos = yPoint.pos
	# xPoint.update(screen, camera, grabbedPoints)
	# yPoint.update(screen, camera, grabbedPoints)

	# #if the xPoint or yPoint are grabbed, then the mainPoint.pos should be updated to be relative.
	# if xPoint.grabbed or yPoint.grabbed:
	# 	mainPoint.pos = Vector2(xPoint.pos.x, yPoint.pos.y)
	# 	mainPoint.updateStaticPos()

	# mainPoint.update(screen, camera, grabbedPoints) #this has to be below the update calls of the other points.
	for i in range(len(circles)):
		circles[i].update(screen, camera, grabbedPoints)
	# mainCircle.update(screen, camera, grabbedPoints)

	pygame.display.flip()
	pygame.mouse.get_rel()
pygame.quit()