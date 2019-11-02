from wxPython.lib.evtmgr import eventManager
  aButton = wxButton(somePanel, -1, 'Click me')
  eventManager.Register(self.someMethod, EVT_BUTTON, aButton)