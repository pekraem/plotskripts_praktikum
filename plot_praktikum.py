from ROOT import *
from array import array
import numpy as np

def data_2_array(filepaths):
    """reads given files with messured values (x and y) and creates lists with arrays. filepaths=["path1","path2",...]"""
    x_arraylist=[]
    y_arraylist=[]
    for path in filepaths:
        f_in = open(path)
        x = []#array('f',[])
        y = []#array('f',[])

        for row in f_in:
            r=row.split()
            x.append(float(r[0]))
            y.append(float(r[1]))
        x_arraylist.append(x)
        y_arraylist.append(y)
        f_in.close()
    return x_arraylist, y_arraylist

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