from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggItemManager(models.Manager):
    def get_tag_for(self, obj_type, obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        return TaggedItem.objects.select_related('tag').filter(content_type=content_type, object_id=obj_id)

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label   
    
    class Meta:
        ordering = ['label']

class TaggedItem(models.Model):
    objects = TaggItemManager()
    # what tag applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # product = models.ForeignKey(Product, on_delete=models.CASCADE) Not a good Practise

    # Type (product, video, article)  
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
     # ID
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
