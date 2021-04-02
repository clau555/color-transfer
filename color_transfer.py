import sys
from random import randint
from typing import Union

from PIL import Image


# is used to store the orignal rank of each pixels of the target image
ranks: list[int] = []


def random_vector(amplitude: int) -> tuple[int, int, int]:
    """
    Returns a random vector.\n
    :param amplitude: int
    :return: tuple[int, int, int]
    """
    minimum: int = int(-amplitude / 2)
    maximum: int = int(amplitude / 2)
    return randint(minimum, maximum), randint(minimum, maximum), randint(minimum, maximum)


def order_data_from_vector(pixel_data: tuple[tuple[int, int, int]], vector: tuple[int, int, int],
                           save_ranks: bool = False) -> tuple[tuple[int, int, int]]:
    """
    Orders all pixels in pixel_data according
    to their orthographic projection on the vector.\n
    :param pixel_data: tuple[tuple[int, int, int]]
    :param vector: tuple[int, int, int]
    :param save_ranks: bool
    :return: tuple[tuple[int, int, int]]
    """
    global ranks

    # each element of ranked_pixel_data is composed as follow :
    # [ pixel: tuple, dot_product: int, rank: int ]
    # dot_product is the dot product of pixel and vector
    # rank is the original rank of the pixel in its image
    ranked_pixel_data: list[list[Union[tuple, int]]] = []
    for i in range(len(pixel_data)):
        dot_product: int = pixel_data[i][0] * vector[0] + \
                           pixel_data[i][1] * vector[1] + \
                           pixel_data[i][2] * vector[2]
        ranked_pixel_data.append([pixel_data[i], dot_product, i])

    # sorts pixels according to their dot product
    ranked_pixel_data.sort(key=lambda pixel: pixel[1])

    # reconstructs the ranked pixels data
    pixel_data_ordered: list[tuple[int, int, int]] = [(0, 0, 0)] * len(pixel_data)
    for i in range(len(pixel_data)):
        pixel_data_ordered[i] = ranked_pixel_data[i][0]

        # saves original pixels ranks after sorting
        # this is used later when reorganising sorted pixels
        if save_ranks:
            ranks.append(ranked_pixel_data[i][2])

    return tuple(pixel_data_ordered)


def cost(target_pixel_data: tuple[tuple[int, int, int]], source_pixel_data: tuple[tuple[int, int, int]],
         vector: tuple[int, int, int]) -> float:
    """
    Calculates the distances between every pixels
    of the same rank from the target and source
    (ordered according to the vector pass in argument).\n
    Returns the sum of these distances, which is the cost.\n
    :param target_pixel_data: tuple[tuple[int, int, int]]
    :param source_pixel_data: tuple[tuple[int, int, int]]
    :param vector: tuple[int, int, int]
    :return: float
    """

    # before calculating the distances, we have to order them
    # with our vector to associate the future cost with the vector
    pixel_data1_ordered: tuple[tuple[int, int, int]] = order_data_from_vector(target_pixel_data, vector)
    pixel_data2_ordered: tuple[tuple[int, int, int]] = order_data_from_vector(source_pixel_data, vector)
    distances_sum: float = 0.0

    # calculs the distances sum
    for i in range(len(target_pixel_data)):
        distances_sum += (pixel_data1_ordered[i][0] - pixel_data2_ordered[i][0]) ** 2 + \
                    (pixel_data1_ordered[i][1] - pixel_data2_ordered[i][1]) ** 2 + \
                    (pixel_data1_ordered[i][2] - pixel_data2_ordered[i][2]) ** 2

    return distances_sum


def best_cost_vector(target_im: Image, source_im: Image, loop_number: int) -> tuple[int, int, int]:
    """
    Orders multiple times the source and target pixels according to a random vector.\n
    Returns the vector with the lowest associated cost.\n
    :param target_im: Image
    :param source_im: Image
    :param loop_number: int
    :return: tuple[int, int, int]
    """
    target_pixel_data: tuple[tuple[int, int, int]] = tuple(target_im.getdata())
    source_pixel_data: tuple[tuple[int, int, int]] = tuple(source_im.getdata())

    print("initialization...")
    best_vector: tuple[int, int, int] = random_vector(100)
    best_cost: float = cost(target_pixel_data, source_pixel_data, best_vector)
    costs: list[float] = []

    for i in range(loop_number):
        current_vector: tuple[int, int, int] = random_vector(100)
        current_cost: float = cost(target_pixel_data, source_pixel_data, current_vector)

        if current_cost < best_cost:
            best_cost = current_cost
            best_vector = current_vector

        costs.append(current_cost)

        print("{}\tvector : {}\t\tcost : {}\tbest cost : {}"
              .format(i, current_vector, current_cost, best_cost))

    quality: float = min(costs) / max(costs)
    print("\nbest vector : {}\nquality : {}".format(best_vector, quality))

    return best_vector


def color_transfer(target_im: Image, source_im: Image, loop_number: int) -> Image:
    """
    Executes a color transfert from the source to the target.\n
    Returns the output image.\n
    :param target_im: Image
    :param source_im: Image
    :param loop_number: int
    :return: Image
    """

    # we choose the vector which has the lowest cost when ordering the two images
    best_vector: tuple[int, int, int] = best_cost_vector(target_im, source_im, loop_number)

    # we order our images with the best vector, meaning that same rank pixels
    # of the target and the source will be as close as possible
    target_ordered_pixel_data: tuple[tuple[int, int, int]] = order_data_from_vector(tuple(target_im.getdata()),
                                                                                    best_vector, True)
    source_ordered_pixel_data: tuple[tuple[int, int, int]] = order_data_from_vector(tuple(source_im.getdata()),
                                                                                    best_vector)

    # orders pixels of the source according to their associated target pixels
    pixel_data_output: list[Union[int]] = [0] * len(target_ordered_pixel_data)
    for i in range(len(target_ordered_pixel_data)):
        pixel_data_output[ranks[i]] = source_ordered_pixel_data[i]  # magic

    output_im: Image = Image.new(target_im.mode, target_im.size)
    output_im.putdata(pixel_data_output)

    return output_im


def main(target_file_name: str, source_file_name: str, loop_number: int = 10) -> None:
    target_im: Image = Image.open(target_file_name).convert("RGB")
    source_im: Image = Image.open(source_file_name).convert("RGB")

    # because the two images must be at the same size for our transfer,
    # we crop the biggest if they are not
    if target_im.size != source_im.size:
        if target_im.size[0] * target_im.size[1] > source_im.size[0] * source_im.size[1]:
            target_im = target_im.crop((0, 0, source_im.size[0], source_im.size[1]))
        else:
            source_im = source_im.crop((0, 0, target_im.size[0], target_im.size[1]))

    output_im: Image = color_transfer(target_im, source_im, loop_number)

    output_im.save("output.png")
    output_im.show()


if __name__ == "__main__":
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit("not enough arguments")
