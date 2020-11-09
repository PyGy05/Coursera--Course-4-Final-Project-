
import zipfile

from PIL import Image
import pytesseract
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier(
    'readonly/haarcascade_frontalface_default.xml')

# the rest is up to you!
file = 'readonly/images.zip'
small_file = 'readonly/small_img.zip'
images = {}
file_name_lst = []


def unzip_images(zip_file):

    zf = zipfile.ZipFile(zip_file)

    for file in zf.infolist():

        fileName = file.filename

        z = [Image.open(zf.open(fileName))]

        images[fileName] = [Image.open(zf.open(fileName))]
        file_name_lst.append(fileName)
        # print(fileName)


if __name__ == '__main__':

    # unzip_images(small_file)
    unzip_images(file)

    for name in file_name_lst:
        img = images[name][0]

        images[name].append(
            pytesseract.image_to_string(img).replace('- \n', ''))

        txt = images[name][1]

        if 'Mark' in txt:
            # if 'Christopher' in txt:
            print('Results found in file', name)

            try:
                faces = (face_cascade.detectMultiScale(
                    np.array(img), 1.35, 4)).tolist()

                images[name].append(faces)

                faces_in_file = []

                for x, y, w, h in images[name][2]:
                    faces_in_file.append(img.crop((x, y, x+w, y+h)))

                    contact_sheet = Image.new(
                        img.mode, (550, 110*int(np.ceil(len(faces_in_file)/5))))

                    x = 0
                    y = 0

                    for face in faces_in_file:
                        face.thumbnail((110, 110))
                        contact_sheet.paste(face, (x, y))

                        if x+110 == contact_sheet.width:
                            x = 0
                            y = y + 110
                        else:
                            x = x + 110

                display(contact_sheet)
            except:
                print("But there were no faces in that file!")
