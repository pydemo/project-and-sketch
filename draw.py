#!/usr/bin/env python

import wx

#----------------------------------------------------------------------

class TestPanel(wx.Window):
	def __init__(self, parent):
		
		wx.Panel.__init__(self, parent, -1, size=(400,400))
		self.Bind(wx.EVT_PAINT, self.OnPaint)

		txt = """\
If this build of wxPython includes the new wx.GCDC class (which
provides the wx.DC API on top of the new wx.GraphicsContext class)
then these squares should be transparent.
"""
		wx.StaticText(self, -1, txt, (20, 20))
	def on_paint2(self, event=None):
		# create paint surface
		dc = wx.PaintDC(self)
		dc.Clear()
		#dc.SetBackgroundMode(wx.TRANSPARENT)
		# get image width and height
		iw = self.bmp1.GetWidth()
		ih = self.bmp1.GetHeight()
		# tile/wallpaper the image across the canvas
		for x in range(0, self.fw, iw):
			for y in range(0, self.fh, ih):
				dc.DrawBitmap(self.bmp1, x, y, True)

	def OnPaint(self, evt):
		pdc = wx.PaintDC(self)
		try:
			dc = wx.GCDC(pdc)
		except:
			raise Exception ("""This build of wxPython does not include new wx.GCDC class (which
provides the wx.DC API on top of the new wx.GraphicsContext class).""") 
		
		self.Width, self.Height = self.GetClientSize()
		
		
		if 1:
			filepath = 'test.JPG'
			img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

			img = img.Scale(self.Width, self.Height)
			
	  
			
			
			#dc = wx.PaintDC(self)
			self._Buffer = wx.BitmapFromImage(img)
			dc.DrawBitmap(self._Buffer,0,0)
			#self.Draw(dc)
		#dc.SetPen(wx.Pen(wx.Colour(255,255,255, wx.ALPHA_OPAQUE)))
		dc.SetBrush(wx.Brush(wx.Colour(255,255,255, 128)))
		dc.DrawCircle(50, 275, 25)
		if 0:
			rect = wx.Rect(0,0, 100, 100)
			for RGB, pos in [((178,  34,  34), ( 50,  90)),
							 (( 35, 142,  35), (110, 150)),
							 ((  0,   0, 139), (170,  90))
							 ]:
				r, g, b = RGB
				penclr   = wx.Colour(r, g, b, wx.ALPHA_OPAQUE)
				brushclr = wx.Colour(r, g, b, 128)   # half transparent
				dc.SetPen(wx.Pen(penclr))
				dc.SetBrush(wx.Brush(brushclr))
				rect.SetPosition(pos)
				dc.DrawRoundedRectangle(rect, 8)


			# some additional testing stuff
			dc.SetPen(wx.Pen(wx.Colour(0,0,255, 196)))
			dc.SetBrush(wx.Brush(wx.Colour(0,0,255, 64)))
			dc.DrawCircle(50, 275, 25)
			dc.DrawEllipse(100, 275, 75, 50)
			

	def Draw(self, dc):
		## just here as a place holder.
		## This method should be over-ridden when sub-classed
		pass

########################################################################
class ViewerFrame(wx.Frame):
	""""""

	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title="Image Viewer")
		self.panel=panel = TestPanel(self)
		
		
		
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		
		self.sizer.Add(panel, 1, wx.EXPAND)
		self.SetSizer(self.sizer)
		
		self.Show()
		self.sizer.Fit(self)
		self.Center()
		
#----------------------------------------------------------------------
if __name__ == "__main__":
	app = wx.App()
	frame = ViewerFrame()
	app.MainLoop()

