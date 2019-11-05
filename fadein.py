import wx
 
class Fader(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, title='Test')
        self.amount = 5
        self.delta = 5
        panel = wx.Panel(self, wx.ID_ANY)
        if 1:
            panel.mainSizer = wx.BoxSizer(wx.VERTICAL)
            instructions = wx.StaticText(panel, label='Test', size=(100,100))
            panel.mainSizer.Add(instructions, 0, wx.ALL|wx.CENTER, 5)
            panel.SetSizer(panel.mainSizer)        
            self.sizer = wx.BoxSizer(wx.VERTICAL)

            
            self.sizer.Add(panel, 1, wx.EXPAND)
            self.SetSizer(self.sizer)
            
            self.Show()
            self.sizer.Fit(self)
            self.Center()
        
        self.SetTransparent(self.amount)
 
        ## ------- Fader Timer -------- ##
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.timer.Start(60)
        self.Bind(wx.EVT_TIMER, self.AlphaCycle)
        ## ---------------------------- ##
 
    def AlphaCycle(self, evt):
        self.amount += self.delta
        if self.amount >= 255:
            self.delta = -self.delta
            self.amount = 255
        if self.amount <= 0:
            self.amount = 0
        self.SetTransparent(self.amount)
 
if __name__ == '__main__':
    app = wx.App(False)
    frm = Fader()
    frm.Show()
    app.MainLoop()