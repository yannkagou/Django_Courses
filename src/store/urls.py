from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetails.as_view()),
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetails.as_view(), name='collection-details'),
    path('products/<int:product_pk>/reviews/', views.ReviewList.as_view()),
    path('products/<int:product_pk>/reviews/<int:pk>/', views.ReviewDetails.as_view()),
    path('carts/', views.CartAdd.as_view()),
    path('carts/<int:pk>/', views.CartDetails.as_view()),
    path('carts/<int:cart_pk>/items/', views.CartItemsList.as_view()),
    path('carts/<int:cart_pk>/items/<int:pk>/', views.CartItemsDetails.as_view()),
    path('customers/', views.CustomerAdd.as_view()),
    path('customers/<int:pk>/', views.CustomerDetails.as_view()),
    path('customers/me/', views.CurrentCustomer.as_view()),
    path('orders/', views.OrderList.as_view()),
    path('orders/<int:pk>/', views.OrderDetails.as_view()),
    path('products/<int:product_pk>/images/', views.ProductImageList.as_view()),
    path('products/<int:product_pk>/images/<int:pk>/', views.ProductImageDetails.as_view()),
]