from collections import defaultdict
import os
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np
import xmltodict

root_directory = os.path.join(os.getcwd()) # '/Users/Username/dataset/afhq'
images_directory = os.path.join(root_directory, 'data', 'afhq')

aug_dir_names = ['grey', 'edge', 'part', 'txtr']
aug_dir = []
for name in aug_dir_names:
    dir_name = os.path.join(root_directory, f'data_{name}')
    aug_dir.append(dir_name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        
tasks = ['train', 'val']
categories = ['cat', 'dog', 'wild']

for dir in aug_dir:
    for task in tasks:
        for i in categories:
            dir_name = os.path.join(dir, task, i)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

def to_grey(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        # print(extension)
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(target_directory, image_filename), grey_image)

def to_edge(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            edges = cv2.Canny(image,100,200)
            cv2.imwrite(os.path.join(target_directory , image_filename), edges)

def to_txtr(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            w, h = image.shape[0], image.shape[1]
            xmin, ymin, xmax, ymax = 0, 0, w, h

        txtred_image = image[ymin + int((ymax-ymin)*2/8): ymax - int((ymax-ymin)*4/8),\
                         xmin + int((xmax-xmin)*3/8): xmax - int((xmax-xmin)*3/8)]
        txtred_image = cv2.resize(txtred_image, dsize = (h, w), interpolation = cv2.INTER_LINEAR)

        cv2.imwrite(os.path.join(target_directory , image_filename), txtred_image)

def to_part(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            w, h = image.shape[0], image.shape[1]
            xmin, ymin, xmax, ymax = 0, 0, w, h

        parted_image = image[ymin + int(5/12*h): ymax - int(5/12*h),\
                         xmin + int(1/4*w): xmax - int(1/4*w)]
        parted_image = cv2.resize(parted_image, dsize = (h, w), interpolation = cv2.INTER_LINEAR)

        cv2.imwrite(os.path.join(target_directory , image_filename), parted_image)



if __name__ == "__main__":

    print('-------- Image Generation Start --------')
    for task in tasks:
        # print(task)
        for category in categories:

            path     = os.path.join(images_directory, task, category)
            print(f'looking at {path}')
            filenames = list(sorted(os.listdir(path)))

            filepaths = [i for i in filenames if cv2.imread(os.path.join(path, i)) is not None]
            filepaths = [i for i in filepaths if os.path.splitext(i)[1] == '.jpg']

            # print(category)
            # print(os.path.join(root_directory, f'data_grey', task, category))
            to_grey(filenames, path, os.path.join(root_directory, f'data_grey', task, category))
            to_edge(filenames, path, os.path.join(root_directory, f'data_edge', task, category))
            to_txtr(filenames, path, os.path.join(root_directory, f'data_txtr', task, category))
            to_part(filenames, path, os.path.join(root_directory, f'data_part', task, category))
    print('-------- Image Generation Done --------')