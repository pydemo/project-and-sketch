import wx
from pubsub import pub
 
 
class OtherFrame(wx.Frame):
    """"""
 
    def __init__(self):
        """Constructor"""
        super().__init__(None, title="Secondary Frame")
        panel = wx.Panel(self)
 
        msg = "Enter a Message to send to the main frame"
        instructions = wx.StaticText(panel, label=msg)
        self.msg_txt = wx.TextCtrl(panel, value="")
        close_btn = wx.Button(panel, label="Send and Close")
        close_btn.Bind(wx.EVT_BUTTON, self.on_send_and_slose)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        flags = wx.ALL|wx.CENTER
        sizer.Add(instructions, 0, flags, 5)
        sizer.Add(self.msg_txt, 0, flags, 5)
        sizer.Add(close_btn, 0, flags, 5)
        panel.SetSizer(sizer)
 
    def on_send_and_slose(self, event):
        """
        Send a message and close frame
        """
        msg = self.msg_txt.GetValue()
        pub.sendMessage("panel_listener", message=msg)
        pub.sendMessage("panel_listener", message="test2",
                        arg2="2nd argument!")
        self.Close()
 
 
class MyPanel(wx.Panel):
    """"""
 
    def __init__(self, parent):
        """Constructor"""
        super().__init__(parent)
        pub.subscribe(self.my_listener, "panel_listener")
 
        btn = wx.Button(self, label="Open Frame")
        btn.Bind(wx.EVT_BUTTON, self.on_open_frame)
 
    def my_listener(self, message, arg2=None):
        """
        Listener function
        """
        print(f"Received the following message: {message}")
        if arg2:
            print(f"Received another arguments: {arg2}")
 
    def on_open_frame(self, event):
        """
        Opens secondary frame
        """
        frame = OtherFrame()
        frame.Show()
 
 
class MyFrame(wx.Frame):
    """"""
 
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None,
                          title="New PubSub API Tutorial")
        panel = MyPanel(self)
        self.Show()
 
 
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()    