import sys
from random import randint
from typing import Union

from PIL import Image


indexes: list[int] = []  # is used to store the orignal indexes of each pixels of the target image


def random_vector(amplitude: int = 100) -> tuple[int, int, int]:
    """
    Returns a random vector.\n
    :param amplitude: int
    :return: tuple[int, int, int]
    """
    maximum: int = amplitude // 2
    minimum: int = -maximum
    return randint(minimum, maximum), randint(minimum, maximum), randint(minimum, maximum)


def order_pixels_from_vector(pixels: tuple[tuple[int, int, int]],
                             vector: tuple[int, int, int],
                             save_indexes: bool = False) -> tuple[tuple[int, int, int]]:
    """
    Orders a pixel set according to their orthographic projection on a vector.\n
    :param pixels: tuple[tuple[int, int, int]]
    :param vector: tuple[int, int, int]
    :param save_indexes: bool
    :return: tuple[tuple[int, int, int]]
    """
    global indexes

    """
    each element of ranked_pixels is composed as follow :
    [   
        pixel: tuple[int, int, int],
        dot_product: int,
        index: int
    ]
    pixel is the original image pixel rgb values
    dot_product is the dot product of pixel and vector
    index is the original index of the pixel in its image
    """
    ranked_pixels: list[list[Union[tuple, int]]] = []
    for i in range(len(pixels)):

        dot_product: int = pixels[i][0] * vector[0] + \
                           pixels[i][1] * vector[1] + \
                           pixels[i][2] * vector[2]

        ranked_pixels.append([pixels[i], dot_product, i])

    # sorts pixels according to their dot product
    ranked_pixels.sort(key=lambda data: data[1])

    # reconstructs the ranked pixels
    ordered_pixels: list[tuple[int, int, int]] = [(0, 0, 0)] * len(pixels)
    for i in range(len(pixels)):
        ordered_pixels[i] = ranked_pixels[i][0]

        # saves original pixels ranks after sorting
        # this is used later when reorganising sorted pixels
        if save_indexes:
            indexes.append(ranked_pixels[i][2])

    return tuple(ordered_pixels)


def cost(pixels1: tuple[tuple[int, int, int]],
         pixels2: tuple[tuple[int, int, int]],
         vector: tuple[int, int, int]) -> float:
    """
    Returns the cost between two sets of pixels.\n
    :param pixels1: tuple[tuple[int, int, int]]
    :param pixels2: tuple[tuple[int, int, int]]
    :param vector: tuple[int, int, int]
    :return: float
    """

    # before calculating the distances, we have to order the pixels with our vector
    ordered_pixels1: tuple[tuple[int, int, int]] = order_pixels_from_vector(pixels1, vector)
    ordered_pixels2: tuple[tuple[int, int, int]] = order_pixels_from_vector(pixels2, vector)
    total_cost: float = 0.

    for i in range(len(pixels1)):
        total_cost += (ordered_pixels1[i][0] - ordered_pixels2[i][0]) ** 2 + \
                        (ordered_pixels1[i][1] - ordered_pixels2[i][1]) ** 2 + \
                        (ordered_pixels1[i][2] - ordered_pixels2[i][2]) ** 2

    return total_cost


def best_cost_vector(target_pixels: tuple[tuple[int, int, int]],
                     source_pixels: tuple[tuple[int, int, int]],
                     n: int = 10) -> tuple[int, int, int]:
    """
    Orders n times the source and target pixels according to a random vector.\n
    Returns the vector with the lowest associated cost between the two ordered sets.\n
    :param target_pixels: tuple[tuple[int, int, int]]
    :param source_pixels: tuple[tuple[int, int, int]]
    :param n: int
    :return: tuple[int, int, int]
    """

    print("initialization...\n")

    best_vector: tuple[int, int, int] = random_vector()
    best_cost: float = cost(target_pixels, source_pixels, best_vector)

    for i in range(n):
        current_vector: tuple[int, int, int] = random_vector()
        current_cost: float = cost(target_pixels, source_pixels, current_vector)

        if current_cost < best_cost:
            best_cost = current_cost
            best_vector = current_vector

        print("{}\tvector : {}\t\tcost : {}\t\tbest cost : {}".format(i + 1, current_vector, current_cost, best_cost))

    print("\nbest vector : {}".format(best_vector))

    return best_vector


def color_transfer(target_pixels: tuple[tuple[int, int, int]],
                   source_pixels: tuple[tuple[int, int, int]]) -> tuple[tuple[int, int, int]]:
    """
    Executes a color transfert from the source to the target.\n
    Returns the output image pixels set.\n
    :param target_pixels: tuple[tuple[int, int, int]]
    :param source_pixels: tuple[tuple[int, int, int]]
    :return: tuple[tuple[int, int, int]]
    """

    # we choose the vector which has the lowest cost when ordering the two images
    best_vector: tuple[int, int, int] = best_cost_vector(target_pixels, source_pixels)

    # we order our images with the best vector, meaning that same rank pixels
    # of the target and the source will be as close as possible
    target_ordered_pixels: tuple[tuple[int, int, int]] = order_pixels_from_vector(target_pixels, best_vector, True)
    source_ordered_pixels: tuple[tuple[int, int, int]] = order_pixels_from_vector(source_pixels, best_vector)

    # orders pixels of the source according to their associated target pixels
    output_pixels: list[tuple[int, int, int]] = [(0, 0, 0)] * len(target_ordered_pixels)
    for i in range(len(target_ordered_pixels)):
        output_pixels[indexes[i]] = source_ordered_pixels[i]  # magic

    return tuple(output_pixels)


def main(target_file_name: str, source_file_name: str) -> None:

    target_im: Image = Image.open(target_file_name).convert("RGB")
    source_im: Image = Image.open(source_file_name).convert("RGB")

    # the two images must have the same number of pixels for our transfer
    if target_im.size[0] * target_im.size[1] != source_im.size[0] * source_im.size[1]:
        sys.exit("The two images must have the same number of pixels.")

    # images conversion into pixel sets
    target_pixels: tuple[tuple[int, int, int]] = tuple(target_im.getdata())
    source_pixels: tuple[tuple[int, int, int]] = tuple(source_im.getdata())

    # main program
    output_pixels: tuple[tuple[int, int, int]] = color_transfer(target_pixels, source_pixels)

    # pixel set to image
    output_im: Image = Image.new(target_im.mode, target_im.size)
    output_im.putdata(output_pixels)

    output_im.save("output.png")
    output_im.show()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit("not enough arguments")
