from decimal import Decimal

from rest_framework import serializers

from .models import Product, Collection, Review, Cart, Order, CartItem, OrderItem, Customer


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review    
        fields = ["id", "name", "description", "date", "product"]

    product = serializers.StringRelatedField()

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    
class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'inventory', 'description', 'collection', 'price_with_tax', 'reviews']

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
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]  

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    
    
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found')
        return value
    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except CartItem.DoesNotExist:
            # self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity) That is redondant
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']