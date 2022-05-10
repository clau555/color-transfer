# Color transfer using one-dimensional optimal transport

A color transfer consists of giving the colors of a source image to a target image.<br>
Here, a pixel of the source can be used only one time, and the two images must be of the same area.<br>
The operation then boils down to rearranging the pixels of the source image to make it resemble the target image as 
closely as possible.

## Requirements

```
pip install -r requirements.txt
```

- [numpy](https://pypi.org/project/numpy/) ```pip install numpy```
- [pillow](https://pypi.org/project/Pillow/) ```pip install pillow```
- [tqmd](https://pypi.org/project/tqdm/) ```pip install tqmd```

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
python color_transfer.py space.jpg sky.jpg -sa output.jpg -sh
```
The colors of `sky.jpg` will be transferred to `space.jpg`, the output image will be stored inside `output.jpg`,
and a preview of the output will be show at the end of the execution.

### Inputs

![space](space.jpg)
![sky](sky.jpg)

### Output

![output](output.jpg)

## Method

The transfer is made by sorting each image pixels according to their dot product with a certain vector.
The two sorted lists of the source and target are then compared to make each pixel of same rank correspond to each 
other.
The source can then be rearranged according to these correspondences.

To find the vector that would sort them best, the goal is to rotate a vector in all the positive directions and find the 
one with the lowest associated cost.
The search would be done by finding the three angles components of the vector.
For each x, y and z angle, we start with a unit vector of 0° rotation around the current angle axis, and then compute
its associated cost.
Then, we increment the angle by 1°, and repeat the process until 90° at maximum.
If at some point, the cost becomes higher than the previous one, meaning that we have found an optimal angle, we stop 
the search and return the previous angle.
Once each angle is found, we compute the unit vector corresponding to these angles, which is the best vector.