import wx

class Example(wx.Frame):

	def __init__(self, *args, **kw):
		super(Example, self).__init__(*args, **kw)

		self.InitUI()

	def InitUI(self):

		self.Bind(wx.EVT_PAINT, self.OnPaint)

		self.SetTitle("Shapes")
		self.Centre()


	def OnPaint(self, e):

		#dc = wx.PaintDC(self)
		pdc = wx.PaintDC(self)
		dc = wx.GCDC(pdc)
		dc.SetBrush(wx.Brush('#777'))
		dc.SetPen(wx.Pen("#777"))
		center= ( 290, 40)
		start = ( 240, 40)
		end	  = ( 340, 40)
		dc.SetPen(wx.Pen(wx.Colour(255,255,255, wx.ALPHA_OPAQUE)))
		dc.SetBrush(wx.Brush(wx.Colour(255,255,255, 128)))

		#DrawArc (xStart, yStart, xEnd, yEnd, xc, yc)
		dc.DrawArc(*start, *end, *center)			
		if 1: 
			dc.SetPen(wx.Pen('WHITE',1, wx.PENSTYLE_SOLID))
			#dc.DrawPoint(240, 40)
			dc.SetBrush(wx.Brush('WHITE'))
			dc.DrawCircle(*start, 2)
		if 1: 
			dc.SetPen(wx.Pen(wx.Colour(255,0,0, wx.ALPHA_OPAQUE),5))
			#dc.DrawPoint(240, 40)
			dc.SetBrush(wx.Brush(wx.Colour(255,0,0, 128)))
			dc.DrawCircle(*end, 2)
		if 1: 
			dc.SetPen(wx.Pen('YELLOW',1, wx.PENSTYLE_SOLID))
			#dc.DrawPoint(240, 40)
			dc.SetBrush(wx.Brush('YELLOW'))
			dc.DrawCircle(*center, 2)			
		
		if 0:
			dc.DrawEllipse(20, 20, 90, 60)
			dc.DrawRoundedRectangle(130, 20, 90, 60, 10)		
			dc.DrawRectangle(20, 120, 80, 50)
			dc.DrawPolygon(((130, 140), (180, 170), (180, 140), (220, 110), (140, 100)))
			dc.DrawSpline(((240, 170), (280, 170), (285, 110), (325, 110)))

			dc.DrawLines(((20, 260), (100, 260), (20, 210), (100, 210)))
			dc.DrawCircle(170, 230, 35)
			dc.DrawRectangle(250, 200, 60, 60)


def main():

	app = wx.App()
	ex = Example(None)
	ex.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()
