# Binary Visualization

## Requirements
This project requires several dependencies:
- `matplotlib`
- `numpy`
- `vaex` (optional, but you have to comment out the import)
- `ipyvolume` (optional, required for 3D visualization)
- `jupyter` (optional, required for 3D visualization)

## Background
This project is heavily inspired by [CantorDust](https://github.com/Battelle/cantordust), but is written in Python as a standalone visualizer instead of a Ghidra plugin. I can't take credit for the idea, but I extended it into 3 dimensions using [ipyvolume](https://ipyvolume.readthedocs.io/en/latest/). 

## Usage
### 2D
This project somes with a commandline tool/library `vis.py`. To do simple 2D visualization using matplotlib, try `./vis.py [File to visualize]`. It supports multiple backends including plain `numpy` as well as `vaex`, which is overkill but I thought it was an interesting library to try out. For more information on running the CLI tool, simply run `./vis.py -h`. 
<p align="center">
  <img width=300 height=300 alt="Placeholder for 2d img" src="" />
</p>



### 3D
To visualize a binary in 3D, `jupyter` is required. Start up a jupyter notebook with `jupyter notebook` and open the `volume-render.ipynb` file.
<p align="center">
  <img width=300 height=300 alt="Placeholder for 3d img" src="" />
</p>

