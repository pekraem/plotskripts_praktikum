from ROOT import *
from array import array
import numpy as np


class plot:
    def __init__(self, name="Plot", path, typ="graph", fits=[], color=kBlack, outfile="_plot.pdf"):
        """Initialise a new instance of 'plot' class with attributes:
        -name: name and title of the plot
        -path ist a string with path of data, to plot more than one dataset in the same plot, use 'addPath'
        -typ can be graph (TGraphErrors), hist (TH1F - normaly filled), hist_bin (TH1F - set bin by bin)
        -fit is a list with all fits, shape: [["type",xmin="",xmax=""],[...]...], better use 'addFit'
        -color can be used to change the color of the datapoints"""
        self.name=name
        if path!='':
            self.path=path
        else:
            print "no plot without path!"
        self.typ=typ
        self.fits=fits
        self.color=color
        self.outfile=self.name+outfile
        self.multiData=False                #flag for multiple Datasets
        
        self.listOfFitFkts=[]
    
    def addPath(self, pathstr):
        """sets flag multiData=True, converts self.path to list with path and adds new pathstring to this list"""
        if multidata==False:
            self.multiData=True
            self.path=[self.path]
        self.path.append(pathstr)
        
    def addFit(self, ftyp="lin", fxmin=-999, fxmax=999, findex=0):
        """adds fit to plot, ftyp can be 'lin' for a linear fit or 'gaus' for gaussian fit. fxmin and fxmax sets fitting range.
        findex is only used for multiData plots and points to the dataset"""
        self.fit.append([ftyp,fxmin,fxmax,findex])
        
    def setName(self,name):
        self.name=name
        
    def setTyp(self, typ):
        self.typ=typ
    
    def setOutfile(self, outpath):
        self.outfile=outpath
        
    def executePlot(self):
        if self.typ=='graph':
            
        

def data_2_array(filepaths, index):
    """reads given files with messured values (x and y) and creates a list with arrays. filepaths=["path1","path2",...]"""
    x_arraylist=[]
    y_arraylist=[]
    if type(filepaths)==string:
        filepaths=[filepaths]
    for path in filepaths:
        f_in = open(path)
        x = []#array('f',[])
        #y = []#array('f',[])

        for row in f_in:
            r=row.split()
            x.append(float(r[index]))
            #y.append(float(r[1]))
        x_arraylist.append(x)
        #y_arraylist.append(y)
        f_in.close()
    return x_arraylist#, y_arraylist

def arrays_2_tgrapherrors(x,y,ex=[],ey=[],names=[]):
    """creates TGraphErrors class for each data set. x are x-coordinates of datapoints, y are y-coordinates of datapoints. ex are x-errors, ey are y-errors (both optional). x,y,ex,ey are lists of arrays. x=[array1,array2,...]. Returns list with TGraphErrors"""
    g = TGraphErrors()
    g.SetMarkerStyle(8)
    g.SetMarkerSize(0.5)
    graphlist = []
    for i in range(len(x)):
        tmp = g.Clone()
        if ex==[]:
            ex = [[] for i in range(len(x))]
            ex[i]=[0.1]*len(x[i])
        if ey==[]:
            ey=[[] for i in range(len(x))]
            ey[i]=[0.1]*len(x[i])
        if names==[]:
            tmp.SetName("Dataset_"+str(i))
            tmp.SetTitle("Dataset_"+str(i))
        else:
            tmp.SetName(names[i])
            tmp.SetTitle(names[i])
        for n in range(len(x[i])):
            #X=x[i][n]
            #Y=y[i][n]
            #EX=ex[i][n]
            #EY=ey[i][n]
            #tmp.SetPoint(n,X,Y)
            #tmp.SetPointError(n,EX,EY)
            tmp.SetPoint(n,x[i][n],y[i][n])
            tmp.SetPointError(n,ex[i][n],ey[i][n])
        graphlist.append(tmp)
    return graphlist

def draw_graphs(graphlist):
    c = TCanvas('c','c',800,600)
    for graph in graphlist:
        graph.Draw("AP SAME")
    raw_input()
    

def fit_gaus(data, x_min, x_max):
    """fits a gaussian distribution to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, mean and error"""
    fkt = TF1("fkt","gaus",x_min,x_max)
    data.Fit("fkt","R")
    mean = fkt.GetParameter(1)
    error = fkt.GetParError(1)
    return fkt, mean, error

def fit_lin(data, x_min, x_max):
    """fits a linear slope to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, gradient and error"""
    fkt = TF1("fkt","[0]*x+[1]",x_min,x_max)
    grad = fkt.GetParameter(0)
    error = fkt.GetParamError(0)
    data.fit("fkt","R")
    return fkt, grad, error