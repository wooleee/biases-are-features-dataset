from collections import defaultdict
import os
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np


root_directory = os.path.join(os.getcwd()) # '/Users/Username/dataset'
images_directory = os.path.join(root_directory, "images")
masks_directory = os.path.join(root_directory, "annotations", "trimaps")

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

# to_silo(correct_images_filenames, images_directory, os.path.join(root_directory, "images_silo"))

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

# to_back(correct_images_filenames, images_directory, os.path.join(root_directory, "images_back"))

"""## GREY"""

def to_grey(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(target_directory , image_filename), grey_image)

# to_grey(correct_images_filenames, images_directory, os.path.join(root_directory, "images_grey"))

"""## TXTR"""

def preprocess_mask_txtr(mask):
    mask = mask.astype(np.uint8)
    mask[(mask == 2.0) | (mask == 3.0)] = 0.0
    mask[mask == 1.0] = 255
    return mask

def to_txtr(images_filenames, images_directory, target_directory):
    for i, image_filename in enumerate(images_filenames):
        extension = os.path.splitext(image_filename)[1] # find extension to exclue '.mat'
        if (extension == '.jpg'):
            image = cv2.imread(os.path.join(images_directory, image_filename))
            mask = cv2.imread(os.path.join(masks_directory, image_filename.replace(".jpg", ".png")), cv2.IMREAD_UNCHANGED,)
        _,thresh = cv2.threshold(mask,1,255,0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # contours: (1, 4, 1, 2)
        bbs = []
        for contour in contours:
            bb = cv2.boundingRect(contour)
            bbs.append(bb)

        # bbs 맨뒤의 요소: 이미지 전체 박스 지칭 (0,0,w,h)
        # bbs 맨뒤에서 두번째 요소: Mask 지칭
        
        if len(bbs) > 1:
            x,y,w,h = bbs[-2]
            if not w > 50 or h > 50: # 이미지 bb가 지극히 작아서 (= 너비와 높이가 50픽셀도 안되어서) BB를 Crop하면 texture는 커녕 점의 형태에 가까운 이미지를 Return합니다. 이럴경우 그냥 이미지 전체에 가운데 1/2만 뽑아내도록 구현했습니다.
                x,y,w,h = bbs[-1]
                x += int(w/4)
                y += int(h/4)
                w = int(w/2)
                h = int(h/2)

        else:
            x,y,w,h = bbs[-1]

        txtred_image = image[y + int(h/4): y + int(3*h/4), x + int(w/4): x + int(3*w/4)]
        cv2.imwrite(os.path.join(target_directory , image_filename), txtred_image)

# to_txtr(correct_images_filenames, images_directory, os.path.join(root_directory, "images_txtr"))

if __name__ == "__main__":
    print('--- Image Generation Start ---')

    to_grey(correct_images_filenames, images_directory, os.path.join(root_directory, "images_grey"))
    print('-- Greyscaled Image Generation Done')

    to_silo(correct_images_filenames, images_directory, os.path.join(root_directory, "images_silo"))
    print('-- Silouetted Image Generation Done')

    to_back(correct_images_filenames, images_directory, os.path.join(root_directory, "images_back"))
    print('-- Background Only Image Generation Done')

    to_txtr(correct_images_filenames, images_directory, os.path.join(root_directory, "images_txtr"))
    print('-- Texture Only Image Generation Done')

    print('--- Image Generation Done ---')