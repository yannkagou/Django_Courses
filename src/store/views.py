from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import action

from .models import Product, Collection, Review, Cart, Order, CartItem, OrderItem, Customer
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer


# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         collections = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(collections, many=True)

#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = CollectionSerializer(request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_details(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')).all(), pk=pk)

#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)

#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer( collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)
    
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({"error": "Collection cannot be deleted because it's include one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             products, 
#             many=True,
#             context={'request': request}
#             )

#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = ProductSerializer(request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class ProductList(APIView):
#     def get(self, request):
#         products = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             products, 
#             many=True,
#             context={'request': request}
#             )

#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_details(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     if request.method == 'GET':
        
#         serializer = ProductSerializer(
#                         product,
#                         context={'request': request}
#                     )

#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer( product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data)
    
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response({"error": "Product cannot be deleted because it's associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class CollectionDetails(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be deleted because it's include one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
class ProductDerails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({"error": "Product cannot be deleted because it's associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ReviewList(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {"product_id": self.kwargs['product_pk']}
    

class ReviewDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {"product_id": self.kwargs['product_pk']}
    

class CartAdd(CreateAPIView):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartDetails(RetrieveDestroyAPIView):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemsList(ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}

class CartItemsDetails(RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        return {"cart_id": self.kwargs['cart_pk']}
    
class CustomerAdd(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetails(RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CurrentCustomer(APIView):
    def get(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        serializer = CustomerSerializer(customer)

        return Response(serializer.data)
    
    def put(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        serializer = CustomerSerializer(customer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)




    