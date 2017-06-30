#!/usr/bin/python
import os, shutil
import subprocess
from PIL import Image
import numpy as np

print 'Input working directory:',
root = raw_input()
download = root + '/download'
target = root + '/images/'
images = os.listdir(download)

# --------------------------------------
# Prepare images

print len(images), 'total images to convert'

result = []
means = []
for i, v in enumerate(images):
    inp = os.path.join(download, v)
    d = os.path.join(target, str(i))
    out = d + "/img.jpg"
    if not os.path.exists(d):
        os.makedirs(d)

    print '\r', i, inp,
    bashCommand = r'convert -resize 256x256! -background white -alpha remove -type truecolor ' + inp + " " + out
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    process.wait()

    if os.path.exists(out):
        means += [np.array(Image.open(out)).mean(axis=(0, 1))]
        result += [out]

means = np.mean(means, axis=0)

print '\rConvert completed'


# --------------------------------------
# Make list of train files

print len(result), 'images to train'
cur_dir = os.getcwd()

f = open(root + '/train.txt', 'w')
for i, r in enumerate(result):
    path = os.path.join(cur_dir, r)
    f.write(path + ' ' + str(i) + '\n')

f = open(root + '/val.txt', 'w')
for i, r in enumerate(result):
    path = os.path.join(cur_dir, r)
    f.write(path + ' ' + str(i) + '\n')


# --------------------------------------
# Configs

def config(path, replace):
    name = os.path.basename(path)
    out = root + '/'+name
    text = open(path).read()

    for k in replace:
        text = text.replace(k, replace[k])

    open(out, 'w').write(text)

config('templates/train_val.prototxt',
       {'#MEAN_R#': str(means[0]),
        '#MEAN_G#': str(means[1]),
        '#MEAN_B#': str(means[2]),
        '#CATEGORIES_NUMBER#': str(len(result)),
        '#BATCH_SIZE#': str(80),
        'data/': root + '/'
        })

config('templates/deploy.prototxt', {'#CATEGORIES_NUMBER#': str(len(result))})

config('templates/solver.prototxt', {'data/': root + '/'})




