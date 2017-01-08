import glob, cv2
import numpy

TILE_SIZE = 25
images = {}
float_cache = {}
CURRENT_TILE = 1
current_tile_float = 1


def warm_up():
    for img in glob.iglob(str(TILE_SIZE) + "/**/*.jpg", recursive=True):
        imread = cv2.imread(img)
        images[img] = {'float' : imread.astype("float"), 'img': imread}


def create_blank(width, height, rgb_color=(0, 0, 0)):
    image = numpy.zeros((height, width, 3), numpy.uint8)
    color = tuple(reversed(rgb_color))
    image[:] = color
    return image


def mse(first_float, second):
    err = numpy.sum((first_float - second['float']) ** 2)
    err /= float(TILE_SIZE ** 2)
    return err


def find_similar(img):
    comparer = GetSimilar(img)
    return min(images, key=comparer.compare)


class GetSimilar:
    def __init__(self, pattern):
        self.pattern = pattern.astype("float")

    def compare(self, img_to_compare):
        return mse(self.pattern, images[img_to_compare])

warm_up()
base_img = cv2.imread('base_img.jpg')
height, width, channels = base_img.shape
cropped_height = round((height / TILE_SIZE)) * TILE_SIZE
cropped_width = round((width / TILE_SIZE)) * TILE_SIZE

cropped_base_image = base_img[0:cropped_height, 0:cropped_width]
rows = []
image_from_tiles = create_blank(cropped_width, cropped_height)

total_tiles = ((cropped_height / TILE_SIZE) + 1) * (cropped_width / TILE_SIZE)

for x in range(1, round(cropped_height / TILE_SIZE) + 1):
    row = []
    for y in range(1, round(cropped_width / TILE_SIZE) + 1):
        cropped_part = cropped_base_image[(x - 1) * TILE_SIZE: x * TILE_SIZE, (y - 1) * TILE_SIZE: y * TILE_SIZE]
        similar_file = find_similar(cropped_part)
        similar_fragment = cv2.imread(similar_file)
        images.pop(similar_file)
        image_from_tiles[(x - 1) * TILE_SIZE: x * TILE_SIZE, (y - 1) * TILE_SIZE: y * TILE_SIZE] = similar_fragment
        cv2.imwrite('result.jpg', image_from_tiles)
        print(str(y + (x-1) * ((cropped_width / TILE_SIZE) + 1)) + '/' + str(total_tiles))



