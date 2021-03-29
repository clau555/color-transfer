import sys
from random import randint

from PIL import Image


ranks = []


def random_vector(amplitude: int) -> tuple[int, int, int]:
    minimum = int(-amplitude / 2)
    maximum = int(amplitude / 2)
    return randint(minimum, maximum), randint(minimum, maximum), randint(minimum, maximum)


def order_data_from_vector(pixel_data: tuple, vector: tuple, save_ranks: bool = False) -> tuple:
    global ranks

    # each element of ranked_pixel_data is composed like this :
    # [pixel:tuple, dot_product:int, rank:int]
    # dot_product is the dot product of pixel and vector
    # rank is the original rank of pixel in its image
    ranked_pixel_data = []
    for i in range(len(pixel_data)):
        dot_product = pixel_data[i][0] * vector[0] + \
                      pixel_data[i][1] * vector[1] + \
                      pixel_data[i][2] * vector[2]
        ranked_pixel_data.append([pixel_data[i], dot_product, i])

    # sorts pixels according to their dot product
    ranked_pixel_data.sort(key=lambda pixel: pixel[1])

    # clean data reconstruction
    pixel_data_ordered = [None] * len(pixel_data)
    for i in range(len(pixel_data)):
        pixel_data_ordered[i] = ranked_pixel_data[i][0]

        # saving original pixels ranks after sorting
        # to be used later when reorganising sorted pixels
        if save_ranks:
            ranks.append(ranked_pixel_data[i][2])

    return tuple(pixel_data_ordered)


def cost(pixel_data1: tuple, pixel_data2: tuple, vector: tuple) -> float:
    pixel_data1_ordered = order_data_from_vector(pixel_data1, vector)
    pixel_data2_ordered = order_data_from_vector(pixel_data2, vector)
    distance = 0.0

    for i in range(len(pixel_data1)):
        distance += (pixel_data1_ordered[i][0] - pixel_data2_ordered[i][0]) ** 2 + \
                    (pixel_data1_ordered[i][1] - pixel_data2_ordered[i][1]) ** 2 + \
                    (pixel_data1_ordered[i][2] - pixel_data2_ordered[i][2]) ** 2

    return distance


def get_best_cost_vector(im1: Image, im2: Image, loop_number: int) -> tuple:
    pixel_data1 = tuple(im1.getdata())
    pixel_data2 = tuple(im2.getdata())

    print("initialization...")
    best_vector = random_vector(99)
    best_cost = cost(pixel_data1, pixel_data2, best_vector)
    costs = []
    for i in range(loop_number):
        vector = random_vector(99)
        current_cost = cost(pixel_data1, pixel_data2, vector)
        if current_cost < best_cost:
            best_cost = current_cost
            best_vector = vector
        costs.append(current_cost)
        print("{}\tvector : {}\t\tcost : {}\tbest cost : {}".format(i, vector, current_cost, best_cost))

    quality = min(costs) / max(costs)
    print("\nbest vector : {}\nquality : {}".format(best_vector, quality))

    return best_vector


def color_transfer(im1: Image, im2: Image, loop_number: int) -> Image:

    best_vector = get_best_cost_vector(im1, im2, loop_number)

    ordered_pixel_data1 = order_data_from_vector(tuple(im1.getdata()), best_vector, True)
    ordered_pixel_data2 = order_data_from_vector(tuple(im2.getdata()), best_vector)

    pixel_data_output = [None] * len(ordered_pixel_data1)
    for i in range(len(ordered_pixel_data1)):
        pixel_data_output[ranks[i]] = ordered_pixel_data2[i]  # magic

    im_output = Image.new(im1.mode, im1.size)
    im_output.putdata(pixel_data_output)

    return im_output


def main(file_name1: str, file_name2: str, loop_number: int = 10) -> None:
    im1 = Image.open(file_name1).convert("RGB")
    im2 = Image.open(file_name2).convert("RGB")

    if im1.size != im2.size:
        sys.exit("The two images must have the same dimensions")

    im_output = color_transfer(im1, im2, loop_number)

    im_output.save("output.png")
    im_output.show()
    im1.close()
    im2.close()


if __name__ == "__main__":
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit("not enough arguments")
