import wx

class Example(wx.Frame):

	def __init__(self, *args, **kw):
		super(Example, self).__init__(*args, **kw)

		self.InitUI()

	def InitUI(self):

		self.Bind(wx.EVT_PAINT, self.OnPaint)

		self.SetTitle("Custom patterns")
		self.SetSize((900,600))
		self.Centre()

	def OnPaint(self, e):

		dc = wx.PaintDC(self)

		dc.SetPen(wx.Pen('#C7C3C3'))

		brush1 = wx.Brush(wx.Bitmap(r'images\patt1.jpg'))
		dc.SetBrush(brush1)
		dc.DrawRectangle(10, 15, 800, 350)

		brush2 = wx.Brush(wx.Bitmap(r'images\patt2.jpg'))
		dc.SetBrush(brush2)
		dc.DrawRectangle(10, 460, 800, 150)

		brush3 = wx.Brush(wx.Bitmap(r'images\patt3.jpg'))
		dc.SetBrush(brush3)
		dc.DrawRectangle(10, 620, 800, 150)


def main():

	app = wx.App()
	ex = Example(None)
	ex.Show()
	app.MainLoop()


if __name__ == '__main__':
	main()