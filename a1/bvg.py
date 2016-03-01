# bvg.py
#
# A parser for the BVG format. It should not be necessary to modify or
# understand the contents of this file, besides the BVGRendererBase class
# (which you should subclass for your solution).
#
# B. Bird - 01/02/2016

import sys
from point import Point, Vector2d


class BVGRendererBase:
	def create_canvas(self, dimensions, background_colour, scale_factor):
		raise NotImplementedError()
	
	def render_line(self, endpoint1, endpoint2, colour, thickness):
		raise NotImplementedError()
		
	def render_circle(self, center, radius, line_colour, line_thickness):
		raise NotImplementedError()
		
	def render_filledcircle(self, center, radius, line_colour, line_thickness, fill_colour):
		raise NotImplementedError()
	
	def render_triangle(self, point1, point2, point3, line_colour, line_thickness, fill_colour):
		raise NotImplementedError()
	
	def render_gradient_triangle(self, point1, point2, point3, line_colour, line_thickness, colour1, colour2, colour3):
		raise NotImplementedError()
		
class ParsingException:
	def __init__(self,line,line_number,message, position=-1):
		self.line = line
		self.line_number = line_number
		self.message = message
		self.position = position
		
def print_error(s):
	print >>sys.stderr,s
	
def tuple_to_vector2d(t):
	return Vector2d(t[0],t[1])
		
class BVGReader:
	def __init__(self, renderer):
		self.renderer = renderer
	def parse_file(self, file):
		try: 
			self._parse(file)
		except ParsingException, e:
			print_error("Error on line %d: %s"%(e.line_number,e.message))
			if e.position >= 0:
				print_error("\t%s"%e.line.rstrip())
				print_error("\t%s^"%(' '*e.position))
				return False
		return True
			#sys.exit(0)
			
	def _parse(self,f):
		shape_handlers = {
							'Canvas':self.parse_Canvas,
							'Line':self.parse_Line,
							'Circle':self.parse_Circle,
							'FilledCircle':self.parse_FilledCircle,
							'Triangle': self.parse_Triangle,
							'GradientTriangle':self.parse_GradientTriangle,
						 }
		self.line_number = 0
		for line in f:
			self.line = line
			self.line_number += 1
			if line.strip() == '':
				continue
			shape_type = line.split()[0]
			if shape_type not in shape_handlers:
				raise ParsingException(self.line, self.line_number, "Invalid shape type \"%s\""%shape_type, 0)
			shape_handlers[shape_type](line)
			
			
	def parse_int_tuple(self,line,start_pos, expected_length):
		while start_pos < len(line) and line[start_pos].isspace():
			start_pos += 1
		if start_pos >= len(line) or line[start_pos] != '(':
			raise ParsingException(self.line, self.line_number, "Expected '('", start_pos)
		values = []
		pos = start_pos+1
		v = ''
		while pos < len(line):
			c = line[pos]
			if c.strip() == '':
				pos += 1
				continue
			if c == ')':
				if len(v) > 0:
					values.append(int(v))
					v = ''
				break
			if c == ',':
				if len(values) == expected_length:
					raise ParsingException(self.line, self.line_number, "Too many values",pos)
				values.append(int(v))
				v = ''
				pos += 1
				continue
			if c not in '0123456789':
				raise ParsingException(self.line,self.line_number, "Invalid character",pos)
			v += c
			pos += 1
		if pos >= len(line) or line[pos] != ')':
			raise ParsingException(self.line, self.line_number, "Expected ')'", pos)
		if len(values) < expected_length:
			raise ParsingException(self.line, self.line_number, "Expected %d more values"%(expected_length-len(values)), pos)
		return (pos+1,tuple(values))
		
	
	def parse_fixed_tuple_func(self, tuple_size):
		return lambda line,start_pos: self.parse_int_tuple(line,start_pos,tuple_size)
		
	def parse_single_int(self,line,start_pos):
		while start_pos < len(line) and line[start_pos].isspace():
			start_pos += 1
		if start_pos >= len(line):
			return None
		pos = start_pos
		value = ''
		while pos < len(line) and line[pos].isdigit():
			value += line[pos]
			pos += 1		
		return (pos+1,int(value))
		
	def parse_key_name(self,line,start_pos):
		while start_pos < len(line) and line[start_pos].isspace():
			start_pos += 1
		if start_pos >= len(line):
			return None
		pos = start_pos
		name = ''
		while pos < len(line) and (line[pos].isalpha() or line[pos].isdigit() or line[pos] == '_'):
			name += line[pos]
			pos += 1
		while pos < len(line) and line[pos].isspace():
			pos += 1
			
		if pos >= len(line) or line[pos] != '=':
			raise ParsingException(self.line, self.line_number, "Expected '='", pos)			
		return (pos+1,name)
		
		
	def parse_general(self,line,command,keys):
		first_space_pos = 0
		while first_space_pos < len(line) and line[first_space_pos].isspace():
			first_space_pos += 1
		assert first_space_pos < len(line)
		while first_space_pos < len(line) and not line[first_space_pos].isspace():
			first_space_pos += 1
		
		pos = first_space_pos
		parsed_keys = {}
		while 1:
			while pos < len(line) and line[pos].isspace():
				pos += 1
			Q = self.parse_key_name(line,pos)
			if Q is None:
				break
			next_pos,key_name = Q
			if key_name not in keys:
				raise ParsingException(self.line, self.line_number, "Invalid attribute \"%s\""%key_name, pos)
			if key_name in parsed_keys:
				raise ParsingException(self.line, self.line_number, "Duplicate attribute \"%s\""%key_name, pos)
			next_pos, value = keys[key_name][0](line,next_pos)
			parsed_keys[key_name] = value
			pos = next_pos
			
		for k in keys:
			if k not in parsed_keys:
				if keys[k][1] is None:
					raise ParsingException(self.line, self.line_number, "Missing attribute \"%s\""%k, pos)
				parsed_keys[k] = keys[k][1]
		return parsed_keys
		
	def parse_Canvas(self,line):
		keys = {
					'dimensions': (self.parse_fixed_tuple_func(2), None),
					'background_colour': (self.parse_fixed_tuple_func(2), None),
					'scale_factor': (self.parse_single_int, 1),
			   }
		parsed_keys = self.parse_general(line,'Canvas',keys)
		self.renderer.create_canvas(
				parsed_keys['dimensions'],
				parsed_keys['background_colour'],
				parsed_keys['scale_factor'])
	def parse_Line(self,line):
		keys = {
					'from': (self.parse_fixed_tuple_func(2), None),
					'to': (self.parse_fixed_tuple_func(2), None),
					'colour': (self.parse_fixed_tuple_func(3), None),
					'thickness': (self.parse_single_int, 1),
			   }
		parsed_keys = self.parse_general(line,'Line',keys)
		self.renderer.render_line(
				tuple_to_vector2d(parsed_keys['from']),
				tuple_to_vector2d(parsed_keys['to']),
				parsed_keys['colour'],
				parsed_keys['thickness'])
	def parse_Circle(self,line):
		keys = {
					'center': (self.parse_fixed_tuple_func(2), None),
					'radius': (self.parse_single_int, None),
					'line_colour': (self.parse_fixed_tuple_func(3), None),
					'line_thickness': (self.parse_single_int, 1),
			   }
		parsed_keys = self.parse_general(line,'Line',keys)
		self.renderer.render_circle(
				tuple_to_vector2d(parsed_keys['center']),
				parsed_keys['radius'],
				parsed_keys['line_colour'],
				parsed_keys['line_thickness'])
	def parse_FilledCircle(self,line):
		keys = {
					'center': (self.parse_fixed_tuple_func(2), None),
					'radius': (self.parse_single_int, None),
					'line_colour': (self.parse_fixed_tuple_func(3), None),
					'line_thickness': (self.parse_single_int, 1),
					'fill_colour': (self.parse_fixed_tuple_func(3), None),
			   }
		parsed_keys = self.parse_general(line,'Line',keys)
		self.renderer.render_filledcircle(
				tuple_to_vector2d(parsed_keys['center']),
				parsed_keys['radius'],
				parsed_keys['line_colour'],
				parsed_keys['line_thickness'],
				parsed_keys['fill_colour'])
	def parse_Triangle(self,line):
		keys = {
					'point1': (self.parse_fixed_tuple_func(2), None),
					'point2': (self.parse_fixed_tuple_func(2), None),
					'point3': (self.parse_fixed_tuple_func(2), None),
					'line_colour': (self.parse_fixed_tuple_func(3), None),
					'line_thickness': (self.parse_single_int, 1),
					'fill_colour': (self.parse_fixed_tuple_func(3), None),
			   }
		parsed_keys = self.parse_general(line,'Line',keys)
		self.renderer.render_triangle(
				tuple_to_vector2d(parsed_keys['point1']),
				tuple_to_vector2d(parsed_keys['point2']),
				tuple_to_vector2d(parsed_keys['point3']),
				parsed_keys['line_colour'],
				parsed_keys['line_thickness'],
				parsed_keys['fill_colour'])
	def parse_GradientTriangle(self,line):
		keys = {
					'point1': (self.parse_fixed_tuple_func(2), None),
					'point2': (self.parse_fixed_tuple_func(2), None),
					'point3': (self.parse_fixed_tuple_func(2), None),
					'line_colour': (self.parse_fixed_tuple_func(3), None),
					'line_thickness': (self.parse_single_int, 1),
					'colour1': (self.parse_fixed_tuple_func(3), (255, 0, 0) ),
					'colour2': (self.parse_fixed_tuple_func(3), (0, 255, 0) ),
					'colour3': (self.parse_fixed_tuple_func(3), (0, 0, 255) ),
			   }
		parsed_keys = self.parse_general(line,'Line',keys)
		self.renderer.render_gradient_triangle(
				tuple_to_vector2d(parsed_keys['point1']),
				tuple_to_vector2d(parsed_keys['point2']),
				tuple_to_vector2d(parsed_keys['point3']),
				parsed_keys['line_colour'],
				parsed_keys['line_thickness'],
				parsed_keys['colour1'],
				parsed_keys['colour2'],
				parsed_keys['colour3'],
				)
		
		
if __name__ == '__main__':
	print_error("Don't run bvg.py directly")