from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        collections = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(collections, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CollectionSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def collection_details(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')).all(), pk=pk)

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)

        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer( collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({"error": "Collection cannot be deleted because it's include one or more products."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            products, 
            many=True,
            context={'request': request}
            )

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        
        serializer = ProductSerializer(
                        product,
                        context={'request': request}
                    )

        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer( product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response({"error": "Product cannot be deleted because it's associated with an order item."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)