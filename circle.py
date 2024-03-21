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
	def update(self, screen, camera, grabbedPoints, mousePos = None): #draw : bool = True):
		mousePos = pygame.mouse.get_pos() if mousePos == None else mousePos
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