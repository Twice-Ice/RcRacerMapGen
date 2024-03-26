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
		mousePos = Vector2(pygame.mouse.get_pos())
		if math.dist(mousePos, self.pos + camera) <= 5 and len(grabbedPoints) < 1: #if the mouse is in range to grab this point and isn't already grabbing a point.
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

	def updatePos(self, pos):
		self.pos = pos
		self.updateStaticPos()


class Circle:
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X//2, SCREEN_Y//2), iterations : int = 10, drawColor : tuple = (150, 150, 150)):
		self.pos = pos
		self.iterations = iterations
		self.cooldown = 0

		self.drawColor = drawColor

		self.cPoint = Point(self.pos, (0, 255, 0))
		self.p1 = Point(self.pos + Vector2(0, 100), (0, 0, 255))
		self.p2 = Point(self.pos + Vector2(100, 0), (255, 0, 0))

		self.xLen = abs(self.cPoint.pos.x - self.p1.pos.x)
		self.yLen = abs(self.cPoint.pos.y - self.p2.pos.y)

		self.cPoint.pos = Vector2(self.p1.pos.x, self.p2.pos.y)
		self.cPoint.updateStaticPos()

	'''
	So the way that positional stuff is controlled is that for all points other than the mainPoint, their position is just set to the mouse if they are grabbed.
	When they are released, their position is updated to the world position of the mouse on screen. So, SS -> WS (Screen Space, World Space)

	A similar setup is happening with the mainPoint. If it's grabbed, then it's position is just set to the mouse.
	However, all other points have their relative positions stored, and then are moved to their relativePos + mainPoint.pos (mainPoint.pos == mouse)
	When mainPoint is released though, the other point's staticPosition is updated to reflect that which was shown on screen while mainPoint.grabbed == True.
	'''
	def update(self, screen, delta, camera, grabbedPoints, wheel):
		#updates self.cooldown
		if self.cooldown > 0:
			self.cooldown -= delta
		else:
			self.cooldown = 0

		#updats this in order to account for culling
		self.xLen = abs(self.cPoint.pos.x - self.p1.pos.x)
		self.yLen = abs(self.cPoint.pos.y - self.p2.pos.y)

		#flips the p1 and p2 if f is pressed
		#this MUST happen before the points are updated. Otherwise the points update the next frame after this has happened and it looks weird.
		keys = pygame.key.get_pressed()
		if keys[pygame.K_f] and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.cooldown = CD
			tempPos = self.p2.pos
			self.p2.pos = self.p1.pos
			self.p1.pos = tempPos
			self.p2.updateStaticPos()
			self.p1.updateStaticPos()

		if self.cPoint.grabbed:
			#updates each of the points to it's relative position before cPoint was grabbed and adds the mouse (or, cPoint.pos)
			self.p1.pos = self.p1.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			self.p2.pos = self.p2.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			#When cPoint is released. This is only called once.
			if not pygame.mouse.get_pressed(3)[0]:
				#updates the static position of x and y Points.
				self.p1.updateStaticPos()
				self.p2.updateStaticPos()
		else:
			#updating the cPoint based on the p1 and p2 prevents cPoint not updating after it's released.
			self.cPoint.pos = Vector2(self.p1.pos.x, self.p2.pos.y)
			self.cPoint.updateStaticPos()

		#updates the cPoint to p1.x and p2.y only if p1 or p2 are grabbed. 
		if self.p1.grabbed or self.p2.grabbed:
			self.cPoint.pos = Vector2(self.p1.pos.x, self.p2.pos.y)
			self.cPoint.updateStaticPos()

		if (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.iterations += wheel
			if self.iterations < 1:
				self.iterations = 1

		#draws all points along the quarter circle
		#has to happen before the points update to avoid inconcistency issues.
		self.drawCirclePoints(screen, camera)

		#updates cPoint and draws to the screen.
		self.cPoint.update(screen, camera, grabbedPoints)

		#updates x and y points and draws them to the screen.
		self.p1.update(screen, camera, grabbedPoints)
		self.p2.update(screen, camera, grabbedPoints)

	def drawCirclePoints(self, screen, camera):
		#relative positions to centerPoint.
		tempRelXPos = self.p1.pos - self.cPoint.pos
		tempRelYPos = self.p2.pos - self.cPoint.pos

		if tempRelXPos.y < 0 and tempRelYPos.x > 0: #Q1
			minDegrees = 270
			maxDegrees = 360
		elif tempRelXPos.y < 0 and tempRelYPos.x < 0: #Q2
			minDegrees = 180
			maxDegrees = 270
		elif tempRelXPos.y > 0 and tempRelYPos.x > 0: #Q3
			minDegrees = 0
			maxDegrees = 90
		elif tempRelXPos.y > 0 and tempRelYPos.x < 0: #Q4
			minDegrees = 90
			maxDegrees = 180
		else:
			minDegrees = 0
			maxDegrees = 90

		#len of the points relative to eachother.
		self.xLen = abs(self.p2.pos.x - self.p1.pos.x)
		self.yLen = abs(self.p1.pos.y - self.p2.pos.y)

		#draws (self.iterations) points along the quarter circle.
		for i in range(self.iterations + 1):
			percent = i / self.iterations
			angle = math.radians(90 * percent + minDegrees)
			x = math.cos(angle) * self.xLen + self.cPoint.pos.x
			y = math.sin(angle) * self.yLen + self.cPoint.pos.y

			if pointOnScreen(Vector2(x, y), camera, 1): #culls points when off screen.
				pygame.draw.circle(screen, self.drawColor, (x, y) + camera, 1)

class Line:
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X//2, SCREEN_Y//2), iterations : int = 10, drawColor : tuple = (150, 150, 150)):
		self.pos = pos
		self.iterations = iterations
		self.cooldown = 0
		self.drawColor = drawColor

		self.cPoint = Point(self.pos, (0, 255, 0))
		self.p1 = Point(self.pos + Vector2(0, 100), (0, 0, 255))
		self.p2 = Point(self.pos + Vector2(100, 0), (255, 0, 0))

		self.updateLens()

		self.cPoint.updatePos(self.p2.pos + Vector2((self.p1.pos.x - self.p2.pos.x) * .5, (self.p1.pos.y - self.p2.pos.y) * .5))

	def updateLens(self):
		self.xLen = abs(self.p1.pos.x - self.p2.pos.x)
		self.yLen = abs(self.p1.pos.y - self.p2.pos.y)

	def update(self, screen, delta, camera, grabbedPoints, wheel):
		#updates self.cooldown
		if self.cooldown > 0:
			self.cooldown -= delta
		else:
			self.cooldown = 0

		self.updateLens()

		#flips the p1 and p2 if f is pressed
		#this MUST happen before the points are updated. Otherwise the points update the next frame after this has happened and it looks weird.
		keys = pygame.key.get_pressed()
		if (keys[pygame.K_f] and keys[pygame.K_x]) and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.cooldown = CD
			tempX = self.p1.pos.x
			self.p1.updatePos(Vector2(self.p2.pos.x, self.p1.pos.y))
			self.p2.updatePos(Vector2(tempX, self.p2.pos.y))
		elif (keys[pygame.K_f] and keys[pygame.K_y]) and self.cooldown == 0 and (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.cooldown = CD
			tempY = self.p1.pos.y
			self.p1.updatePos(Vector2(self.p1.pos.x, self.p2.pos.y))
			self.p2.updatePos(Vector2(self.p2.pos.x, tempY))

		if self.cPoint.grabbed:
			#updates each of the points to it's relative position before cPoint was grabbed and adds the mouse (or, cPoint.pos)
			self.p1.pos = self.p1.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			self.p2.pos = self.p2.staticPos + (self.cPoint.pos - self.cPoint.staticPos)
			#When cPoint is released. This is only called once.
			if not pygame.mouse.get_pressed(3)[0]:
				#updates the static position of x and y Points.
				self.p1.updateStaticPos()
				self.p2.updateStaticPos()
		else:
			#updating the cPoint based on the p1 and p2 prevents cPoint not updating after it's released.
			self.cPoint.updatePos(self.p2.pos + Vector2((self.p1.pos.x - self.p2.pos.x) * .5, (self.p1.pos.y - self.p2.pos.y) * .5))

		#updates the cPoint to p1.x and p2.y only if p1 or p2 are grabbed. 
		if self.p1.grabbed or self.p2.grabbed:
			self.cPoint.updatePos(self.p2.pos + Vector2((self.p1.pos.x - self.p2.pos.x) * .5, (self.p1.pos.y - self.p2.pos.y) * .5))

		if (self.p1.highlighted or self.p2.highlighted or self.cPoint.highlighted):
			self.iterations += wheel
			if self.iterations < 1:
				self.iterations = 1

		#draws all points along the quarter circle
		#has to happen before the points update to avoid inconcistency issues.
		self.drawLinePoints(screen, camera)

		#updates cPoint and draws to the screen.
		self.cPoint.update(screen, camera, grabbedPoints)

		#updates x and y points and draws them to the screen.
		self.p1.update(screen, camera, grabbedPoints)
		self.p2.update(screen, camera, grabbedPoints)

	def drawLinePoints(self, screen, camera):
		#len of p1 compared to p2
		len = self.p1.pos - self.p2.pos
		
		#draws (self.iterations) points along the line
		for i in range(self.iterations + 1):
			percent = i / self.iterations
			#points are a percent of len away from p2.
			pos = self.p2.pos + Vector2(len.x * percent, len.y * percent)

			if pointOnScreen(pos, camera, 1): #culls points when off screen.
				pygame.draw.circle(screen, self.drawColor, pos + camera, 1)