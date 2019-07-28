#%matplotlib inline
from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
from main import MAP_DIR, ANNOT_SAVE_PATH


image_directory = MAP_DIR
annotation_file = ANNOT_SAVE_PATH

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
image_ids = example_coco.getImgIds()
print(len(image_ids))
