import os
import cv2
import glob
import numpy as np
import xml.etree.ElementTree as ET

img_dir = './models/object_detection/data/images/'
train_dir = 'train'
test_dir = 'test'
main_dir = [train_dir, test_dir]
for dir in main_dir:
    if not os.path.exists(f'{img_dir}/new{dir}'): 
        os.mkdir(f'{img_dir}/new{dir}')
    for file in glob.glob(f'{img_dir}{dir}/*jpg'):
        filename = os.path.basename(file)
        print(filename)
        img = cv2.imread(f'{img_dir}{dir}/{filename}')
        size = img.shape
        height = int(size[1]/4)
        width = int(size[0]/4)
        print(height,width)
        img_data = cv2.resize(img,(height,width))
        cv2.imwrite(f'{img_dir}/new{dir}/{filename}', img_data)
        #cv2.imshow('My Image', img_data)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    for file in glob.glob(f'{img_dir}{dir}/*xml'):
        filename = os.path.basename(file)
        print(filename)
        tree = ET.parse(f'{img_dir}{dir}/{filename}')
        root = tree.getroot()
        for size in root.findall('size'):
            new_width = int(int(size.find('width').text)/4)
            new_height = int(int(size.find('height').text)/4)
            size.find('width').text = str(new_width)
            size.find('height').text = str(new_height)
            print(new_width,new_height)
        for bndbox in root.iter('bndbox'):
            new_xmin = int(int(bndbox.find('xmin').text)/4)
            new_ymin = int(int(bndbox.find('ymin').text)/4)
            new_xmax = int(int(bndbox.find('xmax').text)/4)
            new_ymax = int(int(bndbox.find('ymax').text)/4)
            bndbox.find('xmin').text = str(new_xmin)
            bndbox.find('ymin').text = str(new_ymin)
            bndbox.find('xmax').text = str(new_xmax)
            bndbox.find('ymax').text = str(new_ymax)
            print(new_xmin,new_ymin,new_xmax,new_ymax)
        tree.write(f'{img_dir}/new{dir}/{filename}')

