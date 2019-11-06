# -*- coding: utf-8 -*-
#py.bat 3iv.py 10 C:\Users\alex_\OneDrive\Pictures\Sony7rM4\55mm\protest\1-20-2019\insta_base jpg

import glob
import os, sys, math
import wx
import cv2
import numpy as np
from pubsub import pub 
from pprint import pprint as pp
import cv2
from six import unichr
e=sys.exit



import wx.lib.buttons

import speedmeter.SpeedMeter as SM
from math import pi, sqrt



if 0:
    dr=r'C:\Users\alex_\OneDrive\Pictures\Sony7rM4\55mm\protest\1-20-2019\insta_base'
    dr=r'C:\Users\alex_\OneDrive\Documents\Gallery\1'
        
        
pp(sys.argv)
interval_sec = int(sys.argv[1])
img_dir = sys.argv[2]
assert os.path.isdir(img_dir)

ext = sys.argv[3]


try:
    import cStringIO
except ImportError:
    import io as cStringIO

#----------------------------------------------------------------------

keyMap = {
    wx.WXK_BACK : "WXK_BACK",
    wx.WXK_TAB : "WXK_TAB",
    wx.WXK_RETURN : "WXK_RETURN",
    wx.WXK_ESCAPE : "WXK_ESCAPE",
    wx.WXK_SPACE : "WXK_SPACE",
    wx.WXK_DELETE : "WXK_DELETE",
    wx.WXK_START : "WXK_START",
    wx.WXK_LBUTTON : "WXK_LBUTTON",
    wx.WXK_RBUTTON : "WXK_RBUTTON",
    wx.WXK_CANCEL : "WXK_CANCEL",
    wx.WXK_MBUTTON : "WXK_MBUTTON",
    wx.WXK_CLEAR : "WXK_CLEAR",
    wx.WXK_SHIFT : "WXK_SHIFT",
    wx.WXK_ALT : "WXK_ALT",
    wx.WXK_MENU : "WXK_MENU",
    wx.WXK_PAUSE : "WXK_PAUSE",
    wx.WXK_CAPITAL : "WXK_CAPITAL",
    #wx.WXK_PRIOR : "WXK_PRIOR",
    #wx.WXK_NEXT : "WXK_NEXT",
    wx.WXK_END : "WXK_END",
    wx.WXK_HOME : "WXK_HOME",
    wx.WXK_LEFT : "WXK_LEFT",
    wx.WXK_UP : "WXK_UP",
    wx.WXK_RIGHT : "WXK_RIGHT",
    wx.WXK_DOWN : "WXK_DOWN",
    wx.WXK_SELECT : "WXK_SELECT",
    wx.WXK_PRINT : "WXK_PRINT",
    wx.WXK_EXECUTE : "WXK_EXECUTE",
    wx.WXK_SNAPSHOT : "WXK_SNAPSHOT",
    wx.WXK_INSERT : "WXK_INSERT",
    wx.WXK_HELP : "WXK_HELP",
    wx.WXK_NUMPAD0 : "WXK_NUMPAD0",
    wx.WXK_NUMPAD1 : "WXK_NUMPAD1",
    wx.WXK_NUMPAD2 : "WXK_NUMPAD2",
    wx.WXK_NUMPAD3 : "WXK_NUMPAD3",
    wx.WXK_NUMPAD4 : "WXK_NUMPAD4",
    wx.WXK_NUMPAD5 : "WXK_NUMPAD5",
    wx.WXK_NUMPAD6 : "WXK_NUMPAD6",
    wx.WXK_NUMPAD7 : "WXK_NUMPAD7",
    wx.WXK_NUMPAD8 : "WXK_NUMPAD8",
    wx.WXK_NUMPAD9 : "WXK_NUMPAD9",
    wx.WXK_MULTIPLY : "WXK_MULTIPLY",
    wx.WXK_ADD : "WXK_ADD",
    wx.WXK_SEPARATOR : "WXK_SEPARATOR",
    wx.WXK_SUBTRACT : "WXK_SUBTRACT",
    wx.WXK_DECIMAL : "WXK_DECIMAL",
    wx.WXK_DIVIDE : "WXK_DIVIDE",
    wx.WXK_F1 : "WXK_F1",
    wx.WXK_F2 : "WXK_F2",
    wx.WXK_F3 : "WXK_F3",
    wx.WXK_F4 : "WXK_F4",
    wx.WXK_F5 : "WXK_F5",
    wx.WXK_F6 : "WXK_F6",
    wx.WXK_F7 : "WXK_F7",
    wx.WXK_F8 : "WXK_F8",
    wx.WXK_F9 : "WXK_F9",
    wx.WXK_F10 : "WXK_F10",
    wx.WXK_F11 : "WXK_F11",
    wx.WXK_F12 : "WXK_F12",
    wx.WXK_F13 : "WXK_F13",
    wx.WXK_F14 : "WXK_F14",
    wx.WXK_F15 : "WXK_F15",
    wx.WXK_F16 : "WXK_F16",
    wx.WXK_F17 : "WXK_F17",
    wx.WXK_F18 : "WXK_F18",
    wx.WXK_F19 : "WXK_F19",
    wx.WXK_F20 : "WXK_F20",
    wx.WXK_F21 : "WXK_F21",
    wx.WXK_F22 : "WXK_F22",
    wx.WXK_F23 : "WXK_F23",
    wx.WXK_F24 : "WXK_F24",
    wx.WXK_NUMLOCK : "WXK_NUMLOCK",
    wx.WXK_SCROLL : "WXK_SCROLL",
    wx.WXK_PAGEUP : "WXK_PAGEUP",
    wx.WXK_PAGEDOWN : "WXK_PAGEDOWN",
    wx.WXK_NUMPAD_SPACE : "WXK_NUMPAD_SPACE",
    wx.WXK_NUMPAD_TAB : "WXK_NUMPAD_TAB",
    wx.WXK_NUMPAD_ENTER : "WXK_NUMPAD_ENTER",
    wx.WXK_NUMPAD_F1 : "WXK_NUMPAD_F1",
    wx.WXK_NUMPAD_F2 : "WXK_NUMPAD_F2",
    wx.WXK_NUMPAD_F3 : "WXK_NUMPAD_F3",
    wx.WXK_NUMPAD_F4 : "WXK_NUMPAD_F4",
    wx.WXK_NUMPAD_HOME : "WXK_NUMPAD_HOME",
    wx.WXK_NUMPAD_LEFT : "WXK_NUMPAD_LEFT",
    wx.WXK_NUMPAD_UP : "WXK_NUMPAD_UP",
    wx.WXK_NUMPAD_RIGHT : "WXK_NUMPAD_RIGHT",
    wx.WXK_NUMPAD_DOWN : "WXK_NUMPAD_DOWN",
    #wx.WXK_NUMPAD_PRIOR : "WXK_NUMPAD_PRIOR",
    wx.WXK_NUMPAD_PAGEUP : "WXK_NUMPAD_PAGEUP",
    #wx.WXK_NUMPAD_NEXT : "WXK_NUMPAD_NEXT",
    wx.WXK_NUMPAD_PAGEDOWN : "WXK_NUMPAD_PAGEDOWN",
    wx.WXK_NUMPAD_END : "WXK_NUMPAD_END",
    wx.WXK_NUMPAD_BEGIN : "WXK_NUMPAD_BEGIN",
    wx.WXK_NUMPAD_INSERT : "WXK_NUMPAD_INSERT",
    wx.WXK_NUMPAD_DELETE : "WXK_NUMPAD_DELETE",
    wx.WXK_NUMPAD_EQUAL : "WXK_NUMPAD_EQUAL",
    wx.WXK_NUMPAD_MULTIPLY : "WXK_NUMPAD_MULTIPLY",
    wx.WXK_NUMPAD_ADD : "WXK_NUMPAD_ADD",
    wx.WXK_NUMPAD_SEPARATOR : "WXK_NUMPAD_SEPARATOR",
    wx.WXK_NUMPAD_SUBTRACT : "WXK_NUMPAD_SUBTRACT",
    wx.WXK_NUMPAD_DECIMAL : "WXK_NUMPAD_DECIMAL",
    wx.WXK_NUMPAD_DIVIDE : "WXK_NUMPAD_DIVIDE",

    wx.WXK_WINDOWS_LEFT : "WXK_WINDOWS_LEFT",
    wx.WXK_WINDOWS_RIGHT : "WXK_WINDOWS_RIGHT",
    wx.WXK_WINDOWS_MENU : "WXK_WINDOWS_MENU",

    wx.WXK_SPECIAL1 : "WXK_SPECIAL1",
    wx.WXK_SPECIAL2 : "WXK_SPECIAL2",
    wx.WXK_SPECIAL3 : "WXK_SPECIAL3",
    wx.WXK_SPECIAL4 : "WXK_SPECIAL4",
    wx.WXK_SPECIAL5 : "WXK_SPECIAL5",
    wx.WXK_SPECIAL6 : "WXK_SPECIAL6",
    wx.WXK_SPECIAL7 : "WXK_SPECIAL7",
    wx.WXK_SPECIAL8 : "WXK_SPECIAL8",
    wx.WXK_SPECIAL9 : "WXK_SPECIAL9",
    wx.WXK_SPECIAL10 : "WXK_SPECIAL10",
    wx.WXK_SPECIAL11 : "WXK_SPECIAL11",
    wx.WXK_SPECIAL12 : "WXK_SPECIAL12",
    wx.WXK_SPECIAL13 : "WXK_SPECIAL13",
    wx.WXK_SPECIAL14 : "WXK_SPECIAL14",
    wx.WXK_SPECIAL15 : "WXK_SPECIAL15",
    wx.WXK_SPECIAL16 : "WXK_SPECIAL16",
    wx.WXK_SPECIAL17 : "WXK_SPECIAL17",
    wx.WXK_SPECIAL18 : "WXK_SPECIAL18",
    wx.WXK_SPECIAL19 : "WXK_SPECIAL19",
}

if 'wxMac' in wx.PlatformInfo:
    keyMap[wx.WXK_RAW_CONTROL] = 'WXK_RAW_CONTROL'
    keyMap[wx.WXK_CONTROL] = "WXK_CONTROL"
    keyMap[wx.WXK_COMMAND] = "WXK_COMMAND"
else:
    keyMap[wx.WXK_COMMAND] = "WXK_COMMAND"
    keyMap[wx.WXK_CONTROL] = "WXK_CONTROL"



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
    
#----------------------------------------------------------------------

class KeySink(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent, -1, style=wx.WANTS_CHARS
                          #| wx.RAISED_BORDER
                          #| wx.SUNKEN_BORDER
                           , name="sink")

        self.SetBackgroundColour(wx.BLUE)
        self.haveFocus = False
        self.callSkip = True
        self.logKeyDn = True
        self.logKeyUp = True
        self.logChar = True

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_CHAR, self.OnChar)


    def SetCallSkip(self, skip):
        self.callSkip = skip

    def SetLogKeyUp(self, val):
        self.logKeyUp = val

    def SetLogKeyDn(self, val):
        self.logKeyDn = val

    def SetLogChar(self, val):
        self.logChar = val


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        rect = self.GetClientRect()
        dc.SetTextForeground(wx.WHITE)
        dc.DrawLabel("Click here and then press some keys",
                     rect, wx.ALIGN_CENTER | wx.ALIGN_TOP)
        if self.haveFocus:
            dc.SetTextForeground(wx.GREEN)
            dc.DrawLabel("Have Focus", rect, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)
        else:
            dc.SetTextForeground(wx.RED)
            dc.DrawLabel("Need Focus!", rect, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM)


    def OnSetFocus(self, evt):
        self.haveFocus = True
        self.Refresh()

    def OnKillFocus(self, evt):
        self.haveFocus = False
        self.Refresh()

    def OnMouse(self, evt):
        if evt.ButtonDown():
            self.SetFocus()


    def OnKeyDown(self, evt):
        if self.logKeyDn:
            self.GetParent().keylog.LogKeyEvent("KeyDown", evt)
        if self.callSkip:
            evt.Skip()

    def OnKeyUp(self, evt):
        if self.logKeyUp:
            self.GetParent().keylog.LogKeyEvent("KeyUp", evt)
        if self.callSkip:
            evt.Skip()

    def OnChar(self, evt):
        if self.logChar:
            self.GetParent().keylog.LogKeyEvent("Char", evt)    

########################################################################
class ViewerPanel( wx.Window):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        global img_dir, ext, interval_sec
        """Constructor"""
        #wx.Panel.__init__(self, parent)
        wx.Window.__init__(self, parent, -1, style=wx.WANTS_CHARS
                          #| wx.RAISED_BORDER
                          #| wx.SUNKEN_BORDER
                           , name="sink")        
        width, height = wx.DisplaySize()
        self.picPaths = []
        self.is_fs =False
        self.btns={}
        self.currentPicture = 0
        self.totalPictures = 0
         
        pub.subscribe(self.updateImages, ("update images"))

        self.slideTimer = wx.Timer(self)
        self.sec_left = -1
        #self.slideTimer.Bind(wx.EVT_TIMER, self.update)
        displays = (wx.Display(i) for i in range(wx.Display.GetCount()))
        sizes = [display.GetGeometry().GetSize() for display in displays]
        d1=sizes[0]
        self.dh, self.dw = d1.height, d1.width  
        self.photoMaxSize = self.dh        
        self.layout()

        
        dr=img_dir
        self.picPaths=glob.glob(os.path.join(dr, '*.%s' % ext ))
        self.updateImages(msg=self.picPaths)
        self.Bind(wx.EVT_TIMER, self.update, self.slideTimer)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        #self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        #self.Bind(wx.EVT_CHAR, self.OnChar)        
        self.SetFocus()
        if 1:
            self.ttimer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.watch, self.ttimer)
            #self.timer.Start(1000)
        if 1:
            watch_h, watch_w = 175, 175
            size= (watch_h, watch_w)
            panel = wx.Panel(self, size=size, pos=(5, self.photoMaxSize-watch_h-5-15))

            self.SpeedWindow = SM.SpeedMeter(panel,size=size,
                                              extrastyle=#SM.SM_DRAW_HAND |
                                              #SM.SM_DRAW_PARTIAL_SECTORS |
                                              SM.SM_DRAW_SECTORS |
                                              #SM.SM_DRAW_MIDDLE_TEXT |
                                              #SM.SM_DRAW_SECONDARY_TICKS |
                                              SM.SM_DRAW_PARTIAL_FILLER #|
                                              #SM.SM_DRAW_SHADOW
                                              , interval= interval_sec
                                              )

            # We Want To Simulate A Clock. Somewhat Tricky, But Did The Job
            self.SpeedWindow.SetAngleRange(0, 5*pi)

            intervals = range(0, interval_sec)
            self.SpeedWindow.SetIntervals(intervals)

            colours = [wx.SystemSettings.GetColour(0)]*(interval_sec-1)
            self.SpeedWindow.SetIntervalColours(colours)
            if 0:
                ticks = [str(interval) for interval in intervals]
                ticks[-1] = ""
                ticks[0] = "12"
                self.SpeedWindow.SetTicks(ticks)
                self.SpeedWindow.SetTicksColour(wx.BLUE)
                self.SpeedWindow.SetTicksFont(wx.Font(11, wx.SCRIPT, wx.NORMAL, wx.BOLD, True))
                self.SpeedWindow.SetNumberOfSecondaryTicks(4)

            # Set The Colour For The External Arc        
            #self.SpeedWindow.SetArcColour(wx.BLUE)

            #self.SpeedWindow.SetHandColour(wx.BLACK)

            #self.SpeedWindow.SetMiddleText("0 s")
            #self.SpeedWindow.SetMiddleTextColour(wx.RED)

            # We Set The Background Colour Of The SpeedMeter OutSide The Control
            #self.SpeedWindow.SetSpeedBackground(wx.WHITE)

            # Set The Colour For The Shadow
            #self.SpeedWindow.SetShadowColour(wx.Colour(128, 128, 128))        

            self.SpeedWindow.SetSpeedValue(0)

            # These Are Cosmetics For our SpeedMeter Control

            # Create The Timer For The Clock
            self.timer = wx.PyTimer(self.ClockTimer)
            self.currvalue = 0
            if 1:
                bsizer2 = wx.BoxSizer(wx.VERTICAL)

                hsizer2 = wx.BoxSizer(wx.HORIZONTAL) 
                stattext2 = wx.StaticText(panel, -1, "Image Clock", style=wx.ALIGN_CENTER)

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
                       
            else:
                self.stopped = 0
                bsizer2 = wx.BoxSizer(wx.VERTICAL)
    def ClockTimer(self):
        if self.currvalue >= interval_sec:
            self.currvalue = 0
        else:
            self.currvalue = self.currvalue + 1

        #self.SpeedWindow.SetMiddleText(str(self.currvalue) + " s")            
        self.SpeedWindow.SetSpeedValue(self.currvalue/5 if self.currvalue/5 !=1.0 else 1.01)   
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

            
    def OnKeyDown(self, evt):
        key_code = evt.GetKeyCode()
        if key_code in [83]: #Start/Stop
        
            
            if 1:
                label="Slide Show"
                btn=self.btns[label]
                if btn.GetLabel() in [label]:
                    self.showMsg('START')
                else:
                    self.showMsg('STOP')
                self.setSlideShow(btn)
        elif key_code in [81]: #Exit
            self.GetParent().Close()
        elif key_code in [80, 32]: #Pause
        
            
            if 1:
                label="Slide Show"
                btn=self.btns[label]
                if btn.GetLabel() in [label]:
                    self.showMsg('Unpause')
                else:
                    self.showMsg('Pause')
                self.setSlideShow(btn)
                
        elif key_code in [70]: #Full screen
            self.is_fs = not self.is_fs
            self.GetParent().ShowFullScreen(self.is_fs)           
        elif key_code == wx.WXK_ESCAPE:
            #self.GetParent().Close()
            self.GetParent().ShowFullScreen(False)
            label="Slide Show"
            btn=self.btns[label]
            if btn.GetLabel() in ['Stop']:
                self.setSlideShow(btn)
                                
        else:
            evt.Skip()
        keyname = keyMap.get(key_code, None)
        self.LogKeyEvent("KeyDown", evt)            
    #----------------------------------------------------------------------
    def update(self, event):
        global interval_sec
        """
        Called when the slideTimer's timer event fires. Loads the next
        picture from the folder by calling th nextPicture method
        """
        print('interval timer')
        self.Clean()
        self.sec_left = interval_sec
        self.timer.Stop()
        self.currvalue=0
        self.timer.Start(1000)
        
        self.nextPicture()            
        
    #----------------------------------------------------------------------
    def watch(self, event):
        """
        Called when the slideTimer's timer event fires. Loads the next
        picture from the folder by calling th nextPicture method
        """
        print ('countdown',self.sec_left )
        if self.sec_left>-1:
            self.sec_left -= 1
            print(self.sec_left)
            if self.sec_left in [2,1]:
                
                print('ticker', self.sec_left)
                self.showMsg(str(self.sec_left-1), 1000, clean =False)
            elif self.sec_left in [-1]:
                self.Clean()
                
                
        
        
    def showMsg(self,msg, timeout=3000, clean=True):  
        self.Clean()
        
        self.text=text = TransparentText(self, label=msg, size= (20, 120), pos=(self.NewW/2, self.NewH/2))
        
        text.SetForegroundColour(wx.Colour(wx.WHITE))
        print(self.dh, self.dw)
        font = wx.Font(425*(self.NewW+ (self.dw-self.NewW)/3)/self.dw, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.BOLD, False)
        text.SetFont(font)
        m_w, m_h=text.GetClientSize()
        text.SetPosition((self.NewW/2-m_w/2, self.NewH/2-m_h/2))       
        if clean:
            wx.CallLater(timeout, self.Clean)
        
    def OnKeyUp(self, evt):
        self.LogKeyEvent("KeyUp", evt)  
    def OnChar(self, evt):
        self.LogKeyEvent("Char", evt)       
 
    def Clean(self):
        if hasattr(self, 'text') and self.text:
        
                self.Freeze()
                if hasattr(self, 'text') and self.text:
                    
                    self.text.Destroy()
                #self.Refresh()
                self.Thaw()
    def AfterRun(self,msg):
       dlg=wx.MessageDialog(self, msg, "Called after", wx.OK|wx.ICON_INFORMATION)
       dlg.ShowModal()
       dlg.Destroy()   
    def LogKeyEvent(self, evType, evt):
        keycode = evt.GetKeyCode()
        keyname = keyMap.get(keycode, None)

        if keyname is None:
            if keycode < 256:
                if keycode == 0:
                    keyname = "NUL"
                elif keycode < 27:
                    keyname = u"Ctrl-%s" % unichr(ord('A') + keycode-1)
                else:
                    keyname = u"\"%s\"" % unichr(keycode)
            else:
                keyname = u"(%s)" % keycode

        UniChr = ''
        if "unicode" in wx.PlatformInfo:
            UniChr = "\"" + unichr(evt.GetUnicodeKey()) + "\""

        modifiers = ""
        for mod, ch in [(evt.ControlDown(),    'C'),
                        (evt.AltDown(),        'A'),
                        (evt.ShiftDown(),      'S'),
                        (evt.MetaDown(),       'M'),
                        (evt.RawControlDown(), 'R'),]:
            if mod:
                modifiers += ch
            else:
                modifiers += '-'
        if 0:
            id = self.InsertItem(self.GetItemCount(), evType)
            self.SetItem(id, 1, keyname)
            self.SetItem(id, 2, str(keycode))
            self.SetItem(id, 3, modifiers)
            self.SetItem(id, 4, str(evt.GetUnicodeKey()))
            self.SetItem(id, 5, UniChr)
            self.SetItem(id, 6, str(evt.GetRawKeyCode()))
            self.SetItem(id, 7, str(evt.GetRawKeyFlags()))

            self.EnsureVisible(id)
        else:
            pp (dict(evType=evType, keyname=keyname,keycode=str(keycode),modifiers=modifiers, GetUnicodeKey=str(evt.GetUnicodeKey()), 
            UniChr=UniChr, GetRawKeyCode=str(evt.GetRawKeyCode()), GetRawKeyFlags=str(evt.GetRawKeyFlags())))
    def OnTest1Start(self, evt):
        self.t1 = wx.Timer(self)
        self.t1.Start(1000)
        
        self.log.write("EVT_TIMER timer started\n")
        self.t1b2.Enable()
        
    def OnTest1Timer(self, evt):
        print ("got EVT_TIMER event\n")     
        
        self.nextPicture()
    
    #----------------------------------------------------------------------
    def layout(self):
        """
        Layout the widgets on the panel
        """
        
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        img = wx.EmptyImage(self.photoMaxSize,self.photoMaxSize)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL|wx.CENTER, 5)
        self.imageLabel = wx.StaticText(self, label="")
        self.mainSizer.Add(self.imageLabel, 0, wx.ALL|wx.CENTER, 5)
        
        btnData = [("Previous", btnSizer, self.onPrevious),
                   ("Slide Show", btnSizer, self.onSlideShow),
                   ("Next", btnSizer, self.onNext)]
        for data in btnData:
            label, sizer, handler = data
            self.btnBuilder(label, sizer, handler)
            
        self.mainSizer.Add(btnSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)
            
    #----------------------------------------------------------------------
    def btnBuilder(self, label, sizer, handler):
        """
        Builds a button, binds it to an event handler and adds it to a sizer
        """
        self.btns[label]=btn = wx.Button(self, label=label)
        btn.Bind(wx.EVT_BUTTON, handler)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        
    #----------------------------------------------------------------------
    def loadImage(self, image):
        """"""
        image_name = os.path.basename(image)
        print (image)
        if 1:
            imageFile = image
            data = open(imageFile, "rb").read()
            
            # convert to a data stream
            stream = cStringIO.BytesIO(data)
            img= wx.ImageFromStream( stream )
            #pp(dir(im))
            W = img.GetWidth()
            H = img.GetHeight()
            print('wxPython:',img.GetSize(), W, H)   
            if 1:            
                stream.seek(0)            
                cv = cv2.imdecode(np.asarray( bytearray(stream.read() ) , dtype=np.uint8), 0 )
                o_h, o_w = cv.shape
                print('cv2:',o_h, o_w, self.dh, self.dw )
                # convert to a bitmap

            
            
        #img = wx.Image(image, wx.BITMAP_TYPE_JPEG)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        print (W,H, img.GetSize())
        if 0:
            if W > H:
                NewW = self.photoMaxSize
                NewH = self.photoMaxSize * H / W
            else:
                NewH = self.photoMaxSize
                NewW = self.photoMaxSize * W / H
            img = img.Scale(NewW,NewH)

            
        if o_h> o_w and 1:
        
        
            img_centre = wx.Point( img.GetWidth()/2, img.GetHeight()/2 )
      
            img = img.Rotate(math.pi/2, img_centre)
            
        if o_h> self.dh:
                NewH = self.dh
                NewW = o_w * self.dh / o_h
                print ('new:', NewH, NewW )
                img = img.Scale(NewW,NewH)
        else:
                NewH = self.dh
                NewW = o_w * self.dh / o_h
                print ('new:', NewH, NewW )
                img = img.Scale(NewW,NewH)  				
                
        
        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.imageLabel.SetLabel(image_name)
        self.NewH = NewH
        self.NewW = NewW
        self.Refresh()
        pub.sendMessage("resize", msg="")
        
    #----------------------------------------------------------------------
    def nextPicture(self):
        """
        Loads the next picture in the directory
        """
        if self.currentPicture == self.totalPictures-1:
            self.currentPicture = 0
        else:
            self.currentPicture += 1
        self.loadImage(self.picPaths[self.currentPicture])
        
    #----------------------------------------------------------------------
    def previousPicture(self):
        """
        Displays the previous picture in the directory
        """
        if self.currentPicture == 0:
            self.currentPicture = self.totalPictures - 1
        else:
            self.currentPicture -= 1
        self.loadImage(self.picPaths[self.currentPicture])
        

        
    #----------------------------------------------------------------------
    def updateImages(self, msg, arg2=None):
        """
        Updates the picPaths list to contain the current folder's images
        """
        self.picPaths = msg
        self.totalPictures = len(self.picPaths)
        self.loadImage(self.picPaths[0])
        
    #----------------------------------------------------------------------
    def onNext(self, event):
        """
        Calls the nextPicture method
        """
        self.nextPicture()
    
    #----------------------------------------------------------------------
    def onPrevious(self, event):
        """
        Calls the previousPicture method
        """
        self.previousPicture()
    
    #----------------------------------------------------------------------
    def onSlideShow(self, event):
        """
        Starts and stops the slideshow
        """
        btn = event.GetEventObject()
        self.setSlideShow(btn)
        
    def setSlideShow(self, btn):
        global interval_sec
        label = btn.GetLabel()
        print (label)
        if label == "Slide Show":
            self.sec_left = interval_sec
            self.slideTimer.Start(interval_sec*1000)
            self.ttimer.Start(1000)
            self.timer.Start(1000) 
            btn.SetLabel("Stop")
        else:
            self.slideTimer.Stop()
            self.ttimer.Stop()
            self.timer.Stop() 
            btn.SetLabel("Slide Show")
            
########################################################################
class ViewerFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Image Viewer")
        self.panel=panel = ViewerPanel(self)
        self.folderPath = ""
        pub.subscribe(self.resizeFrame, ("resize"))
        
        self.initToolbar()
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        
        self.Show()
        self.sizer.Fit(self)
        self.Center()
        #self.Maximize(True)
        #self.ShowFullScreen(True)
       
        
    #----------------------------------------------------------------------
    def initToolbar(self):
        """
        Initialize the toolbar
        """
        self.toolbar = self.CreateToolBar()
        self.toolbar.SetToolBitmapSize((16,16))
        
        open_ico = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, (16,16))
        openTool = self.toolbar.AddSimpleTool(wx.ID_ANY, open_ico, "Open", "Open an Image Directory")
        self.Bind(wx.EVT_MENU, self.onOpenDirectory, openTool)
        
        self.toolbar.Realize()
        
    #----------------------------------------------------------------------
    def onOpenDirectory(self, event):
        """
        Opens a DirDialog to allow the user to open a folder with pictures
        """
        dlg = wx.DirDialog(self, "Choose a directory",
                           style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.folderPath = dlg.GetPath()
            print (self.folderPath)
            picPaths = glob.glob(self.folderPath + "\\*.JPG")
            pp (picPaths)
        #pub.sendMessage("update images", msg=picPaths)
        #self.panel.updateImages(msg=picPaths)
        
    #----------------------------------------------------------------------
    def resizeFrame(self, msg):
        """"""
        self.sizer.Fit(self)
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = ViewerFrame()
    app.MainLoop()
    