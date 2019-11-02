import wx
import wx.lib.imagebrowser as imagebrowser
import Image
import ImageFilter
import ImageEnhance

class MenuExample(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1050, 650))
        #self.CreateStatusBar()
        self.control = wx.ScrolledWindow(self,-1)
        self.pict = "untitled.jpg"
        self.bmp = wx.Image(self.pict,wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        wx.StaticBitmap(self.control, -1, self.bmp)
        self.control.SetScrollbars(20, 20, 55, 40)
       
        menubar = wx.MenuBar()
        file = wx.Menu()
        about = wx.MenuItem(file,1, '&About\tCtrl+A')
       
        quit = wx.MenuItem(file, 2, '&Quit\tCtrl+Q')
        color = wx.MenuItem(file,3, '&color\tCtrl+C')
        tools = wx.MenuItem(file,4,'&toolbox\tCtrl+t')


        file.AppendItem(quit)
        file.AppendItem(about)
        file.AppendItem(color)
        file.AppendItem(tools)
       
       
        self.Bind(wx.EVT_MENU, self.OnQuit, id=2)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=1)
        self.Bind(wx.EVT_MENU, self.OnColor, id=3)
        self.Bind(wx.EVT_MENU, self.OnImage, id=4)
       
        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)

        self.Centre()
        self.Show(True)

    def OnQuit(self, event):
        self.Close()

    def OnAbout(self,event):
        d = wx.MessageDialog(self, "Simple editor created by varsha", "About simple editor", wx.OK)
        d.ShowModal()
        d.Destroy()
    def OnColor(self,event):
        dialog = imagebrowser.ImageDialog(self, set_dir = 'c:\MS\thesis\python')
        if dialog.ShowModal()== wx.ID_OK:
            print "you selected file:" + dialog.GetFile()
        dialog.Destroy()

    def OnImage(self,event):
        toolbar = self.CreateToolBar()

       # use appropriate icon files in the folder

        toolbar.AddSimpleTool(101, wx.Bitmap('zoomin.png'), 'Zoomin','')
        toolbar.AddSimpleTool(102, wx.Bitmap('zoomout.png'), 'Zoomout','')

 

        toolbar.AddSimpleTool(103, wx.Bitmap('undo.png'),'Rotate clockwise','')
       
        toolbar.Realize()
        self.Bind(wx.EVT_TOOL, self.OnQuit, id=101)
        self.Bind(wx.EVT_TOOL, self.OnRotate, id=103)

    def OnRotate(self,event):
        im1 = Image.open(self.pict)
        im11=im1.rotate(90)
        ext = ".jpg"
        im11.save("rotate" + ext)

        try:
           
           
            self.control = wx.ScrolledWindow(self,-1)
            self.bmp = wx.Image('rotate.jpg',wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
            wx.StaticBitmap(self.control, -1, self.bmp)
        except:
            print "exception"
            self.Close()
       

app = wx.App()
MenuExample(None, -1, 'Menubar')
app.MainLoop()