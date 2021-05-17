from collections import defaultdict
import os
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np
import xmltodict

root_directory = os.path.join(os.getcwd()) # '/Users/Username/dataset/oxford'
print(root_directory)
images_directory = os.path.join(root_directory,  "images")
masks_directory = os.path.join(root_directory, "annotations", "trimaps")
xml_directory = os.path.join(root_directory,  "annotations", "xmls")
# Dir_name 
# [GREY]Grey Scale - rgb2gray
# [SILO]실루엣 - 고양이 흰색 그외 검정색
# [TXTR]텍스쳐 - 바운딩 박스 크롭하고 그 중 Half
# [BACK]배경 - 고양이 검정색 배경 그대로

aug_dir_names = ['grey', 'silo', 'txtr', 'back']
for name in aug_dir_names:
    dir_name = os.path.join(root_directory, f'images_{name}')
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

images_filenames = list(sorted(os.listdir(images_directory)))
correct_images_filenames = [i for i in images_filenames if cv2.imread(os.path.join(images_directory, i)) is not None]
correct_images_filenames = [i for i in correct_images_filenames if os.path.splitext(i)[1] == '.jpg']

"""## SILO"""

# mask == 1.0: 고양이 부분
# mask == 2.0: 배경 부분
# mask == 3.0: 테두리 부분
def preprocess_mask_silo(mask):
    mask = mask.astype(np.uint8)
    mask[(mask == 2.0) | (mask == 3.0)] = 0.0
    mask[mask == 1.0] = 255
    return mask

def to_silo(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            mask = cv2.imread(os.path.join(masks_directory, image_filename.replace(".jpg", ".png")), cv2.IMREAD_UNCHANGED,)
            silouetted = preprocess_mask_silo(mask)    
            cv2.imwrite(os.path.join(target_directory , image_filename), silouetted)



"""## BACK"""

def preprocess_mask_back(mask):
    mask = mask.astype(np.uint8)
    mask[mask == 2.0] = 255
    mask[(mask == 1.0) | (mask == 3.0)] = 0
    return mask

def to_back(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            mask = cv2.imread(os.path.join(masks_directory, image_filename.replace(".jpg", ".png")), cv2.IMREAD_UNCHANGED,)
            mask = preprocess_mask_back(mask)  
            background_only = cv2.bitwise_and(image, image, mask = mask)
            cv2.imwrite(os.path.join(target_directory , image_filename), background_only)



"""## GREY"""

def to_grey(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(target_directory , image_filename), grey_image)



"""## TXTR"""

def get_bb(image_filename):
    '''
    About: Finding Bounding Box for each image, using xml file. If no xml file found, just return zeros.
    Input: Image_filename
    Output: xmin, ymin, xmax, ymax (location of bb)
    '''
    xml_dir = os.path.join(xml_directory, image_filename.replace(".jpg", ".xml"))
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

def to_txtr(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            w, h = image.shape[0], image.shape[1]
            xmin, ymin, xmax, ymax = get_bb(image_filename)
            
        if xmin == 0 and ymin == 0 and xmax == 0 and ymax == 0:
            xmax = w
            ymax = h

        txtred_image = image[ymin + int((ymax-ymin)/4): ymax - int((ymax-ymin)/4),\
                         xmin + int((xmax-xmin)/4): xmax - int((xmax-xmin)/4)]
        txtred_image = cv2.resize(txtred_image, dsize = (h, w), interpolation = cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(target_directory , image_filename), txtred_image)


if __name__ == "__main__":
    print('-------- Image Generation Start --------')

    to_grey(correct_images_filenames, images_directory, os.path.join(root_directory, "images_grey"))
    print('-- Greyscaled Image Generation Done')

    to_silo(correct_images_filenames, images_directory, os.path.join(root_directory, "images_silo"))
    print('-- Silouetted Image Generation Done')

    to_back(correct_images_filenames, images_directory, os.path.join(root_directory, "images_back"))
    print('-- Background Only Image Generation Done')

    to_txtr(correct_images_filenames, images_directory, os.path.join(root_directory, "images_txtr"))
    print('-- Texture Only Image Generation Done')

    print('-------- Image Generation Done --------')