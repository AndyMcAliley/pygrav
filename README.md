# README #

### What is this repository for? ###

PyGrav is a toy for playing with the 2D gravity problem. It allows you to change a density model in the directions of the singular vectors of the sensitivity matrix, and view the effect on the data. Recently added 3D modeling capability.

### How do I get set up? ###

Get the code:
```
git clone https://github.com/AndyMcAliley/pygrav.git
```


Run the code:
```
python toy.py
```

Use it for gravity modeling:
copy grav.py to your project
``` python
import grav
G = grav.sens3d(x_nodes,y_nodes,z_nodes,observation_locations)
```
For more details, see the grav_example.ipynb notebook.
