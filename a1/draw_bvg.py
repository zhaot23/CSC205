# draw_bvg.py
#
# Starter code for CSC 205 Assignment 1 (Python)
#
# B. Bird - 01/02/2016

import sys
import bvg
from point import Vector2d
import png


class PNGCanvas:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		#Store each pixel as a sequence of 3 bytes (r, g, b) in a flat array
		#(This is to cater to the odd input format of the PNG encoder)
		self.pixels = [0]*width*height*3
		
	#Return a pixel value as an (R,G,B) tuple
	def get_pixel(self,x,y):
		base_index = 3*(x + y*self.width)
		return (self.pixels[base_index],self.pixels[base_index+1],self.pixels[base_index+2])
		
	#Set a pixel value to a given (R,G,B) tuple
	def set_pixel(self,x,y,colour):
		base_index = 3*(x + y*self.width)
		self.pixels[base_index] = colour[0]
		self.pixels[base_index+1] = colour[1]
		self.pixels[base_index+2] = colour[2]
		
	#Convenience operators to allow use of square brackets instead of get_pixel
	#and set_pixel
	
	def __getitem__(self,key):
		return self.get_pixel(key[0],key[1])
	def __setitem__(self,key,colour):
		self.set_pixel(key[0],key[1],colour)
		
	def save_image(self,filename):
		f = open(filename, 'wb')
		pngwriter = png.Writer(self.width, self.height,compression=9)
		pngwriter.write_array(f, self.pixels)
		f.close()

		
		

		
class BVGRenderer(bvg.BVGRendererBase):
	def create_canvas(self, dimensions, background_colour, scale_factor):
		width,height = dimensions
		self.width = width
		self.height = height
		self.canvas = PNGCanvas(width, height)
		for x in xrange(width):
			for y in xrange(height):
				self.canvas[x,y] = background_colour



				
# using Bresenham's line algorithm				
	def render_line(self, endpoint1, endpoint2, colour, thickness):
		steep = 0
		x1,y1 = endpoint1
		x2,y2 = endpoint2
# difference between starting and ending points
		dx = abs(x2 - x1)
		dy = abs(y2 - y1)
# calculate direction of the vector		
		if (x2 - x1) > 0: 
			sx = 1
		else: 
			sx = -1
		
		if (y2 - y1) > 0: 
			sy= 1
		else: 
			sy = -1	
# dy is the major axis
		if dy > dx:
			steep = 1
			x1,y1 = y1,x1
			dx,dy = dy,dx
			sx,sy = sy,sx			
# dx is the major axis
		d = (2 * dy) - dx
		for i in range(0, dx):
			if steep:
				if y1 < self.width and x1 < self.height and x1>=0 and y1>=0:
					self.canvas[y1,x1] = colour
			else: 
				if x1 < self.width and y1 < self.height and x1>=0 and y1>=0:
					self.canvas[x1,y1] = colour
			while d >= 0:
				y1 = y1 + sy
				d = d - (2 * dx)
			x1 = x1 + sx
			d = d + (2 * dy)
		if x2 < self.width and y2 < self.height and x2>=0 and y2>=0:	
			self.canvas[x2,y2] = colour

		
	def render_circle(self, center, radius, line_colour, line_thickness):
		x0,y0 = center
		x = 0
		y = radius
		p = 1-radius
				
		while x <= y:
			if x0+x < self.width and y0+y < self.height and x0+x>=0 and y0+y>=0:
				self.canvas[x0+x,y0+y] = line_colour
			if x0+x < self.width and y0-y < self.height and x0+x>=0 and y0-y>=0:
				self.canvas[x0+x,y0-y] = line_colour
			if x0+y < self.width and y0+x < self.height and x0+y>=0 and y0+x>=0:
				self.canvas[x0+y,y0+x] = line_colour
			if x0+y < self.width and y0-x < self.height and x0+y>=0 and y0-x>=0:
				self.canvas[x0+y,y0-x] = line_colour
			if x0-x < self.width and y0+y < self.height and x0-x>=0 and y0+y>=0:
				self.canvas[x0-x,y0+y] = line_colour
			if x0-x < self.width and y0-y < self.height and x0-x>=0 and y0-y>=0:
				self.canvas[x0-x,y0-y] = line_colour
			if x0-y < self.width and y0+x < self.height and x0-y>=0 and y0+x>=0:
				self.canvas[x0-y,y0+x] = line_colour
			if x0-y < self.width and y0-x < self.height and x0-y>=0 and y0-x>=0:
				self.canvas[x0-y,y0-x] = line_colour

			x = x + 1
			if p <= 0:
				p = p + (2 * x + 1)
			else:
				y = y - 1
				p = p + (2 * (x - y) + 1)

		
	def render_filledcircle(self, center, radius, line_colour, line_thickness, fill_colour):
		x0,y0 = center
		x = 0
		y = radius
		p = 1 - radius
				
		while x <= y:
			self.render_line((x0+y,y0+x),(x0-y,y0+x),fill_colour,line_thickness)
			self.render_line((x0-y,y0-x),(x0+y,y0-x),fill_colour,line_thickness)
			self.render_line((x0-x,y0-y),(x0+x,y0-y),fill_colour,line_thickness)
			self.render_line((x0+x,y0+y),(x0-x,y0+y),fill_colour,line_thickness)
			x = x + 1

			
			if p <= 0:
				p = p + (2 * x + 1)
			else:
				y = y - 1
				p = p + (2 * (x - y) + 1)
		
		self.render_circle(center, radius, line_colour, line_thickness)
			
	
	def render_triangle(self, point1, point2, point3, line_colour, line_thickness, fill_colour):
		x1,y1 = point1
		x2,y2 = point2
		x3,y3 = point3
		#get the bounding box of the triangle
		maxX = max(point1.x, point2.x, point3.x) 
		minX = min(point1.x, point2.x, point3.x) 
		maxY = max(point1.y, point2.y, point3.y)
		minY = min(point1.y, point2.y, point3.y)
		
		#panning vectors of edge (v1,v2) and (v1,v3)
		v1 = Vector2d(point2.x - point1.x, point2.y - point1.y)
		v2 = Vector2d(point3.x - point1.x, point3.y - point1.y)
		
		#iterate over each pixel of bounding box and check if it's inside
		for x in range (minX, maxX+1):		
			for y in range (minY, maxY+1):		  
				q = Vector2d(x - x1, y - y1)

				s = (float(q.x * v2.y - q.y * v2.x)) / (v1.x * v2.y - v1.y * v2.x)
				t = (float(v1.x * q.y - v1.y * q.x)) / (v1.x * v2.y - v1.y * v2.x)

				if ( (s >= 0) and (t >= 0) and (s + t <= 1)):
					self.canvas[x,y] = fill_colour
				
		self.render_line(point1, point2, line_colour, line_thickness)
		self.render_line(point2, point3, line_colour, line_thickness)
		self.render_line(point3, point1, line_colour, line_thickness)
	
	def render_gradient_triangle(self, point1, point2, point3, line_colour, line_thickness, colour1, colour2, colour3):
		x1,y1 = point1
		x2,y2 = point2
		x3,y3 = point3
		#get the bounding box of the triangle
		maxX = max(point1.x, point2.x, point3.x) 
		minX = min(point1.x, point2.x, point3.x) 
		maxY = max(point1.y, point2.y, point3.y)
		minY = min(point1.y, point2.y, point3.y)
		
		#panning vectors of edge (v1,v2) and (v1,v3)
		v1 = Vector2d(point2.x - point1.x, point2.y - point1.y)
		v2 = Vector2d(point3.x - point1.x, point3.y - point1.y)	
		
		deltaRed12 = colour2[0] - colour1[0]
		deltaGreen12 = colour2[1] - colour1[1]
		deltaBlue12 = colour2[2] - colour1[2]
		deltaRed13 = colour3[0] - colour1[0]
		deltaGreen13 = colour3[1] - colour1[1]
		deltaBlue13 = colour3[2] - colour1[2]	
		
		#iterate over each pixel of bounding box and check if it's inside
		for x in range (minX, maxX+1):		
			for y in range (minY, maxY+1):		  
				q = Vector2d(x - x1, y - y1)

				s = (float(q.x * v2.y - q.y * v2.x)) / (v1.x * v2.y - v1.y * v2.x)
				t = (float(v1.x * q.y - v1.y * q.x)) / (v1.x * v2.y - v1.y * v2.x)

				if ( (s > 0) and (t > 0) and (s + t <= 1)):
					resRed = colour1[0] + int(s * deltaRed12) + int(t * deltaRed13)
					resGreen = colour1[1] + int(s * deltaGreen12) + int(t * deltaGreen13)
					resBlue = colour1[2] + int(s * deltaBlue12) + int(t * deltaBlue13)
					newcolour = [resRed,resGreen,resBlue]
					self.canvas[x,y] = newcolour
		
		
		self.render_line(point1, point2, line_colour, line_thickness)
		self.render_line(point2, point3, line_colour, line_thickness)
		self.render_line(point3, point1, line_colour, line_thickness)
		
	def save_image(self,filename):
		self.canvas.save_image(filename)

		
if len(sys.argv) < 3:
	print >>sys.stderr,'Usage: %s <input filename> <output filename>'%(sys.argv[0])
	sys.exit(0)
	
input_filename = sys.argv[1]
output_filename = sys.argv[2]

renderer = BVGRenderer()
reader = bvg.BVGReader(renderer)
with open(input_filename) as input_file:
	if reader.parse_file(input_file):
		print >>sys.stderr,"File parsed successfully"
		renderer.save_image(output_filename)
