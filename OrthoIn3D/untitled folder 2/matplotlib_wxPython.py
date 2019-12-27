import wx
import random
 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import matplotlib.pyplot as plt
 
class p1(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()
     
    def plot(self):
        ''' plot some random stuff '''
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.hold(False)
        ax.plot(data, '*-')
        self.canvas.draw()    
       
 
class TestFrame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.sp = wx.SplitterWindow(self)
        self.p1 = p1(self.sp)
        self.p2 = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.p1,self.p2,470)
 
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText("Wow")
         
        self.plotbut = wx.Button(self.p2,-1,"plot", size=(40,20),pos=(160,10))
        self.plotbut.Bind(wx.EVT_BUTTON,self.plot)
         
        self.sibut = wx.Button(self.p2,-1,"Zoom", size=(40,20),pos=(60,10))
        self.sibut.Bind(wx.EVT_BUTTON,self.zoom)
         
        self.hmbut = wx.Button(self.p2,-1,"Home", size=(40,20),pos=(110,10))
        self.hmbut.Bind(wx.EVT_BUTTON,self.home)
         
        self.hibut = wx.Button(self.p2,-1,"Pan", size=(40,20),pos=(10,10))
        self.hibut.Bind(wx.EVT_BUTTON,self.pan)
         
    def zoom(self,event):
        self.statusbar.SetStatusText("Zoom")
        self.p1.toolbar.zoom()
 
    def home(self,event):
        self.statusbar.SetStatusText("Home")
        self.p1.toolbar.home()
         
    def pan(self,event):
        self.statusbar.SetStatusText("Pan")
        self.p1.toolbar.pan()
 
    def plot(self,event):
        self.p1.plot()       
 
app = wx.App(redirect=False)
frame = TestFrame(None,"Matplotlib and WxPython with Pan/Zoom functionality")
frame.Show()
app.MainLoop()