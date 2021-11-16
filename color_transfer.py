import sys
import numpy as np
from PIL import Image
from tqdm import tqdm


def sorted_pixels_from_vector(pixels, vector):
    """
    Returns the sorted pixels array and the indices that would sort them.\n
    Sorts all pixels in the pixels array according to their dot products with the vector,
    ie their projection on the vector.\n
    :param pixels: Pixels array to sort.
    :param vector: 3 dimensional vector.
    :return: The sorted pixels array, and the sorting indices array.
    """
    sorted_indexes = np.argsort(pixels.dot(vector))
    sorted_pixels = pixels[sorted_indexes]
    return sorted_pixels, sorted_indexes


def cost(pixels_1, pixels_2):
    """
    Returns the cost between two array of pixels.\n
    The cost is the sum of all the distances separating each corresponding pixels between the two sets.\n
    The distance between two pixels is their difference squared.\n
    :param pixels_1: Pixels array.
    :param pixels_2: Pixels array.
    :return: The cost between the two sets.
    """
    return np.sum((pixels_1 - pixels_2) ** 2)


def random_transport_draw(target_pixels, source_pixels):
    """
    Returns the cost of a transport between the two pixel sets, determined randomly by a vector.\n
    Returns also the sorted source pixels set, with its sorted indexes.\n
    :param target_pixels: Targeted image pixels array.
    :param source_pixels: Source image pixels array.
    :return: Tuple composed of
    the cost of the transport between the two pixels sets,
    pixels set sorted according to a random vector,
    and sorted indices of the the pixel set.
    """
    vector = np.random.rand(3)
    sorted_target_pixels, sorted_indexes = sorted_pixels_from_vector(target_pixels, vector)
    sorted_source_pixels = sorted_pixels_from_vector(source_pixels, vector)[0]
    transport_cost = cost(sorted_target_pixels, sorted_source_pixels)
    return transport_cost, sorted_source_pixels, sorted_indexes


def color_transfer(target_pixels, source_pixels, n=40):
    """
    Returns the resulting pixel array of a color transfer from the source pixel array to the target pixel array.\n
    :param target_pixels: Targeted pixels array, whose colors must change.
    :param source_pixels: Source pixels array, used as a palette.
    :param n: Number of random transport to try.
    :return: Output pixels array.
    """

    print("initialization")

    # the best vector is the vector with the lowest associated cost,
    # we initialize it randomly with its associated pixels set
    best_cost, best_sorted_pixels, best_sorted_indexes = random_transport_draw(target_pixels, source_pixels)

    for _ in tqdm(range(n), desc="processing"):
        current_cost, current_sorted_pixels, current_sorted_indexes = random_transport_draw(target_pixels, source_pixels)

        if current_cost < best_cost:
            best_cost = current_cost
            best_sorted_pixels = current_sorted_pixels
            best_sorted_indexes = current_sorted_indexes

    # reorganization of each pixels according to their corresponding pixel on target image
    output_pixels = np.zeros(best_sorted_pixels.shape).astype(int)
    output_pixels[best_sorted_indexes] = best_sorted_pixels

    print("color transfer finished")

    return output_pixels


def main(target_file_name, source_file_name):
    target_im = Image.open(target_file_name).convert("RGB")
    source_im = Image.open(source_file_name).convert("RGB")

    # the two images must be the same size
    if target_im.size[0] * target_im.size[1] != source_im.size[0] * source_im.size[1]:
        sys.exit("The two images must have the same number of pixels.")

    # images conversion into pixels array
    target_pixels = np.array(target_im.getdata())
    source_pixels = np.array(source_im.getdata())

    # main program
    output_pixels = color_transfer(target_pixels, source_pixels)

    # converting pixels output to a new image
    output_pixels = np.reshape(output_pixels, (target_im.size[1], target_im.size[0], 3))
    output_im = Image.fromarray(output_pixels.astype(np.uint8))

    output_im.save("output.jpg")
    output_im.show()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit("not enough arguments")
