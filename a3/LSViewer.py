# LSViewer.py
#
#
# B. Bird - 02/09/2016

import sys, os, platform
#Set up import paths for the SDL2 libraries
if platform.system() == 'Linux':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_linux')
elif platform.system() == 'Darwin':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_osx')
elif platform.system() == 'Windows':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_windows')

  
import sdl2
import sdl2.ext
from sdl2 import *
import sdl2.sdlgfx
import time
import math

import numpy
from transformed_renderer import TransformedRenderer
from LSystem import LSystem, LSystemParseException

def IdentityMatrix(n):
	return numpy.matrix(numpy.identity(n))

def Rotation(radians):
	M = IdentityMatrix(3)
	M[0,0] = M[1,1] = numpy.cos(radians)
	M[1,0] = -numpy.sin(radians)
	M[0,1] = numpy.sin(radians)
	return M

def Translation(tx,ty):
	M = IdentityMatrix(3)
	M[0,2] = tx
	M[1,2] = ty
	return M
	
def Scale(sx,sy):
	M = IdentityMatrix(3)
	M[0,0] = sx
	M[1,1] = sy
	return M

class A3Canvas:
	CANVAS_SIZE_X = 800
	CANVAS_SIZE_Y = 600
	
	def __init__(self, L_system):
		self.LS_iterations = 0
		self.L_system = L_system
		
	def draw_leaf(self, tr):
		vx = [0,1.0 ,1.25,   1,  0,  -1,-1.25,-1]
		vy = [0,0.75,1.75,2.75,4.0,2.75, 1.75,0.75]
		numVerts = 8;
		tr.fill_polygon(vx,vy,numVerts, 64+10*self.LS_iterations,224,0, 255)
		tr.draw_polygon(vx,vy,numVerts, 64+10*self.LS_iterations,128,0, 255)
	
	def leaf_shadow(self, tr):
		vx = [0,1.0 ,1.25,   1,  0,  -1,-1.25,-1]
		vy = [0,0.75,1.75,2.75,4.0,2.75, 1.75,0.75]
		numVerts = 8;
		tr.fill_polygon(vx,vy,numVerts, 255,255,255, 255)
		

	
	def draw_stem(self, tr, viewportTransform):	
		tr.fill_rectangle(-1,0,1,7,139-5*self.LS_iterations,69-5*self.LS_iterations,19-1*self.LS_iterations,255)
		viewportTransform *= Translation(0,7)
		
	def stem_shadow(self, tr, viewportTransform):	
		tr.fill_rectangle(-1,0,1,7,255,255,255,255)
		viewportTransform *= Translation(0,7)
	
	def draw_apple(self, tr):	
		tr.fill_circle(0,3,1,255,0,0,255)
		
	def draw(self,renderer,frame_delta_seconds):

		ls_string = self.L_system.generate_system_string(self.LS_iterations)
		print "Drawing with %d iterations."%(self.LS_iterations)
		print "System string: %s"%ls_string

		sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
		sdl2.SDL_RenderClear(renderer);
		
		tr = TransformedRenderer(renderer)
		viewportTransform = IdentityMatrix(3)
		
		
		if filename == "ex3.txt":
			viewportTransform *= Translation(40,100)
		elif filename == "ex4.txt" or filename == "ex5.txt"or filename == "ex7.txt":
			viewportTransform *= Translation( 50,self.CANVAS_SIZE_Y -15)
		elif filename == "ex6.txt":
			viewportTransform *= Translation(self.CANVAS_SIZE_X/2,self.CANVAS_SIZE_Y/2)
		else:
			viewportTransform *= Translation(self.CANVAS_SIZE_X/2,self.CANVAS_SIZE_Y)
		
		viewportTransform *= Scale(1,-1)
		viewportTransform *= Scale(self.CANVAS_SIZE_X/100.0,self.CANVAS_SIZE_Y/100.0)
		
		tr2 = TransformedRenderer(renderer)
		shadowviewportTransform = IdentityMatrix(3)
		shadowviewportTransform *= Translation(self.CANVAS_SIZE_X/2,self.CANVAS_SIZE_Y)
		shadowviewportTransform *= Scale(1,-1)
		shadowviewportTransform *= Scale(self.CANVAS_SIZE_X/100.0,self.CANVAS_SIZE_Y/100.0)
		shadowviewportTransform *= Rotation(45 * math.pi/180)
		
		if filename == "ex7.txt":
			viewportTransform *= Rotation(-65 * math.pi/180)
		
		stack = []
		stack2 = []

		for i in range(len(ls_string)):
		
			tr2.set_transform(shadowviewportTransform)
			tr.set_transform(viewportTransform)			
			
			if ls_string[i] == "L":		
				if filename == "shadow.txt":
					self.leaf_shadow(tr2)
				self.draw_leaf(tr)
			elif ls_string[i] == "T":
				if filename == "shadow.txt":
					self.stem_shadow(tr2,shadowviewportTransform)						
				self.draw_stem(tr,viewportTransform)
			
			elif ls_string[i] == "o":
				self.draw_apple(tr)
						
			elif ls_string[i] == "+":
				if filename == "ex4.txt":		
					viewportTransform *= Rotation(-90 * math.pi/180)
				elif filename == "ex5.txt":
					viewportTransform *= Rotation(-60 * math.pi/180)
				elif filename == "ex6.txt":		
					viewportTransform *= Rotation(90 * math.pi/180)
				elif filename == "ex7.txt":		
					viewportTransform *= Rotation(25 * math.pi/180)
				elif filename == "shadow.txt":
					shadowviewportTransform *= Rotation(-30 * math.pi/180)
					viewportTransform *= Rotation(-30 * math.pi/180)
				else:
					viewportTransform *= Rotation(-30 * math.pi/180)
				
			elif ls_string[i] == "-":
				if filename == "ex4.txt":			
					viewportTransform *= Rotation(90 * math.pi/180)
				elif filename == "ex5.txt":
					viewportTransform *= Rotation(60 * math.pi/180)
				elif filename == "ex6.txt":		
					viewportTransform *= Rotation(-90 * math.pi/180)
				elif filename == "ex7.txt":		
					viewportTransform *= Rotation(-25 * math.pi/180)
				elif filename == "shadow.txt":
					shadowviewportTransform *= Rotation(30 * math.pi/180)
					viewportTransform *= Rotation(30 * math.pi/180)
				else:
					viewportTransform *= Rotation(30 * math.pi/180)			
				
			elif ls_string[i] == "s":
				if filename == "shadow.txt":
					shadowviewportTransform *= Scale(0.9,0.9)
				viewportTransform *= Scale(0.9,0.9)
				
			elif ls_string[i] == "S":
				if filename == "shadow.txt":
					shadowviewportTransform *= Scale(1/0.9,1/0.9)
				viewportTransform *= Scale(1/0.9,1/0.9)
				
			elif ls_string[i] == "h":
				if filename == "shadow.txt":
					shadowviewportTransform *= Scale(0.9,1)
				viewportTransform *= Scale(0.9,1)
				
			elif ls_string[i] == "H":
				if filename == "shadow.txt":
					shadowviewportTransform *= Scale(1/0.9,1)
				viewportTransform *= Scale(1/0.9,1)
				
			elif ls_string[i] == "v":
				if filename == "shadow.txt":
					shadowviewportTransform *= Scale(1,0.9)
				viewportTransform *= Scale(1,0.9)
				
			elif ls_string[i] == "V":
				if filename == "shadow.txt":
					shadowviewportTransform *= Scale(1,1/0.9)
				viewportTransform *= Scale(1,1/0.9)
				
			elif ls_string[i] == "[":
				if filename == "ex2.txt":
					stack.append(numpy.matrix(viewportTransform))
					viewportTransform *= Rotation(-45 * math.pi/180)
				elif filename == "shadow.txt":
					stack2.append(numpy.matrix(shadowviewportTransform))
					stack.append(numpy.matrix(viewportTransform))					
				else:
					stack.append(numpy.matrix(viewportTransform))
				
			elif ls_string[i] == "]":
				if filename == "ex2.txt":
					viewportTransform = stack.pop()
					viewportTransform *= Rotation(45 * math.pi/180)
				elif filename == "shadow.txt":
					try:
						shadowviewportTransform = stack2.pop()
					except IndexError:
						pass
					viewportTransform = stack.pop()
				else:			
					viewportTransform = stack.pop()
				
			elif ls_string[i] == "F":
				tr.draw_line(0,0,1,0,1, 0, 255, 0, 255)
				viewportTransform *= Translation(1,0)
				
			elif ls_string[i] == "A":
				if filename == "ex2.txt":
					tr.draw_line(0,0,0,0.7,1, 0, 255, 0, 255)
					viewportTransform *= Translation(0,0.7)
				elif filename == "ex3.txt":
					if i == len(ls_string)-1:
						viewportTransform *= Translation(40,100+self.LS_iterations*5)
						viewportTransform *= Scale(1,-1)
						viewportTransform *= Scale(self.CANVAS_SIZE_X/100.0,self.CANVAS_SIZE_Y/100.0)
					tr.draw_line(0,0,90,0,1, 0, 255, 0, 255)
					viewportTransform *= Translation(90-(2/3*self.LS_iterations),0)
				else:
					tr.draw_line(0,0,1,0,1, 0, 255, 0, 255)
					viewportTransform *= Translation(1,0)
					
			elif ls_string[i] == "B":
				if filename == "ex2.txt":
					tr.draw_line(0,0,0,0.7,1, 0, 255, 0, 255)
					viewportTransform *= Translation(0,0.7)
				elif filename == "ex3.txt":
					if i == len(ls_string)-1:
						viewportTransform *= Translation(40,100+self.LS_iterations*5)
						viewportTransform *= Scale(1,-1)
						viewportTransform *= Scale(self.CANVAS_SIZE_X/100.0,self.CANVAS_SIZE_Y/100.0)
					viewportTransform *= Translation(90-(2/3*self.LS_iterations),-10)

				else:
					tr.draw_line(0,0,1,0,1, 0, 255, 0, 255)
					viewportTransform *= Translation(1,0)
			
				
		sdl2.SDL_RenderPresent(renderer)

	def frame_loop(self,renderer):
		last_frame = time.time()
		self.draw(renderer,0)
		while True:
			current_frame = time.time()
			frame_time = current_frame-last_frame
			all_events = sdl2.ext.get_events()
			for event in all_events:
				if event.type == sdl2.SDL_QUIT:
					return
				elif event.type == sdl2.SDL_KEYDOWN:
					key_code = event.key.keysym.sym
					if key_code == sdl2.SDLK_UP:
						self.LS_iterations += 1
					elif key_code == sdl2.SDLK_DOWN:
						self.LS_iterations = max(self.LS_iterations-1, 0)
					elif key_code == sdl2.SDLK_ESCAPE:
						exit()
					self.draw(renderer,frame_time)
				elif event.type == sdl2.SDL_MOUSEMOTION:
					pass
				elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
					pass
				elif event.type == sdl2.SDL_MOUSEBUTTONUP:
					pass
			self.CANVAS_SIZE_X = window.size[0]
			self.CANVAS_SIZE_Y = window.size[1]
			self.draw(renderer,frame_time)
			last_frame = current_frame
			


if len(sys.argv) < 2:
	print 'Usage: python %s <input file>'%sys.argv[0]
	sys.exit(0)
	
filename = sys.argv[1]
try:
	L = LSystem(filename)
except LSystemParseException:
	print 'Error parsing %s'%filename
	sys.exit(0)

sdl2.ext.init()

window = sdl2.ext.Window("CSC 205 A3", size=(A3Canvas.CANVAS_SIZE_X, A3Canvas.CANVAS_SIZE_Y),flags = (sdl2.SDL_WINDOW_RESIZABLE))
window.show()

renderer = sdl2.SDL_CreateRenderer(window.window, -1,0)# sdl2.SDL_RENDERER_PRESENTVSYNC | sdl2.SDL_RENDERER_ACCELERATED);


sdl2.SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255)
sdl2.SDL_RenderClear(renderer)
sdl2.SDL_RenderPresent(renderer)

canvas = A3Canvas(L)		
canvas.frame_loop(renderer)
		
sdl2.SDL_DestroyRenderer(renderer)
