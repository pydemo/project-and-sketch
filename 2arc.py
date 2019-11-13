import wx
from math import cos, sin, pi

class Example(wx.Frame):

	def __init__(self, *args, **kw):
		super(Example, self).__init__(*args, **kw)

		self.InitUI()

	def InitUI(self):

		self.Bind(wx.EVT_PAINT, self.OnPaint)

		self.SetTitle("Shapes")
		self.Centre()

	def CircleCoords(self, radius, angle, centerX, centerY):
		"""
		Converts the input values into logical x, y coordinates.
		:param `radius`: the :class:`SpeedMeter` radius;
		:param `angle`: the angular position of the mouse;
		:param `centerX`: the `x` position of the :class:`SpeedMeter` center;
		:param `centerX`: the `y` position of the :class:`SpeedMeter` center.        
		"""

		x = radius*cos(angle) + centerX
		y = radius*sin(angle) + centerY

		return x, y

	def OnPaint(self, e):

		#dc = wx.PaintDC(self)
		pdc = wx.PaintDC(self)
		dc = wx.GCDC(pdc)
		dc.SetBrush(wx.Brush('#777'))
		dc.SetPen(wx.Pen("#777"))
		center= ( 200, 100)
		radius= 100
		angle= pi/4		
		start = self.CircleCoords(radius, -pi*3/4, *center )
		end	  = self.CircleCoords(radius, -pi, *center )
		
		

		dc.SetPen(wx.Pen(wx.Colour(255,255,255, wx.ALPHA_OPAQUE)))
		dc.SetBrush(wx.Brush(wx.Colour(255,255,255, 128)))

		#DrawArc (xStart, yStart, xEnd, yEnd, xc, yc)
		dc.DrawArc(*start, *end, *center)			
		if 1: 
			dc.SetPen(wx.Pen('WHITE',2, wx.PENSTYLE_SOLID))
			dc.SetBrush(wx.Brush('WHITE'))
			dc.DrawCircle(*start, 2)
			
		if 1: 
			dc.SetPen(wx.Pen('RED',3, wx.PENSTYLE_SOLID))	
			dc.SetBrush(wx.Brush('RED'))
			dc.DrawCircle(*end, 2)
			
		if 1: 
			dc.SetPen(wx.Pen('YELLOW',2, wx.PENSTYLE_SOLID))
			dc.SetBrush(wx.Brush('YELLOW'))
			dc.DrawCircle(*center, 2)		



def main():

	app = wx.App()
	ex = Example(None)
	ex.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()
