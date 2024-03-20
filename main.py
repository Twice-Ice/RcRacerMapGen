import pygame
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, FPS, CD
from circle import Point

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

mainPoint = Point(Vector2(SCREEN_X//2, SCREEN_Y//2), (0, 255, 0))

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
		tempPoints.append(Point(Vector2(pygame.mouse.get_pos()) - camera))
		print("made a new point!")
		#append a new circle.
	
	if pygame.mouse.get_pressed(3)[2]:
		camera += mouseVel

	mainPoint.update(screen, camera, mouseVel, grabbedPoints)

	for i in range(len(tempPoints)):
		tempPoints[i].update(screen, camera, mouseVel, grabbedPoints, mainPoint.pos)

	pygame.display.flip()
	pygame.mouse.get_rel()
pygame.quit()