from ROOT import *
from array import array
import numpy as np
import re

class plot:
    def __init__(self, name="Plot", path="", typ="graph", fits=[], color=kBlack, outfile="_plot.pdf"):
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
        self.canvasList=[]
        self.legendList=[]
        self.fit=[]
        self.errorList=[]
        self.peakList=[]
        self.xCal=1.
        self.xOffset=0.
        self.yCal=1.
        self.yOffset=0.
        self.xTitle='no title set'
        self.yTitle='no title set'
        self.sigmaList=[]
        self.sigmaErrList=[]
        self.x_min=0
        self.x_max=0
        self.margins=[0.3,0.07,0.07,0.1]
        
    def setXCal(self,val):
        self.xCal=val

    def setYCal(self,val):
        self.yCal=val
        
    def setXOffset(self,val):
        self.xOffset=val        

    def setYOffset(self,val):
        self.yOffset=val
        
    def setXTitle(self,val):
        self.xTitle=val
        
    def setYTitle(self,val):
        self.yTitle=val
        
    def addPath(self, pathstr):
        """sets flag multiData=True, converts self.path to list with path and adds new pathstring to this list"""
        if multidata==False:
            self.multiData=True
            self.path=[self.path]
        self.path.append(pathstr)
        
    def addFit(self, ftyp="lin", fxmin=-999, fxmax=999, findex=0, name='', col=kRed, par=[], fkt=""):
        """adds fit to plot, ftyp can be 'lin' for a linear fit, 'gaus' for gaussian fit or "own" for an own fit formula. fxmin and fxmax sets fitting range.
        findex is only used for multiData plots and points to the dataset"""
        self.fits.append([ftyp,fxmin,fxmax,findex,name,col,par,fkt])
        
    def addXarray(self, index, opt=''):
        """adds column from self.path with index to X-Values list (self.X)"""
        x_list=data_2_array(self.path, index)
        for i in range(len(x_list)):
            #exec("x_list[i]=self.xOffset+self.xCal*x_list[i]"+opt)
            #exec("x_list[i]=self.xCal*x_list[i]"+opt)
            #exec("x_list[i]=x_list[i]"+opt)
            exec("x_list[i]=self.xCal*(self.xOffset+x_list[i])"+opt)
        self.X.append(x_list)
    
    def addYarray(self, index, opt=''):
        """adds column from self.path with index to Y-Values list (self.Y)"""
        y_list=data_2_array(self.path, index)
        for i in range(len(y_list)):
            #exec("y_list[i]=self.yOffset+self.yCal*y_list[i]"+opt)
            #exec("y_list[i]=self.yCal*y_list[i]"+opt)
            #exec("y_list[i]=y_list[i]"+opt)
            exec("y_list[i]=self.yCal*(self.yOffset+y_list[i])"+opt)
        self.Y.append(y_list)
        
    def addEXarray(self, index, opt=''):
        """adds column from self.path with index to eX-Values list (self.eX). Opt may be used to compute the error, e.g. sqrt() for poisson errors"""
        ex_list=data_2_array(self.path, index)
        if opt == 'sqrt':
            for i in range(len(ex_list)):
                ex_list[i]=np.sqrt(ex_list[i])
        self.eX.append(ex_list)
        
    def addEYarray(self, index, opt=''):
        """adds column from self.path with index to eY-Values list (self.ey). Opt may be used to compute the error, e.g. sqrt() for poisson errors"""
        ey_list=data_2_array(self.path, index)
        if opt == 'sqrt':
            for i in range(len(ey_list)):
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
            #if not self.eX:
                #self.eX[0]=len(self.X)[0]*[0]
            #if not self.eY:
                #self.eY[0]=len(self.Y)[0]*[0]
            self.pltList.append(arrays_2_tgrapherrors(self.X,self.Y,self.eX,self.eY,self.name))
            
        if self.typ=='histo_bin':
            gStyle.SetOptStat(0)
            self.pltList.append(arrays_2_histBin(self.Y,self.xOffset,self.xCal,self.X,self.name))
            
        #implement histo functs
        
        for plt in self.pltList:
            self.canvasList.append(createCanvas(self.name,self.margins))
            self.canvasList[-1].SaveAs(self.outfile.replace(".pdf",".pdf["))
            self.legendList.append(create_legend(self.margins))
            print self.name,"plt=", plt
            self.legendList[-1].AddEntry3(plt[-1],str(self.name))
            plt[-1].GetXaxis().SetTitle(self.xTitle)
            plt[-1].GetYaxis().SetTitle(self.yTitle)
            if type(plt[-1])==TGraphErrors:
                plt[-1].Draw("AP")
            if type(plt[-1])==TH1F:
                plt[-1].Draw("E")
            #canvasList[-1].SaveAs(self.outfile)
            for fit in self.fits:
                if fit[0]=='lin':
                    if fit[4]=='':
                        fit[4]="linear_fit_"+self.fits.index(fit)
                    #fkt,grad,error=fit_lin(plt[-1],self.xOffset+self.xCal*fit[1],self.xOffset+self.xCal*fit[2])
                    #fkt,grad,error=fit_lin(plt[-1],self.xCal*fit[1],self.xCal*fit[2])
                    #fkt,grad,error=fit_lin(plt[-1],fit[1],fit[2])
                    fkt,grad,error=fit_lin(plt[-1],self.xCal*(self.xOffset+fit[1]),self.xCal*(self.xOffset+fit[2]))
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(grad)
                    self.errorList.append(error)
                    self.legendList[-1].AddEntry3(fkt,str(fit[4])+" ("+str(round(grad,2))+"+-%s)"%float("%.2g"%error))#"+str(round(error,2))+")x")
                    fkt.Draw("same")
            for fit in self.fits:
                if fit[0]=='gaus':
                    if fit[4]=='':
                        fit[4]="gaussian_fit_"+self.fits.index(fit)
                    #fkt,mean,error=fit_gaus(plt[-1],self.xOffset+self.xCal*fit[1],self.xOffset+self.xCal*fit[2],self.xOffset+self.xCal*fit[6],self.xOffset+self.xCal*fit[7],self.xOffset+self.xCal*fit[8])
                    #fkt,mean,error=fit_gaus(plt[-1],self.xCal*fit[1],self.xCal*fit[2],self.xCal*fit[6],self.xCal*fit[7],self.xCal*fit[8])
                    #fkt,mean,error=fit_gaus(plt[-1],fit[1],fit[2],fit[6],fit[7],fit[8])
                    fkt,mean,error=fit_gaus(plt[-1],self.xCal*(self.xOffset+fit[1]),self.xCal*(self.xOffset+fit[2]),self.xCal*(self.xOffset+fit[6]),self.xCal*(self.xOffset+fit[7]),self.xCal*(self.xOffset+fit[8]))
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(mean)
                    self.errorList.append(error)
                    self.legendList[-1].AddEntry3(fkt,str(fit[4])+"mean="+str(round(mean,2))+"+-%s"%float("%.2g"%error))#+str(round(error,2)))      
                    fkt.Draw("same")
            for fit in self.fits:
                if fit[0]=='neg_gaus':
                    if fit[4]=='':
                        fit[4]="gaussian_fit_"+self.fits.index(fit)
                    #fkt,mean,error=fit_neg_gaus(plt[-1],self.xOffset+self.xCal*fit[1],self.xOffset+self.xCal*fit[2],self.xOffset+self.xCal*fit[6],self.xOffset+self.xCal*fit[7],self.xOffset+self.xCal*fit[8],self.xOffset+self.xCal*fit[9])
                    #fkt,mean,error=fit_neg_gaus(plt[-1],self.xCal*fit[1],self.xCal*fit[2],self.xCal*fit[6],self.xOffset+self.xCal*fit[7],self.xCal*fit[8],self.xCal*fit[9])
                    #fkt,mean,error=fit_neg_gaus(plt[-1],fit[1],fit[2],fit[6],fit[7],fit[8],fit[9])
                    fkt,mean,error=fit_neg_gaus(plt[-1],self.xCal*(self.xOffset+fit[1]),self.xCal*(self.xOffset+fit[2]),self.xCal*(self.xOffset+fit[6]),self.xCal*(self.xOffset+fit[7]),self.xCal*(self.xOffset+fit[8]),self.xCal*(self.xOffset+fit[9]))
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(mean)
                    self.errorList.append(error)
                    self.sigmaList.append(fkt.GetParameter(3))
                    self.sigmaErrList.append(fkt.GetParError(3))
                    self.legendList[-1].AddEntry3(fkt,str(fit[4])+"mean="+str(round(mean,2))+"+-"+str(round(error,2)))      
                    fkt.Draw("same")
            for fit in self.fits:
                if fit[0]=='sqr':
                    if fit[4]=='':
                        fit[4]="quadratic_fit_"+self.fits.index(fit)
                    #fkt,mean,error=fit_sqr(plt[-1],self.xOffset+self.xCal*fit[1],self.xOffset+self.xCal*fit[2])
                    #fkt,mean,error=fit_sqr(plt[-1],self.xCal*fit[1],self.xCal*fit[2])
                    #fkt,mean,error=fit_sqr(plt[-1],fit[1],fit[2])
                    fkt,mean,error=fit_sqr(plt[-1],self.xCal*(self.xOffset+fit[1]),self.xCal*(self.xOffset+fit[2]))
                    self.peakList.append(mean)
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(mean)
                    self.errorList.append(error)
                    self.legendList[-1].AddEntry3(fkt,str(fit[4])+" peak "+str(round(mean,2)))      
                    fkt.Draw("same")                     
            for fit in self.fits:
                if fit[0]=='breitWig':
                    if fit[4]=='':
                        fit[4]="Breit-Wigner_fit_"+self.fits.index(fit)
                    #fkt,mean,error=fit_sqr(plt[-1],self.xOffset+self.xCal*fit[1],self.xOffset+self.xCal*fit[2])
                    #fkt,mean,error=fit_sqr(plt[-1],self.xCal*fit[1],self.xCal*fit[2])
                    #fkt,mean,error=fit_sqr(plt[-1],fit[1],fit[2])
                    fkt,mean,error=fit_sqr(plt[-1],self.xCal*(self.xOffset+fit[1]),self.xCal*(self.xOffset+fit[2]))
                    self.peakList.append(mean)
                    self.listOfFitFkts.append(fkt)
                    self.parList.append(mean)
                    self.errorList.append(error)
                    self.legendList[-1].AddEntry3(fkt,str(fit[4])+" peak "+str(round(mean,2)))      
                    fkt.Draw("same") 
            self.legendList[-1].Draw("same")
            self.canvasList[-1].SaveAs(self.outfile)
            self.canvasList[-1].SaveAs(self.outfile.replace(".pdf",".pdf]"))
            
    #not common implemented. change faktor and offset
    def saveFitResults_Tex(self, textfile, faktor=1, offset=0, anfang='', ende='\\\\\n'):
        os = ''
        for peak,error in zip(self.parList,self.errorList):
            n_peak=(peak-offset)*faktor
            n_error=error*faktor
            print "peak at",peak,"+-",error,"\n"
            os += anfang + str(round(peak,2)) + '&' + str(round(error,2)) + '&' + str(round(n_peak,3)) + '&' + str(round(n_error,3)) + ende
        tex = open(textfile,'w')
        tex.write(os)
        tex.close()
            
def create_legend(margins=[0.1,0.1,0.1,0.1]): 
    legend=TLegend()
    legend.SetX1NDC(1-margins[0])
    legend.SetX2NDC(1.)
    legend.SetY1NDC(1)
    legend.SetY2NDC(0.93)
    legend.SetBorderSize(0);
    legend.SetLineStyle(0);
    legend.SetTextFont(42);
    legend.SetTextSize(0.035);
    legend.SetFillStyle(0);
    return legend.Clone()

def createCanvas(name, margins=[0.1,0.1,0.1,0.1]):
    c=TCanvas(name,name,1920,1080)
    c.SetRightMargin(margins[0])
    c.SetTopMargin(margins[1])
    c.SetLeftMargin(margins[2])
    c.SetBottomMargin(margins[3])
    return c.Clone()        

def data_2_array(filepaths, index):
    """reads given files with messured values (x and y) and creates a list with arrays. filepaths=["path1","path2",...]"""
    x_arraylist=[]
    y_arraylist=[]
    if type(filepaths)==string:
        filepaths=[filepaths]
    for path in filepaths:
        f_in = open(path)
        print path
        x = []#array('f',[])
        #y = []#array('f',[])

        for row in f_in:
            r=row.split()
            x.append(float(r[index]))
            #y.append(float(r[1]))
        #x_arraylist.append(x)
        #y_arraylist.append(y)
        f_in.close()
    return x#_arraylist#, y_arraylist

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
            tmp.SetName(names)
            tmp.SetTitle(names)
        for n in range(len(x[i])):
            #X=x[i][n]
            #Y=y[i][n]
            #EX=ex[i][n]
            #EY=ey[i][n]
            #tmp.SetPoint(n,X,Y)
            #tmp.SetPointError(n,EX,EY)
            #print i, n
            #print x
            #print y
            tmp.SetPoint(n,x[i][n],y[i][n])
            tmp.SetPointError(n,ex[i][n],ey[i][n])
        graphlist.append(tmp)
    return graphlist

def arrays_2_histBin(y,xOffset,xCal,x=[],names=[]):
    """creates TH1F class for each data set. x are indices of bins, y are Binentries. x,y,ex,ey are lists of arrays. x=[array1,array2,...]. Returns list with TH1Fs"""
    histoList=[]
    for i in range(len(y)):
        if x==[]:
            nbins = len(y[i])
            bmin = (1+xOffset)*xCal
            bmax = (len(y[i])+xOffset)*xCal
        else:
            nbins = len(x[i])
            bmin = min(x[i])
            bmax = max(x[i])
        h= TH1F("h","h",nbins,bmin,bmax)
        tmp=h.Clone()
        for k in range(len(y[i])):
            if x==[]:
                tmp.SetBinContent(k,y[i][k])
            else:
                tmp.SetBinContent(x[i][k],y[i][k])
        if names==[]:
            tmp.SetName("Dataset_"+str(i))
            tmp.SetTitle("Dataset_"+str(i))
        else:
            tmp.SetName(names)
            tmp.SetTitle(names)
        histoList.append(tmp)
    return histoList
        

def draw_graphs(graphlist):
    c = TCanvas('c','c',800,600)
    for graph in graphlist:
        graph.Draw("AP SAME")
    raw_input()

def neg_gaus(x, par):
    # negative gaus distribution with offset
    f = par[0]+par[1]*np.exp(0.5*((x[0]-par[2])/(par[3]))**2) 
    return f

def fit_gaus(data, x_min, x_max, norm, mean, sigma):
    """fits a gaussian distribution to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, mean and error"""
    fkt = TF1("fkt","gaus",x_min,x_max)
    fkt.SetParameter(0,norm)
    fkt.SetParameter(1,mean)
    fkt.SetParameter(2,sigma)
    data.Fit("fkt","R")
    mean = fkt.GetParameter(1)
    error = fkt.GetParError(1)
    return fkt, mean, error

def fit_neg_gaus(data, x_min, x_max, offset, norm, mean, sigma):
    """fits a gaussian distribution to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, mean and error"""
    fkt = TF1("fkt",neg_gaus,x_min,x_max,4)
    fkt.SetParameter(0,offset)
    fkt.SetParameter(1,norm)
    fkt.SetParameter(2,mean)
    if sigma==0:
        sigma=1
    fkt.SetParameter(3,sigma)
    data.Fit("fkt","R")
    mean = fkt.GetParameter(2)
    error = fkt.GetParError(2)
    return fkt, mean, error

def fit_lin(data, x_min, x_max, par=[]):
    """fits a linear slope to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, gradient and error"""
    fkt = TF1("fkt","[0]*x+[1]",x_min,x_max)
    if (len(par)!=0):
        fkt.SetParameter(0,par[0])
        fkt.SetParameter(1,par[1])
    data.Fit("fkt","R")
    grad = fkt.GetParameter(0)
    error = fkt.GetParError(0)
    return fkt, grad, error

def fit_BW(data, x_min, x_max):
    """fits a linear slope to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, gradient and error"""
    fkt = TF1("fkt",BreitWig,x_min,x_max,5)
    width = fkt.GetParameter(0)          #width
    w_error = fkt.GetParamError(0)        
    mean = fkt.GetParameter(1)
    m_error = fkt.GetParamError(1)
    data.Fit("fkt","R")
    return fkt, width, w_error, mean, m_error

def fit_sqr(data, x_min, x_max):
    """fits a linear slope to a given data set. data must be a fitable ROOTObject (TH1F or TGraphErrors etc). x_min and x_max are cuts on the fitrange, returns the fitfunction, gradient and error"""
    fkt = TF1("fkt","[0]+[1]*x+[2]*x**2",x_min,x_max)
    data.Fit("fkt","R")
    par1 = fkt.GetParameter(1)
    par2 = fkt.GetParameter(2)
    er1 = fkt.GetParError(1)
    er2 = fkt.GetParError(2)
    print par1, par2
    peak=-par1/(2*par2)
    error = np.sqrt((er2/(2*par2))**2+((par1*er1)/(2*par2**2))**2)
    print 'peak at',peak,'+-',error
    return fkt, peak, error

def AddEntry3( self, histo, label, option='L'):
    self.SetY1NDC(self.GetY1NDC()-0.07)
    width=self.GetX2NDC()-self.GetX1NDC()
    print "width = ",width
    print "X1NDC = ",self.GetX1NDC()
    print "X2NDC = ",self.GetX2NDC()
    ts=self.GetTextSize()
    print "textsize=",ts
    neglen = 0
    sscripts = re.findall("_{.+?}|\^{.+?}",label)
    for s in sscripts:
	neglen = neglen + 3
    symbols = re.findall("#[a-zA-Z]+",label)
    for symbol in symbols:
	neglen = neglen + len(symbol)-1
    #label+=' ('+str(round(10*histo.Integral())/10.)+')'
    newwidth=max((len(label)-neglen)*0.005*0.05/ts+0.1,width) 
    if (newwidth>width):
        print "yeeees"
        ts=((len(label)-neglen)*0.005*0.05)/(newwidth-0.1)*width/newwidth
        self.SetTextSize(ts)
    nnewwidth=max((len(label)-neglen)*0.005*0.05/ts+0.1,width)  
    print "X1NDC = ",self.GetX1NDC()
    print "X2NDC = ",self.GetX2NDC()
    print "newwidth = ",newwidth
    print "newnewwidth = ",nnewwidth
    print "textsize=",ts
    #newwidth=max((len(label))*0.015*0.05/ts+0.1,width)
    #self.SetX1NDC(self.GetX2NDC()-nnewwidth)
    #self.SetX1NDC((histo.GetXaxis().GetXmax()-histo.GetXaxis().GetXmin())*1.05)
    #self.SetX2NDC(self.GetX1NDC()+width)
    #print (histo.GetXaxis().GetXmax()-histo.GetXaxis().GetXmin())*1.05
    self.AddEntry(histo, label, option)
TLegend.AddEntry3 = AddEntry3

def BreitWig(x, par):
    f = (par[0]/2.)*par[2]/((x[0] - par[1])*(x[0] - par[1]) + (par[0]/2.)*(par[0]/2.)) + bkg1(x, par)
    return f

def bkg1(x, par):
    # Simple background model with constant and linear term.
    return par[3] + par[4]*x[0]
