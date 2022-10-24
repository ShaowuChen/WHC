# WHC: Weighted Hybrid Criterion for Filter Pruning on Convolutional Neural Networks
(submitted to ICASSP 2023)

The implementaion is based on [FPGM](https://github.com/he-y/filter-pruning-geometric-median). Thanks to YangHe for his help and contribution. 




# 1. Environment:
python3.6.12 ; Torch 1.3.1.

# 2. Description for files:

```
  ├── pruning_cifar10_orig.py: Code for CIFAR-10
  ├── pruning_imagenet.py: Code for ImageN
  ├── run.sh: Script demo to run the code
  ├── utils.py 
  ├── models
```


# 3. Log files and CKPT:
Find log files and checkpoints in 
[WHC Google Drive](https://drive.google.com/drive/folders/1HRo16Ddfic8OQ1WGb_Dc2o6pJ6zywXpv?usp=sharing).

Find pre-trained CIFAR-10 parameters (unpruned) in [FPGM Google Drive](https://drive.google.com/drive/u/0/folders/1gbTTykmn6gk4IEug3jwDKFA5gDaNjowu). 

Find Pytorch official pre-trained ImageNet parameters (unpruned) in 
 [resnet18](https://download.pytorch.org/models/resnet18-5c106cde.pth),
 [resnet34](https://download.pytorch.org/models/resnet34-333f7ec4.pth),
 [resnet50](https://download.pytorch.org/models/resnet50-19c8e357.pth),
 [resnet101](https://download.pytorch.org/models/resnet101-5d3b4d8f.pth).
