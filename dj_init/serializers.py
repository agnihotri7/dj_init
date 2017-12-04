"""
"""
from django.conf import settings
from django.core.files import File
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile


class EmptySerializer(serializers.Serializer):
    """
    """
    pass


class DateTimeSerializer(serializers.Serializer):
    """
    """
    datetime = serializers.DateTimeField()


class ImageURLField(serializers.ImageField):
    """
    """

    # def to_representation(self, obj):
    #     request =  self.context.get('request')
    #     try:
    #         return request.build_absolute_uri(str(obj.url))
    #     except ValueError:
    #         return None

    def to_internal_value(self, data):
        if not data:
            return None

        request = self.context.get('request')
        media_url = self.context.get('request').get_host() + "/media/"

        if type(data) == InMemoryUploadedFile:
            return data

        if data.startswith(media_url) or data.startswith("http://" + media_url) or data.startswith("https://" + media_url):

            if len(data.split('media/')) != 2:
                raise serializers.ValidationError("Image you have uploaded has some problem. Upload a correct image.")

            relative_path = data.split('media/')[1].replace("%20"," ")

            absolute_path = settings.MEDIA_ROOT + relative_path
            try:
                # tmp_file = open(absolute_path, 'r')     # for python 2
                tmp_file = open(absolute_path, 'rb')    # for python 3
            except (IOError, Exception) as e:
                raise serializers.ValidationError("Image you have uploaded has some problem. Upload a correct image.")

            if not "/tmp/" in data:
                return absolute_path.split('media/')[1]
            else:
                return File(tmp_file)
        else:
            raise serializers.ValidationError("Image you have uploaded has some problem. Upload a correct image.")
