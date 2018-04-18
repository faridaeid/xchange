from django.db import models

from profiles.models import User

#
# class Category(models.Model):
#     cat_id = models.AutoField(primary_key=True)
#     cat_name = models.CharField(max_length=30)
#     cat_descr = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = 'category'
#
#
# class Product(models.Model):
#     product_id = models.AutoField(primary_key=True)
#     product_name = models.CharField(max_length=30)
#     product_specs = models.CharField(max_length=200)
#     product_price = models.DecimalField(max_digits=20, decimal_places=3)
#     number_in_stock = models.PositiveIntegerField()
#     category_id = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_id')
#
#     class Meta:
#         db_table = 'product'
#
#
# class Store(models.Model):
#     store_id = models.AutoField(primary_key=True)
#     store_name = models.CharField(max_length=40)
#     create_date = models.DateField()
#     owner = models.ForeignKey(User, models.DO_NOTHING)
#
#     class Meta:
#         db_table = 'store'
#
#
# class StoreCategories(models.Model):
#     store_id = models.ForeignKey(Store, models.DO_NOTHING, db_column='store_id')
#     category_id = models.ForeignKey(Category, models.DO_NOTHING, db_column='categorsy_id')
#
#     class Meta:
#         db_table = 'store_categories'
#         unique_together = (('store_id', 'category_id'),)
#
#
# class Cart(models.Model):
#     cart_id = models.AutoField(primary_key=True)
#     owner_id = models.ForeignKey(User, models.DO_NOTHING, db_column='owner_id')
#
#     class Meta:
#         db_table = 'cart'
#
#
# class CartProducts(models.Model):
#
#     cart_id = models.ForeignKey(Cart, models.DO_NOTHING, db_column='cart_id')
#     product_id = models.ForeignKey(Product, models.DO_NOTHING, db_column='product_id')
#     quantity = models.PositiveIntegerField()
#
#     class Meta:
#         db_table = 'cart_products'
#         unique_together = ('cart_id', 'product_id')
#
#
# class Order(models.Model):
#     seller_id = models.ForeignKey(User, models.DO_NOTHING, related_name='seller_id', db_column='seller_id')
#     buyer_id = models.ForeignKey(User, models.DO_NOTHING, related_name='buyer_id', db_column='buyer_id')
#     product_id = models.ForeignKey(Product, models.DO_NOTHING, db_column='product_id')
#     quantity = models.PositiveIntegerField()
#     order_date = models.DateField()
#
#     class Meta:
#         db_table = 'order'
#         unique_together = ('seller_id', 'buyer_id', 'product_id')


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        db_table = 'cart'


class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, models.DO_NOTHING, primary_key=True)
    product = models.ForeignKey('Product', models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    is_checkedout = models.IntegerField()

    class Meta:
        db_table = 'cart_products'
        unique_together = (('cart', 'product'),)


class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=30)
    cat_descr = models.CharField(max_length=100)

    class Meta:
        db_table = 'category'


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=30)
    product_specs = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=20, decimal_places=3)
    number_in_stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        db_table = 'product'


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=40)
    create_date = models.DateField()
    owner = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        db_table = 'store'


class StoreCategories(models.Model):
    store = models.ForeignKey(Store, models.DO_NOTHING, primary_key=True)
    category = models.ForeignKey('Category', models.DO_NOTHING)

    class Meta:
        db_table = 'store_categories'
        unique_together = (('store', 'category'),)


class Transaction(models.Model):
    buyer = models.ForeignKey(User, models.DO_NOTHING, primary_key=True, related_name='buyer')
    seller = models.ForeignKey(User, models.DO_NOTHING, related_name='seller')
    product = models.ForeignKey(Product, models.DO_NOTHING)
    quantity = models.PositiveIntegerField()
    transation_date = models.DateField()

    class Meta:
        db_table = 'transaction'
        unique_together = (('buyer', 'seller', 'product'),)

