# sample_ball.py
#
# A sample program consisting of an animated ball which bounces off of the edges of the screen.
#
# B. Bird - 01/27/2016

import sys, os, platform
#Set up import paths for the SDL2 libraries
if platform.system() == 'Linux':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_linux')
elif platform.system() == 'Darwin':
	os.environ['PYSDL2_DLL_PATH'] = os.path.join(os.getcwd(),'lib_osx')
  
import sdl2
import sdl2.ext
from sdl2 import *
import sdl2.sdlgfx
import time
import math
import random
from point import Vector2d


def rotate_vector( v, angle_degrees ):
	rot_x, rot_y = math.cos(angle_degrees*math.pi/180), math.sin(angle_degrees*math.pi/180)
	return Vector2d( v.x*rot_x - v.y*rot_y, rot_x*v.y+rot_y*v.x )

class A2Canvas:
	CANVAS_SIZE_X = 800
	CANVAS_SIZE_Y = 600
	BALL_RADIUS = 10
	BALL_VELOCITY = 0
	START = [20,25,30,35,-20,-25,-30,-35]
	PADDLE_SPEED = 25

	playerscore = 0
	aiscore = 0

	paddle_height = 80
	paddle_width = 20
	
	PLAYERWIN = False
	AIWIN = False
	
	BALL_COLOURS = ( 
					(0,0,0),
					(255,0,0),
					(0,255,0),
					(0,0,255),
					(0,255,255),
					(255,0,255),
					(255,255,0)
				   )
	
	
	def __init__(self):

		self.paddle1_pos = Vector2d(20,300)
		self.paddle2_pos = Vector2d(780,300)	

		self.ball_position = Vector2d(self.CANVAS_SIZE_X/2, self.CANVAS_SIZE_Y/2)
		self.ball_direction = rotate_vector( Vector2d( 1, 0 ), random.choice(self.START) )
		self.ball_colour_idx = 0
		


#===========================================================================================================
				
	def draw(self,renderer,frame_delta_seconds):

		position_delta = frame_delta_seconds*self.BALL_VELOCITY

		new_position = self.ball_position + position_delta*self.ball_direction
		
		if self.paddle1_pos.y < 50:
			self.paddle1_pos.y = 50
		elif self.paddle1_pos.y > 550:
			self.paddle1_pos.y = 550
			
		if self.paddle2_pos.y < 50:
			self.paddle2_pos.y = 50
		elif self.paddle2_pos.y > 550:
			self.paddle2_pos.y = 550

		#AI
		dy = self.PADDLE_SPEED * frame_delta_seconds
		
		if self.ball_position.x < 400:
			if self.paddle1_pos.y  > self.ball_position.y:   # ball top half
				if self.paddle1_pos.y - self.ball_position.y > 50:
					self.paddle1_pos -= Vector2d(0,dy*8)
				else:
					self.paddle1_pos -= Vector2d(0,dy*3)
			else:												# ball bottom half
				if self.ball_position.y - self.paddle1_pos.y > 50:
					self.paddle1_pos += Vector2d(0,dy*8)
				else:
					self.paddle1_pos += Vector2d(0,dy*3)
		else:
			if self.paddle1_pos.y > (self.CANVAS_SIZE_Y / 2):
				self.paddle1_pos -= Vector2d(0,dy)
			elif self.paddle1_pos.y < (self.CANVAS_SIZE_Y / 2):
				self.paddle1_pos += Vector2d(0,dy)



#===========================================================================================================
		#The ball collides with the edge of the screen if the new position is less than BALL_RADIUS
		#pixels away from any edge.

		
		if new_position.x <= self.BALL_RADIUS+30:
			#Collide with left edge
			if self.paddle1_pos.y+60 >= new_position.y >= self.paddle1_pos.y-60:
				if self.paddle1_pos.y -35 >= new_position.y >= self.paddle1_pos.y - 60:  #hit top
					if self.ball_direction.x < 0 and self.ball_direction.y > 0:
						self.ball_direction = rotate_vector(self.ball_direction,180)
						self.BALL_VELOCITY = 450
					else:
						self.ball_direction.x = -self.ball_direction.x;
						self.BALL_VELOCITY = 350
				elif self.paddle1_pos.y + 60 >= new_position.y >= self.paddle1_pos.y + 35: #hit bottom
					if self.ball_direction.x < 0 and self.ball_direction.y < 0:
						self.ball_direction = rotate_vector(self.ball_direction,180)
						self.BALL_VELOCITY = 450
					else:
						self.ball_direction.x = -self.ball_direction.x;
						self.BALL_VELOCITY = 350
				else:					
					#Mirror the direction around the y axis (since the ball bounces)
					self.ball_direction.x = -self.ball_direction.x;
					self.BALL_VELOCITY = 350

				#Determine how far past the collision point the new position is.
				offset_x = (self.BALL_RADIUS+30)-new_position.x;	
				new_position.x += 2*offset_x;
				
				self.ball_colour_idx += 1
				if self.ball_colour_idx >= len(self.BALL_COLOURS):
					self.ball_colour_idx = 0
					
			elif new_position.x <= 10:               #you score
				self.ball_position = Vector2d(self.CANVAS_SIZE_X/2, self.CANVAS_SIZE_Y/2)
				
				self.BALL_VELOCITY = 0
				self.playerscore += 1
				if self.playerscore == 5:
					self.PLAYERWIN = True
				canvas.frame_loop(renderer)
		#===========================================================================================================				
		elif new_position.x >= self.CANVAS_SIZE_X - (self.BALL_RADIUS+30):
			#Collide with right edge
			if self.paddle2_pos.y+60 >= new_position.y >= self.paddle2_pos.y-60:
				if self.paddle2_pos.y -35 >= new_position.y >= self.paddle2_pos.y - 60:  #hit top
					if self.ball_direction.x > 0 and self.ball_direction.y > 0:
						self.ball_direction = rotate_vector(self.ball_direction,180)
						self.BALL_VELOCITY = 450
					else:
						self.ball_direction.x = -self.ball_direction.x;
						self.BALL_VELOCITY = 350
				elif self.paddle2_pos.y + 60 >= new_position.y >= self.paddle2_pos.y + 35: #hit bottom
					if self.ball_direction.x > 0 and self.ball_direction.y < 0:
						self.ball_direction = rotate_vector(self.ball_direction,180)
						self.BALL_VELOCITY = 450
					else:
						self.ball_direction.x = -self.ball_direction.x;
						self.BALL_VELOCITY = 350
				else:
					#Mirror the direction around the y axis (since the ball bounces)
					self.ball_direction.x = -self.ball_direction.x;
					self.BALL_VELOCITY = 350
					
				#Determine how far past the collision point the new position is.
				offset_x = new_position.x - (self.CANVAS_SIZE_X-(self.BALL_RADIUS+30));
				new_position.x -= 2*offset_x;
				
				self.ball_colour_idx += 1
				if self.ball_colour_idx >= len(self.BALL_COLOURS):
					self.ball_colour_idx = 0
					
			elif new_position.x >= 790:				# ai score
				self.ball_position = Vector2d(self.CANVAS_SIZE_X/2, self.CANVAS_SIZE_Y/2)
			
				self.BALL_VELOCITY = 0
				self.aiscore += 1				
				if self.aiscore == 5:
					self.AIWIN = True
				canvas.frame_loop(renderer)
				
		#===========================================================================================================		
		elif new_position.y <= self.BALL_RADIUS:
			#Collide with top

			#Determine how far past the collision point the new position is.
			offset_y = self.BALL_RADIUS-new_position.y;
			#Mirror the direction around the x axis (since the ball bounces)
			self.ball_direction.y = -self.ball_direction.y;
			new_position.y += 2*offset_y;
		#===========================================================================================================			
		elif new_position.y >= self.CANVAS_SIZE_Y - self.BALL_RADIUS:
			#Collide with bottom

			#Determine how far past the collision point the new position is.
			offset_y = new_position.y - (self.CANVAS_SIZE_Y-self.BALL_RADIUS)
			#Mirror the direction around the x axis (since the ball bounces)
			self.ball_direction.y = -self.ball_direction.y
			new_position.y -= 2*offset_y
		self.ball_position = new_position

#===========================================================================================================
		sdl2.SDL_SetRenderDrawColor(renderer, 128, 128, 128, 255);
		sdl2.SDL_RenderClear(renderer);
	
		ball_colour = self.BALL_COLOURS[self.ball_colour_idx];
		pos_x, pos_y = int(self.ball_position.x), int(self.ball_position.y)
		
		paddle1_pos_TL = self.paddle1_pos - Vector2d(10,40)
		paddle1_pos_BR = self.paddle1_pos + Vector2d(10,40)
		paddle2_pos_TL = self.paddle2_pos - Vector2d(10,40)
		paddle2_pos_BR = self.paddle2_pos + Vector2d(10,40)
		
		sdl2.sdlgfx.stringRGBA(renderer,550,0,'Your Score:'+str(self.playerscore),0,0,0,255)
		sdl2.sdlgfx.stringRGBA(renderer,150,0,'AI Score:'+str(self.aiscore),0,0,0,255)
		
		if self.PLAYERWIN == True:
			sdl2.sdlgfx.stringRGBA(renderer,500,300,'YOU WIN!',255,0,0,255)
			
		if self.AIWIN == True:
			sdl2.sdlgfx.stringRGBA(renderer,500,300,'YOU LOST',0,255,0,255)
		
		if self.BALL_VELOCITY == 0:
			if self.playerscore == 0 and self.aiscore == 0:				
				sdl2.sdlgfx.stringRGBA(renderer,500,300,'5 goal to win',0,0,0,255)
				sdl2.sdlgfx.stringRGBA(renderer,500,350,'press SPACE to start',0,0,0,255)
				sdl2.sdlgfx.stringRGBA(renderer,500,380,'press ESC to quit',0,0,0,255)
			elif self.AIWIN == True or self.PLAYERWIN == True:
				sdl2.sdlgfx.stringRGBA(renderer,500,350,'press R to restart',0,0,0,255)
				sdl2.sdlgfx.stringRGBA(renderer,500,380,'press ESC to quit',0,0,0,255)
				
		
			
		
		sdl2.sdlgfx.lineRGBA(renderer,400,0,400,800,0,0,0,255)
		sdl2.sdlgfx.filledCircleRGBA(renderer,pos_x,pos_y,self.BALL_RADIUS,ball_colour[0],ball_colour[1],ball_colour[2],255);

		sdl2.sdlgfx.boxRGBA(renderer,int(paddle1_pos_TL.x),int(paddle1_pos_TL.y),int(paddle1_pos_BR.x),int(paddle1_pos_BR.y),0,0,0,255);
		sdl2.sdlgfx.filledCircleRGBA(renderer,int(self.paddle1_pos.x),int( self.paddle1_pos.y+40),self.BALL_RADIUS,0,0,0,255);
		sdl2.sdlgfx.filledCircleRGBA(renderer,int(self.paddle1_pos.x),int( self.paddle1_pos.y-40),self.BALL_RADIUS,0,0,0,255);
		
		sdl2.sdlgfx.boxRGBA(renderer,int(paddle2_pos_TL.x),int(paddle2_pos_TL.y),int(paddle2_pos_BR.x),int(paddle2_pos_BR.y),0,0,0,255);
		sdl2.sdlgfx.filledCircleRGBA(renderer,int (self.paddle2_pos.x),int (self.paddle2_pos.y+40),self.BALL_RADIUS,0,0,0,255);
		sdl2.sdlgfx.filledCircleRGBA(renderer,int (self.paddle2_pos.x),int (self.paddle2_pos.y-40),self.BALL_RADIUS,0,0,0,255);
		
		sdl2.SDL_RenderPresent(renderer)

#===========================================================================================================

	def frame_loop(self,renderer):
		last_frame = time.time()
		print 'frame loop'
		while True:
			current_frame = time.time()
			frame_time = current_frame-last_frame
			dy = frame_time * self.PADDLE_SPEED
			all_events = sdl2.ext.get_events()
			for event in all_events:
				if event.type == sdl2.SDL_QUIT:
					return
				elif event.type == sdl2.SDL_KEYDOWN:
					#print 'KeyDown: key code ', SDL_GetKeyName(event.key.keysym.sym)
					key_code = event.key.keysym.sym
					if key_code == sdl2.SDLK_UP:
						self.ball_colour_idx += 1
						if self.ball_colour_idx >= len(self.BALL_COLOURS):
							self.ball_colour_idx = 0
					elif key_code == sdl2.SDLK_DOWN:
						self.ball_colour_idx -= 1
						if self.ball_colour_idx < len(self.BALL_COLOURS):
							self.ball_colour_idx = len(self.BALL_COLOURS)-1
					elif key_code == sdl2.SDLK_r:
						self.playerscore = 0 
						self.aiscore = 0
						self.PLAYERWIN = False
						self.AIWIN = False
					#elif key_code == sdl2.SDLK_q:			
						#self.paddle1_pos.y += dy			
						#self.paddle1_pos.y -= 25
					#elif key_code == sdl2.SDLK_a:
						#self.paddle1_pos.y += 25
					elif key_code == sdl2.SDLK_p:
						self.paddle2_pos.y -= 25
					elif key_code == sdl2.SDLK_l:
						self.paddle2_pos.y += 25
					elif key_code == sdl2.SDLK_ESCAPE:
						exit()
					elif key_code == sdl2.SDLK_SPACE:
						if self.playerscore != 5 and self.aiscore != 5:
							self.BALL_VELOCITY = 350
						else:
							pass
					
				elif event.type == sdl2.SDL_MOUSEMOTION:
					#print 'MouseMotion: ',event.motion.x, event.motion.y
					self.paddle2_pos.y = event.motion.y
				elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
					#print 'MouseDown: ', event.button.button, event.button.x, event.button.y	
					pass
				elif event.type == sdl2.SDL_MOUSEBUTTONUP:
					#print 'MouseUp: ', event.button.button, event.button.x, event.button.y
					pass
			self.draw(renderer,frame_time)
			last_frame = current_frame
		
#===========================================================================================================
sdl2.ext.init()

window = sdl2.ext.Window("CSC 205 A2", size=(A2Canvas.CANVAS_SIZE_X, A2Canvas.CANVAS_SIZE_Y))
window.show()

renderer = sdl2.SDL_CreateRenderer(window.window, -1,0)# sdl2.SDL_RENDERER_PRESENTVSYNC | sdl2.SDL_RENDERER_ACCELERATED);


sdl2.SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255)
sdl2.SDL_RenderClear(renderer)
sdl2.SDL_RenderPresent(renderer)
sdl2.SDL_ShowCursor(SDL_DISABLE);

canvas = A2Canvas()		
canvas.frame_loop(renderer)
		
sdl2.SDL_DestroyRenderer(renderer)
