# Color transfer by one-dimensional optimal transport

A color transfer consists of giving the colors of a source image to a target image.<br>
Here, a pixel of the source can be used only one time.<br>
The operation then boils down to rearranging the pixels of the source image to make it resemble the target image as 
closely as possible.

## Packages

- [numpy](https://pypi.org/project/numpy/) ```pip install numpy```
- [pillow](https://pypi.org/project/Pillow/) ```pip install pillow```
- [tqmd](https://pypi.org/project/tqdm/) ```pip install tqmd```

## Usage example

```python color_transfer.py space.jpg sky.jpg -sa output.jpg -sh```<br>
The colors of sky.jpg will be transferred to space.jpg, the output image will be stored inside output.jpg,
and a preview of the output will be show at the end of the execution.

Inputs

<img src="space.jpg" width="320" alt="target_img"/> <img src="sky.jpg" width="320" alt="source_img"/>

Output

<img src="output.jpg" width="640" alt="output_img"/>
