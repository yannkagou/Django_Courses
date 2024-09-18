from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDerails.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetails.as_view(), name='collection-details'),
    path('products/<int:product_pk>/reviews/', views.ReviewList.as_view()),
    path('products/<int:product_pk>/reviews/<int:pk>/', views.ReviewDetails.as_view()),
]