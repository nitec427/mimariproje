from helpers import read_img_files
import random

image_counts, image_paths = read_img_files.read_files('unprocessed')

my_arr = [i+1 for i in range(image_counts)]
random.shuffle(my_arr)

for i in range(image_counts):
    # zip paths and their random ids
    print(image_paths[i], my_arr[i])


result = tuple(zip(image_paths, my_arr))
sorted_result = sorted(result, key=lambda x: x[1])
print(sorted_result)
