# 0. The Oxford-IIIT Pet Dataset - Augmented
- This repo is the part of 'Biases are Features' project
- Image data are from https://github.com/ml4py/dataset-iiit-pet that contain no miscellaneous error.

# 1. Directory

```
+-- README.md
+-- assets
+-- annotations
        +-- trimaps
             +-- {}.png
        +-- xmls
        +-- list.txt
        +-- README
        +-- test.txt
        +-- test-pet.txt
        +-- trainval.txt
        +-- trainval-pet.txt
+-- images
        +-- {}.jpg
+-- images_grey 
        +-- {}.jpg
+-- images_silo 
        +-- {}.jpg
+-- images_txtr 
        +-- {}.jpg
+-- images_back
        +-- {}.jpg
+-- old
+-- data_gen.py
+-- requirements.txt
```

# 2. How To Use
Execute Beolw

```
python data_gen.py
```

# 3. Aug methods
There are four augmentations. Detailed explanation and the name of function are shown. Code is in data_gen.py file.


## 3.0. original: 원 이미지<br>

![](/assets/sample_original.jpg)

## 3.1. grey: 단순 Greyscale로 만드는 과정
  - func: to_grey()
  - 그냥 Grey Scale <br>

![](/assets/sample_grey.jpg) <br>

## 3.2. silo: Sillouette을 만드는 과정
  - func: to_silo()
  - 물체 Mask 부분은 흰색, 그 외는 모두 검정색 <br>

![](/assets/sample_silo.jpg) <br>

## 3.3. txtr: Texture를 뽑는 과정
  - Bounding Box x, y, w, h라고 하면, x, y, 0.5w, 0.5h Box로 Crop하는 과정
  - func: to_txtr()  <br>

![](/assets/sample_txtr.jpg)<br>


## 3.4. back: Background_only를 만드는 과정
  - 물체 Mask 부분은 검정색, 그 외 배경은 모두 원 이미지
  - func: to_back() <br>

![](/assets/sample_back.jpg) <br>


# References
Official: 
- https://www.robots.ox.ac.uk/~vgg/data/pets/ 
  
Ref:
- https://albumentations.ai/docs/examples/pytorch_semantic_segmentation/
- https://github.com/ml4py/dataset-iiit-pet