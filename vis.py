#!/usr/bin/env python3
import vaex
import ipyvolume as ipv
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import argparse, sys, os
import warnings

def getFileData(file):
    with open(file,"rb") as binFile:
        fileBytes = list(binFile.read())
    return fileBytes

def genCoords(data, dims = 2):
    data = np.asarray(data,dtype=np.ubyte)
    return np.lib.stride_tricks.sliding_window_view(data,dims,axis=0)

def genNdGrid(coords, dims = 2):
    grid = np.zeros((256,) * dims,dtype=np.ubyte)
    for coord in coords:
        grid[tuple(coord)] += 1
    return grid

def mplPlot(data):
    assert np.all(np.isfinite(data))
    im = plt.pcolormesh(data, cmap='hot',norm = LogNorm(), shading = "flat")
    cbar = plt.colorbar(im)
    cbar.set_label("Log(count)")
    ax = plt.gca()
    ax.set_facecolor("black")

def vaexPlot(data, dims = 2, isOutputFile = True):
    df = vaex.from_arrays(d=data)
    lim = "100%" if isOutputFile else "99%"
    if dims == 2:
        hm = df.viz.heatmap(df.d[:,0],df.d[:,1], limits=lim, what = [np.log(vaex.stat.count()+1)], colorbar = isOutputFile)
    elif dims == 3:
        raise NotImplementedError("No 3D support from vaex yet")
        #df.plot_widget(df.d[:,0], df.d[:,1], df.d[:,2], what = [np.log(vaex.stat.count()+1)] )
        #ipv.quickscatter(df.d[:,0],df.d[:,1],df.d[:,2], size = 1, marker = "sphere")
    else:
        raise ValueError("Too many dimensions")

def streamlinePlot():
    ax = plt.gca()
    im = ax.collections
    for i in im:
        cb = i.colorbar
        if cb is None:
            continue
        cb.remove()
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(left=False, bottom=False,
                   labelleft=False,labelbottom=False)
    fig = ax.get_figure()
    fig.tight_layout()
    fig.subplots_adjust(top=1.0,
                        bottom= 0.0,
                        left = 0.0,
                        right = 1.0)
    fig.set_size_inches(4,4,forward=True)


def beautifyPlot(file):
    ax = plt.gca()
    fig = ax.get_figure()
    fig.tight_layout()
    fig.subplots_adjust(top=0.95)
    fig.subplots_adjust(bottom=0.05)
    ax.set_title(f"{os.path.basename(file)}")
    ax.set_xlabel("")
    ax.set_ylabel("")

def parseArgs(argList):
    args = argparse.ArgumentParser(description="Binary visualizer")
    args.add_argument(metavar="File",dest='files',nargs='+',help="Files to plot")
    args.add_argument("--dimensions","-d",type=int,default=2,choices=[2,3],help="Number of dimensions to visualize binary in")
    args.add_argument("--mode","-m",default="mpl",choices=["matplotlib","mpl","vaex","v"],help="Visualization mode/library to use")
    args.add_argument("--outputfile","-o",help="File to output image to")
    args = args.parse_args(argList)
    return args


def main(**args):
    dims = args.get('dimensions')
    for file in args.get('files'):
        fileBytes = getFileData(file)
        coords = genCoords(fileBytes,dims)
        displayingResults = args.get('outputfile') is None
        if args.get('mode') in ['mpl','matplotlib']:
            grid = genNdGrid(coords, dims)
            mplPlot(grid)
        else:
            vaexPlot(coords, dims, displayingResults)

        if displayingResults:
            beautifyPlot(file)
            plt.show()
        else:
            streamlinePlot()
            #plt.show()
            plt.savefig(args.get('outputfile'),
                        bbox_inches='tight',
                        dpi = 64,
                        pad_inches=0)

if __name__ == '__main__':
    args = parseArgs(sys.argv[1::])
    main(**vars(args))
