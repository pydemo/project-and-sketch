import wx
from math import cos, sin, pi

class Example(wx.Frame):

	def __init__(self, *args, **kw):
		super(Example, self).__init__(*args, **kw)

		self.InitUI()
		self.currval=1
		self.center		= ( 200, 100)
		self.radius		= 80
		self.increment	= pi/16

		self.timer = wx.Timer(self)		
		self.Bind(wx.EVT_TIMER, self.update, self.timer)
		self.timer.Start(1000)
		
	def update(self, event):
		print('timer')
		
		self.currval +=1
		self.Freeze()
		self.Refresh()
		self.Thaw()


		
		
	def draw_arc(self):
		center		= self.center
		radius		= self.radius
		increment	= self.increment
		start_angle = -pi + self.currval * increment
		angle = -increment		
		start = self.CircleCoords(radius, start_angle, *center )
		end	  = self.CircleCoords(radius, start_angle+angle, *center )
		print (start,end, self.currval)
		
		dc=self.dc
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
		#self.Refresh()
		
		
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
		pdc = wx.PaintDC(self)
		self.dc = wx.GCDC(pdc)
		self.draw_arc()



def main():

	app = wx.App()
	ex = Example(None)
	ex.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()
