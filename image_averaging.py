#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import math
import os
import random as rand

# 3rd party
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


def images_avg(dataset_path, s=(128, 128), k=16):
    if not os.path.isdir(dataset_path):
        print('''Dataset path '{}' is not exists'''.format(dataset_path))
        return

    dataset = []

    for root, dirs, file_names in os.walk(dataset_path):
        if root != dataset_path:
            files = []

            for file_name in file_names:
                if file_name.endswith('.jpg'):
                    files.append(file_name)

            tmp = {'name': os.path.basename(root), 'files': files}
            dataset.append(tmp)

    if 1 <= k <= len(dataset):
        dataset = rand.sample(dataset, k)
    else:
        print('Sample size must be in range [1, dataset_size]')
        return

    plt.gcf().canvas.set_window_title(
        'Average of images ({}x{}) from {} random categories'.format(s[0], s[1], k))
    plt.figure(1)
    grid_rows = grid_cols = math.ceil(math.sqrt(k))

    categories_processed = 0
    for category_idx, category in enumerate(dataset):
        avg_img_data = np.array([[0, 0, 0]] * (s[0] * s[1]))
        valid_imgs_cnt = 0

        for file in category['files']:
            img_path = os.path.join(dataset_path, category['name'], file)
            img = Image.open(img_path)

            if img:
                tmp_img = img.copy()
                img.close()

                if tmp_img.mode != 'RGB':
                    tmp_img = tmp_img.convert(mode='RGB')

                tmp_img = tmp_img.resize(s)
                img_data = np.array(tmp_img.getdata())
                avg_img_data += img_data

                valid_imgs_cnt += 1
            else:
                print('''Couldn't read image {}'''.format(img_path))

        if valid_imgs_cnt:
            avg_img_data //= valid_imgs_cnt

            out = Image.new(mode='RGB', size=s)
            img_data = [(i[0], i[1], i[2]) for i in avg_img_data]
            out.putdata(img_data)

            axes = plt.subplot(grid_rows, grid_cols, category_idx + 1)
            axes.axis('off')
            plt.title(category['name'], fontsize=8, verticalalignment='center')
            plt.imshow(out)

            categories_processed += 1

        else:
            print('''Couldn't read images from {} category'''.format(category['name']))

    if categories_processed:
        plt.show()
    else:
        print('''Nothing to show. Couldn't process any category from dataset''')
