from django.contrib import admin

from .models import (
    User,
    Category,
    Product,
    ProductVariant,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Wishlist,
)


# ============================================================
# USER
# ============================================================

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "user_id",
        "full_name",
        "email",
        "phone",
        "is_admin",
        "city",
        "state",
        "created_at",
    )

    list_filter = (
        "is_admin",
        "city",
        "state",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# CATEGORY
# ============================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "category_id",
        "category_name",
        "description",
    )

    search_fields = (
        "category_name",
    )

    ordering = (
        "category_name",
    )


# ============================================================
# PRODUCT
# ============================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "product_id",
        "product_name",
        "category",
        "product_type",
        "brand",
        "price",
        "gender",
        "is_active",
        "created_at",
    )

    list_filter = (
        "category",
        "product_type",
        "gender",
        "is_active",
    )

    search_fields = (
        "product_name",
        "brand",
        "product_type",
        "description",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# PRODUCT VARIANT
# ============================================================

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):

    list_display = (
        "variant_id",
        "product",
        "size",
        "stock_quantity",
    )

    list_filter = (
        "size",
    )

    search_fields = (
        "product__product_name",
        "size",
    )

    ordering = (
        "product",
        "size",
    )


# ============================================================
# CART
# ============================================================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "cart_id",
        "user",
        "created_at",
    )

    search_fields = (
        "user__full_name",
        "user__email",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# CART ITEM
# ============================================================

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):

    list_display = (
        "cart_item_id",
        "cart",
        "variant",
        "quantity",
    )

    search_fields = (
        "cart__user__full_name",
        "cart__user__email",
        "variant__product__product_name",
    )


# ============================================================
# ORDER
# ============================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_id",
        "user",
        "order_date",
        "total_amount",
        "payment_method",
        "order_status",
    )

    list_filter = (
        "order_status",
        "payment_method",
    )

    search_fields = (
        "user__email",
        "user__full_name",
    )

    ordering = (
        "-order_date",
    )


# ============================================================
# ORDER ITEM
# ============================================================

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order_item_id",
        "order",
        "variant",
        "quantity",
        "price",
    )

    search_fields = (
        "order__user__email",
        "variant__product__product_name",
    )


# ============================================================
# WISHLIST
# ============================================================

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "wishlist_id",
        "user",
        "product",
        "created_at",
    )

    search_fields = (
        "user__full_name",
        "user__email",
        "product__product_name",
    )

    ordering = (
        "-created_at",
    )