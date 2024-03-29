import argparse

import numpy as np
from PIL import Image
from tqdm import tqdm


def cost(pixels_1, pixels_2):
    """
    Returns the cost between the two pixels arrays.

    :param pixels_1: Pixels array.
    :param pixels_2: Pixels array.
    :return: Cost between the sets of pixels.
    """
    return np.sum((pixels_1 - pixels_2) ** 2)


def sort_by_vector(pixels, vector):
    """
    Returns the sorted pixels array and the indices that would sort them.
    Sorts all pixels in the array according to their dot products with the vector, ie their projection on the
    vector.

    :param pixels: Pixels array to sort.
    :param vector: 3 dimensional vector.
    :return: Sorted pixels array, sorting indices array.
    """
    sorted_indexes = np.argsort(pixels.dot(vector))
    sorted_pixels = pixels[sorted_indexes]
    return sorted_pixels, sorted_indexes


def sort_and_cost(target_pixels, source_pixels, vector):
    """
    Returns the cost between the target and source that have been sorted by the vector.

    :param target_pixels: Pixels array to sort.
    :param source_pixels: Pixels array to sort.
    :param vector: 3 dimensional vector.
    :return: Cost between the sets of pixels.
    """
    sorted_target_pixels, _ = sort_by_vector(target_pixels, vector)
    sorted_source_pixels, _ = sort_by_vector(source_pixels, vector)
    return cost(sorted_target_pixels, sorted_source_pixels)


def find_best_vector(target_pixels, source_pixels):
    """
    Returns the vector that would sort the target and source pixels arrays with the lowest cost.

    :param target_pixels: Pixels array to sort.
    :param source_pixels: Pixels array to sort.
    :return: Best vector.
    """
    axis_vectors = np.identity(3)
    axis_vectors[[0, 2]] = axis_vectors[[2, 0]]
    axis_vectors[[1, 2]] = axis_vectors[[2, 1]]

    best_costs = np.array([sort_and_cost(target_pixels, source_pixels, vector) for vector in axis_vectors])
    best_vectors = np.zeros((3, 3))

    axis_strings = ['x', 'y', 'z']

    for axis in range(3):
        for angle in tqdm(range(1, 91), desc=f"Searching {axis_strings[axis]} angle"):
            rad = np.deg2rad(angle)

            vector = [np.cos(rad), np.sin(rad)]
            vector.insert(axis, 0)
            vector = np.array(vector, dtype=float)

            cost_ = sort_and_cost(target_pixels, source_pixels, vector)

            if cost_ < best_costs[axis]:
                best_costs[axis] = cost_
                best_vectors[axis] = vector
            else:
                break

    best_vector = np.sum(best_vectors, axis=0)
    best_vector /= np.linalg.norm(best_vector)  # converting to unit vector

    print(f"Best sorting vector: {np.round(best_vector, 2)}")
    return best_vector


def color_transfer(target_pixels, source_pixels):
    """
    Returns the resulting pixels array of a color transfer from the source pixels array to the target pixels array.

    :param target_pixels: Targeted pixels array, whose colors must change.
    :param source_pixels: Source pixels array, used as a palette.
    :return: Output pixels array.
    """
    # the best vector is the vector with the lowest associated cost,
    # we initialize it randomly with its associated pixels set
    best_vector = find_best_vector(target_pixels, source_pixels)

    _, sorting_indexes = sort_by_vector(target_pixels, best_vector)
    sorted_source_pixels, _ = sort_by_vector(source_pixels, best_vector)

    # reorganization of each pixel according to their corresponding pixel on target image
    output_pixels = np.zeros(sorted_source_pixels.shape).astype(int)
    output_pixels[sorting_indexes] = sorted_source_pixels

    return output_pixels


def main(target_file_name, source_file_name, output_file_name, show_output):
    """
    :param target_file_name: Target image file path.
    :param source_file_name: Source image file path.
    :param output_file_name: Output image file path.
    :param show_output: Shows preview of the output image at the end if true.
    """
    # loading images
    target_im = Image.open(target_file_name).convert("RGB")
    source_im = Image.open(source_file_name).convert("RGB")

    # the two images must be the same size
    if target_im.size[0] * target_im.size[1] != source_im.size[0] * source_im.size[1]:
        exit("The two images must have the same number of pixels.")

    # images conversion into pixels array
    print("Converting images into arrays...")
    target_pixels = np.array(target_im.getdata())
    source_pixels = np.array(source_im.getdata())

    # main program
    output_pixels = color_transfer(target_pixels, source_pixels)

    # converting pixels output to a new image
    output_pixels = np.reshape(output_pixels, (target_im.size[1], target_im.size[0], 3))
    output_im = Image.fromarray(output_pixels.astype(np.uint8))

    # saving
    output_im.save(output_file_name)
    print(f"Output saved in `{output_file_name}`")

    if show_output:
        output_im.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("target_image", type=str, help="Targeted image.")
    parser.add_argument("source_image", type=str, help="Source image.")
    parser.add_argument("-sa", "--save", type=str, default="output.jpg", help="Output file to save.")
    parser.add_argument("-sh", "--show", action="store_true", help="Preview the output at the end.")
    args = parser.parse_args()

    main(args.target_image, args.source_image, args.save, args.show)
