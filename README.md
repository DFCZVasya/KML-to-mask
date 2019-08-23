# KML to mask

This repository will help you convert KML files to coco format, which is used to train convolutional neural networks of mask type.
---------------
Project source can be downloaded from:
https://github.com/DFCZVasya/KML_to_mask.git
---------------

List of used libraries:
```
numpy
Pillow
requests
opencv
skimage
pycocotools
matplotlib
pylab
```

To run the program, you need to change the following lines in the **main.py**:

```ruby
GOOGLE_MAPS_API_KEY = 'your_API_key'   

DATA_DIR = os.path.abspath(r'your DATA DIR')
MAP_DIR = os.path.join(DATA_DIR, 'your MAP DIR')
MASKS_DIR = os.path.join(DATA_DIR, 'your MASKS DIR')
ANNOT_DIR = os.path.join(DATA_DIR, 'your ANNOTATION DIR')
ANNOT_SAVE_PATH = os.path.join(ANNOT_DIR, 'coco.json')  # you also can chose your own name
KAGGLE_SAVE_PATH = os.path.join(ANNOT_DIR, 'kaggle.csv')
```
You can read how to get API key here: https://developers.google.com/maps/documentation/maps-static/get-api-key

Also you need to change: 
```ruby
INFO = {
    "description": "hills",
    "url": " yor url for download your data or something else",
    "version": "0.1.0",
    "year": 2019,
    "contributor": " ",
    "date_created": datetime.datetime.utcnow().isoformat(' ')
}

LICENSES = [
    {
        "id": 1,
        "name": "Attribution-NonCommercial-ShareAlike License",
        "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
    }
]

CATEGORIES = [
    {
        'id': 1,
        'name': 'hill',
        'supercategory': 'artefact',
    }
]
```
These lines are responsible for the configuration of your output **json** file.

After that, you can run the program through the terminal using the command:
```
$ python main.py
```
To visualize the results, you need to change the following lines in the **visualization.py**:
```ruby
DST_DIR = 'DIR_FOR_HASHED_MAPS' #your save dir for hashed maps
coco_hashed_path = os.path.join(ANNOT_DIR, 'coco_hashed.json') #you can choose your own path
csv_hashed_path = os.path.join(ANNOT_DIR, 'kaggle_hashed.csv') #you can choose your own path

```
After that, you can run the program through the terminal using the command:
```
$ pytnon visualization.py
```
