from KML_to_mask import *
from make_masks import *
from specification_of_image import *
from PIL import Image
import numpy as np

GOOGLE_MAPS_API_KEY = 'your_API_key'

DATA_DIR = os.path.abspath(r'your DATA DIR')
MAP_DIR = os.path.join(DATA_DIR, 'your MAP DIR')
MASKS_DIR = os.path.join(DATA_DIR, 'your MASKS DIR')
ANNOT_DIR = os.path.join(DATA_DIR, 'your ANNOTATION DIR')
ANNOT_SAVE_PATH = os.path.join(ANNOT_DIR, 'coco.json')  # you also can chose your own name
KAGGLE_SAVE_PATH = os.path.join(ANNOT_DIR, 'kaggle.csv')

zoom = 17
size = 640

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


def main():
    coco_output = {
        "info": INFO,
        "licenses": LICENSES,
        "categories": CATEGORIES,
        "images": [],
        "annotations": []
    }

    image_id = 1
    segmentation_id = 1

    # filter for jpeg images
    for root, _, files in os.walk(MAP_DIR):

        image_files = filter_for_jpeg(root, files)
        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)
            image_info = create_image_info(
                image_id, os.path.basename(image_filename), image.size, coco_url = '')
            coco_output["images"].append(image_info)

            # filter for associated png annotations
            for root, _, files in os.walk(MASKS_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:

                    class_id = [x['id'] for x in CATEGORIES if x['name'] in annotation_filename][0]

                    category_info = {'id': class_id, 'is_crowd': 'crowd' in annotation_filename}
                    binary_mask = np.asarray(Image.open(annotation_filename)
                        .convert('1')).astype(np.uint8)

                    annotation_info = create_annotation_info(
                        segmentation_id, image_id, category_info, binary_mask,
                        image.size, tolerance=2)

                    if annotation_info is not None:
                        coco_output["annotations"].append(annotation_info)

                    segmentation_id = segmentation_id + 1

            image_id = image_id + 1

    with open(COCO_SAVE_PATH, 'w') as output_json_file:
        json.dump(coco_output, output_json_file)

def main_kaggle_csv():
    kaggle_output = []
    kaggle_output.append(['ImageId', 'EncodedPixels', 'Width', 'Height'])

    # filter for jpeg images
    for root, _, files in os.walk(MAP_DIR):

        image_files = filter_for_jpeg(root, files)
        # go through each image
        for image_filename in image_files:
            image = Image.open(image_filename)
            ImageId = os.path.basename(image_filename)
            Width = image.size[0]
            Height = image.size[1]

            # filter for associated png annotations
            for root, _, files in os.walk(MASKS_DIR):
                annotation_files = filter_for_annotations(root, files, image_filename)

                # go through each associated annotation
                for annotation_filename in annotation_files:
                    binary_mask = np.asarray(Image.open(annotation_filename)
                        .convert('1')).astype(np.uint8)
                    EncodedPixels = rle_encode_kaggle_style(binary_mask)
                    kaggle_output.append([ImageId,
                                         str(EncodedPixels),
                                         str(Width),
                                         str(Height)])

    with open(KAGGLE_SAVE_PATH, 'w', newline='') as output_csv_file:
        writer = csv.writer(output_csv_file)
        for line in kaggle_output:
            writer.writerow(line)


if __name__ == "__main__":
    read_kml_and_load_maps(ANNOT_DIR, MAP_DIR, MASKS_DIR, GOOGLE_MAPS_API_KEY, zoom, size)
    remove_masks_with_ovelapping_pixels(MASKS_DIR)
    print('annotating started ...')
    main()
    print('COCO annotation completed')
    main_kaggle_csv()
    print('KAGGLE annotation completed')
