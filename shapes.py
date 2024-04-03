import pygame
import math
import random
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, CD

def pointOnScreen(pos, camera, size):
	ssPoint = pos + camera #screen space point. Converts pos from ws to ss.
	size = abs(size) #only ever should be a positive value.
	if ssPoint.x + size > 0 and ssPoint.x - size < SCREEN_X and ssPoint.y + size > 0 and ssPoint.y - size < SCREEN_Y:
		return True
	else:
		return False

class drawnShape:
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X/2, SCREEN_Y/2), iterations : int = 10, drawColor : tuple = (150, 150, 150), drawMode : str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None):
		self.pos = pos
		self.iterations = iterations
		self.drawColor = drawColor
		self.wheel = 0
		self.drawMode = drawMode

		self.cooldown = 0
		self.cPoint = Point(self.pos, (0, 255, 0))
		self.p1 = Point(self.pos + Vector2(0, 100), (0, 0, 255))
		self.p2 = Point(self.pos + Vector2(100, 0), (255, 0, 0))

		if p1Pos != None:
			self.p1.setPos(p1Pos)
		if p2Pos != None:
			self.p2.setPos(p2Pos)

		self.updateCPointPos()

	def update(self, screen, delta, camera, grabbedPoints, wheel, drawMode):
		if self.cooldown > 0:
			self.cooldown -= delta
		else:
			self.cooldown = 0

		self.wheel = wheel
		self.drawMode = drawMode

		keys = pygame.key.get_pressed()
		#flips the shape on the x and y axis
		if keys[pygame.K_f] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.cooldown = CD
			tempPos = self.p2.pos
			self.p2.setPos(self.p1.pos)
			self.p1.setPos(tempPos)
		#flips the shape on the x axis
		if keys[pygame.K_x] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.cooldown = CD
			tempX = self.p1.pos.x
			self.p1.setPos(Vector2(self.p2.pos.x, self.p1.pos.y))
			self.p2.setPos(Vector2(tempX, self.p2.pos.y))
		#flips the shape on the y axis
		elif keys[pygame.K_y] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.cooldown = CD
			tempY = self.p1.pos.y
			self.p1.setPos(Vector2(self.p1.pos.x, self.p2.pos.y))
			self.p2.setPos(Vector2(self.p2.pos.x, tempY))

		if self.cPoint.grabbed:
			#updates each of the points to it's relative position before cPoint was grabbed and adds the mouse (or, cPoint.pos)
			self.p1.pos = self.p1.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			self.p2.pos = self.p2.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			#When cPoint is released. This is only called once.
			if not pygame.mouse.get_pressed(3)[0]:
				#updates the static position of x and y Points.
				self.p1.updateStaticPos()
				self.p2.updateStaticPos()
		elif self.cPoint.grabbed == False or self.p1.grabbed or self.p2.grabbed:
			#updates the cPoint if p1 or p2 is grabbed.
			self.updateCPointPos()
		
		#when scrollwheel is used, the wheel function is called
		if (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			if self.wheel != 0:
				self.wheelFunction()

		#draws all points/lines in the shape based on the self.drawMode.
		#has to happen before the points update to avoid inconcistency issues.
		self.draw(screen, camera)

		#updates cPoint and draws to the screen.
		self.cPoint.update(screen, camera, grabbedPoints)

		#updates x and y points and draws them to the screen.
		self.p1.update(screen, camera, grabbedPoints)
		self.p2.update(screen, camera, grabbedPoints)

	#updates the cPoints to where the cPoint should be relative to p1 and p2. This function should set cPoint's pos to whatever your equation for it's pos is.
	def updateCPointPos(self):
		raise SyntaxError("Why tf are you supering this lmao")

	#handles what happens when self.wheel != 0. (or when the scrollwheel is used.)
	def wheelFunction(self):
		self.iterations += self.wheel
		if self.iterations < 1:
			self.iterations = 1

	#draws the shape based on the drawMode of the shape.
	def draw(self, screen, camera):
		#points uses self.getPoints to store a list of Vector2s for positions of all points along the shape that should be drawn.
		points = self.getPoints()
		#from there the points will be drawn depending on the draw mode.
		if self.drawMode == "points":
			for i in range(len(points)):
				if pointOnScreen(points[i], camera, 1): #culls points when off screen.
					pygame.draw.circle(screen, self.drawColor, points[i] + camera, 1)
		elif self.drawMode == "lines":
			for i in range(len(points) - 1):
				if pointOnScreen(points[i], camera, 1) or pointOnScreen(points[i + 1], camera, 1):
					pygame.draw.line(screen, self.drawColor, points[i] + camera, points[i + 1] + camera, 1)
		else:
			raise TypeError(f"{self.drawMode} is not a valid drawMode.")
	
	#returns a list of Vector2s for all positions of each point in the shape. (based on the #iterations.)
	def getPoints(self):
		raise SyntaxError("Why tf are you supering this lmao")

	def saveData(self):
		points = self.getPoints()
		saveString = f"{type(self)}; {self.p1.pos}; {self.p2.pos}; {self.iterations}\n"
		for point in range(len(points)):
			saveString += f"({points[point].x}, {points[point].y})"
			if point < len(points) - 1:
				saveString += "; "
			elif point == len(points) - 1:
				saveString += "\n"
		return saveString

class Point:
	def __init__(self, pos : Vector2 = Vector2(0, 0), color : tuple = (255, 255, 255)):
		self.pos = pos
		self.staticPos = pos
		self.color = color
		self.size = 2
		self.grabbed = False
		self.highlighted = False
	
	#staticPos is the position of the point when it was last grabbed.
	#grabbed points is a list of all points that are held. This is to prevent holding more than one point when adjusting all points.
	def update(self, screen, camera, grabbedPoints): #draw : bool = True):
		keys = pygame.key.get_pressed()
		maxGrabbed = 1 if not keys[pygame.K_LSHIFT] else 2

		mousePos = Vector2(pygame.mouse.get_pos())
		if math.dist(mousePos, self.pos + camera) <= 5 and len(grabbedPoints) < maxGrabbed: #if the mouse is in range to grab this point and isn't already grabbing a point.
			self.highlighted = True
			if pygame.mouse.get_pressed(3)[0] and not self.grabbed: #if the point is clicked on.
				self.grabbed = True
				grabbedPoints.append(self) #adds itself to the list of all grabbed points.
		elif not self.grabbed: #only will set self.highlighted to False if the point isn't grabbed AND the mouse isn't in range of the point.
			self.highlighted = False

		#if the mouse was close enough to activate the highlighted bool, then the point will be slightly larger.
		#having the code seperate allows for the particle to appear highlighted even though it's not technically in distance because the mouse moves too fast.
		if self.highlighted: 
			self.size = 5 #size when held
		else:
			# self.size = math.dist(mousePos, self.pos + camera)
			self.size = 2 #default size if it's not grabbed.

		if self.grabbed:
			self.pos = mousePos - camera
			pygame.draw.circle(screen, self.color, self.pos + camera, self.size) #draws to self.pos, which == mousePos
			if not pygame.mouse.get_pressed(3)[0]: #when lmb is released. (only calls once)
				self.grabbed = False
				self.highlighted = False
				self.pos = mousePos - camera #position is updated
				self.staticPos = self.pos #updates staticPos
				grabbedPoints.remove(self) #removed from list of held points.
		elif pointOnScreen(self.pos, camera, self.size): #culls points when off screen
			#if the point isn't being held by the mouse, then it's position is set to it's position in the world space.
			pygame.draw.circle(screen, self.color, self.pos + camera, self.size)
	
	def updateStaticPos(self):
		self.staticPos = self.pos

	def setPos(self, pos):
		self.pos = pos
		self.updateStaticPos()

class Circle(drawnShape):
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X//2, SCREEN_Y//2), iterations : int = 5, drawColor : tuple = (150, 150, 150), drawMode : str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None, curveMult : float = 0):
		super().__init__(pos, iterations, drawColor, drawMode, p1Pos, p2Pos)
		self.curveMult = curveMult

	def saveData(self):
		points = self.getPoints()
		saveString = f"{type(self)}; {self.p1.pos}; {self.p2.pos}; {self.iterations}; {self.curveMult}\n"
		for point in range(len(points)):
			saveString += f"({points[point].x}, {points[point].y})"
			if point < len(points) - 1:
				saveString += "; "
			elif point == len(points) - 1:
				saveString += "\n"
		return saveString

	def updateCPointPos(self):
		self.cPoint.setPos(Vector2(self.p1.pos.x, self.p2.pos.y))

	def wheelFunction(self):
		keys = pygame.key.get_pressed()
		#if LCTRL is pressed, then the wheel function will be treated differently. Otherwise it just does as default.
		if keys[pygame.K_LCTRL]:
			speed = 5
			#LSHIFT makes it so that you change the curveMult slower.
			if keys[pygame.K_LSHIFT]:
				speed = 15
			self.curveMult += self.wheel / speed
		elif not keys[pygame.K_LCTRL]:
			super().wheelFunction()

	def getPoints(self):
		#relative positions to centerPoint.
		tempRelXPos = self.p1.pos - self.cPoint.pos
		tempRelYPos = self.p2.pos - self.cPoint.pos

		if tempRelXPos.y < 0 and tempRelYPos.x > 0: #Q1
			minDegrees = 270
		elif tempRelXPos.y < 0 and tempRelYPos.x < 0: #Q2
			minDegrees = 180
		elif tempRelXPos.y > 0 and tempRelYPos.x > 0: #Q3
			minDegrees = 0
		elif tempRelXPos.y > 0 and tempRelYPos.x < 0: #Q4
			minDegrees = 90
		else:
			minDegrees = 0

		#len of the points relative to eachother.
		xLen = abs(self.p2.pos.x - self.p1.pos.x)
		yLen = abs(self.p1.pos.y - self.p2.pos.y)

		#draws (self.iterations) points along the quarter circle.
		returnPoints = []
		for i in range(self.iterations + 1):
			percent = i / self.iterations
			angle = (90 * percent + minDegrees)

			#idfk how this math works, I just asked chatGPT lmao
			factor = math.sin(percent * math.pi)

			#multiplies each of the scales by self.curveMult, which is only applied based on the factor. (factor depends on the percent.)
			y = math.sin(math.radians(angle)) * (yLen * (1 + self.curveMult * factor)) + self.cPoint.pos.y
			x = math.cos(math.radians(angle)) * (xLen * (1 + self.curveMult * factor)) + self.cPoint.pos.x

			returnPoints.append(Vector2(x, y))
		return returnPoints
	
class Line(drawnShape):
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X//2, SCREEN_Y//2), iterations : int = 1, drawColor : tuple = (150, 150, 150), drawMode : str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None):
		super().__init__(pos, iterations, drawColor, drawMode, p1Pos, p2Pos)

	def updateCPointPos(self):
		#half the distance from p2.
		self.cPoint.setPos(self.p2.pos + Vector2((self.p1.pos.x - self.p2.pos.x) * .5, (self.p1.pos.y - self.p2.pos.y) * .5))

	def getPoints(self):
		#len of p1 compared to p2
		len = self.p1.pos - self.p2.pos
		
		returnPoints = []
		#defines (#self.iterations) points along the line
		for i in range(self.iterations + 1):
			percent = i / self.iterations
			#points are a percent of len away from p2.
			pos = self.p2.pos + Vector2(len.x * percent, len.y * percent)

			returnPoints.append(pos)
		return returnPoints
	
class LockedLine(Line):
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X//2, SCREEN_Y//2), iterations : int = 1, drawColor : tuple = (150, 150, 150), drawMode : str = "points", p1Pos : Vector2 = None, p2Pos : Vector2 = None):
		super().__init__(pos, iterations, drawColor, drawMode, p1Pos, p2Pos)
		self.angle = random.randint(0, 360)
		self.p1.setPos(Vector2(math.cos(self.angle) * 50, math.sin(self.angle) * 50) + self.cPoint.pos)
		self.p2.setPos(Vector2(math.cos(self.angle) * -50, math.sin(self.angle) * -50) + self.cPoint.pos)

	def update(self, screen, delta, camera, grabbedPoints, wheel, drawMode):
		super().update(screen, delta, camera, grabbedPoints, wheel, drawMode)
		tempRelDistance = Vector2(pygame.mouse.get_pos()) - (self.cPoint.pos - camera)
		distance = tempRelDistance.x if abs(tempRelDistance.x) > abs(tempRelDistance.y) else tempRelDistance.y
		if self.p1.grabbed:
			pos = Vector2(math.cos(self.angle) * distance, math.sin(self.angle) * distance)
			self.p1.setPos(pos + self.cPoint.pos)
			pygame.draw.circle(screen, self.drawColor, pos + self.cPoint.pos, 2)
		if self.p2.grabbed:
			pos = Vector2(math.cos(self.angle) * distance, math.sin(self.angle) * distance)
			self.p2.setPos(pos + self.cPoint.pos)
			pygame.draw.circle(screen, self.drawColor, pos + self.cPoint.pos, 2)

	def updateCPointPos(self):
		if not (self.p1.grabbed or self.p2.grabbed):
			super().updateCPointPos()