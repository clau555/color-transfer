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


def cost(target_pixel_data: tuple, source_pixel_data: tuple, vector: tuple) -> float:
    pixel_data1_ordered = order_data_from_vector(target_pixel_data, vector)
    pixel_data2_ordered = order_data_from_vector(source_pixel_data, vector)
    distance = 0.0

    for i in range(len(target_pixel_data)):
        distance += (pixel_data1_ordered[i][0] - pixel_data2_ordered[i][0]) ** 2 + \
                    (pixel_data1_ordered[i][1] - pixel_data2_ordered[i][1]) ** 2 + \
                    (pixel_data1_ordered[i][2] - pixel_data2_ordered[i][2]) ** 2

    return distance


def get_best_cost_vector(target_im: Image, source_im: Image, loop_number: int) -> tuple:
    target_pixel_data = tuple(target_im.getdata())
    source_pixel_data = tuple(source_im.getdata())

    print("initialization...")
    best_vector = random_vector(99)
    best_cost = cost(target_pixel_data, source_pixel_data, best_vector)
    costs = []
    for i in range(loop_number):
        vector = random_vector(99)
        current_cost = cost(target_pixel_data, source_pixel_data, vector)
        if current_cost < best_cost:
            best_cost = current_cost
            best_vector = vector
        costs.append(current_cost)
        print("{}\tvector : {}\t\tcost : {}\tbest cost : {}".format(i, vector, current_cost, best_cost))

    quality = min(costs) / max(costs)
    print("\nbest vector : {}\nquality : {}".format(best_vector, quality))

    return best_vector


def color_transfer(target_im: Image, source_im: Image, loop_number: int) -> Image:

    best_vector = get_best_cost_vector(target_im, source_im, loop_number)

    target_ordered_pixel_data = order_data_from_vector(tuple(target_im.getdata()), best_vector, True)
    source_ordered_pixel_data = order_data_from_vector(tuple(source_im.getdata()), best_vector)

    pixel_data_output = [None] * len(target_ordered_pixel_data)
    for i in range(len(target_ordered_pixel_data)):
        pixel_data_output[ranks[i]] = source_ordered_pixel_data[i]  # magic

    im_output = Image.new(target_im.mode, target_im.size)
    im_output.putdata(pixel_data_output)

    return im_output


def main(target_file_name: str, source_file_name: str, loop_number: int = 10) -> None:
    target_im = Image.open(target_file_name).convert("RGB")
    source_im = Image.open(source_file_name).convert("RGB")

    if target_im.size != source_im.size:
        if target_im.size[0] * target_im.size[1] > source_im.size[0] * source_im.size[1]:
            target_im = target_im.crop((0, 0, source_im.size[0], source_im.size[1]))
        else:
            source_im = source_im.crop((0, 0, target_im.size[0], target_im.size[1]))

    im_output = color_transfer(target_im, source_im, loop_number)

    im_output.save("output.png")
    im_output.show()


if __name__ == "__main__":
    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
    elif len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        sys.exit("not enough arguments")
