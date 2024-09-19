from decimal import Decimal

from rest_framework import serializers

from .models import Product, Collection, Review, Cart, Order, CartItem, OrderItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'inventory', 'description', 'collection', 'price_with_tax']

    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-details'
    )

    # collection = serializers.StringRelatedField()

    # collection = CollectionSerializer()

    price_with_tax = serializers.SerializerMethodField(method_name='calculated_tax')

    def calculated_tax(self, product: Product):
        return product.unit_price * Decimal(1.19)
    
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review    
        fields = ["id", "name", "description", "date", "product"]

    product = serializers.StringRelatedField()

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]
    
    def get_total_price(self, cartitem: CartItem):
        return cartitem.quantity * cartitem.product.unit_price
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    items = CartItemSerializer(many=True)

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.unit_price for item in cart.items.all()])
