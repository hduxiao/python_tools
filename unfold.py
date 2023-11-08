import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
 

aa = torch.ones(2,3)
bb = aa + 1
aa = aa.view(-1,1)
bb = bb.view(-1,1)
 
cc = torch.stack((aa,bb),dim=1).view(-1,6)
print(cc)
 
## tensor([[1., 2., 1., 2., 1., 2.],
##        [1., 2., 1., 2., 1., 2.]])

def torch_pool(inputs, target_size):
    #NCHW
    H = target_size[0]
    W = target_size[1]
    s_p1 = (torch.arange(W, dtype=torch.float32) * (inputs.size(-1) / W)).long()
    e_p1 = ((torch.arange(W, dtype=torch.float32)+1) * (inputs.size(-1) / W)).ceil().long()
 
    s_p2 = (torch.arange(H, dtype=torch.float32) * (inputs.size(-2) / H)).long()
    e_p2 = ((torch.arange(H, dtype=torch.float32)+1) * (inputs.size(-2) / H)).ceil().long()
 
    pooled2 = []
    for i_H in range(H):
      pooled = []
      for i_W in range(W):
          res = torch.mean(inputs[:, :, s_p2[i_H]:e_p2[i_H],s_p1[i_W]:e_p1[i_W]], dim=(-2,-1), keepdim=True)
          pooled.append(res)
      pooled = torch.cat(pooled, -1)
      pooled2.append(pooled)
    pooled2 = torch.cat(pooled2,-2)
    return pooled2


def torch_pool2(inputs, target_size):
    m = nn.AvgPool2d([2, 2], [3, 3])

    o1 = m(inputs)

    inputs2 = torch.flip(inputs, dims=(3,))
    o2 = torch.flip(m(inputs2), dims=(3,))

    inputs3 = torch.flip(inputs, dims=(2,))
    o3 = torch.flip(m(inputs3), dims=(2,))

    inputs4 = torch.flip(inputs, dims=(2, 3))
    o4 = torch.flip(m(inputs4), dims=(2, 3))

    o1 = o1.view(1, inputs.shape[1], -1, 1)
    o2 = o2.view(1, inputs.shape[1], -1, 1)
    o5 = torch.stack((o1, o2), dim=3).view(1, inputs.shape[1], -1, int(target_size[1]))

    o3 = o3.view(1, inputs.shape[1], -1, 1)
    o4 = o4.view(1, inputs.shape[1], -1, 1)
    o6 = torch.stack((o3, o4), dim=3).view(1, inputs.shape[1], -1, int(target_size[1]))

    o7 = torch.zeros(1, inputs.shape[1], target_size[0], target_size[1])
    for i in range(o7.shape[2]):
        if i % 2 == 0:
            o7[:, :, int(i)] = o5[:, :, int(i/2)]
        else:
            o7[:, :, int(i)] = o6[:, :, int(i/2)]

    return o7


alist = torch.randn(1, 64, 282, 492)
input_size = np.array(alist.shape[2:])
output_size = np.array([188, 328])
 
adp = torch.nn.AdaptiveAvgPool2d(output_size)
adplist = adp(alist)
#x = torch_pool(alist, list(output_size))
x2 = torch_pool2(alist, list(output_size))

print(alist)
print(adplist)
#print(x)
print(x2)