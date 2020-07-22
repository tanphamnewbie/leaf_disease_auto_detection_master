import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from keras.preprocessing import image

#Tạo model giống như model khi train trên Colab
model = Sequential()
model.add(Conv2D(16,(3,3), activation='relu', input_shape=(150,150,3)))
model.add(MaxPooling2D(2,2))
model.add(Conv2D(32,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(2,2))
model.add(Flatten())
model.add(Dense(128,activation='relu'))
model.add(Dense(512,activation='relu'))
model.add(Dense(4, activation='softmax'))

#Load weight model từ file .h5
model.load_weights(".\weight\model06072020.h5")

#Load ảnh muốn test và tiền xử lí ảnh trước khi predict
path = "./test_file/greening/greening (165).png"
img = image.load_img(path, target_size=(150,150))
x = image.img_to_array(img)/255
x = np.expand_dims(x, axis=0)
image = np.vstack([x])

#Predict ảnh
classes = model.predict(image,batch_size=10)

#Xử lí sau predict và in ra output
label=np.argmax(classes)
loai_la=['blackspot','canker','greening','healthy']
print("This leaf is %s " %(loai_la[label]))






