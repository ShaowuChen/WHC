# WHC
Welcome! (Readme Need update)

This repository contains codes for the paper:




Feel free to ask me questions, and please cite our work if it help:
```

```


***
# 1.Environment:
python3.6.12 ; Tensorflow1.15; MATLAB R2021a
***
# 2.Files
## 2.1 Structure
```
--
  ├── resnet.py
  ├── train_resnet.py
  ├── resnet_decom.py
  ├── train_resnet_decom.py
  ├── inference_evaluating_time.py
  ├── util
  │   ├── get_parameter.py
  │   ├── pytorch_pth2tensorflow_npy.py
  │   ├── cifar10_input.py
  │   ├── cifar100_input.py
  │   ├── dataset.py
  │   ├── image_processing.py
  |   └── imagenet_data.py
  ├── draw_pictures
  │   ├── draw_Bi_JSVD_curves.m
  |   └── draw_time_figure.py
```

## 2.2 Description:
```
  ├── resnet.py: Define the original networks for CIFAR-10/CIFAR-100/ImageNet
  
  ├── train_resnet.py: Use this code to train the original networks from scratch or fine-tune the pre-trained networks transferred from Pytorch for ImageNet
  
  ├── resnet_decom.py: Define the decomposed networks for CIFAR-10/CIFAR-100/ImageNet
  
  ├── train_resnet_decom.py: Use this code to fine-tune or train the decomposed networks from scratch.
  
  ├── inference_evaluating_time.py: Test the time for inference/Realistic Acceleartion.
  
  ├── util
  │   ├── get_parameter.py: Obtain the factorized weights using decomposition methods
  │   ├── pytorch_pth2tensorflow_npy.py: Create a dictionary contains pre-trained Pytorch weights for ResNet34 on ImageNet to transfer the model to TensorFlow
  │   ├── cifar10_input.py: Load CIFAR-10
  │   ├── cifar100_input.py: Load CIFAR-100
  │   ├── dataset.py：Load ImageNet (TF records format)
  │   ├── image_processing.py：Load ImageNet (TF records format)
  |   └── imagenet_data.py：Load ImageNet (TF records format)
  
  ├── draw_pictures
  │   ├── draw_Bi_JSVD_curves.m: (Matlab) Draw the Figure 3 and 4
  |   └── draw_time_figure.py: Draw the Figure 5 (a) to (d)
```


***
# 3.Demo (How to run)
#### 1. train a original network from scratch like this:
```c
python train_resnet.py --model=resnet34 --dataset=cifar10 --from_scratch=True  --bool_regularizer=True --gpu=0 --batch_size=128 --epoch=300 --num_lr=1e-1 change_lr=[140,200,250]  --lr_decay=10
```
#### 2、set a rank rate, choose a method to compress network follow the 'pre-train->decompose->fine-tune' pipeline:

```c
python train_resnet_decom.py  --method=lJSVD --model=resnet34 --dataset=cifar100  --repeat_exp_times=3  --batch_size=128 --bool_regularizer=True --exp_path=cifar10_300epoch --from_scratch=False --epoch=300 --num_lr=1e-1 --change_lr="[140,200,250]" --max_to_keep=10 --rank_rate_SVD=0.04
```
#### or train it from scratch:
```c
python train_resnet_decom.py  --method=lJSVD --model=resnet34 --dataset=cifar100  --repeat_exp_times=3  --batch_size=128 --bool_regularizer=True --exp_path=cifar10/from_scratch   --from_scratch=True --epoch=300 --num_lr=1e-1 --change_lr="[140,200,250]" --max_to_keep=10 --rank_rate_SVD=0.04
```
***
# 4.Resources

 1. [CIFAR10/CIFAR100 data sets](http://www.cs.toronto.edu/~kriz/cifar.html)
 2. [Pre-trained weights for ResNet34 on ImageNet](https://download.pytorch.org/models/resnet34-333f7ec4.pth)
