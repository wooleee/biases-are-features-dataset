from collections import defaultdict
import os
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np
import xmltodict

root_directory   = os.path.join(os.getcwd()) # '/Users/Username/dataset/afhq'
images_directory = os.path.join(root_directory, 'data', 'afhq')
xml_directory    = os.path.join(root_directory, 'xml')

aug_dir_names = ['grey', 'edge', 'txtr', 'ear', 'eye', 'nose']
aug_dir = []
for name in aug_dir_names:
    dir_name = os.path.join(root_directory, f'data_{name}')
    aug_dir.append(dir_name)
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        
# tasks = ['train', 'val']
# categories = ['cat', 'dog', 'wild']
tasks = ['val']
categories = ['cat', 'dog']
for dir in aug_dir:
    for task in tasks:
        for i in categories:
            dir_name = os.path.join(dir, task, i)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

def get_bb(task, category, aug_name, image_filename):
    '''
    About: Finding Bounding Box for each image, using xml file. If no xml file found, just return zeros.
    Input: Image_filename
    Output: xmin, ymin, xmax, ymax (location of bb)
    '''
    # print(task)
    xml_dir = os.path.join(xml_directory, task, f'{category}_{aug_name}', image_filename.replace(".jpg", ".xml"))
    try:
        f = open(xml_dir)
        doc = xmltodict.parse(f.read()) 
        xmin = int(doc['annotation']['object']['bndbox']['xmin'])
        ymin = int(doc['annotation']['object']['bndbox']['ymin'])
        xmax = int(doc['annotation']['object']['bndbox']['xmax'])
        ymax = int(doc['annotation']['object']['bndbox']['ymax'])
    except:
        xmin, ymin, xmax, ymax = 0,0,0,0

    return xmin, ymin, xmax, ymax

def to_augs(images_filenames, images_directory, aug_name):
    target_directory = os.path.join(root_directory, f'data_{aug_name}', task, category)
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            # print(image_filename)
            image = cv2.imread(os.path.join(images_directory, image_filename))
            w, h = image.shape[0], image.shape[1]
            xmin, ymin, xmax, ymax = get_bb(task, category, aug_name, image_filename)
            
        if xmin == 0 and ymin == 0 and xmax == 0 and ymax == 0:
            xmax = w
            ymax = h

        txtred_image = image[ymin:ymax, xmin:xmax]
        txtred_image = cv2.resize(txtred_image, dsize = (h, w), interpolation = cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(target_directory, image_filename), txtred_image) 

def to_grey(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        # print(extension)
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(target_directory, image_filename), grey_image)
# to_grey(filenames, path, os.path.join(root_directory, f'data_grey', type, category))

def to_edge(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            edges = cv2.Canny(image,100,200)
            cv2.imwrite(os.path.join(target_directory , image_filename), edges)
# to_edge(filenames, path, os.path.join(root_directory, f'data_edge', type, category))

tasks = ['val']
categories = ['cat', 'dog']
augs = ['ear', 'eye', 'nose', 'txtr']

if __name__ == "__main__":

    print('-------- Image Generation Start --------')
    for task in tasks:
        # print(task)
        for category in categories:

            path      = os.path.join(images_directory, task, category)
            filenames = list(sorted(os.listdir(path)))
            filepaths = [i for i in filenames if cv2.imread(os.path.join(path, i)) is not None]
            filepaths = [i for i in filepaths if os.path.splitext(i)[1] == '.jpg']

            to_grey(filenames, path, os.path.join(root_directory, f'data_grey', task, category))
            to_edge(filenames, path, os.path.join(root_directory, f'data_edge', task, category))
            for aug_name in augs:
                to_augs(filenames, path, aug_name)
    print('-------- Image Generation Done --------')