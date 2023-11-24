#!/usr/bin/env python

""" 
Ver 3.0
PyVI : Visual Inspection of Astronomical Data
	by Min-Su Shin (University of Michigan)
	msshin at umich.edu
 * supports DS9 and Aladin with Virtual Observatory SAMP.

Ver 2.5
PyVI : Visual Inspection of Astronomical Data
	by Min-Su Shin (University of Michigan)
	msshin at umich.edu
 * supports FITS files by using the DS9 viewer.

Ver 2.0
PyVI : Visual Inspection of Astronomical Data
	by Min-Su Shin (University of Michigan)
	msshin at umich.edu
 * shows the text file corresponding to each item in the list 
   if text files exist and the file names are given in the list.

Ver 1.0
PyVI : Visual Inspection of Astronomical Data
	by Min-Su Shin (Princeton University)
	msshin at astro.princeton.edu
 * shows the graphic file corresponding to each item in the list.
 * requires the Python Image Library (PIL).
"""

import sys, os
import getopt
import string

import curses
import Tkinter

use_fits = 0 # default : no FITS files


class image_db:
	"""
	Database class of images files
	"""
	def __init__(self, infn, outfn, dir_images, dir_texts):
		"""
		infn : list filename
		outfn : log filename
		dir_images : the directory name of image files
		dir_texts : the directory name of text files
		"""
		self.outfn = outfn
		self.dir_images = dir_images
		self.dir_texts = dir_texts
		try:
			fd = open(infn, 'r')
		except:
			print "Error : opening the file failed."
		all_lines = fd.readlines()
		fd.close()
#		one_line = all_lines[0]
#		temp = string.split(one_line)
#		self.num_cols = len(temp)
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
#			out_str = string.join(self.data_list[ind]) \
#			+ " " + self.db_list[ind] + "\n"
			out_str = self.db_list[ind] + "\n"
			fd.write(out_str)
		fd.close()
	def close(self):
		fd = open(self.outfn, 'w')
		for ind in range(0, self.num_rows):
#			out_str = string.join(self.data_list[ind]) \
#			+ " " + self.db_list[ind] + "\n"
			out_str = self.db_list[ind] + "\n"
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
		'Min-Su Shin.')
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
		if use_fits > 0:
			# SAMP
			self.use_hub = sampy.SAMPHubServer()
			self.use_hub.start()
			PyVI_metadata = { 'samp.name': 'PyVI' }
			self.use_client = sampy.SAMPIntegratedClient(metadata = PyVI_metadata)
			self.use_client.connect()
			if use_fits == 3:
				self.screen.addstr(11,0, "Please, start DS9 and Aladin, check their connections to SAMP, and then type any key.")
			if use_fits == 2:
				self.screen.addstr(11,0, "Please, start Aladin, check its connection to SAMP, and then type any key.")
			if use_fits == 1:
				self.screen.addstr(11,0, "Please, start DS9, check its connection to SAMP, and then type any key.")
			self.screen.refresh()
			while 1:
				c = self.screen.getch()
				break
		while run_tag > 0:
			self.screen.clear()
			data_line = self.db[ind]
			fn = self.db.dir_images + "/" + data_line[0]
			if len(data_line) > 1 :
				txt_fn = self.db.dir_texts + "/" + data_line[1]
			else :
				txt_fn = None
			outstr = string.join(data_line, ' ')
			result = self.db.query(ind)
			outstr = outstr + " input = " + result
			# show the text messages
			if txt_fn :
				try:
					infd = open(txt_fn, 'r')
					all_txts = infd.readlines()
					infd.close()
					max_length=0
					max_height=0
					for one_txt in all_txts:
						if len(one_txt) > max_length:
							max_length = len(one_txt)
						max_height = max_height + 1
					all_txts = string.join(all_txts)
				except:
#					print "The text file %s doesn't exist." % (txt_fn)
					all_txts="The text file %s doesn't exist." % (txt_fn)
					max_height = 1
					max_length = len(all_txts)
			# show the image
			if use_fits < 1:
				try :
					img_arr = Image.open(fn)
				except :
					print "PIL can't read the file "+fn
					self.close()
				pic = ImageTk.PhotoImage(img_arr)
				try:
					label_image.grid_forget()
				except:
					temp_dummy = 0
				if txt_fn:
					label_image = Tkinter.Label(root, compound="top", image=pic, text=all_txts, padx=0, pady=0)
				else:
					label_image = Tkinter.Label(root, compound="top", image=pic, padx=0, pady=0)
				label_image.grid()
				root.title(data_line[0])
				root.update()
			else:
				if txt_fn:
					try:
						label_image.grid_forget()
					except:
						temp_dummy = 0
					label_image = Tkinter.Label(root, text=all_txts, padx=0, pady=0)
					label_image.grid()
					root.title(data_line[0])
					root.update()
				if (use_fits == 1) or (use_fits == 3): # DS9 is on.
					ds9_cmd = "file "+fn # NOTE: modify this command depending on your preferences.
					self.use_client.callAll("ds9_data", {"samp.mtype": "ds9.set", "samp.params": {"cmd": ds9_cmd}})
				if (use_fits == 2) or (use_fits == 3): # Aladin is on.
					aladin_cmd = "reset; load "+fn # NOTE: modify this command depending on your preferences.
					self.use_client.callAll("aladin_data", {"samp.mtype": "script.aladin.send", "samp.params": {"script": aladin_cmd}})
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
		# SAMP
		try:
			if (use_fits == 1) or (use_fits == 3): # DS9 is on.
				ds9_cmd = "exit"
				self.use_client.callAll("ds9_data", {"samp.mtype": "ds9.set", "samp.params": {"cmd": ds9_cmd}})
			if (use_fits == 2) or (use_fits == 3): # Aladin is on.
				aladin_cmd = "quit"
				self.use_client.callAll("aladin_data", {"samp.mtype": "script.aladin.send", "samp.params": {"script": aladin_cmd}})
			if use_fits > 0:
				self.use_client.disconnect()
				self.use_hub.stop()
		except:
			pass
		sys.exit()
		


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print """PyVI.py [list filename] [log filename] --ds9 --aladin --image_dir [the directory name of image files] --text_dir [the directory name of text files]
		Example) PyVI.py sel.list log.list --ds9 --image_dir ./Gallery --text_dir ./Extra_text
		--ds9 : PyVI will use the DS9 as an image viewer which supports FITS files. You must check the DS9 first whether it is available with the SAMP.
		--aladin : PyVI will use the Aladin as an image viewer which supports FITS and other file formats such as JPEG and PNG. You must check the Aladin first whether it is available with the SAMP. If both --ds9 and --aladin options are selected, both viewers are used in the PyVI.
		--image_dir and --text_dir : the directory names are optional
		if the directory names are not given, the current working directory is a default directory."""
		sys.exit()
	else :
		infn = sys.argv[1]
		outfn = sys.argv[2]
	dir_images = "./"
	dir_texts = "./"
	try:
		opts, args = getopt.getopt(sys.argv[3:], "", ["ds9", "aladin", "image_dir=", "text_dir="])
		for o, a in opts:
			if o == "--image_dir":
				dir_images = a
			if o == "--text_dir":
				dir_texts = a
			if o == "--ds9":
				use_fits = use_fits + 1 # use FITS files
			if o == "--aladin":
				use_fits = use_fits + 2 # use FITS files
	except:
		print "# the directory names = %s %s\n" % (dir_images, dir_texts)
	db = image_db(infn, outfn, dir_images, dir_texts)
	if use_fits < 1:
		from PIL import Image, ImageTk
	else :
		import sampy
	db_inf = curses_interface(db, infn)
