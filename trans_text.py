"""
Static text with transparent background
"""

import wx

class TransparentText(wx.StaticText):
  def __init__(self, parent, id=wx.ID_ANY, label='', 
               pos=wx.DefaultPosition, size=wx.DefaultSize, 
               style=wx.TRANSPARENT_WINDOW, name='transparenttext'):
    wx.StaticText.__init__(self, parent=parent, id=id, label=label, pos=pos, size=(100,50), style=style, name=name)

    self.Bind(wx.EVT_PAINT, self.on_paint)
    self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
    self.Bind(wx.EVT_SIZE, self.on_size)

  def on_paint(self, event):
    bdc = wx.PaintDC(self)
    dc = wx.GCDC(bdc)

    font_face = self.GetFont()
    font_color = self.GetForegroundColour()

    dc.SetFont(font_face)
    dc.SetTextForeground(font_color)
    dc.DrawText(self.GetLabel(), 0, 0)

  def on_size(self, event):
    self.Refresh()
    event.Skip()
    
import wx
 
class Fader(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, title='Test')
        self.amount = 5
        self.delta = 5
        panel = wx.Panel(self, wx.ID_ANY)
        panel.mainSizer = wx.BoxSizer(wx.VERTICAL)
        str = "This is a different font."
        text = TransparentText(panel, label=str, size= (20, 120))
        
        
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        text.SetFont(font)
        
        panel.mainSizer.Add(text, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(panel.mainSizer)        
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.Show()
        self.sizer.Fit(self)
        self.Center()

        



 
if __name__ == '__main__':
    app = wx.App(False)
    frm = Fader()
    frm.Show()
    app.MainLoop()    