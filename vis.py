#!/usr/bin/env python3
import vaex
import ipyvolume as ipv
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
import argparse, sys, os

def getFileData(file):
    with open(file,"rb") as binFile:
        fileBytes = list(binFile.read())
    return fileBytes

def genCoords(data, dims = 2):
    data = np.asarray(data,dtype=np.ubyte)
    return np.lib.stride_tricks.sliding_window_view(data,dims,axis=0)

def genNdGrid(coords, dims = 2):
    grid = np.zeros((256,) * dims)
    for coord in coords:
        grid[tuple(coord)] += 1
    return grid

def mplPlot(data):
    plt.imshow(data, interpolation = 'none',cmap='hot',norm = LogNorm(), origin = "lower")
    ax = plt.gca()
    ax.set_facecolor("black")

def vaexPlot(data, dims = 2):
    df = vaex.from_arrays(d=data)
    if dims == 2:
        df.viz.heatmap(df.d[:,0],df.d[:,1], limits="99%", what = [np.log(vaex.stat.count()+1)])
    elif dims == 3:
        raise NotImplementedError("No 3D support from vaex yet")
        #df.plot_widget(df.d[:,0], df.d[:,1], df.d[:,2], what = [np.log(vaex.stat.count()+1)] )
        #ipv.quickscatter(df.d[:,0],df.d[:,1],df.d[:,2], size = 1, marker = "sphere")

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
    args = args.parse_args(argList)
    return args


def main(**args):
    dims = args.get('dimensions')
    for file in args.get('files'):
        fileBytes = getFileData(file)
        coords = genCoords(fileBytes,dims)
        if args.get('mode') in ['mpl','matplotlib']:
            grid = genNdGrid(coords, dims)
            mplPlot(grid)
        else:
            vaexPlot(coords, dims)
        beautifyPlot(file)
        plt.show()

if __name__ == '__main__':
    args = parseArgs(sys.argv[1::])
    main(**vars(args))
