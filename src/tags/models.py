from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# from store.models import Product

class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggItem(models.Model):
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # product = models.ForeignKey(Product, on_delete=models.CASCADE) Not a good Practise

    # Type (product, video, article)
    # ID
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
