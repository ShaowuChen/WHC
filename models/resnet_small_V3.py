import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init
#from .res_utils import DownsampleA, DownsampleC, DownsampleD
import math

class DownsampleA(nn.Module):  

  def __init__(self, nIn, nOut, stride):
    super(DownsampleA, self).__init__() 
    self.avg = nn.AvgPool2d(kernel_size=1, stride=stride)   

  def forward(self, x):   
    x = self.avg(x)  
    return torch.cat((x, x.mul(0)), 1)  


class ResNetBasicblock(nn.Module):
  expansion = 1
  """
  RexNet basicblock (https://github.com/facebook/fb.resnet.torch/blob/master/models/resnet.lua)
  """
  def __init__(self, inplanes, planes, index, stride=1, downsample=None):
    super(ResNetBasicblock, self).__init__()

    self.conv_a = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
    self.bn_a = nn.BatchNorm2d(planes)

    self.conv_b = nn.Conv2d(planes, planes, kernel_size=3, stride=1, padding=1, bias=False)
    self.bn_b = nn.BatchNorm2d(planes)

    self.downsample = downsample
    self.inplanes = inplanes
    self.index = index
    
  def forward(self, x):
    residual = x

    basicblock = self.conv_a(x)
    basicblock = self.bn_a(basicblock)
    basicblock = F.relu(basicblock, inplace=True)

    basicblock = self.conv_b(basicblock)
    basicblock = self.bn_b(basicblock)

    if self.downsample is not None:
      residual = self.downsample(x)
    
#    out = self.out.cuda()
#    out.zero_()
#    out = torch.FloatTensor(self.inplanes, basicblock.size()[1], basicblock.size()[2]).zero_()
#    out.index_add_(0, self.index[0], residual.data)
#    out.index_add_(0, self.index[1], basicblock.data)
    out = torch.rand(self.inplanes, basicblock.size()[1], basicblock.size()[2])

    return F.relu(out, inplace=True)

class CifarResNet(nn.Module):
  """
  ResNet optimized for the Cifar dataset, as specified in
  https://arxiv.org/abs/1512.03385.pdf
  """
  def __init__(self, block, depth, num_classes, index, rate=[16, 16, 32, 64, 16, 32, 64]):
    """ Constructor
    Args:
      depth: number of layers.
      num_classes: number of classes
      base_width: base width
    """
    super(CifarResNet, self).__init__()

    #Model type specifies number of layers for CIFAR-10 and CIFAR-100 model   
    assert (depth - 2) % 6 == 0, 'depth should be one of 20, 32, 44, 56, 110'
    layer_blocks = (depth - 2) // 6
    self.stage_num = (depth - 2) // 3
    print ('CifarResNet : Depth : {} , Layers for each block : {}'.format(depth, layer_blocks))
    print(len(index))
    self.num_classes = num_classes
    self.rate = rate
    self.index = index
    
    self.conv_1_3x3 = nn.Conv2d(3, rate[0], kernel_size=3, stride=1, padding=1, bias=False)
    self.bn_1 = nn.BatchNorm2d(rate[0])
    print(len(index[1 : self.stage_num + 1]))
    self.inplanes = rate[0]
    self.stage_1 = self._make_layer(block, rate[4], rate[1], index[1 : self.stage_num + 1], layer_blocks, 1)
    self.stage_2 = self._make_layer(block, rate[5], rate[2], index[self.stage_num + 1 : self.stage_num * 2 + 1], layer_blocks, 2)
    self.stage_3 = self._make_layer(block, rate[6], rate[3], index[self.stage_num * 2 + 1 : self.stage_num * 3 + 1], layer_blocks, 2)
    self.avgpool = nn.AvgPool2d(8)
    self.classifier = nn.Linear(64*block.expansion, num_classes)

    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        m.weight.data.normal_(0, math.sqrt(2. / n))
        #m.bias.data.zero_()
      elif isinstance(m, nn.BatchNorm2d):
        m.weight.data.fill_(1)
        m.bias.data.zero_()
      elif isinstance(m, nn.Linear):
        init.kaiming_normal(m.weight)
        m.bias.data.zero_()

  def _make_layer(self, block, inplanes, planes, index, blocks, stride=1):
    downsample = None
    if stride != 1 :
        
      downsample = DownsampleA(self.inplanes, planes * block.expansion, stride)
#    print(self.inplanes)
    layers = []
    i=0
    j=2
    
    layers.append(block(self.inplanes, planes, index[i:j], stride, downsample))
#    self.inplanes = planes * block.expansion
    i += 2
    j += 2
    
    self.inplanes = inplanes 
    print(inplanes)
    for i in range(1, blocks):
      layers.append(block(self.inplanes, planes,index[i:j]))
      i += 2
      j += 2
    return nn.Sequential(*layers)

  def forward(self, x):
    x = self.conv_1_3x3(x)
    x = F.relu(self.bn_1(x), inplace=True)
    x = self.stage_1(x)
    x = self.stage_2(x)
    x = self.stage_3(x)
    x = self.avgpool(x)
    x = x.view(x.size(0), -1)
    return self.classifier(x)

def resnet20_small(index, rate,num_classes=10):
  """Constructs a ResNet-20 model for CIFAR-10 (by default)
  Args:
    num_classes (uint): number of classes
  """
  model = CifarResNet(ResNetBasicblock, 20, num_classes, index, rate)
  return model

def resnet32_small(index, rate,num_classes=10):
  """Constructs a ResNet-32 model for CIFAR-10 (by default)
  Args:
    num_classes (uint): number of classes
  """
  model = CifarResNet(ResNetBasicblock, 32, num_classes,index, rate)
  return model

def resnet44_small(index, rate,num_classes=10):
  """Constructs a ResNet-44 model for CIFAR-10 (by default)
  Args:
    num_classes (uint): number of classes
  """
  model = CifarResNet(ResNetBasicblock, 44, num_classes,index, rate)
  return model

def resnet56_small(index, rate,num_classes=10):
  """Constructs a ResNet-56 model for CIFAR-10 (by default)
  Args:
    num_classes (uint): number of classes
  """
  model = CifarResNet(ResNetBasicblock, 56, num_classes,index, rate)
  return model

def resnet110_small(index, rate,num_classes=10):
  """Constructs a ResNet-110 model for CIFAR-10 (by default)
  Args:
    num_classes (uint): number of classes
  """
  model = CifarResNet(ResNetBasicblock, 110, num_classes,index, rate)
  return model
