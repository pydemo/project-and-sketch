# -*- coding: utf-8 -*-
#py.bat 3iv.py 10 C:\Users\alex_\OneDrive\Pictures\Sony7rM4\55mm\protest\1-20-2019\insta_base jpg

import glob
import os, sys, math
import wx
import cv2
import numpy as np
from pubsub import pub 
from pprint import pprint as pp
import cv2
from six import unichr
from include.utils import TransparentText, keyMap
from ui.iv.view.ViewerPanel import ViewerPanel
e=sys.exit



import wx.lib.buttons

import speedmeter.SpeedMeter as SM
from math import pi, sqrt



if 0:
	dr=r'C:\Users\alex_\OneDrive\Pictures\Sony7rM4\55mm\protest\1-20-2019\insta_base'
	dr=r'C:\Users\alex_\OneDrive\Documents\Gallery\1'
		
		
pp(sys.argv)
interval_sec = int(sys.argv[1])
img_dir = sys.argv[2]
assert os.path.isdir(img_dir)

ext = sys.argv[3]


try:
	import cStringIO
except ImportError:
	import io as cStringIO





class ViewerFrame(wx.Frame):
	""""""

	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title="Image Viewer")
		self.panel=panel = ViewerPanel(self)
		self.folderPath = ""
		pub.subscribe(self.resizeFrame, ("resize"))
		
		#self.initToolbar()
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		
		self.sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		
		self.Show()
		self.sizer.Fit(self)
		self.Center()
		#self.Maximize(True)
		#self.ShowFullScreen(True)
	   
		
	#----------------------------------------------------------------------
	def initToolbar(self):
		"""
		Initialize the toolbar
		"""
		self.toolbar = self.CreateToolBar()
		self.toolbar.SetToolBitmapSize((16,16))
		
		open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
		openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
		self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
		
		self.toolbar.Realize()
		
	#----------------------------------------------------------------------
	def onOpenDirectory(self, event):
		"""
		Opens a DirDialog to allow the user to open a folder with pictures
		"""
		dlg = wx.DirDialog(self, "Choose a directory",
						   style=wx.DD_DEFAULT_STYLE)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.folderPath = dlg.GetPath()
			print (self.folderPath)
			picPaths = glob.glob(self.folderPath + "\\*.JPG")
			pp (picPaths)
		#pub.sendMessage("update images", msg=picPaths)
		#self.panel.updateImages(msg=picPaths)
		
	#----------------------------------------------------------------------
	def resizeFrame(self, msg):
		""""""
		self.sizer.Fit(self)
		
#----------------------------------------------------------------------
if __name__ == "__main__":
	app = wx.App()
	frame = ViewerFrame()
	app.MainLoop()
	