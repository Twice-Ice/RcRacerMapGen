import pygame
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, BG_COLOR, FPS, CD
from shapes import Point, Circle, Line
import os
from SaveFile import File

pygame.init

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

doExit = False
clock = pygame.time.Clock()
cooldown = 0
grabbedPoints = []
camera = Vector2(0, 0)
mouseVel = pygame.mouse.get_rel()

saveFile = None

globalDrawMode = "lines"
shapes = []
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

	#gets list of keys pressed this frame
	keys = pygame.key.get_pressed()

	#creates a new shape at the mouse
	if keys[pygame.K_c] and cooldown == 0:
		cooldown = CD
		if item == "Circle":
			shapes.append(Circle(Vector2(pygame.mouse.get_pos()) - camera, drawMode = globalDrawMode))
		elif item == "Line":
			shapes.append(Line(Vector2(pygame.mouse.get_pos()) - camera, drawMode = globalDrawMode))

	#changes shape by going up in the list of shapes
	elif (keys[pygame.K_UP] or keys[pygame.K_w]) and cooldown == 0:
		cooldown = CD
		item = itemList[itemList.index(item) + 1 if itemList.index(item) + 1 < len(itemList) else 0]

	#changes shape by going down in the list of shapes
	elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and cooldown == 0:
		cooldown = CD
		item = itemList[itemList.index(item) - 1]

	#changes draw mode from points to lines or lines to points
	elif keys[pygame.K_m] and cooldown == 0:
		cooldown = CD
		globalDrawMode = "points" if globalDrawMode == "lines" else "lines"

	#saves the file
	elif keys[pygame.K_LCTRL] and keys[pygame.K_s]:
		#if shift is pressed a new file will be made
		if keys[pygame.K_LSHIFT]:
			saveFile = File()
			saveFile.saveFile()
		#if there isn't already a file for this instance of the application, a new one is created
		elif saveFile == None:
			saveFile = File()
			saveFile.saveFile()
		#opens the file in write mode
		with open(saveFile.filePath, "w") as file:
			#creates a string with all of the shapes, and their individual points defined in the string
			totalSaveString = ""
			for shape in range(len(shapes)):
				totalSaveString += shapes[shape].saveData()
			#writes this string to the file
			file.write(totalSaveString)

	#loads a file and sets that as this app instance's saveFile
	elif keys[pygame.K_LCTRL] and keys[pygame.K_l]:
		saveFile = File()
		saveFile.loadFile()

		shapesInFile = []
		with open(saveFile.filePath, "r") as file:
			for line in file:
				shapesInFile.append(line.strip())
		
		for shape in range(len(shapes)-1, -1, -1):
			del shapes[shape]
		
		for shape in range(0, len(shapesInFile), 2):
			case = shapesInFile[shape].split("; ")
			if case[0] == "<class 'shapes.Circle'>":
				p1 = case[1].split(", ")
				p1PosX = p1[0][1:]
				p1PosY = p1[1][:-1]
				p1Pos = Vector2(int(p1PosX), int(p1PosY))

				p2 = case[2].split(", ")
				p2PosX = p2[0][1:]
				p2PosY = p2[1][:-1]
				p2Pos = Vector2(int(p2PosX), int(p2PosY))

				iterations = int(case[3])

				curveMult = float(case[4])
				shapes.append(Circle(p1Pos = p1Pos, p2Pos = p2Pos, iterations = iterations, curveMult = curveMult))
			elif case[0] == "<class 'shapes.Line'>":
				p1 = case[1].split(", ")
				p1PosX = p1[0][1:]
				p1PosY = p1[1][:-1]
				p1Pos = Vector2(float(p1PosX), float(p1PosY))

				p2 = case[2].split(", ")
				p2PosX = p2[0][1:]
				p2PosY = p2[1][:-1]
				p2Pos = Vector2(float(p2PosX), float(p2PosY))

				iterations = int(case[3])
				shapes.append(Line(p1Pos = p1Pos, p2Pos = p2Pos, iterations = iterations))

	#moves the camera
	if pygame.mouse.get_pressed(3)[2]:
		camera += mouseVel
	
	#draws and updates all circles
	for i in range(0, len(shapes)):
		'''
		More detailed for next line:
		circles = [0, 1, 2]
		as counting through i and len(circles), circles[1] is deleted.
		this leaves the table as:
		circles = [0, 2] but then the max of i is still 2 instead of the now updated 1.
		the following line of code would just not go into the next spot in the table if it doesn't exist anymore.
		'''
		if i < len(shapes): # this line prevents the case where a circles is deleted and then i < len(circles) so an index error happens.
			shapes[i].update(screen, delta, camera, grabbedPoints, wheel, globalDrawMode)
			#deletes the circle if any of it's points are highlighted and backspace or x is pressed.
			if cooldown == 0 and (keys[pygame.K_BACKSPACE] or (keys[pygame.K_LCTRL] and keys[pygame.K_x])) and (shapes[i].cPoint.highlighted or shapes[i].p1.highlighted or shapes[i].p2.highlighted):
				del shapes[i]

	pygame.display.flip()
	pygame.mouse.get_rel()
pygame.quit()