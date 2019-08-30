#%matplotlib inline
from pycocotools.coco import COCO
import os
import json
import pickle
import hashlib
from shutil import copyfile
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import csv
from main import MAP_DIR, ANNOT_SAVE_PATH, DATA_DIR, MASKS_DIR, ANNOT_DIR, KAGGLE_SAVE_PATH

###########################################################

path_to_table = os.path.join(ANNOT_DIR, 'map_list.pickle')
scv_legend_path = os.path.join(ANNOT_DIR, 'legend.csv')
IMG_DIR = MAP_DIR
coco_path = ANNOT_SAVE_PATH
csv_path = KAGGLE_SAVE_PATH

DST_DIR = 'DIR_FOR_HASHED_MAPS' #your save dir for hashed maps
coco_hashed_path = os.path.join(ANNOT_DIR, 'coco_hashed.json') #you can choose your own path
csv_hashed_path = os.path.join(ANNOT_DIR, 'kaggle_hashed.csv') #you can choose your own path

with open(path_to_table, 'rb') as f:
        obj2map = pickle.load(f)
legend = []
legend.append(['fileName', 'macroRegion'])

files = [file for file in os.listdir(IMG_DIR) if file.endswith('jpg')]
with open(coco_path, 'r') as f:
    coco_ann = f.read()

with open(csv_path, 'r') as f:
    csv_ann = f.read()

for file in files:
    src = os.path.join(IMG_DIR, file)
    file_hash = hashlib.sha224(file.encode()).hexdigest()[:10]
    dst_file = file_hash + '.jpg'
    dst = os.path.join(DST_DIR, dst_file)
    coco_ann = coco_ann.replace(file, dst_file)
    csv_ann = csv_ann.replace(file, dst_file)
    copyfile(src, dst)
    for gl_map in obj2map:
        if file.split('.jpg')[0] in gl_map:
            legend.append([dst_file, gl_map[-1]])

with open(coco_hashed_path, 'w') as f:
    f.write(coco_ann)

with open(csv_hashed_path, 'w') as f:
    f.write(csv_ann)

with open(scv_legend_path, 'w', newline='') as output_csv_file:
    writer = csv.writer(output_csv_file)
    for line in legend:
        writer.writerow(line)

###########################################################

image_directory = DST_DIR
annotation_file = coco_hashed_path

example_coco = COCO(annotation_file)
categories = example_coco.loadCats(example_coco.getCatIds())
category_names = [category['name'] for category in categories]
print('Custom COCO categories: \n{}\n'.format(' '.join(category_names)))

category_names = set([category['supercategory'] for category in categories])
print('Custom COCO supercategories: \n{}'.format(' '.join(category_names)))

category_ids = example_coco.getCatIds(catNms=['hill'])
image_ids = example_coco.getImgIds()
index = np.random.randint(0, len(image_ids))
image_data = example_coco.loadImgs(image_ids[index])[0]
print(image_data)

image = io.imread(image_directory + '/' + image_data['file_name'])
plt.imshow(image)
plt.axis('off')
pylab.rcParams['figure.figsize'] = (8.0, 10.0)
annotation_ids = example_coco.getAnnIds(imgIds=image_data['id'], catIds=category_ids, iscrowd=None)
annotations = example_coco.loadAnns(annotation_ids)
example_coco.showAnns(annotations)
