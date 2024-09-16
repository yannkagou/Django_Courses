from decimal import Decimal

from rest_framework import serializers

from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.IntegerField()
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'inventory', 'description', 'collection', 'price_with_tax']

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-details'
    )

    price_with_tax = serializers.SerializerMethodField(method_name='calculated_tax')

    def calculated_tax(self, product: Product):
        return product.unit_price * Decimal(1.19)
    
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data
    
