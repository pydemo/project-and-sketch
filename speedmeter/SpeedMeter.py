# --------------------------------------------------------------------------- #
# SPEEDMETER Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 25 Sep 2005
# Latest Revision: 10 Oct 2005, 22.40 CET
#
#
# TODO List/Caveats
#
# 1. Combination Of The Two Styles:
#
#    SM_DRAW_PARTIAL_FILLER
#    SM_DRAW_SECTORS
#
#    Does Not Work Very Well. It Works Well Only In Case When The Sector Colours
#    Are The Same For All Intervals.
#
#
# Thanks To Gerard Grazzini That Has Tried The Demo On MacOS, I Corrected A
# Bug On Line 246
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@agip.it
# andrea_gavan@tin.it
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #
import sys, math
from pprint import pprint as pp
e=sys.exit
xrange = range

"""Description:

SpeedMeter Tries To Reproduce The Behavior Of Some Car Controls (But Not Only),
By Creating An "Angular" Control (Actually, Circular). I Remember To Have Seen
It Somewhere, And I Decided To Implement It In wxPython.

SpeedMeter Starts Its Construction From An Empty Bitmap, And It Uses Some
Functions Of The wx.DC Class To Create The Rounded Effects. Everything Is
Processed In The Draw() Method Of SpeedMeter Class.

This Implementation Allows You To Use Either Directly The wx.PaintDC, Or The
Better (For Me) Double Buffered Style With wx.BufferedPaintDC. The Double
Buffered Implementation Has Been Adapted From The wxPython Wiki Example:

http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing


Usage:

SpeedWindow1 = SM.SpeedMeter(parent,
                             bufferedstyle,
                             extrastyle,
                             mousestyle
                             )

None Of The Options (A Part Of Parent Class) Are Strictly Required, If You
Use The Defaults You Get A Very Simple SpeedMeter. For The Full Listing Of
The Input Parameters, See The SpeedMeter __init__() Method.


Methods And Settings:

SpeedMeter Is Highly Customizable, And In Particular You Can Set:

- The Start And End Angle Of Existence For SpeedMeter;
- The Intervals In Which You Divide The SpeedMeter (Numerical Values);
- The Corresponding Thicks For The Intervals;
- The Interval Colours (Different Intervals May Have Different Filling Colours);
- The Ticks Font And Colour;
- The Background Colour (Outsize The SpeedMeter Region);
- The External Arc Colour;
- The Hand (Arrow) Colour;
- The Hand's Shadow Colour;
- The Hand's Style ("Arrow" Or "Hand");
- The Partial Filler Colour;
- The Number Of Secondary (Intermediate) Ticks;
- The Direction Of Increasing Speed ("Advance" Or "Reverse");
- The Text To Be Drawn In The Middle And Its Font;
- The Icon To Be Drawn In The Middle;
- The First And Second Gradient Colours (That Fills The SpeedMeter Control);
- The Current Value.

For More Info On Methods And Initial Styles, Please Refer To The __init__()
Method For SpeedMeter Or To The Specific Functions.


SpeedMeter Control Is Freeware And Distributed Under The wxPython License. 

Latest Revision: Andrea Gavana @ 10 Oct 2005, 22.40 CET

"""

#----------------------------------------------------------------------
# Beginning Of SPEEDMETER wxPython Code
#----------------------------------------------------------------------

import wx
import wx.lib.colourdb
import wx.lib.fancytext as fancytext

from math import pi, sin, cos, log, sqrt, atan2

#----------------------------------------------------------------------
# DC Drawing Options
#----------------------------------------------------------------------
# SM_NORMAL_DC Uses The Normal wx.PaintDC
# SM_BUFFERED_DC Uses The Double Buffered Drawing Style

SM_NORMAL_DC = 0
SM_BUFFERED_DC = 1

#----------------------------------------------------------------------
# SpeedMeter Styles
#----------------------------------------------------------------------
# SM_ROTATE_TEXT: Draws The Ticks Rotated: The Ticks Are Rotated
#                 Accordingly To The Tick Marks Positions
# SM_DRAW_SECTORS: Different Intervals Are Painted In Differend Colours
#                  (Every Sector Of The Circle Has Its Own Colour)
# SM_DRAW_PARTIAL_SECTORS: Every Interval Has Its Own Colour, But Only
#                          A Circle Corona Is Painted Near The Ticks
# SM_DRAW_HAND: The Hand (Arrow Indicator) Is Drawn
# SM_DRAW_SHADOW: A Shadow For The Hand Is Drawn
# SM_DRAW_PARTIAL_FILLER: A Circle Corona That Follows The Hand Position
#                         Is Drawn Near The Ticks
# SM_DRAW_SECONDARY_TICKS: Intermediate (Smaller) Ticks Are Drawn Between
#                          Principal Ticks
# SM_DRAW_MIDDLE_TEXT: Some Text Is Printed In The Middle Of The Control
#                      Near The Center
# SM_DRAW_MIDDLE_ICON: An Icon Is Drawn In The Middle Of The Control Near
#                      The Center
# SM_DRAW_GRADIENT: A Gradient Of Colours Will Fill The Control
# SM_DRAW_FANCY_TICKS: With This Style You Can Use XML Tags To Create
#                      Some Custom Text And Draw It At The Ticks Position.
#                      See wx.lib.fancytext For The Tags.

SM_ROTATE_TEXT = 1
SM_DRAW_SECTORS = 2
SM_DRAW_PARTIAL_SECTORS = 4
SM_DRAW_HAND = 8
SM_DRAW_SHADOW = 16
SM_DRAW_PARTIAL_FILLER = 32
SM_DRAW_SECONDARY_TICKS = 64
SM_DRAW_MIDDLE_TEXT = 128
SM_DRAW_MIDDLE_ICON = 256
SM_DRAW_GRADIENT = 512
SM_DRAW_FANCY_TICKS = 1024

#----------------------------------------------------------------------
# Event Binding
#----------------------------------------------------------------------
# SM_MOUSE_TRACK: The Mouse Left Click/Drag Allow You To Change The
#                 SpeedMeter Value Interactively

SM_MOUSE_TRACK = 1


fontfamily = range(70, 78)
familyname = ["default", "decorative", "roman", "script", "swiss", "modern", "teletype"]

weights = range(90, 93)
weightsname = ["normal", "light", "bold"]

styles = [90, 93, 94]
stylesname = ["normal", "italic", "slant"]

#----------------------------------------------------------------------
# BUFFERENDWINDOW Class
# This Class Has Been Taken From The wxPython Wiki, And Slightly
# Adapted To Fill My Needs. See:
#
# http://wiki.wxpython.org/index.cgi/DoubleBufferedDrawing
#
# For More Info About DC And Double Buffered Drawing.
#----------------------------------------------------------------------

class BufferedWindow(wx.Window):

    """

    A Buffered window class.

    To use it, subclass it and define a Draw(DC) method that takes a DC
    to draw to. In that method, put the code needed to draw the picture
    you want. The window will automatically be double buffered, and the
    screen will be automatically updated when a Paint event is received.

    When the drawing needs to change, you app needs to call the
    UpdateDrawing() method. Since the drawing is stored in a bitmap, you
    can also save the drawing to file by calling the
    SaveToFile(self,file_name,file_type) method.

    """


    def __init__(self, parent, id,
                 pos = wx.DefaultPosition,
                 size = wx.DefaultSize,
                 style=wx.NO_FULL_REPAINT_ON_RESIZE,
                 bufferedstyle=SM_BUFFERED_DC):
        
        wx.Window.__init__(self, parent, id, pos, size, style)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)

        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None)
        

    def Draw(self, dc):
        ## just here as a place holder.
        ## This method should be over-ridden when sub-classed
        pass


    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        
        if self._bufferedstyle == SM_BUFFERED_DC:
            dc = wx.BufferedPaintDC(self, self._Buffer)
        else:
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self._Buffer,0,0)


    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        self.Width, self.Height = self.GetClientSize()

        # Make new off screen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.

        # This seems required on MacOS, it doesn't like wx.EmptyBitmap with
        # size = (0, 0)
        # Thanks to Gerard Grazzini
        
        if "__WXMAC__" in wx.Platform:
            if self.Width == 0:
                self.Width = 1
            if self.Height == 0:
                self.Height = 1
        print (self.Width, self.Height)
        if 1:
            filepath = 'test.JPG'
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

            img = img.Scale(self.Width, self.Height)
            
      
            
            
        
        
       
            self._Buffer = wx.Bitmap(img)
        else:
            
            
            self._Buffer = wx.Bitmap(self.Width, self.Height)
        self.UpdateDrawing()


    def UpdateDrawing(self):
        """
        This would get called if the drawing needed to change, for whatever reason.

        The idea here is that the drawing is based on some data generated
        elsewhere in the system. IF that data changes, the drawing needs to
        be updated.

        """

        if self._bufferedstyle == SM_BUFFERED_DC:
            dc = wx.BufferedDC(wx.ClientDC(self), self._Buffer)
            self.Draw(dc)
        else:
            # update the buffer
            dc = wx.MemoryDC()
            dc.SelectObject(self._Buffer)

            self.Draw(dc)
            ## update the screen
            wx.ClientDC(self).Blit(0, 0, self.Width, self.Height, dc, 0, 0)
        

#----------------------------------------------------------------------
# SPEEDMETER Class
# This Is The Main Class Implementation. See __init__() Method For
# Details.
#----------------------------------------------------------------------

class SpeedMeter(BufferedWindow):
    
    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, extrastyle=SM_DRAW_HAND,
                 bufferedstyle=SM_BUFFERED_DC,
                 mousestyle=0, interval=10):
        """ Default Class Constructor.

        Non Standard wxPython Parameters Are:

        a) extrastyle: This Value Specifies The SpeedMeter Styles:
           - SM_ROTATE_TEXT: Draws The Ticks Rotated: The Ticks Are Rotated
                             Accordingly To The Tick Marks Positions;
           - SM_DRAW_SECTORS: Different Intervals Are Painted In Differend Colours
                              (Every Sector Of The Circle Has Its Own Colour);
           - SM_DRAW_PARTIAL_SECTORS: Every Interval Has Its Own Colour, But Only
                                      A Circle Corona Is Painted Near The Ticks;
           - SM_DRAW_HAND: The Hand (Arrow Indicator) Is Drawn;
           - SM_DRAW_SHADOW: A Shadow For The Hand Is Drawn;
           - SM_DRAW_PARTIAL_FILLER: A Circle Corona That Follows The Hand Position
                                     Is Drawn Near The Ticks;
           - SM_DRAW_SECONDARY_TICKS: Intermediate (Smaller) Ticks Are Drawn Between
                                      Principal Ticks;
           - SM_DRAW_MIDDLE_TEXT: Some Text Is Printed In The Middle Of The Control
                                  Near The Center;
           - SM_DRAW_MIDDLE_ICON: An Icon Is Drawn In The Middle Of The Control Near
                                  The Center;
           - SM_DRAW_GRADIENT: A Gradient Of Colours Will Fill The Control;
           - SM_DRAW_FANCY_TICKS: With This Style You Can Use XML Tags To Create
                                  Some Custom Text And Draw It At The Ticks Position.
                                  See wx.lib.fancytext For The Tags.

        b) bufferedstyle: This Value Allows You To Use The Normal wx.PaintDC Or The
                          Double Buffered Drawing Options:
           - SM_NORMAL_DC Uses The Normal wx.PaintDC;
           - SM_BUFFERED_DC Uses The Double Buffered Drawing Style.

        c) mousestyle: This Value Allows You To Use The Mouse To Change The SpeedMeter
                       Value Interactively With Left Click/Drag Events:

           - SM_MOUSE_TRACK: The Mouse Left Click/Drag Allow You To Change The
                             SpeedMeter Value Interactively.

        """

        self._extrastyle = extrastyle
        self._bufferedstyle = bufferedstyle
        self._mousestyle = mousestyle
        self.interval=interval

        if self._extrastyle & SM_DRAW_SECTORS and self._extrastyle & SM_DRAW_GRADIENT:
            errstr = "\nERROR: Incompatible Options: SM_DRAW_SECTORS Can Not Be Used In "
            errstr = errstr + "Conjunction With SM_DRAW_GRADIENT."
            raise errstr

        if self._extrastyle & SM_DRAW_PARTIAL_SECTORS and self._extrastyle & SM_DRAW_SECTORS:
            errstr = "\nERROR: Incompatible Options: SM_DRAW_SECTORS Can Not Be Used In "
            errstr = errstr + "Conjunction With SM_DRAW_PARTIAL_SECTORS."
            raise errstr

        if self._extrastyle & SM_DRAW_PARTIAL_SECTORS and self._extrastyle & SM_DRAW_PARTIAL_FILLER:
            errstr = "\nERROR: Incompatible Options: SM_DRAW_PARTIAL_SECTORS Can Not Be Used In "
            errstr = errstr + "Conjunction With SM_DRAW_PARTIAL_FILLER."
            raise Exception(errstr)       

        if self._extrastyle & SM_DRAW_FANCY_TICKS and self._extrastyle & SM_ROTATE_TEXT:
            errstr = "\nERROR: Incompatible Options: SM_DRAW_FANCY_TICKS Can Not Be Used In "
            errstr = errstr + "Conjunction With SM_ROTATE_TEXT."
            raise Exception(errstr)

        if self._extrastyle & SM_DRAW_SHADOW and self._extrastyle & SM_DRAW_HAND == 0:
            errstr = "\nERROR: Incompatible Options: SM_DRAW_SHADOW Can Be Used Only In "
            errstr = errstr + "Conjunction With SM_DRAW_HAND."
            
        if self._extrastyle & SM_DRAW_FANCY_TICKS:
            wx.lib.colourdb.updateColourDB()
            
        
        self.SetAngleRange()
        #e()
        self.SetIntervals()
        self.SetSpeedValue()
        self.SetIntervalColours()
        #self.SetArcColour()
        #self.SetTicks()
        #self.SetTicksFont()
        #self.SetTicksColour()
        #self.SetSpeedBackground()
        #self.SetHandColour()
        #self.SetShadowColour()
        self.SetFillerColour()
        self.SetDirection()
        #self.SetNumberOfSecondaryTicks()
        #self.SetMiddleText()
        #self.SetMiddleTextFont()
        #self.SetMiddleTextColour()
        #self.SetFirstGradientColour()
        #self.SetSecondGradientColour()
        #self.SetHandStyle()
        #self.DrawExternalArc()
        
        BufferedWindow.__init__(self, parent, id, pos, size,
                                style=wx.NO_FULL_REPAINT_ON_RESIZE,
                                bufferedstyle=bufferedstyle)

        if self._mousestyle & SM_MOUSE_TRACK:
            self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseMotion)
                    
        
    def Draw(self, dc):
        """ Draws Everything On The Empty Bitmap.

        Here All The Chosen Styles Are Applied. """
        
        size  = self.GetClientSize()
        #print(size, 222222)
        if size.x < 21 or size.y < 21:
            return

        new_dim = size.Get()
        
        if not hasattr(self, "dim"):
            self.dim = new_dim

        self.scale = min([float(new_dim[0]) / self.dim[0],
                          float(new_dim[1]) / self.dim[1]])

        # Create An Empty Bitmap
        if 1:
            filepath = 'test.JPG'
            img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

            img = img.Scale(size.width, size.height)
            
      
            
            
        
        
       
            self.faceBitmap = wx.Bitmap(img)
        else:
            self.faceBitmap = wx.Bitmap(size.width, size.height)
        
        #dc.BeginDrawing()

        #   speedbackground = self.GetSpeedBackground()
        # Set Background Of The Control        
        #dc.SetBackground(wx.Brush(speedbackground))
        #dc.Clear()

        centerX = self.faceBitmap.GetWidth()/2
        centerY = self.faceBitmap.GetHeight()/2

        self.CenterX = centerX
        self.CenterY = centerY

        # Get The Radius Of The Sector. Set It A Bit Smaller To Correct Draw After
        radius = min(centerX, centerY) - 2

        self.Radius = radius        

        # Get The Angle Of Existance Of The Sector
        anglerange = self.GetAngleRange()
        #pp(anglerange)
        #pp(self._anglerange)
        #e()
        startangle = anglerange[1]
        #startangle=math.pi/2
        endangle = anglerange[0]
        #endangle = endangle*2
        self.StartAngle = startangle
        self.EndAngle = endangle

        # Initialize The Colours And The Intervals - Just For Reference To The
        # Children Functions
        colours = None
        intervals = None

        if self._extrastyle & SM_DRAW_SECTORS or self._extrastyle & SM_DRAW_PARTIAL_SECTORS:
            # Get The Intervals Colours        
            colours = self.GetIntervalColours()[:]

        textangles = []
        colourangles = []
        xcoords = []
        ycoords = []

        # Get The Intervals (Partial Sectors)
        intervals = self.GetIntervals()[:]

        start = min(intervals)
        end = max(intervals)
        span = end - start

        self.StartValue = start
        self.EndValue = end
        
        self.Span = span
            
        # Get The Current Value For The SpeedMeter
        currentvalue = self.GetSpeedValue() #+ 7*(10/self.interval)

        # Get The Direction Of The SpeedMeter
        direction = self.GetDirection()
        if direction == "Reverse":
            intervals.reverse()

            if self._extrastyle & SM_DRAW_SECTORS or self._extrastyle & SM_DRAW_PARTIAL_SECTORS:
                colours.reverse()

            currentvalue = end - currentvalue

        # This Because DrawArc Does Not Draw Last Point
        offset = 0.1*self.scale/180     

        xstart, ystart = self.CircleCoords(radius+1, -endangle, centerX, centerY)
        xend, yend = self.CircleCoords(radius+1, -startangle-offset, centerX, centerY)
        
        #startangle=0
        # Calculate The Angle For The Current Value Of SpeedMeter
        accelangle = (currentvalue - start)/float(span)*(startangle-endangle) - startangle
        print('accelangle = ' ,accelangle, currentvalue)
        dc.SetPen(wx.TRANSPARENT_PEN)

        if self._extrastyle & SM_DRAW_PARTIAL_FILLER:
            if 1:
                r=170.0
                # Get Some Data For The Partial Filler
                fillercolour = self.GetFillerColour()                
                fillerendradius = radius - r*self.scale
                fillerstartradius = radius
                
                if direction == "Advance":
                    fillerstart = accelangle
                    fillerend = -startangle
                else:
                    fillerstart = -endangle
                    fillerend = accelangle

                #xs1, ys1 = self.CircleCoords(fillerendradius, fillerstart, centerX, centerY)
                #xe1, ye1 = self.CircleCoords(fillerendradius, fillerend, centerX, centerY)
                xs2, ys2 = self.CircleCoords(fillerstartradius, fillerstart, centerX, centerY)
                xe2, ye2 = self.CircleCoords(fillerstartradius, fillerend, centerX, centerY)

                # Get The Sector In Which The Current Value Is
                intersection = self.GetIntersection(currentvalue, intervals)
                sectorradius = radius - r*self.scale
            
        else:
            
            sectorradius = radius


            

        # This Is Needed To Fill The Partial Sector Correctly
        #xold, yold = self.CircleCoords(radius, startangle+endangle, centerX, centerY)
        if 1:
            # Draw The Sectors        
            for ii, interval in enumerate(intervals):

                if direction == "Advance":
                    current = interval - start
                else:
                    current = end - interval
                
                angle = (current/float(span))*(startangle-endangle) - startangle            
                angletext = -((pi/2.0) + angle)*180/pi
                textangles.append(angletext)
                colourangles.append(angle)
                xtick, ytick = self.CircleCoords(radius, angle, centerX, centerY)
                
                # Keep The Coordinates, We Will Need Them After To Position The Ticks            
                xcoords.append(xtick)
                ycoords.append(ytick)
                x = xtick
                y = ytick
                if 1:
                    if self._extrastyle & SM_DRAW_SECTORS:                
                        if self._extrastyle & SM_DRAW_PARTIAL_FILLER:
                            if direction == "Advance":
                                if current > currentvalue:
                                    x, y = self.CircleCoords(radius, angle, centerX, centerY)                    
                                else:
                                    x, y = self.CircleCoords(sectorradius, angle, centerX, centerY)
                            if 0:
                                if current < end - currentvalue:
                                    x, y = self.CircleCoords(radius, angle, centerX, centerY)                    
                                else:
                                    x, y = self.CircleCoords(sectorradius, angle, centerX, centerY)
                        #else:
                        #    x, y = self.CircleCoords(radius, angle, centerX, centerY)
                        

                if ii > 0 :
                    if self._extrastyle & SM_DRAW_PARTIAL_FILLER and ii == intersection:
                        # We Got The Interval In Which There Is The Current Value. If We Choose
                        # A "Reverse" Direction, First We Draw The Partial Sector, Next The Filler

                        dc.SetBrush(wx.Brush(speedbackground))
                        if 0:
                            if direction == "Reverse":
                                if self._extrastyle & SM_DRAW_SECTORS:
                                    dc.SetBrush(wx.Brush(colours[ii-1]))
                                    
                                dc.DrawArc(xe2, ye2, xold, yold, centerX, centerY)
                        
                        if 0:
                            if self._extrastyle & SM_DRAW_SECTORS:
                                dc.SetBrush(wx.Brush(colours[ii-1]))
                            else:
                                dc.SetBrush(wx.Brush(speedbackground))

                                                
                        #dc.DrawArc(xs1, ys1, xe1, ye1, centerX, centerY)
                        if 0:
                            if self._extrastyle & SM_DRAW_SECTORS:
                                dc.SetBrush(wx.Brush(colours[ii-1]))
                                # Here We Draw The Rest Of The Sector In Which The Current Value Is
                                if direction == "Advance":
                                    dc.DrawArc(xs1, ys1, x, y, centerX, centerY)
                                    x = xs1
                                    y = ys1
                                else:
                                    dc.DrawArc(xe2, ye2, x, y, centerX, centerY)
                            
                    elif self._extrastyle & SM_DRAW_SECTORS:
                        dc.SetBrush(wx.Brush(colours[ii-1]))
                        if 1:
                            # Here We Still Use The SM_DRAW_PARTIAL_FILLER Style, But We Are Not
                            # In The Sector Where The Current Value Resides
                            if self._extrastyle & SM_DRAW_PARTIAL_FILLER and ii != intersection:
                                if direction == "Advance":
                                    dc.DrawArc(x, y, xold, yold, centerX, centerY)
                                else:
                                    if ii < intersection:
                                        dc.DrawArc(x, y, xold, yold, centerX, centerY)

                            # This Is The Case Where No SM_DRAW_PARTIAL_FILLER Has Been Chosen
                            else:
                                dc.DrawArc(x, y, xold, yold, centerX, centerY)

                else:
                    if 1:
                        if self._extrastyle & SM_DRAW_PARTIAL_FILLER and self._extrastyle & SM_DRAW_SECTORS:
                            dc.SetBrush(wx.Brush(fillercolour))                
                            dc.DrawArc(xs2, ys2, xe2, ye2, centerX, centerY)
                            x, y = self.CircleCoords(sectorradius, angle, centerX, centerY)
                            #dc.SetBrush(wx.Brush(colours[ii]))
                            #dc.DrawArc(xs1, ys1, xe1, ye1, centerX, centerY)
                            x = xs2
                            y = ys2
                
                xold = x
                yold = y

        

  

    def SetIntervals(self, intervals=None):
        """ Sets The Intervals For SpeedMeter (Main Ticks Numeric Values)."""

        if intervals is None:
            intervals = [0, 50, 100]

        self._intervals = intervals


    def GetIntervals(self):
        """ Gets The Intervals For SpeedMeter. """
        
        return self._intervals
        

    def SetSpeedValue(self, value=None):
        """ Sets The Current Value For SpeedMeter. """
        #self._speedvalue = -10
        #return
        if value is None:
            value = (max(self._intervals) - min(self._intervals))/2.0
        else:
            if value < min(self._intervals):
                raise "\nERROR: Value Is Smaller Than Minimum Element In Points List"
                return
            elif value > max(self._intervals):
                raise "\nERROR: Value Is Greater Than Maximum Element In Points List"
                return
            
        self._speedvalue = value
        print('self._speedvalue = ', self._speedvalue)
        try:
            self.UpdateDrawing()
        except:
            pass
        

    def GetSpeedValue(self):
        """ Gets The Current Value For SpeedMeter. """

        return self._speedvalue
    

    def SetAngleRange(self, start=0, end=pi):
        """ Sets The Range Of Existence For SpeedMeter.

        This Values *Must* Be Specifiend In RADIANS.
        """
        
        self._anglerange = [start, end]


    def GetAngleRange(self):
        """ Gets The Range Of Existence For SpeedMeter.

        The Returned Values Are In RADIANS.
        """
        
        return self._anglerange        
        

    def SetIntervalColours(self, colours=None):
        """ Sets The Colours For The Intervals.

        Every Intervals (Circle Sector) Should Have A Colour.
        """
        
        if colours is None:
            if not hasattr(self, "_anglerange"):
                errstr = "\nERROR: Impossible To Set Interval Colours,"
                errstr = errstr + " Please Define The Intervals Ranges Before."
                raise Exception (errstr)
                return
            
            colours = [wx.WHITE]*len(self._intervals)
        else:
            if len(colours) != len(self._intervals) - 1:
                errstr = "\nERROR: Length Of Colour List Does Not Match Length"
                errstr = errstr + " Of Intervals Ranges List."
                raise Exception (errstr)
                return

        self._intervalcolours = colours
        

    def GetIntervalColours(self):
        """ Gets The Colours For The Intervals."""
        
        if hasattr(self, "_intervalcolours"):
            return self._intervalcolours
        else:
            raise "\nERROR: No Interval Colours Have Been Defined"


    def SetTicks(self, ticks=None):
        """ Sets The Ticks For SpeedMeter Intervals (Main Ticks String Values)."""
        
        if ticks is None:
            if not hasattr(self, "_anglerange"):
                errstr = "\nERROR: Impossible To Set Interval Ticks,"
                errstr = errstr + " Please Define The Intervals Ranges Before."
                raise errstr
                return

            ticks = []
            
            for values in self._intervals:
                ticks.append(str(values))
                
        else:
            if len(ticks) != len(self._intervals):
                errstr = "\nERROR: Length Of Ticks List Does Not Match Length"
                errstr = errstr + " Of Intervals Ranges List."
                raise errstr
                return

        self._intervalticks = ticks
            

    def GetTicks(self):
        """ Gets The Ticks For SpeedMeter Intervals (Main Ticks String Values)."""
        
        if hasattr(self, "_intervalticks"):
            return self._intervalticks
        else:
            raise "\nERROR: No Interval Ticks Have Been Defined"


    def SetTicksFont(self, font=None):
        """ Sets The Ticks Font."""
        
        if font is None:
            self._originalfont = [wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, False)]
            self._originalsize = 10
        else:
            self._originalfont = [font]
            self._originalsize = font.GetPointSize()


    def GetTicksFont(self):
        """ Gets The Ticks Font."""
        
        return self._originalfont[:], self._originalsize
        

    def SetTicksColour(self, colour=None):
        """ Sets The Ticks Colour."""
        
        if colour is None:
            colour = wx.BLUE

        self._tickscolour = colour


    def GetTicksColour(self):
        """ Gets The Ticks Colour."""
        
        return self._tickscolour
    

    def SetSpeedBackground(self, colour=None):
        """ Sets The Background Colour Outside The SpeedMeter Control."""
        
        if colour is None:
            colour = wx.WHITE #SystemSettings.GetColour(0)
        colour = wx.WHITE
        self._speedbackground = colour


    def GetSpeedBackground(self):
        """ Gets The Background Colour Outside The SpeedMeter Control."""

        return self._speedbackground        


    def SetHandColour(self, colour=None):
        """ Sets The Hand (Arrow Indicator) Colour."""
        
        if colour is None:
            colour = wx.RED

        self._handcolour = colour


    def GetHandColour(self):
        """ Gets The Hand (Arrow Indicator) Colour."""
        
        return self._handcolour
        

    def SetArcColour(self, colour=None):
        """ Sets The External Arc Colour (Thicker Line)."""
        
        if colour is None:
            colour = wx.BLACK

        self._arccolour = colour


    def GetArcColour(self):
        """ Gets The External Arc Colour."""
        
        return self._arccolour        


    def SetShadowColour(self, colour=None):
        """ Sets The Hand's Shadow Colour."""
        
        if colour is None:
            colour = wx.Colour(150, 150, 150)

        self._shadowcolour = colour


    def GetShadowColour(self):
        """ Gets The Hand's Shadow Colour."""
        
        return self._shadowcolour        


    def SetFillerColour(self, colour=None):
        """ Sets The Partial Filler Colour.

        A Circle Corona Near The Ticks Will Be Filled With This Colour, From
        The Starting Value To The Current Value Of SpeedMeter.
        """
        
        if colour is None:
            colour = wx.Colour(255, 150, 50)
        colour = wx.Colour(255, 255, 255)

        self._fillercolour = colour


    def GetFillerColour(self):
        """ Gets The Partial Filler Colour."""
        
        return self._fillercolour
    

    def SetDirection(self, direction=None):
        """ Sets The Direction Of Advancing SpeedMeter Value.

        Specifying "Advance" Will Move The Hand In Clock-Wise Direction (Like Normal
        Car Speed Control), While Using "Reverse" Will Move It CounterClock-Wise
        Direction.
        """
        
        if direction is None:
            direction = "Advance"

        if direction not in ["Advance", "Reverse"]:
            raise '\nERROR: Direction Parameter Should Be One Of "Advance" Or "Reverse".'
            return

        self._direction = direction


    def GetDirection(self):
        """ Gets The Direction Of Advancing SpeedMeter Value."""

        return self._direction

    
    def SetNumberOfSecondaryTicks(self, ticknum=None):
        """ Sets The Number Of Secondary (Intermediate) Ticks. """
        
        if ticknum is None:
            ticknum = 3

        if ticknum < 1:
            raise "\nERROR: Number Of Ticks Must Be Greater Than 1."
            return
        
        self._secondaryticks = ticknum


    def GetNumberOfSecondaryTicks(self):
        """ Gets The Number Of Secondary (Intermediate) Ticks. """
        
        return self._secondaryticks            


    def SetMiddleText(self, text=None):
        """ Sets The Text To Be Drawn Near The Center Of SpeedMeter. """
        
        if text is None:
            text = ""

        self._middletext = text


    def GetMiddleText(self):
        """ Gets The Text To Be Drawn Near The Center Of SpeedMeter. """
        
        return self._middletext


    def SetMiddleTextFont(self, font=None):
        """ Sets The Font For The Text In The Middle."""
        
        if font is None:
            self._middletextfont = wx.Font(1, wx.SWISS, wx.NORMAL, wx.BOLD, False)
            self._middletextsize = 10.0
            self._middletextfont.SetPointSize(self._middletextsize)
        else:
            self._middletextfont = font
            self._middletextsize = font.GetPointSize()
            self._middletextfont.SetPointSize(self._middletextsize)


    def GetMiddleTextFont(self):
        """ Gets The Font For The Text In The Middle."""
        
        return self._middletextfont, self._middletextsize
    

    def SetMiddleTextColour(self, colour=None):
        """ Sets The Colour For The Text In The Middle."""
        
        if colour is None:
            colour = wx.BLUE

        self._middlecolour = colour


    def GetMiddleTextColour(self):
        """ Gets The Colour For The Text In The Middle."""
        
        return self._middlecolour
    

    def SetMiddleIcon(self, icon):
        """ Sets The Icon To Be Drawn Near The Center Of SpeedMeter. """
        
        if icon.Ok():
            self._middleicon = icon
        else:
            raise "\nERROR: Invalid Icon Passed To SpeedMeter."


    def GetMiddleIcon(self):
        """ Gets The Icon To Be Drawn Near The Center Of SpeedMeter. """
        
        return self._middleicon        


    def GetMiddleIconDimens(self):
        """ Used Internally. """
        
        return self._middleicon.GetWidth(), self._middleicon.GetHeight()        
        

    def CircleCoords(self, radius, angle, centerX, centerY):
        """ Used Internally. """
        
        x = radius*cos(angle) + centerX
        y = radius*sin(angle) + centerY
        
        return x, y


    def GetIntersection(self, current, intervals):
        """ Used Internally. """

        if self.GetDirection() == "Reverse":
            interval = intervals[:]
            interval.reverse()
        else:
            interval = intervals
            
        indexes = range(len(intervals))
        try:
            intersection = [ind for ind in indexes if interval[ind] <= current <= interval[ind+1]]
        except:
            if self.GetDirection() == "Reverse":
                intersection = [len(intervals) - 1]
            else:
                intersection = [0]

        return intersection[0]


    def SetFirstGradientColour(self, colour=None):
        """ Sets The First Gradient Colour (Near The Ticks). """
        
        if colour is None:
            colour = wx.Colour(145, 220, 200)
        colour = wx.Colour(255, 255, 255)
        self._firstgradientcolour = colour

        
    def GetFirstGradientColour(self):
        """ Gets The First Gradient Colour (Near The Ticks). """
        
        return self._firstgradientcolour


    def SetSecondGradientColour(self, colour=None):
        """ Sets The Second Gradient Colour (Near The Center). """
        
        if colour is None:
            colour = wx.WHITE

        self._secondgradientcolour = colour

        
    def GetSecondGradientColour(self):
        """ Gets The First Gradient Colour (Near The Center). """
        
        return self._secondgradientcolour


    def SetHandStyle(self, style=None):
        """ Sets The Style For The Hand (Arrow Indicator).

        By Specifying "Hand" SpeedMeter Will Draw A Polygon That Simulates The Car
        Speed Control Indicator. Using "Arrow" Will Force SpeedMeter To Draw A
        Simple Arrow. """
        
        if style is None:
            style = "Hand"

        if style not in ["Hand", "Arrow"]:
            raise '\nERROR: Hand Style Parameter Should Be One Of "Hand" Or "Arrow".'
            return

        self._handstyle = style


    def GetHandStyle(self):
        """ Sets The Style For The Hand (Arrow Indicator)."""
        
        return self._handstyle        
        

    def DrawExternalArc(self, draw=True):
        """ Specify Wheter Or Not You Wish To Draw The External (Thicker) Arc. """
        
        self._drawarc = draw


    def OnMouseMotion(self, event):
        """ Handles The Mouse Events.

        Here Only Left Clicks/Drags Are Involved. Should SpeedMeter Have Something More?
        """
        
        mousex = event.GetX()
        mousey = event.GetY()

        if event.Leaving():
            return

        pos = self.GetClientSize()
        size = self.GetPosition()
        centerX = self.CenterX
        centerY = self.CenterY

        direction = self.GetDirection()

        if event.LeftIsDown():
            
            angle = atan2(float(mousey) - centerY, centerX - float(mousex)) + pi - self.EndAngle
            if angle >= 2*pi:
                angle = angle - 2*pi

            if direction == "Advance":
                currentvalue = (self.StartAngle - self.EndAngle - angle)*float(self.Span)/(self.StartAngle - self.EndAngle) + self.StartValue
            else:
                currentvalue = (angle)*float(self.Span)/(self.StartAngle - self.EndAngle) + self.StartValue
                
            if currentvalue >= self.StartValue and currentvalue <= self.EndValue:
                self.SetSpeedValue(currentvalue)
                        
        event.Skip()
        

    def GetSpeedStyle(self):
        """ Returns A List Of Strings And A List Of Integers Containing The Styles. """
        
        stringstyle = []
        integerstyle = []
        
        if self._extrastyle & SM_ROTATE_TEXT:
            stringstyle.append("SM_ROTATE_TEXT")
            integerstyle.append(SM_ROTATE_TEXT)

        if self._extrastyle & SM_DRAW_SECTORS:
            stringstyle.append("SM_DRAW_SECTORS")
            integerstyle.append(SM_DRAW_SECTORS)

        if self._extrastyle & SM_DRAW_PARTIAL_SECTORS:
            stringstyle.append("SM_DRAW_PARTIAL_SECTORS")
            integerstyle.append(SM_DRAW_PARTIAL_SECTORS)

        if self._extrastyle & SM_DRAW_HAND:
            stringstyle.append("SM_DRAW_HAND")
            integerstyle.append(SM_DRAW_HAND)

        if self._extrastyle & SM_DRAW_SHADOW:
            stringstyle.append("SM_DRAW_SHADOW")
            integerstyle.append(SM_DRAW_SHADOW)

        if self._extrastyle & SM_DRAW_PARTIAL_FILLER:
            stringstyle.append("SM_DRAW_PARTIAL_FILLER")
            integerstyle.append(SM_DRAW_PARTIAL_FILLER)

        if self._extrastyle & SM_DRAW_SECONDARY_TICKS:
            stringstyle.append("SM_DRAW_SECONDARY_TICKS")
            integerstyle.append(SM_DRAW_SECONDARY_TICKS)

        if self._extrastyle & SM_DRAW_MIDDLE_TEXT:
            stringstyle.append("SM_DRAW_MIDDLE_TEXT")
            integerstyle.append(SM_DRAW_MIDDLE_TEXT)
        
        if self._extrastyle & SM_DRAW_MIDDLE_ICON:
            stringstyle.append("SM_DRAW_MIDDLE_ICON")
            integerstyle.append(SM_DRAW_MIDDLE_ICON)

        if self._extrastyle & SM_DRAW_GRADIENT:
            stringstyle.append("SM_DRAW_GRADIENT")
            integerstyle.append(SM_DRAW_GRADIENT)
        
        if self._extrastyle & SM_DRAW_FANCY_TICKS:
            stringstyle.append("SM_DRAW_FANCY_TICKS")
            integerstyle.append(SM_DRAW_FANCY_TICKS)


        return stringstyle, integerstyle

