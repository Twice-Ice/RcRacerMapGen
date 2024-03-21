import pygame
import math
import random
from pygame import Vector2
from globals import SCREEN_X, SCREEN_Y, CD

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

		#if the mouse was close enough to activate the highlighted bool, then the point will be slightly larger.
		#having the code seperate allows for the particle to appear highlighted even though it's not technically in distance because the mouse moves too fast.
		if self.highlighted: 
			self.highlighted = self.grabbed #this is to update self.highlighted in the case that the point is no longer grabbed.
			self.size = 5 #size when held
		else:
			# self.size = math.dist(mousePos, self.pos + camera)
			self.size = 2 #default size if it's not grabbed.

		if self.grabbed:
			self.pos = mousePos
			pygame.draw.circle(screen, self.color, self.pos, self.size) #draws to self.pos, which == mousePos
			if not pygame.mouse.get_pressed(3)[0]: #when lmb is released. (only calls once)
				self.grabbed = False
				self.pos = mousePos - camera #position is updated
				self.staticPos = self.pos #updates staticPos
				grabbedPoints.remove(self) #removed from list of held points.
		else:
			#if the point isn't being held by the mouse, then it's position is set to it's position in the world space.
			pygame.draw.circle(screen, self.color, self.pos + camera, self.size)
	
	def updateStaticPos(self):
		self.staticPos = self.pos


class Circle:
	def __init__(self, pos : Vector2 = Vector2(SCREEN_X//2, SCREEN_Y//2), iterations : int = 10):
		self.pos = pos
		self.iterations = iterations

		self.cPoint = Point(self.pos, (0, 255, 0))
		self.xPoint = Point(self.pos + Vector2(100, 0), (255, 0, 0))
		self.yPoint = Point(self.pos + Vector2(0, 100), (0, 0, 255))

		self.cPoint.pos = Vector2(self.xPoint.pos.x, self.yPoint.pos.y)
		self.cPoint.updateStaticPos()

	'''
	So the way that positional stuff is controlled is that for all points other than the mainPoint, their position is just set to the mouse if they are grabbed.
	When they are released, their position is updated to the world position of the mouse on screen. So, SS -> WS (Screen Space, World Space)

	A similar setup is happening with the mainPoint. If it's grabbed, then it's position is just set to the mouse.
	However, all other points have their relative positions stored, and then are moved to their relativePos + mainPoint.pos (mainPoint.pos == mouse)
	When mainPoint is released though, the other point's staticPosition is updated to reflect that which was shown on screen while mainPoint.grabbed == True.
	'''
	def update(self, screen, camera, grabbedPoints):
		if self.cPoint.grabbed:
			#updatees each of the points to it's relative position before cPoint was grabbed and adds the mouse (or, cPoint.pos)
			self.xPoint.pos = (self.xPoint.staticPos - self.cPoint.staticPos) + self.cPoint.pos
			self.yPoint.pos = (self.yPoint.staticPos - self.cPoint.staticPos) + self.cPoint.pos
			if not pygame.mouse.get_pressed(3)[0]:
				self.xPoint.staticPos = self.xPoint.pos
				self.yPoint.staticPos = self.yPoint.pos
		self.xPoint.update(screen, camera, grabbedPoints)
		self.yPoint.update(screen, camera, grabbedPoints)

		if self.xPoint.grabbed or self.yPoint.grabbed:
			self.cPoint.pos = Vector2(self.xPoint.pos.x, self.yPoint.pos.y)
			self.cPoint.updateStaticPos()

		self.cPoint.update(screen, camera, grabbedPoints)