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
        self.X=[]
        self.Y=[]
        self.eX=[]
        self.eY=[]
        self.listOfFitFkts=[]
        #self.histoList=[]
        self.pltList=[]
        self.parList=[]
        
    
    def addPath(self, pathstr):
        """sets flag multiData=True, converts self.path to list with path and adds new pathstring to this list"""
        if multidata==False:
            self.multiData=True
            self.path=[self.path]
        self.path.append(pathstr)
        
    def addFit(self, ftyp="lin", fxmin=-999, fxmax=999, findex=0, name='', col=kRed):
        """adds fit to plot, ftyp can be 'lin' for a linear fit or 'gaus' for gaussian fit. fxmin and fxmax sets fitting range.
        findex is only used for multiData plots and points to the dataset"""
        self.fit.append([ftyp,fxmin,fxmax,findex])
        
    def addXarray(self, index):
        """adds column from self.path with index to X-Values list (self.X)"""
        x_list=data_2_array(self.path, index)
        self.X.append(x_list)
    
    def addYarray(self, index):
        """adds column from self.path with index to Y-Values list (self.Y)"""
        y_list=data_2_array(self.path, index)
        self.X.append(y_list)
        
    def addEXarray(self, index, opt=''):
        """adds column from self.path with index to eX-Values list (self.eX). Opt may be used to compute the error, e.g. sqrt() for poisson errors"""
        ex_list=data_2_array(self.path, index)
        if opt == 'sqrt':
            for i in range(len(ex_list)):
                ex_list[i]=np.sqrt(ex_list[i])
        self.X.append(ex_list)
        
    def addEYarray(self, index, opt=''):
        """adds column from self.path with index to eY-Values list (self.ey). Opt may be used to compute the error, e.g. sqrt() for poisson errors"""
        ey_list=data_2_array(self.path, index)
        if opt == 'sqrt':
            for i in range(len(ex_list)):
                ey_list[i]=np.sqrt(ey_list[i])
        self.eY.append(ey_list)
        
    def setName(self,name):
        self.name=name
        
    def setTyp(self, typ):
        self.typ=typ
    
    def setOutfile(self, outpath):
        self.outfile=outpath
        
    def executePlot(self):
        if self.typ=='graph':
            if !=self.eX[0]:
                self.eX[0]=len(self.X)[0]*[0]
            if !=self.eY[0]:
                self.eY[0]=len(self.Y)[0]*[0]
            self.pltList.append(arrays_2_tgrapherrors(self.X,self.Y,self.eX,self.eY))
            
        #implement histo functs
        
        for plt in self.pltList:
            self.canvasList.append(createCanvas(self.name))
            canvasList[-1].SaveAs(self.outfile.replace(".pdf",".pdf["))
            self.legendList.append(create_legend())
            self.legendList[-1].AddEntry(plt,self.name)
            plt.Draw()
            #canvasList[-1].SaveAs(self.outfile)
            for fit in self.fits:
                if fit[0]=='lin':
                    if fit[4]=='':
                        fit[4]="linear_fit_"+self.fits.index(fit)
                    fkt,grad,error=fit_lin(plt,fit[1],fit[2])
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(grad)
                    self.errorList.append(error)
                    self.legendList[-1].AddEntry(fkt,fit[4]+" ("+round(grad,2)+"+-"+round(error,2)+")x")
                    fkt.Draw("same")
            for fit in self.fits:
                if fit[0]=='gaus':
                    if fit[4]=='':
                        fit[4]="gaussian_fit_"+self.fits.index(fit)
                    fkt,mean,error=fit_gaus(plt,fit[1],fit[2])
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(mean)
                    self.errorList.append(error)
                    self.legendList[-1].AddEntry(fkt,fit[4]+"mean="+round(mean,2)+"+-"+round(error,2))      
                    fkt.Draw("same")
            self.legendList[-1].Draw("same")
            canvasList[-1].SaveAs(self.outfile)
            canvasList[-1].SaveAs(self.outfile.replace(".pdf",".pdf]"))
            
def create_legend(): 
    legend=TLegend()
    legend.SetX1NDC(0.85)
    legend.SetX2NDC(0.95)
    legend.SetY1NDC(0.92)
    legend.SetY2NDC(0.93)
    legend.SetBorderSize(0);
    legend.SetLineStyle(0);
    legend.SetTextFont(42);
    legend.SetTextSize(0.05);
    legend.SetFillStyle(0);
    return legend.Clone()

def createCanvas(name)
    c=TCanvas(name,name,1024,768)
    c.SetRightMargin(0.05)
    c.SetTopMargin(0.05)
    c.SetLeftMargin(0.15)
    c.SetBottomMargin(0.15)
    return c.Clone()        

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