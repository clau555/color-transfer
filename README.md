# Color transfer

A color transfer consists of giving the colors of a source image to a target image.  
**Here, a pixel of the source can be used only one time, and the two images must have the same area.**  
The operation then boils down to rearranging the pixels of the source image to make it resemble the target image as 
closely as possible.

## Requirements

```
pip install -r requirements.txt
```

- [numpy](https://pypi.org/project/numpy/) ```pip install numpy```
- [pillow](https://pypi.org/project/Pillow/) ```pip install pillow```
- [tqdm](https://pypi.org/project/tqdm/) ```pip install tqdm```

## Use

```
positional arguments:
  target_image          Targeted image.
  source_image          Source image.

optional arguments:
  -h, --help            show this help message and exit
  -sa SAVE, --save SAVE
                        Output file to save.
  -sh, --show           Preview the output at the end.
```

## Example

```
python color_transfer.py inputs/space.jpg intputs/sky.jpg -sa outputs/output.jpg -sh
```
The colors of `sky.jpg` will be transferred to `space.jpg`, the output image will be stored inside `output.jpg` in the
outputs' directory, and a preview of the output will be show at the end of the execution.

### Inputs

![space](inputs/space.jpg)
![sky](inputs/sky.jpg)

### Output

![output](outputs/output.jpg)

## Method

### One-dimensional optimal transport

The transfer is made by sorting each image pixels according to their dot product with a certain vector.
The two sorted lists of the source and target are then compared to make each pixel of same rank correspond to each 
other.
The source can then be rearranged according to these correspondences.

### Optimal vector search

To find the vector that would sort them best, the goal is to rotate a vector in all the positive directions and find the 
one with the lowest associated cost.  
The search would be done by finding the three angles components of the vector.
For each x, y, z unit vectors, we increment them by an angle of 1° and look at their associated cost.
We repeat the process until 90° in the worst case.
If at some point, the cost becomes higher than the previous one, we stop the search and return the previous vector.  
Once each component vector is found, we compute the corresponding unit vector, which is the best vector.

Ultimately, the precision of the result vector depends on the angle precision that is incremented at each steps.
But increasing the angle precision will also increase the computation time.
