import os
import math

from PIL import Image

from django.conf import settings
from django.utils.timezone import now
from django.core.files.images import get_image_dimensions


def create_image_thumbnail(image_path, ratio=(100, 100)):
    """
    Create thumbnail of Image specified width and height.
    """
    print(image_path)
    file_name, ext = os.path.splitext(image_path)
    thumb_path = "%s_thumb%s" %(file_name, ext)
    ext = '.jpg' if not ext else ext

    if os.path.exists(image_path):
        image = Image.open(image_path, mode='r')
        image.thumbnail(ratio, Image.ANTIALIAS)
        image.save("%s_thumb%s" % (file_name, ext))


def create_multi_size_thumbnail(image_path):
    """
    """
    print(image_path)
    file_name, ext = os.path.splitext(image_path)
    thumb_path = "%s_thumb%s" %(file_name, ext)
    ext = '.jpg' if not ext else ext

    if os.path.exists(image_path) and not os.path.exists(thumb_path): # Check if image file exists at image_path and its thumb doesn't exists.
        image = Image.open(image_path, mode='r')
        image_width, image_height = image.size

        small_dimension = min(image_width, image_height)
        thumb_percentage = math.ceil((150 * 100)/small_dimension)/100 # thumb size should not be less than 150

        # Dictionay containing thumb_name as key and tuple of image's width and height as its value.
        aspect_ratios = {
            '3x': (int(image_width * .75), int(image_height * .75)),
            '2x': (int(image_width * .50), int(image_height * .50)),
            '1x': (int(image_width * .25), int(image_height * .25)),
            'thumb': (int(image_width * thumb_percentage), int(image_height * thumb_percentage)),
        }

        resize_image_1x = image.resize(aspect_ratios['1x'], Image.ANTIALIAS)
        resize_image_1x.save("%s_%s%s" % (file_name, '1x', ext))

        resize_image_2x = image.resize(aspect_ratios['2x'], Image.ANTIALIAS)
        resize_image_2x.save("%s_%s%s" % (file_name, '2x', ext))

        resize_image_3x = image.resize(aspect_ratios['3x'], Image.ANTIALIAS)
        resize_image_3x.save("%s_%s%s" % (file_name, '3x', ext))

        print('image_path thumb ratio', aspect_ratios['thumb'])
        resize_image_thumb = image.resize(aspect_ratios['thumb'], Image.ANTIALIAS)
        resize_image_thumb.save("%s_%s%s" % (file_name, 'thumb', ext))

        # for name, ratio in aspect_ratios.items():
        #     thumb_image = image.thumbnail(ratio, Image.ANTIALIAS)
        #     thumb_image.save("%s_%s%s" % (file_name, name, ext))


def get_sq_box_size(image_width, image_height):
    """
    """
    crop_size = abs(image_width - image_height)/2
    if (image_width == image_height) or crop_size <= 10:
        return None

    if image_width > image_height:
        sq_size = image_height

        left = crop_size
        upper = 0
        right = crop_size + sq_size
        lower = sq_size
        box = (int(left), int(upper), int(right), int(lower))

    elif image_width < image_height:
        sq_size = image_width

        left = 0
        upper = crop_size
        right = sq_size
        lower = crop_size + sq_size
        box = (int(left), int(upper), int(right), int(lower))

    return box


def create_crop_image(image_path, media_folder):
    """
    media_folder = "folder_name", in the media folder.
    box = (left, upper, right, lower)

       (left, upper)
     _______*_______________
    |       |       |       |
    |       |       |       |heigth
    |       |       |       |
    |       |       |       |
    ----------------*--------
        width   (right, lower)

    """
    print('crop', image_path)
    file_name, ext = os.path.splitext(image_path)
    ext = '.jpg' if not ext else ext

    try:
        image = Image.open(image_path, mode='r')
        image_width, image_height = image.size
    except FileNotFoundError as e:
        print("%s" %(e))
        return (None, None)

    box = get_sq_box_size(image_width, image_height)
    if not box: return (None, None)

    # new_file_name = "%s/%s_%s%s" %(media_folder, file_name.split('/')[-1], now().strftime("%Y%m%d%H%M%f"), ext)
    new_file_name = "%s/%s%s" %(media_folder, file_name.split('/')[-1], ext)
    new_file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)

    try:
        region = image.crop(box)
        region.save(new_file_path)
        image.close()
    except Exception as e:
        print("%s" %(e))
        return (None, None)

    return (new_file_name, new_file_path)
