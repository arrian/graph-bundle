import svgfig
from svgfig import *
import csv
from collections import defaultdict
from collections import Counter
import random


# s = SVG("rect", x=10, y=10, width=60, height=60)
# print s.xml();

# g = SVG("g", s)
# g.save("c:/Dev/python-line-graph/test.svg")



class Graph:

	width = 1920
	height = 1080
	colgap = 50

	def __init__(self, *columns):
		self.columns = columns
		self.values = set()
		self.max_value = 0

		for column in columns:
			for value in column:
				self.values.add(value)
			for value in Counter(column).items():
				if value[1] > self.max_value:
					self.max_value = value[1]
		print(self.values)
		self.values = list(self.values) # converting set to list for ordered operations
		print('max: ' + str(self.max_value))

		self.groupcount = len(self.values)
		self.colcount = len(self.columns)
		self.rowcount = self.max_value * self.groupcount

		print('groups: ' + str(self.groupcount) + ' columns: ' + str(self.colcount) + ' rows: ' + str(self.rowcount))

		self.draw()

	def draw(self):

		# Create progress counter for each group and column
		global_group_progress = dict()
		for value in self.values:
			global_group_progress[value] = [0] * self.colcount
		
		# Backgrounds
		group_backgrounds = list()
		start = 0
		for x in self.values:
			group_backgrounds.append(SVG('rect', x = 0, y = start, width = self.width, height = self.height / self.groupcount, fill = 'grey'))
			start += self.height / self.groupcount

		background = SVG('g', *group_backgrounds)
		

		# Grouped lines by initial value
		group_groups = list()
		group_num = 0
		for value in self.values:
			#print(self.columns[0])
			indices = [i for i, x in enumerate(self.columns[0]) if x == value]
			print(indices)

			# CAUTION for large number of groups... need more colours
			colour = ['green', 'blue', 'yellow', 'red', 'orange', 'purple'][group_num] # random.choice(['blue', 'green', 'yellow', 'red', 'orange', 'purple'])

			for i in indices:
				print(i)
				for col in range(0, self.colcount):
					current_value = self.columns[col][i]
					print(current_value)
					current_group_index = self.values.index(self.columns[col][i])
					current_group_progress = global_group_progress[current_value][col]
					col_width = (self.width / self.colcount)
					group_height = (self.height / self.groupcount)
					value_height = (group_height / (self.rowcount / self.groupcount))
					group_groups.append(SVG('rect', x = col * col_width, y = current_group_index * group_height + current_group_progress * value_height, width = col_width - self.colgap * (self.colcount - 1), height = value_height, fill = colour))
					global_group_progress[value][col] += 1
			group_num += 1
			#for r in range(0, self.)

		lines = SVG('g', *group_groups)

		svgfig._canvas_defaults['width'] = str(self.width) + 'px'
		svgfig._canvas_defaults['height'] = str(self.height) + 'px'
		svgfig._canvas_defaults['viewBox'] = '0 0 ' + str(self.width) + ' ' + str(self.height)

		image = SVG('g', background, lines)
		image.save("c:/Dev/python-line-graph/test.svg")


columns = defaultdict(list)

with open('survey-data-short.csv', 'rU') as f:
	reader = csv.DictReader(f)
	for row in reader:
		for (k,v) in row.items():
			columns[k].append(v)

#print(columns['aesthetic enjoyment beginning'])

Graph(columns['aesthetic enjoyment beginning'], columns['aesthetic enjoyment middle'], columns['aesthetic enjoyment end'])
#Graph(columns['didactic enjoyment beginning'], columns['didactic enjoyment middle'], columns['didactic enjoyment end'])
