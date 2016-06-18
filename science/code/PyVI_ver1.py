#!/usr/bin/env python

""" PyVI : Visual Inspection of Astronomical Data
	by Min-Su Shin (Princeton University) in 2008
	msshin at astro.princeton.edu
	by Min-Su Shin (University of Michigan) in 2009
	msshin at umich.edu
"""

import sys, os
import getopt
import string

import curses
from PIL import Image, ImageTk
import Tkinter


class image_db:
	"""
	Database class of images files
	"""
	def __init__(self, infn, outfn, dir_images):
		"""
		infn : list filename
		outfn : log filename
		dir_image : directory name of image files
		"""
		self.outfn = outfn
		self.dir_images = dir_images
		try:
			fd = open(infn, 'r')
		except:
			print "Error : opening the file failed."
		all_lines = fd.readlines()
		fd.close()
		one_line = all_lines[0]
		temp = string.split(one_line)
		self.num_cols = len(temp)
		self.num_rows = len(all_lines)
		self.data_list = []
		for one_line in all_lines:
			temp = string.split(one_line)
			self.data_list.append(temp)
		self.db_list = []
		for ind in range(0,self.num_rows):
			self.db_list.append('None')
	def __getitem__(self, index):
		return self.data_list[index]
	def update(self,index, val):
		self.db_list[index] = val
	def query(self,index):
		return self.db_list[index]
	def save(self):
		fd = open(self.outfn, 'w')
		for ind in range(0, self.num_rows):
			out_str = string.join(self.data_list[ind]) \
			+ " " + self.db_list[ind] + "\n"
			fd.write(out_str)
		fd.close()
	def close(self):
		fd = open(self.outfn, 'w')
		for ind in range(0, self.num_rows):
			out_str = string.join(self.data_list[ind]) \
			+ " " + self.db_list[ind] + "\n"
			fd.write(out_str)
		fd.close()

class curses_interface:
	"""
	Curses interface of image DB
	"""
	def __init__(self, db, title=None):
		"""
		db : image_db class
		title : title of image frame
		"""
		self.screen = curses.initscr()
		self.screen.keypad(1)
		curses.noecho()
		curses.cbreak()
		self.db = db
		self.screen.clear()
		self.screen.refresh()
		self.title = title
		self.screen.addstr(1, 0, "PyVI : Visual Inspection of Astronomical Data", \
		curses.A_BOLD)
		self.screen.hline(2, 0, '-', 45)
		self.screen.addstr(3, 0, 'This program was made by ' + \
		'Min-Su Shin (Princeton University) for astronomical data.')
		self.screen.addstr(5, 0, "The number of images is "+str(db.num_rows)\
		+" in the file "+title+".")
		self.screen.addstr(7, 0, "If you want to begin inspection, press s key.")
		self.screen.addstr(8, 0, "If you want to stop, press q key.")
		self.screen.addstr(10,0, ">>")
		self.screen.refresh()
		start_tag = 0
		end_tag = 0
		while 1:
			c = self.screen.getch()
			try :
				c = chr(c)
				if c == 's' :
					start_tag = 1
					break
				elif c == 'q' :
					end_tag = 1
					break
			except :
				temp = -1
		if end_tag == 1:
			self.close()
		elif start_tag == 1:
			return_val = self.run()
			self.close()
		else :
			self.close()
	def run(self):
		ind = 0
		run_tag = 1
		root = Tkinter.Tk()
		root.geometry('+%d+%d' % (50, 50))
		while run_tag > 0:
			self.screen.clear()
			data_line = self.db[ind]
			fn = self.db.dir_images + "/" + data_line[0]
			outstr = string.join(data_line, '\t')
			result = self.db.query(ind)
			outstr = outstr + "\t input = " + result
			try :
				img_arr = Image.open(fn)
			except :
				print "PIL can't read the file "+fn
				self.close()
			try :
				root.geometry('%dx%d' % (img_arr.size[0], img_arr.size[1]))
			except :
				print "Image window does not exist."
				self.close()
			pic = ImageTk.PhotoImage(img_arr)
			label_image = Tkinter.Label(root, image=pic)
			label_image.place(x=0,y=0,width=img_arr.size[0],\
			height=img_arr.size[1])
			root.title(data_line[0])
			root.update()
			self.screen.addstr(1, 0, str(ind+1)+" / "+str(self.db.num_rows), curses.A_BOLD)
			self.screen.addstr(2, 1, "p = prev., n = next, j = jump," \
			+ " l = log, w = write, q = quit")
			self.screen.hline(3, 0, '-', 45)
			self.screen.move(4, 0)
			self.screen.clrtoeol()
			self.screen.addstr(4, 0, "DB info : "+outstr)
			self.screen.addstr(6, 0, ">>")
			self.screen.refresh()
			while 1 :
				c = self.screen.getch()
				try :
					c = chr(c)
					if c == 'q' :
						run_tag = 0
						self.db.close()
						break
					elif c == 'w' :
						self.db.save()
						self.screen.addstr(8, 0, "WRITING DONE", curses.A_STANDOUT)
						self.screen.addstr(6, 0, ">>")
						self.screen.refresh()
					elif c == 'l':
						self.screen.move(7,0)
						self.screen.clrtoeol()
						self.screen.move(8,0)
						self.screen.clrtoeol()
						self.screen.addstr(7, 0, "LOG >>")
						self.screen.refresh()
						curses.echo()
						curses.nocbreak()
						input_str = self.screen.getstr()
						curses.noecho()
						curses.cbreak()
						if input_str != '\n' :
							self.db.update(ind, input_str)
							self.screen.addstr(8, 0, "LOG UPDATED", curses.A_STANDOUT)
							outstr = string.join(data_line, '\t')
							result = self.db.query(ind)
							self.screen.move(4, 0)
							self.screen.clrtoeol()
							outstr = outstr + "\t input = " + result
							self.screen.addstr(4, 0, "DB info : "+outstr)
							self.screen.move(7,0)
							self.screen.clrtoeol()
							self.screen.addstr(6, 0, ">>")
							self.screen.refresh()
						else :
							self.screen.move(7,0)
							self.screen.clrtoeol()
							self.screen.move(8,0)
							self.screen.clrtoeol()
							self.screen.addstr(8, 0, "LOG EMPTY", curses.A_STANDOUT)
							self.screen.addstr(6, 0, ">>")
							self.screen.refresh()
					elif c == 'j':
						self.screen.move(7,0)
						self.screen.clrtoeol()
						self.screen.move(8,0)
						self.screen.clrtoeol()
						self.screen.addstr(7, 0, "jump to ? >>")
						self.screen.refresh()
						curses.echo()
						curses.nocbreak()
						input_str = self.screen.getstr()
						curses.noecho()
						curses.cbreak()
						if input_str != '\n' :
							try :
								new_ind = int(input_str)
								if (new_ind <= self.db.num_rows) and (new_ind >= 1) :
									ind = new_ind - 1
									break
								else :
									break
									
							except :
								break
						else :
							self.screen.move(7,0)
							self.screen.clrtoeol()
							self.screen.move(8,0)
							self.screen.clrtoeol()
							self.screen.addstr(8, 0, "TYPE NUMBER", curses.A_STANDOUT)
							self.screen.addstr(6, 0, ">>")
							self.screen.refresh()
					elif c == 'n' :
						if ind != (self.db.num_rows-1) :
							ind += 1
							break
						else :
							self.screen.addstr(8, 0, "LAST OBJECT", curses.A_STANDOUT)
							self.screen.addstr(6, 0, ">>")
							self.screen.refresh()
					elif c == 'p' :
						if ind != 0 :
							ind -= 1
							break
						else :
							self.screen.addstr(8, 0, "FIRST OBJECT", curses.A_STANDOUT)
							self.screen.addstr(6, 0, ">>")
							self.screen.refresh()
				except :
					temp = -1
		return 0

	def close(self):
		self.db.close()
		self.screen.keypad(0)
		curses.echo()
		curses.nocbreak()
		curses.endwin()
		sys.exit()
		


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print """PyVI.py	[list filename] [log filename] -d [directory name of image files]
		Example) PyVI.py sel.list log.list -d ./Gallery
		-d : directory name is optional"""
		sys.exit()
	else :
		infn = sys.argv[1]
		outfn = sys.argv[2]
	dir_images = "./"
	try:
		opts, args = getopt.getopt(sys.argv[3:], "d:v", ["directory name="])
		for o, a in opts:
			if o == "-d":
				dir_images = a
	except:
		dir_images = "./"
	db = image_db(infn, outfn, dir_images)
	db_inf = curses_interface(db, infn)
