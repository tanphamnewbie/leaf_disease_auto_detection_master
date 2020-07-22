import numpy as np
import cv2
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from keras.preprocessing import image

root = Tk()
root.title( 'Tự động nhận dạng bệnh trên lá')
root.minsize(300, 300)

def open():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=(("png", "*.png"),("All Files", "*.*")))
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    global image
    global img
    global output

    img = cv2.imread(root.filename)
    #img = cv2.resize(img ,((int)(img.shape[1]/3),(int)(img.shape[0]/3)))
    original = img.copy()
    neworiginal = img.copy()

    # Guassian blur
    blur = cv2.GaussianBlur(img, (11, 11), 1)

    # Phát hiện cạnh
    canny = cv2.Canny(blur, 50, 290)
    canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)

    # Vẽ viền
    bordered = cv2.cvtColor(canny, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(bordered, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    maxC = 0
    for x in range(len(contours)):
        if len(contours[x]) > maxC:
            maxC = len(contours[x])
            maxid = x

    cv2.drawContours(neworiginal, contours[maxid], -1, (0, 0, 255))

    # Tạo hình chữ nhật bao quanh lá
    height, width, _ = canny.shape
    min_x, min_y = width, height
    max_x = max_y = 0
    frame = canny.copy()

    # Tách ra từ ảnh gốc
    for contour, hier in zip(contours, hierarchy):
        (x, y, w, h) = cv2.boundingRect(contours[maxid])
        min_x, max_x = min(x, min_x), max(x + w, max_x)
        min_y, max_y = min(y, min_y), max(y + h, max_y)
        if w > 80 and h > 80:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
            roi = img[y:y + h, x:x + w]
            originalroi = original[y:y + h, x:x + w]

    if (max_x - min_x > 0 and max_y - min_y > 0):
        roi = img[min_y:max_y, min_x:max_x]
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)
    cv2.imwrite('Cropped Img.jpg', roi)


    # Tạo model giống như model khi train trên Colab
    model = Sequential()
    model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(150, 150, 3)))
    model.add(MaxPooling2D(2, 2))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(2, 2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(4, activation='softmax'))
    model.summary()

    # Load weight model từ file .h5
    model.load_weights(".\weight\model06072020.h5")

    # Load ảnh muốn test và tiền xử lí ảnh trước khi predict
    img = cv2.resize(roi, (150, 150))
    x = image.img_to_array(img) / 255
    x = np.expand_dims(x, axis=0)
    imgexpand = np.vstack([x])

    # Predict ảnh
    classes = model.predict(imgexpand, batch_size=10)

    # Xử lí sau predict và in ra output
    label = np.argmax(classes)
    loai_la = ['bị bệnh đốm đen.', 'bị bệnh loét.', 'bị bệnh vàng lá.', 'khoẻ mạnh.']
    print("Chiếc lá này %s " % (loai_la[label]))
    root.output = "Chiếc lá này %s" % (loai_la[label])
    my_label = Label(root, text=root.output).pack()
    my_image_label = Label(image=my_image).pack()

my_btn = Button(root, text="Chọn ảnh", command = open).pack()
#my_btn1 = Button(root, text = "Run", command = ka).pack()
root.mainloop()