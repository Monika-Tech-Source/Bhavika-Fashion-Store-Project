import os
import random

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.hashers import make_password

from shop.models import (
    Category,
    Product,
    ProductVariant,
    User,
)


class Command(BaseCommand):

    help = "Seeds categories, admin user, and imports product images with variants"


    # =========================================
    # CLEAN PRODUCT NAME
    # =========================================

    def clean_product_name(self, filename):

        name = os.path.splitext(filename)[0]

        name = name.replace("_", " ").replace("-", " ")

        words = name.split()

        cleaned_words = []

        for word in words:

            if word.isdigit():
                continue

            cleaned_words.append(word)

        if not cleaned_words:
            cleaned_words = ["Fashion", "Item"]

        return " ".join(cleaned_words).title()


    # =========================================
    # DETECT CATEGORY + SUBCATEGORY + GENDER
    # =========================================

    def detect_product_details(self, root_lower, filename_lower):

        path_norm = root_lower.replace("\\", "/")

        # 1. MEN CATEGORY (category_id = 1)
        if "men_products/men_jeans" in path_norm:
            return 1, "mens_jeans", "Men"
        if "men_products/men_shirts_tshirts" in path_norm:
            return 1, "mens_shirts", "Men"

        # 2. WOMEN CATEGORY (category_id = 2)
        if "women_products/women_jeans" in path_norm:
            return 2, "womens_jeans", "Women"
        if "women_products/women_tops" in path_norm:
            return 2, "womens_tops", "Women"

        # 3. KIDS CATEGORY (category_id = 3)
        if "kids_products/boys_kids_products" in path_norm:
            return 3, "boys_kids", "Kids"
        if "kids_products/girls_kids_products" in path_norm:
            return 3, "girls_kids", "Kids"

        # 4. DRESSES CATEGORY (category_id = 4)
        if "dresses/mens_dresses" in path_norm:
            return 4, "mens_dresses", "Men"
        if "dresses/womens_dresses" in path_norm:
            return 4, "womens_dresses", "Women"

        # 5. T-SHIRTS CATEGORY (category_id = 5)
        if "mens_womens_tshirts/mens_related_tshirts" in path_norm:
            return 5, "mens_tshirts", "Men"
        if "mens_womens_tshirts/women_related_tshirts" in path_norm:
            return 5, "womens_tshirts", "Women"

        # 6. SHIRTS CATEGORY (category_id = 6)
        if "men_womens_shirts/mens_related_shirts" in path_norm:
            return 6, "mens_shirts", "Men"
        if "men_womens_shirts/womens_related_shirts" in path_norm:
            return 6, "womens_shirts", "Women"

        # 7. JEANS CATEGORY (category_id = 7)
        if "jeans/mens_related" in path_norm:
            return 7, "mens_jeans", "Men"
        if "jeans/womens_related" in path_norm:
            return 7, "womens_jeans", "Women"

        # 8. FOOTWEAR CATEGORY (category_id = 8)
        if "footwear/mens/mens_casual_sneakers" in path_norm:
            return 8, "casual_sneakers", "Men"
        if "footwear/mens/mens_running_shoes" in path_norm:
            return 8, "running_shoes", "Men"
        if "footwear/mens/mens_sandals" in path_norm:
            return 8, "sandals", "Men"
        if "footwear/womens/womens_casual_sneakers" in path_norm:
            return 8, "casual_sneakers", "Women"
        if "footwear/womens/womens_flats" in path_norm:
            return 8, "flats", "Women"
        if "footwear/womens/womens_heels" in path_norm:
            return 8, "heels", "Women"
        if "footwear/womens/womens_running_shoes" in path_norm:
            return 8, "running_shoes", "Women"
        if "footwear/womens/womens_sandals" in path_norm:
            return 8, "sandals", "Women"

        # 9. ACCESSORIES CATEGORY (category_id = 9)
        if "accessories/classic_handbags" in path_norm:
            return 9, "classic_handbags", "Women"
        if "accessories/mens_accessories" in path_norm:
            return 9, "mens_accessories", "Men"
        if "accessories/mens_womens_leather_belts" in path_norm:
            return 9, "leather_belts", "Men"
        if "accessories/womens_accessories" in path_norm:
            return 9, "womens_accessories", "Women"

        return 1, "mens_shirts", "Men"


    # =========================================
    # SIZES BY CATEGORY
    # =========================================

    def get_sizes(self, category_id):

        if category_id == 8:
            return ["6", "7", "8", "9", "10"]

        if category_id == 9:
            return ["ONE SIZE"]

        if category_id == 3:
            return ["4-5Y", "6-7Y", "8-9Y", "10-11Y"]

        return ["S", "M", "L", "XL"]


    # =========================================
    # SEED CATEGORIES & ADMIN USER
    # =========================================

    def ensure_categories_and_admin(self):

        categories_data = [
            (1, "Men", "Modern essentials, sharp tailoring, and everyday menswear."),
            (2, "Women", "Contemporary silhouettes, effortless dresses, and statement styles."),
            (3, "Kids", "Playful, comfortable, and durable everyday fashion for kids."),
            (4, "Dresses", "From casual day dresses to evening and festive silhouettes."),
            (5, "T-Shirts", "Relaxed tees, graphic prints, polos, and everyday tops."),
            (6, "Shirts", "Crisp formal shirts, casual button-downs, and chic blouses."),
            (7, "Jeans", "Classic denim, high-rise fits, cargos, and tailored trousers."),
            (8, "Footwear", "Sneakers, heels, sandals, loafers, and everyday footwear."),
            (9, "Accessories", "Statement bags, watches, sunglasses, and finishing touches."),
        ]

        for cat_id, cat_name, cat_desc in categories_data:
            Category.objects.update_or_create(
                category_id=cat_id,
                defaults={
                    "category_name": cat_name,
                    "description": cat_desc,
                },
            )

        # Ensure default Admin user exists
        if not User.objects.filter(email="monika.alavelli.tech@gmail.com").exists():
            User.objects.create(
                full_name="Monika Alavelli",
                email="monika.alavelli.tech@gmail.com",
                is_admin=True,
                password=make_password("Monika@123"),
                phone="9182890623",
                address_line1="MVP Colony",
                address_line2="Sector 1",
                city="Visakhapatnam",
                state="Andhra Pradesh",
                pincode="530017",
                created_at=timezone.now(),
            )


    # =========================================
    # MAIN HANDLE FUNCTION
    # =========================================

    def handle(self, *args, **kwargs):

        self.ensure_categories_and_admin()

        products_folder = os.path.join(
            settings.BASE_DIR,
            "shop",
            "static",
            "shop",
            "images",
            "products",
        )

        if not os.path.exists(products_folder):

            self.stdout.write(
                self.style.ERROR(
                    f"Folder not found: {products_folder}"
                )
            )
            return


        brands = [
            "BHAVIKA STUDIO",
            "BHAVIKA ESSENTIALS",
            "URBAN THREAD",
            "ATELIER NINE",
            "MODA LINE",
        ]

        prices = [
            799,
            999,
            1199,
            1299,
            1499,
            1699,
            1899,
            1999,
            2299,
            2499,
        ]


        created_products = 0
        created_variants = 0


        # =====================================
        # SCAN FOLDERS
        # =====================================

        for root, dirs, files in os.walk(products_folder):

            image_files = [
                f for f in sorted(files)
                if f.lower().endswith(
                    (".jpg", ".jpeg", ".png", ".webp", ".avif")
                )
            ]

            if not image_files:
                continue


            for filename in image_files:

                full_path = os.path.join(root, filename)

                static_root = os.path.join(
                    settings.BASE_DIR,
                    "shop",
                    "static",
                )

                relative_static_path = os.path.relpath(
                    full_path,
                    static_root,
                ).replace("\\", "/")


                # Skip if already imported
                existing_product = Product.objects.filter(
                    image_url=relative_static_path
                ).first()

                if existing_product:
                    continue


                root_lower = root.lower()
                filename_lower = filename.lower()

                category_id, product_type, gender = (
                    self.detect_product_details(
                        root_lower,
                        filename_lower,
                    )
                )

                category = Category.objects.filter(
                    category_id=category_id
                ).first()

                if not category:
                    continue


                product_name = self.clean_product_name(
                    filename
                )


                # =================================
                # CREATE PRODUCT
                # =================================

                product = Product.objects.create(
                    category=category,
                    product_name=product_name,
                    description=(
                        f"Premium {product_name.lower()} crafted "
                        f"for modern everyday fashion."
                    ),
                    price=random.choice(prices),
                    brand=random.choice(brands),
                    image_url=relative_static_path,
                    is_active=True,
                    created_at=timezone.now(),
                    product_type=product_type,
                    gender=gender,
                )

                created_products += 1


                # =================================
                # CREATE SIZES / VARIANTS
                # =================================

                sizes = self.get_sizes(category_id)

                for size in sizes:

                    ProductVariant.objects.create(
                        product=product,
                        size=size,
                        stock_quantity=10,
                    )

                    created_variants += 1


        # =====================================
        # SUMMARY
        # =====================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "========================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Products created : {created_products}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Variants created : {created_variants}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "========================================="
            )
        )
