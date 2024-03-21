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
	
	def update(self, screen, camera, mouseVel, grabbedPoints, relativePos = Vector2(0, 0), mousePos = None): #draw : bool = True):
		mousePos = pygame.mouse.get_pos() if mousePos == None else mousePos
		if math.dist(mousePos, self.pos + camera) <= 5 and len(grabbedPoints) < 1:
			# print(f"True, {mousePos}, {self.pos}, {camera}, {self.pos+camera}, {math.dist(mousePos, self.pos + camera)}, {len(grabbedPoints)}")
			self.highlighted = True
			if pygame.mouse.get_pressed(3)[0] and not self.grabbed:
				self.grabbed = True
				grabbedPoints.append(self)
		# else:
			# print(f"False, {mousePos}, {self.pos}, {camera}, {self.pos+camera}, {math.dist(mousePos, self.pos + camera)}, {len(grabbedPoints)}")

		if self.highlighted:
			self.highlighted = self.grabbed
			self.size = 5
		else:
			# self.size = math.dist(mousePos, self.pos + camera)
			self.size = 2

		if self.grabbed:
			self.pos = mousePos
			pygame.draw.circle(screen, self.color, self.pos, self.size)
			if not pygame.mouse.get_pressed(3)[0]: #when lmb is released. (only calls once)
				self.grabbed = False
				self.pos = mousePos - camera
				self.staticPos = self.pos
				# print(self.pos, mousePos, camera)
				grabbedPoints.remove(self)
		else:
			# self.pos = self.staticPos + relativePos #ok so should only do this IF the main point is grabbed. otherwise don't do shit.
			pygame.draw.circle(screen, self.color, self.pos + camera, self.size)

		#relativePos is the position of whatever you want the point to be relative to.
		#staticPos is the position of the point when it was last grabbed.