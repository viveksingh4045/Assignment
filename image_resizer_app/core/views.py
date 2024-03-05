import logging
import base64

from django.shortcuts import render, redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from multiprocessing import Pool
from PIL import Image
from io import BytesIO

#Creating App logger
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
    '''
    View function support both Get and POST method. On get method function
    will render home.html file to user. On valid post method function will render
    home.html with resized image data.
    '''
    if request.method == "POST":
        try:
            logger.info('Request received for resizing images')
            images = request.FILES.getlist('images')
            resizing_factor = int(request.POST['range'])

            if validate_file_type_and_size(images):
                #start multiprocessing for image resizing
                resized_images = []
                pool = Pool(5)
                resized_images = pool.map(resize_image, [(img,resizing_factor) for img in images])
                pool.close()
                pool.join()

            # Render images on the frontend
            logger.info('Request for resizing images have been processed successfully')
            return render(request, 'home.html',{'resized_images':resized_images,
                                                'resizing_factor':resizing_factor})
        except Exception as ex:
            messages.error(request, f'Error - {ex}')
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')


def validate_file_type_and_size(images:list)->bool:
    '''
    Function will take List of images as input and will validate
    file type and size. If file type is image and combined size is 
    less the 50MB function will return true.

    Else function will raise Exception

    :param images: list of images

    :return boolean: True if all conditions are satisfied
    '''
    valid_extension=['apng', 'avif', 'gif', 'jpg',
                      'jpeg', 'jfif', 'pjpeg', 'pjp', 'png', 'svg', 'webp']
    size = 0
    for img in images:
        ext = img.name.split('.')[-1]
        if ext not in valid_extension:
            logger.error(f"Image processing failed Invalid file type - {ext}")
            raise Exception(f'Invalid file type - {ext},'
                            f' Supported file types are - {valid_extension}')
        size += img.size
    if size/1024**2 > 50:
        logger.error(f"Image processing failed file sizes are more then expected limit")
        raise Exception('File sizes are more then expected limit, '
                        f'given size - {size//1024**2}MB, Max allowed limit is - 50MB')
    return True


def resize_image(args)->InMemoryUploadedFile:
    '''
    Function take image and resizing factor in percentage as input
    and returns resized image. Function internally make use of PIL library to
    manipulate image.

    :param image: type - django.core.files.uploadedfile.InMemoryUploadedFile
    :param resizing_factor: type - int

    returns - resized image
    '''
    image:InMemoryUploadedFile = args[0]
    resizing_factor:int=args[1]
    img = Image.open(image)
    #calculating resized width and height based on resizing factor
    width  = int((img.width * resizing_factor) / 100)
    height = int((img.height * resizing_factor) / 100)
    resized_img = img.resize((width, height))
    buffer = BytesIO()
    resized_img.save(buffer, format=img.format)
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode('utf-8')