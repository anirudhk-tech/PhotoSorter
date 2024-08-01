import os
import time
import imghdr
import shutil
from pathlib import Path

images = {}
targetPath = input("Please enter the path to your photo folder. \n")

class PhotoSorter (object):
    def execute ():
        try:
            scanPhotos(targetPath)
            check = movePhotos()

            if check: print("Done!")
            elif check == "exists": print("Please delete the existing photos folder or move it!")
            else: print("There are no pictures in that folder!")

        except Exception as e:
            print(e)
            print("Folder not found.")



def imageType (path):
    return imghdr.what(path)

def imageTime (image):
    return time.ctime(os.path.getctime(image))[-4:]

def movePhotos ():
    if not images: return None

    photosPath = f'{targetPath}/PhotoSorter'
    photos = images.keys()
    years = set(images.values())

    try:
        os.mkdir(photosPath)
    except:
        return "exists"

    for yr in years:
        os.mkdir(f'{photosPath}/{yr}')

    for photo in photos:
        shutil.move(photo, photosPath + '/' + images[photo] + '/' + os.path.basename(photo).split('/')[-1])
        
    return True

def scanPhotos (path):
    entries = os.scandir(path)

    for asset in entries:
        if asset.is_file():
            assetPath = Path(asset)
            if imageType(assetPath) != None:
                images[assetPath] = imageTime(asset)
        else:
            folderPath = Path(asset)
            for folder in os.scandir(folderPath):
                scanPhotos(folderPath)


PhotoSorter.execute()




