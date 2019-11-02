import wx, os, math, time, string
import wx
#wx.lib.analogclock 

global rotation
rotation = 0

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        global rotation
        wxFrame.__init__(self, parent, id, title)
        b = wx.Button(self, -1, "Rotate (tray) ...")
        wx.EVT_BUTTON(self, b.GetId(), self.DisplayNext)
        bg = r'in\Gergiev_art_helps_putin_to_kill.JPG'
        ov = r'in\gergiev_is_war_supporter.JPG'
        self.imageback = wxBitmap("/Users/gerard/desktop/testmoon/background.png")
        self.imgehandp = wx.Image("/Users/gerard/desktop/testmoon/hand.png", wx.BITMAP_TYPE_PNG)
        self.imgehand = self.imgehandp

        EVT_PAINT(self, self.OnPaint)

    def OnPaint(self, event):
         self.Paint(wxPaintDC(self))

    def Paint(self, dc):
        dc.DrawBitmap(self.imageback, 0, 0)
        dc.DrawBitmap(wx.BitmapFromImage(self.imgehand),  
        self.imageback.GetHeight()/2-9, self.imageback.GetWidth()/2-130, useMask=True)

    def DisplayNext(self,event):
        global rotation
        rotation= rotation + 2 * math.pi/12
        self.imgehand = self.imgehandp.Rotate(rotation,  (self.imageback.GetHeight(), self.imageback.GetWidth()))

class MyApp(wxApp):
    def OnInit(self):
        global rotation
        wxInitAllImageHandlers()
        self.frame = MyFrame(None, -1, "Personal Clock (tray)")
        self.frame.Show(true)
        self.SetTopWindow(self.frame)
        rotation = 10
        return true

app = MyApp(0)
app.MainLoop()