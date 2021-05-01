# The Oxford-IIIT Pet Dataset - Augmented
'Biases are Features' 프로젝트의 데이터셋 부분이다.

# Directory

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
        +-- trainval.txt
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
+-- data_gen.ipynb
+-- requirements.txt
```

# Aug methods
원 이미지에 4가지의 조정을 주었다. 상세설명과 함수명이 분류별로 명시돼있다.

## original: 원 이미지<br>

![](/assets/sample_original.jpg)
## grey: 단순 Greyscale로 만드는 과정
  - func: to_grey()
  - 그냥 Grey Scale <br>

![](/assets/sample_grey.jpg)

## silo: Sillouette을 만드는 과정
  - func: to_silo()
  - 물체 Mask 부분은 흰색, 그 외는 모두 검정색

![](/assets/sample_silo.jpg)

## txtr: Texture를 뽑는 과정
  - Bounding Box x, y, w, h라고 하면, x, y, 0.5w, 0.5h Box로 Crop하는 과정
  - func: to_txtr()   <-- Implementing


<img src="https://steamuserimages-a.akamaihd.net/ugc/916923327996368167/2E9A20BCFF717A81A0247C74B761D185A8C10887/" width="400">


## back: Background_only를 만드는 과정
  - 물체 Mask 부분은 검정색, 그 외 배경은 모두 원 이미지
  - func: to_back()

![](/assets/sample_back.jpg)


# References
Official: 
- https://www.robots.ox.ac.uk/~vgg/data/pets/ 
  
Ref:
- https://albumentations.ai/docs/examples/pytorch_semantic_segmentation/
