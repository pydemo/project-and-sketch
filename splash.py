# sample_one.py

import os
import sys
import wx
import wx.lib.agw.advancedsplash as AS

SHOW_SPLASH = True
SPLASH_FN = "img_sample_one.png"
SPLASH_TIME = 5000

# class MyFrame
# class MyApp

#-------------------------------------------------------------------------------

# Test to see if we need to show a splash screen.
# If the splash is enabled (and we're not the application fork),
# then show a splash screen and relaunch the same application
# except as the application fork.

if __name__ == "__main__":
    AppFN = sys.argv[0]

    if SHOW_SPLASH and (len(sys.argv) == 1) and AppFN.endswith(".exe"):
        App = wx.App()

        #--

        bitmap = wx.Bitmap(SPLASH_FN, wx.BITMAP_TYPE_PNG)
        shadow = wx.RED

        frame = AS.AdvancedSplash(None,
                                  bitmap=bitmap,
                                  timeout=SPLASH_TIME,
                                  agwStyle=AS.AS_TIMEOUT |
                                           AS.AS_CENTER_ON_PARENT |
                                           AS.AS_SHADOW_BITMAP,
                                  shadowcolour=shadow)

        #--
        if 0:
            os.spawnl(os.P_NOWAIT,
                      AppFN,
                      '"%s"' % AppFN.replace('"', r'\"'),
                      "NO_SPLASH")

        #--

        App.MainLoop()
        sys.exit()

#-------------------------------------------------------------------------------

import time

# Simulate 1.3s of time spent importing libraries and source files.
time.sleep(1.3)

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    """
    ...
    """
    def __init__(self):
        super(MyFrame, self).__init__(None,
                                      -1,
                                      title="")

        #------------

        # Return application name.
        self.app_name = wx.GetApp().GetAppName()

        #------------

        # Simplified init method.
        self.SetProperties()
        self.CreateCtrls()
        self.BindEvents()
        self.DoLayout()

        #------------

        self.CenterOnScreen()

    #-----------------------------------------------------------------------

    def SetProperties(self):
        """
        ...
        """

        self.SetTitle(self.app_name)

        #------------

        #frameicon = wx.Icon("icon_wxWidgets.ico")
        #self.SetIcon(frameicon)


    def CreateCtrls(self):
        """
        ...
        """

        # Create a panel.
        self.panel = wx.Panel(self, -1)

        #------------

        # Add a button.
        self.btnClose = wx.Button(self.panel,
                                  -1,
                                  "&Close")


    def BindEvents(self):
        """
        Bind some events to an events handler.
        """

        # Bind the close event to an event handler.
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        # Bind the button event to an event handler.
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, self.btnClose)


    def DoLayout(self):
        """
        ...
        """

        # MainSizer is the top-level one that manages everything.
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # wx.BoxSizer(window, proportion, flag, border)
        # wx.BoxSizer(sizer, proportion, flag, border)
        mainSizer.Add(self.btnClose, 1, wx.EXPAND | wx.ALL, 10)

        # Finally, tell the panel to use the sizer for layout.
        self.panel.SetAutoLayout(True)
        self.panel.SetSizer(mainSizer)

        mainSizer.Fit(self.panel)

    #-----------------------------------------------------------------------

    def OnCloseMe(self, event):
        """
        ...
        """

        self.Close(True)


    def OnCloseWindow(self, event):
        """
        ...
        """

        self.Destroy()

#---------------------------------------------------------------------------

class MyApp(wx.App):
    """
    ...
    """
    def OnInit(self):

        #------------

        self.SetAppName("Main frame")

        #------------

        # Simulate 6s of time spent initializing wx components.
        time.sleep(6)

        #------------

        self.frame = MyFrame()
        self.frame.Show(True)

        return True

#---------------------------------------------------------------------------

def main():
    app = MyApp(False)
    app.MainLoop()

#---------------------------------------------------------------------------

if __name__ == "__main__" :
    main()