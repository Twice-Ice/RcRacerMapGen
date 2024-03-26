import pygame
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, FPS, CD
from lines import Point, Circle, Line

pygame.init

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

doExit = False
clock = pygame.time.Clock()
cooldown = 0
grabbedPoints = []
camera = Vector2(0, 0)
mouseVel = pygame.mouse.get_rel()

items = []
item = "Line"
itemList = (
	"Line",
	"Circle",
)

# mainPoint = Point(Vector2(SCREEN_X//2, SCREEN_Y//2), (0, 255, 0))
# p1 = Point(Vector2(mainPoint.pos.x + 100, mainPoint.pos.y), (255, 0, 0))
# p2 = Point(Vector2(mainPoint.pos.x, mainPoint.pos.y + 100), (0, 0, 255))
# #updates the mainPoint so that it's relative to the x and y points.
# mainPoint.pos = Vector2(p1.pos.x, p2.pos.y)
# mainPoint.updateStaticPos()
# print(mainPoint)

# mainCircle = Circle(Vector2(200, 200))

while not doExit:
	delta = clock.tick(FPS)/1000
	screen.fill(BG_COLOR)
	wheel = 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			doExit = True
		if event.type == pygame.MOUSEWHEEL:
			wheel = event.y

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
		if item == "Circle":
			items.append(Circle(Vector2(pygame.mouse.get_pos()) - camera, 25))
		elif item == "Line":
			items.append(Line(Vector2(pygame.mouse.get_pos()) - camera, 25))
	elif (keys[pygame.K_UP] or keys[pygame.K_w]) and cooldown == 0:
		cooldown = CD
		item = itemList[itemList.index(item) + 1 if itemList.index(item) + 1 < len(itemList) else 0]
	elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and cooldown == 0:
		cooldown = CD
		item = itemList[itemList.index(item) - 1]

	#moves the camera
	if pygame.mouse.get_pressed(3)[2]:
		camera += mouseVel
	
	#draws and updates all circles
	for i in range(0, len(items)):
		'''
		More detailed for next line:
		circles = [0, 1, 2]
		as counting through i and len(circles), circles[1] is deleted.
		this leaves the table as:
		circles = [0, 2] but then the max of i is still 2 instead of the now updated 1.
		the following line of code would just not go into the next spot in the table if it doesn't exist anymore.
		'''
		if i < len(items): # this line prevents the case where a circles is deleted and then i < len(circles) so an index error happens.
			items[i].update(screen, delta, camera, grabbedPoints, wheel)
			#deletes the circle if any of it's points are highlighted and backspace or x is pressed.
			if cooldown == 0 and (keys[pygame.K_BACKSPACE] or (keys[pygame.K_LCTRL] and keys[pygame.K_x])) and (items[i].cPoint.highlighted or items[i].p1.highlighted or items[i].p2.highlighted):
				del items[i]

	pygame.display.flip()
	pygame.mouse.get_rel()
pygame.quit()