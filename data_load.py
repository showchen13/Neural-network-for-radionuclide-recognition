import os
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import model_code
import wx
import tkinter as tk
from PyQt5.QtWidgets import QMainWindow,QApplication,QTextEdit,QAction,QFileDialog
import matplotlib.pyplot as plt


class TrainSet(Dataset):
    def __init__(self, data, data_label):
        # 定义好 image 的路径
        self.data, self.label, = data.float(), data_label

    def __getitem__(self, index):
        return self.data[index], self.label[index]

    def __len__(self):
        return len(self.data)


def data_load(batch_size):

    dirs = os.listdir('data/')
    for n, i in enumerate(dirs):
        dirs[n] = 'data/' + i + '/'
    # dirs = ['data/0/', 'data/1/', 'data/2/', 'data/3/', 'data/4/', 'data/5/', 'data/6/', 'data/7/']

    for d, q in enumerate(dirs):
        files_dir = os.listdir(q)
        # ss = '01/2/5/4/'
        # print(float(ss.split('/')[-2]))
        # print(len(files_dir))
        np_list = np.empty((len(files_dir), 2048))
        np_list_label = np.empty((len(files_dir)))

        for i, file_dir in enumerate(files_dir):
            file = open(os.path.join(q, file_dir), 'r')

            list1 = []
            j = 0
            for value in file.readlines():
                word = str(value).split()
                j = j + 1

                if (j >= 11) & (j <= 2058):
                    va = int(word[0])  # 读出来的word为列表类型
                    list1.append(va)

            # print(list1)
            np_list[i] = np.asarray(list1)

            np_list_label[i] = np.asarray(int(q.split('/')[-2]))
            # np_list_label[i] = np.asarray(0)

        if d == 0:
            c = np_list
            l = np_list_label
        else:
            c = np.concatenate((c, np_list), axis=0)
            l = np.concatenate((l, np_list_label), axis=0)

    np_mean = np.mean(c)
    np_std = np.std(c)
    np_list = (c - np_mean) / np_std
    tensor_label_list = torch.LongTensor(l)
    tensor_list = torch.tensor(np_list)
    torch_dataloader = TrainSet(tensor_list, tensor_label_list)
    loader = DataLoader(
        dataset=torch_dataloader,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4
    )
    return loader,len(dirs)


def train(loader,epoch,class_long):
    model1 = model_code.CNN_Series()
    num_ftrs = model1.fc.in_features
    model1.fc = nn.Linear(num_ftrs, class_long)
    model1.train()
    lossfunc = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model1.parameters(), lr=0.01, momentum=0.9, weight_decay=0.0001)
    for epoch in range(epoch):
        for step, (x, y) in enumerate(loader):
            out = model1(torch.unsqueeze(x, dim=1))
            print(out.shape,y.shape)
            loss = lossfunc(out, y)
            print('epoch:{},step:{},loss:{}'.format(epoch, step, loss.item()))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()



    model_dir = 'models/v2'
    # model_dir = tk.filedialog.asksaveasfilename(defaultextension=".pth")
    if os.path.isfile(model_dir):
        os.remove(model_dir)
    # torch.save(model1, 'models/v1.pth')
    torch.save(model1, model_dir)


def predict(dir):
    # classes = ['AM', 'CS+EU', 'CS', 'EU','TH+CS','TH','TH+EU','本底']
    classes = {'0':'AM','1': 'CS+EU','2': 'CS', '3':'EU', '4':'TH+CS','5': 'TH', '6':'TH+EU', '7':'本底','8':'Ba+Co','9':'Ba','10':'Cs+Co','11':'Co','12':'cs+ba'}
    model1 = torch.load('models/v2')
    model1.eval()
    # file = open('data/val/cs/34.spe', 'r')
    file = open(dir, 'r')
    list1 = []
    j = 0
    for value in file.readlines():
        word = str(value).split()
        j = j + 1

        if (j >= 11) & (j <= 2058):
            va = int(word[0])  # 读出来的word为列表类型
            list1.append(va)


    # plt.ylabel('cps')
    # plt.xlabel('ch')
    # plt.plot(range(0, len(list1)), list1)
    # plt.show()


    np_mean = np.mean(list1)
    np_std = np.std(list1)
    np_list = (list1 - np_mean) / np_std
    tensor_list = torch.tensor(np_list, dtype=torch.float32)
    x = torch.unsqueeze(torch.unsqueeze(tensor_list,dim=0),dim=0)
    out = model1(x)
    pred_score = F.softmax(out.data, dim=1)
    if pred_score is not None:
        pred_label = torch.argsort(pred_score[0], descending=True)[:1][0].item()
        # pred_label = classes[int(pred_label)]
        pred_label = classes[str(pred_label)]
        print(pred_label)

    else:
        result = {'result': 'predict score is None'}
    return pred_label, list1









# if __name__ == '__main__':


    # loader = data_load()
    # train(loader)
    # predict()



