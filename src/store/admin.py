from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html
from urllib.parse import urlencode

from .models import Product, Collection, Customer, Order, OrderItem, Cart, CartItem, Promotion,Address


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']

    # @admin.display(ordering='products.counts')
    # def products_count(self, collection):
    #     return collection.products_count
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count=Count('products'))    


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clean_inventory']
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title']
    list_filter = ['collection', 'last_update', InventoryFilter]
    # inlines = [TagInline]

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clean Inventory')
    def clean_inventory(self, request, queryset: QuerySet):
        update_count = queryset.update(inventory=0)
        self.message_user(request, f'{update_count} products were successfully update', messages.ERROR)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_filter = ['membership']
    list_per_page = 10
    list_select_related = ["user"]
    ordering = ['user__first_name', 'user__last_name']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            }))
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


class OderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_select_related = ['customer']
    autocomplete_fields = ['customer']
    inlines = [OderItemInline]

# class CartItemInline(admin.TabularInline):
#     autocomplete_fields = ['product']
#     model = CartItem
#     extra = 1

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['created_at']
#     inlines = [CartItemInline]


# @admin.register(Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['street', 'city', 'customer']
#     list_select_related = ['customer']
#     autocomplete_fields = ['customer']