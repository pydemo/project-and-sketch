import wx
import wx.lib.buttons

import speedmeter.SpeedMeter as SM
from math import pi, sqrt

class MyFrame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "SpeedMeter Demo ;-)",
                         wx.DefaultPosition,
                         size=(400,400),
                         style=wx.DEFAULT_FRAME_STYLE |
                         wx.NO_FULL_REPAINT_ON_RESIZE)
        panel = wx.Panel(self)

        self.SpeedWindow = SM.SpeedMeter(panel,
                                          extrastyle=SM.SM_DRAW_HAND |
                                          SM.SM_DRAW_SECTORS |
                                          SM.SM_DRAW_MIDDLE_TEXT |
                                          SM.SM_DRAW_SECONDARY_TICKS |
                                          SM.SM_DRAW_PARTIAL_FILLER |
                                          SM.SM_DRAW_SHADOW
                                          )

        # We Want To Simulate A Clock. Somewhat Tricky, But Did The Job
        self.SpeedWindow.SetAngleRange(pi/2, 5*pi/2)

        intervals = range(0, 13)
        self.SpeedWindow.SetIntervals(intervals)

        colours = [wx.SystemSettings.GetColour(0)]*12
        self.SpeedWindow.SetIntervalColours(colours)

        ticks = [str(interval) for interval in intervals]
        ticks[-1] = ""
        ticks[0] = "12"
        self.SpeedWindow.SetTicks(ticks)
        self.SpeedWindow.SetTicksColour(wx.BLUE)
        self.SpeedWindow.SetTicksFont(wx.Font(11, wx.SCRIPT, wx.NORMAL, wx.BOLD, True))
        self.SpeedWindow.SetNumberOfSecondaryTicks(4)

        # Set The Colour For The External Arc        
        self.SpeedWindow.SetArcColour(wx.BLUE)

        self.SpeedWindow.SetHandColour(wx.BLACK)

        self.SpeedWindow.SetMiddleText("0 s")
        self.SpeedWindow.SetMiddleTextColour(wx.RED)

        # We Set The Background Colour Of The SpeedMeter OutSide The Control
        self.SpeedWindow.SetSpeedBackground(wx.WHITE)

        # Set The Colour For The Shadow
        self.SpeedWindow.SetShadowColour(wx.Colour(128, 128, 128))        

        self.SpeedWindow.SetSpeedValue(0.0)

        # These Are Cosmetics For our SpeedMeter Control

        # Create The Timer For The Clock
        self.timer = wx.PyTimer(self.ClockTimer)
        self.currvalue = 0

        bsizer2 = wx.BoxSizer(wx.VERTICAL)

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL) 
        stattext2 = wx.StaticText(panel, -1, "A Simple Clock", style=wx.ALIGN_CENTER)

        button2 = wx.Button(panel, -1, "Stop")
        self.stopped = 0
        button2.Bind(wx.EVT_BUTTON, self.OnStopClock)
        button2.SetToolTip(wx.ToolTip("Click To Stop/Resume The Clock"))

        hsizer2.Add(button2, 0, wx.LEFT, 5)
        #hsizer2.Add(stattext2, 1, wx.EXPAND)
        #hsizer2.Add(self.helpbuttons[1], 0, wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, 5)

        bsizer2.Add(self.SpeedWindow, 1, wx.EXPAND)        
        bsizer2.Add(hsizer2, 0, wx.EXPAND)        
        panel.SetSizer(bsizer2)
        self.timer.Start(1000)

    def ClockTimer(self):
        if self.currvalue >= 59:
            self.currvalue = 0
        else:
            self.currvalue = self.currvalue + 1

        self.SpeedWindow.SetMiddleText(str(self.currvalue) + " s")            
        self.SpeedWindow.SetSpeedValue(self.currvalue/5.0)


    def OnStopClock(self, event):

        btn = event.GetEventObject()

        if self.stopped == 0:
            self.stopped = 1
            self.timer.Stop()
            btn.SetLabel("Resume")
        else:
            self.stopped = 0
            self.timer.Start()
            btn.SetLabel("Stop")

if __name__ == "__main__":

    app = wx.App()
    frame = MyFrame()
    frame.Show()
    #frame.Maximize()

    app.MainLoop()