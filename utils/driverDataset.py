from PIL import Image
from torch.utils import data
from torchvision import transforms as T
import torch
import numpy as np
import os

class DriverDataset(data.Dataset):
    def __init__(self, LR_npy_path,GT_npy_path,scale_factor,isTrain):
        
        self.LR_npy_path=LR_npy_path
        self.GT_npy_path=GT_npy_path
        self.isTrain=isTrain
        self.imgs_name=self._fileList_npy(LR_npy_path)
        self.LR_transforms=self.get_default_npy_transform()
        self.GT_transforms=self.get_default_npy_transform()
        
    
    def __getitem__(self, index):
        name=  self.imgs_name[index]
        lr_path=os.path.join(self.LR_npy_path, name+".npy")
        lr=np.load(lr_path)  
        lr = self.LR_transforms(lr)

        gt_path=os.path.join(self.GT_npy_path, name+".npy")
        gt=np.load(gt_path)  
        gt = self.GT_transforms(gt)
        
        if self.isTrain:
            return (lr,gt)
        else:
            
            return (lr,gt,name)

    def __len__(self):
        return len(self.imgs_name)
    
    def _fileList_npy(self,path):
        ret_list=[]
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".npy"):
                    name=name.rstrip(".npy")
                    ret_list.append(name)
        return ret_list

    def get_default_img_transform(self):
        transforms = T.Compose([
                T.ToTensor(), 
                ])
        return transforms
    def get_default_npy_transform(self):
        def trans(array):
            array=torch.from_numpy(array)
            return array.float().div(255)

        return trans

if __name__ == '__main__':
    LR_root="../data/temp/test_LR"
    GT_root="../data/temp/test_GT/npy"
    scale_factor=2
    d=DriverDataset( LR_root=LR_root,GT_root=GT_root,scale_factor=scale_factor)
    n=d.__getitem__(0)
    print(n[0].shape)
    print(n[1].shape)
    print(torch.sum(n[1]))