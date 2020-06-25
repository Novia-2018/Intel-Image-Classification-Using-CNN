#!/usr/bin/env python
# coding: utf-8

# # Convolutional Neural Network

# ### Installing the libraries
!pip install tensorflow!pip install keras
!pip install opencv-python
# ## Importing The Libraries

# In[213]:


import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image as img
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow.keras.layers as Layers
import tensorflow.keras.activations as Actications
import tensorflow.keras.models as Models
import tensorflow.keras.optimizers as Optimizer
import tensorflow.keras.metrics as Metrics
import tensorflow.keras.utils as Utils
from keras.utils.vis_utils import model_to_dot
import os
import matplotlib.pyplot as plot
import cv2
import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix as CM
from random import randint
from IPython.display import SVG
import matplotlib.gridspec as gridspec


# In[184]:


tf.__version__


# In[185]:


cv2.__version__


# # Analising the Data

# In[214]:


X = []
y = []
IMG_SIZE = 150
DIR = "111880_269359_bundle_archive/seg_train/seg_train"
folders = os.listdir(DIR)
folders


# In[216]:


for i, file in enumerate(folders):
    filename = os.path.join(DIR, file)
    print("Folder {} started".format(file))
    try:
        for img in os.listdir(filename):
            path = os.path.join(filename, img)
            img = cv2.imread(path,cv2.IMREAD_COLOR)
            img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))

            X.append(np.array(img))
            y.append(i)
    except:
        print("File {} not read".format(path))
        
    print("Folder {} done".format(file))
    print("The folder {} is labeled as {}".format(file, i))


# In[217]:


np.unique(y, return_counts=True)


# ### Making the functions to get the training and validation set from the Images

# In[223]:


from tqdm import tqdm
X=[]
Z=[]

IMG_SIZE=150
IMAGE_BUILDINGS_DIR='111880_269359_bundle_archive/seg_train/seg_train/buildings'
IMAGE_FOREST_DIR='111880_269359_bundle_archive/seg_train/seg_train/forest'
IMAGE_GLACIER_DIR='111880_269359_bundle_archive/seg_train/seg_train/glacier'
IMAGE_MOUNTAIN_DIR='111880_269359_bundle_archive/seg_train/seg_train/mountain'
IMAGE_SEA_DIR='111880_269359_bundle_archive/seg_train/seg_train/sea'
IMAGE_STREET_DIR='111880_269359_bundle_archive/seg_train/seg_train/street'


# In[224]:


def assign_label(img,image_type):
    return image_type


# In[255]:


def make_train_data(image_type,DIR):
    for img in tqdm(os.listdir(DIR)):
        label=assign_label(img,image_type)
        path = os.path.join(DIR,img)
        img = cv2.imread(path,cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        
        X.append(np.array(img))
        Z.append(__builtins__.str(label))


# In[256]:


make_train_data('Buildings',IMAGE_BUILDINGS_DIR)
print(len(X))


# In[257]:


make_train_data('Forest',IMAGE_FOREST_DIR)
print(len(X))


# In[258]:


make_train_data('Glacier',IMAGE_GLACIER_DIR)
print(len(X))


# In[259]:


make_train_data('Mountain',IMAGE_MOUNTAIN_DIR)
print(len(X))


# In[260]:


make_train_data('Sea',IMAGE_SEA_DIR)
print(len(X))


# In[261]:


make_train_data('Street',IMAGE_STREET_DIR)
print(len(X))


# In[262]:



from IPython.display import display
from PIL import Image 
labels = []
dic = dict()
for i in range(0,6):
    str = '111880_269359_bundle_archive\seg_train\seg_train\\'+dirs[i]
    count = 0
    for j in os.listdir(str):
        str2 = str+"\\"+j
        im = Image.open(str2)
        count += 1
        labels.append(j)
    dic[dirs[i]] = count


# In[263]:


labels1 = []
dic1 = dict()
IMAGE_SIZE = (64,64)
for i in range(0,6):
    str = '111880_269359_bundle_archive\seg_test\seg_test\\'+dirs[i]
    count = 0
    for j in os.listdir(str):
        str2 = str+"\\"+j
        im = Image.open(str2)
        count += 1
        labels1.append(j)
    dic1[dirs[i]] = count


# In[264]:


print ("Number of training examples: {}".format(len(labels)))
print ("Number of testing examples: {}".format(len(labels1)))
print ("Each image is of size: {}".format(IMAGE_SIZE))


# In[265]:


lis1 = []
lis2 = []
for key,val in dic.items():
    lis1.append(val)
    lis2.append(key)


# In[266]:


lis11 = []
lis22 = []
for key,val in dic1.items():
    lis11.append(val)
    lis22.append(key)


# In[267]:


data = {'Name':lis2, 'train':lis1,'test':lis11}
data


# In[268]:


import pandas as pd
df = pd.DataFrame(data)
df


# ## 2.2 ) Visualizing some Random Images

# In[269]:


ax = df.plot.bar(x='Name', y=['train','test'], rot=0)
plt.title('Training sets Input')


# In[270]:


plt.pie(lis1,
        explode=(0, 0, 0, 0, 0, 0) , 
        labels=lis2,
        autopct='%1.1f%%')
plt.axis('equal')
plt.title('Proportion of each observed category')
plt.show()


# In[271]:


import random as rn
fig,ax=plt.subplots(5,3)
fig.set_size_inches(15,15)
for i in range(5):
    for j in range (3):
        l=rn.randint(0,len(Z))
        ax[i,j].imshow(X[l])
        ax[i,j].set_title('Intel_Image: '+Z[l])
        
plt.tight_layout()


# ### Preprocessing the Training set

# In[272]:


train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
seg_train = train_datagen.flow_from_directory('111880_269359_bundle_archive/seg_train/seg_train',
                                                 target_size = (64, 64),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')


# ### Preprocessing the Test set

# In[273]:


test_datagen = ImageDataGenerator(rescale = 1./255)
seg_test = test_datagen.flow_from_directory('111880_269359_bundle_archive/seg_test/seg_test',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'categorical')
IMAGE_SIZE = (64,64)


# ## Part 2 - Building the CNN

# ### Initialising the CNN

# In[281]:


cnn = tf.keras.models.Sequential()


# ### Step 1 - Convolution

# In[282]:


cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 3]))


# ### Step 2 - Pooling

# In[283]:


cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))


# ### Adding a second convolutional layer

# In[284]:


cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))


# ### Step 3 - Flattening

# In[285]:


cnn.add(tf.keras.layers.Flatten())


# ### Step 4 - Full Connection

# In[286]:


cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))


# ### Step 5 - Output Layer

# In[287]:


cnn.add(tf.keras.layers.Dense(units=6, activation='softmax'))


# In[288]:


cnn.summary()


# ## Part 3 - Training the CNN

# ### Compiling the CNN

# In[289]:


cnn.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])


# ### Training the CNN on the Training set and evaluating it on the Test set

# In[290]:


trained= cnn.fit(x = seg_train, validation_data = seg_test, epochs = 25)


# ## Evaluating the Model Performance

# In[291]:


plt.plot(trained.history['loss'])
plt.plot(trained.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epochs')
plt.legend(['train', 'test'])
plt.show()


# In[292]:


plt.plot(trained.history['accuracy'])
plt.plot(trained.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epochs')
plt.legend(['train', 'test'])
plt.show()


# ##  Visualizing Predictons on the Validation Set

# In[298]:


import numpy as np
from keras.preprocessing import image
test_image1 = image.load_img('111880_269359_bundle_archive/seg_pred/seg_pred/5.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image1)
test_image = np.expand_dims(test_image, axis = 0)
result = cnn.predict(test_image)
if result[0][0] == 1:
  prediction = 'Building'
elif result[0][1] == 1:
  prediction = 'Forest'
elif result[0][2] == 1:
  prediction = 'Glacier'
elif result[0][3] == 1:
  prediction = 'Mountain'
elif result[0][4] == 1:
  prediction = 'Sea'
elif result[0][5] == 1:
  prediction = 'Street'
else:
    print("Error")


# In[297]:


result


# In[299]:


print(prediction)

