from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
import numpy as np
import datetime

from .forms import CategoryForm, ProductForm, SearchForm
from .models import Store, Category, Product, Cart

from Encryption import Encryption

def get_store_id(user_id):
    owner = Store.objects.raw('''SELECT * FROM store WHERE owner_id = "{}" '''
                              .format(user_id))
    if len(list(owner)):
        return list(owner)[0].store_id
    else:
        return None


def get_cart_id(user_id):
    owner = Cart.objects.raw('''SELECT * FROM cart WHERE owner_id = "{}"'''
                             .format(user_id))
    if len(list(owner)):
        return list(owner)[0].cart_id
    else:
        return None


class HomePageView(View):
    seller_template_name = 'seller_homepage.html'
    buyer_template_name = 'buyer_homepage.html'
    categoryForm = CategoryForm
    searchForm = SearchForm

    def get(self, request):
        if not request.session.get('account_type'):
            self.set_account_type(request)

        if request.session['account_type'] == 'SB':
            if 'buyer_btn' in request.GET:
                return self.buyer_view(request)
            else:
                return self.seller_view(request)

        if 'S' in request.session['account_type']:
            return self.seller_view(request)

        else:
            return self.buyer_view(request)

    def set_account_type(self, request):
        store_id = get_store_id(request.session['user_id'])
        cart_id = get_cart_id(request.session['user_id'])
        request.session['account_type'] = ''
        if store_id:
            request.session['account_type'] += 'S'
            request.session['store_name'] = list(Store.objects.raw('''SELECT * FROM store WHERE owner_id = "{}"'''
                                                                   .format(request.session['user_id'])))[0].store_name
        if cart_id:
            request.session['account_type'] += 'B'

    def get_my_categories(self, store_id):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT category_id FROM store_categories WHERE store_id = "{}"'''.format(store_id))
            result = cursor.fetchall()
            categories_id = np.asarray(result).reshape(-1)

            if not len(categories_id):
                return None

            result = Category.objects.raw('''SELECT * FROM category WHERE cat_id IN ({})'''
                                          .format(','.join(str(e) for e in categories_id.tolist())))
            return result

    def seller_view(self, request):
        store_id = get_store_id(request.session['user_id'])
        my_categories = self.get_my_categories(store_id)
        category_form = self.categoryForm()
        return render(request,
                      template_name=self.seller_template_name,
                      context={'category_form': category_form,
                               'my_categories': my_categories})

    def buyer_view(self, request):
        search_form = self.searchForm()
        return render(request,
                      template_name=self.buyer_template_name,
                      context={'search_form': search_form})


class LogoutView(View):
    def get(self, request):
        request.session['username'] = None
        request.session['user_id'] = None
        request.session['account_type'] = None
        return redirect('start_view')


class CategoryView(HomePageView):
    def check_cat_name_exixts(self, request, category_name):
        store_id = get_store_id(request.session['user_id'])
        with connection.cursor() as cursor:
            same_name_category = Category.objects.raw('''SELECT * FROM category WHERE cat_name  = "{}"'''
                                                      .format(category_name))

            for category in list(same_name_category):

                cursor.execute('''SELECT COUNT(*) FROM store_categories 
                                                  WHERE category_id = "{}" AND store_id = "{}"'''
                               .format(category.cat_id, store_id))

                (number_of_rows,) = cursor.fetchone()

                if number_of_rows:
                    return number_of_rows

            return 0


class CategoryAddView(CategoryView):
    def post(self, request):
        with connection.cursor() as cursor:

            add_category_form = self.categoryForm(request.POST)

            if add_category_form.is_valid():

                data = add_category_form.cleaned_data
                category_name = data['category_name']

                name_exists = self.check_cat_name_exixts(request, category_name)
                if name_exists:
                    return render(request=request,
                                  template_name=self.seller_template_name,
                                  context={'category_form': add_category_form,
                                           'cat_error': True})

                query = '''INSERT INTO category(cat_name, cat_descr) VALUES ("{}", "{}")'''
                cursor.execute(query
                               .format(add_category_form['category_name'].data,
                                       add_category_form['category_descr'].data))
                cat_id = cursor.lastrowid
                store_id = get_store_id(request.session['user_id'])
                query = '''INSERT INTO store_categories(category_id, store_id) VALUES ("{}", "{}")'''
                cursor.execute(query.format(cat_id, store_id))

                return redirect('homepage_view')


class CategoryEditView(CategoryView):
    def get(self, request, cat_id):
        category_select = Category.objects.raw('''SELECT * FROM category WHERE cat_id = "{}"'''.format(cat_id))
        category = list(category_select)[0]

        edit_category_form = CategoryForm(initial={'category_name': category.cat_name,
                                                   'category_descr': category.cat_descr})

        return render(request,
                      template_name=self.seller_template_name,
                      context={'category_form': edit_category_form,
                               'show_edit_modal': True,
                               'category_id': cat_id})

    def post(self, request, cat_id):
        form = self.categoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:

                number_of_rows = self.check_cat_name_exixts(request, format(data['category_name']))

                myself = len(list(Category.objects.raw(
                    '''SELECT * FROM category WHERE cat_name  = "{}" AND cat_id = "{}"'''
                        .format(data['category_name'], cat_id))))

                if number_of_rows > 1 or number_of_rows == 1 and myself == 0:
                    return render(request=request,
                                  template_name=self.seller_template_name,
                                  context={'category_form': form,
                                           'show_edit_modal': True,
                                           'cat_error': True})

                cursor.execute('''UPDATE category SET cat_name = "{}", cat_descr = "{}"  WHERE cat_id = "{}"'''
                               .format(data['category_name'], data['category_descr'], cat_id))
                return redirect('homepage_view')


class CategoryUpdateView(CategoryView):  # TODO update this shit
    def post(self, request, cat_id):
        form = self.categoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:

                number_of_rows = self.check_cat_name_exixts(request, format(data['category_name']))

                myself = len(list(Category.objects.raw(
                    '''SELECT * FROM category WHERE cat_name  = "{}" AND cat_id = "{}"'''
                        .format(data['category_name'], cat_id))))

                if number_of_rows > 1 or number_of_rows == 1 and myself == 0:
                    return render(request=request,
                                  template_name=self.seller_template_name,
                                  context={'category_form': form,
                                           'show_edit_modal': True,
                                           'cat_error': True})

                cursor.execute('''UPDATE category SET cat_name = "{}", cat_descr = "{}"  WHERE cat_id = "{}"'''
                               .format(data['category_name'], data['category_descr'], cat_id))
                return redirect('homepage_view')


class CategoryDeleteView(View):
    def post(self, request, cat_id):
        with connection.cursor() as cursor:
            store_id = get_store_id(request.session['user_id'])
            cursor.execute('''DELETE FROM store_categories WHERE category_id = "{}" AND store_id = "{}"'''
                           .format(cat_id, store_id))
            cursor.execute('''DELETE from transaction WHERE product_id IN
                              (SELECT product_id from product WHERE  category_id = "{}")'''.format(cat_id))
            cursor.execute('''DELETE from cart_products WHERE product_id IN
                                          (SELECT product_id from product WHERE  category_id = "{}")'''.format(cat_id))
            cursor.execute('''DELETE from product WHERE category_id = "{}"'''.format(cat_id))
            cursor.execute('''DELETE FROM category WHERE cat_id = "{}"'''.format(cat_id))
            return redirect('homepage_view')


class CategoryProductsView(View):
    template_name = 'single_category.html'
    productForm = ProductForm

    def get(self, request, cat_id):
        product_form = self.productForm()

        category_name = list(Category.objects.raw('''SELECT * FROM category WHERE cat_id = "{}"'''
                                                  .format(cat_id)))[0].cat_name

        my_products = Product.objects.raw('''SELECT * FROM product WHERE category_id = "{}"'''.format(cat_id))

        return render(request=request,
                      template_name=self.template_name,
                      context={'my_products': my_products,
                               'product_form': product_form,
                               'category_name': category_name})

    def check_product_name_repeated(self, product_name, cat_id):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT COUNT(*) FROM product 
                                            WHERE product_name = "{}" AND category_id = "{}"'''
                           .format(product_name, cat_id))
            (number_of_rows,) = cursor.fetchone()

            return number_of_rows


class ProductAddView(CategoryProductsView):
    def post(self, request, cat_id):
        form = self.productForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:

                if not self.check_product_name_repeated(data['product_name'], cat_id):

                    cursor.execute('''INSERT INTO product(product_name, product_specs, 
                                  product_price, number_in_stock, category_id) 
                                  VALUES ("{}", "{}", "{}", "{}", "{}")'''
                                   .format(data['product_name'], data['product_specs'],
                                           data['product_price'], data['number_in_stock'], cat_id))

                    return redirect('category_products_view', cat_id=cat_id)
                else:
                    return render(request=request,
                                  template_name=self.template_name,
                                  context={'product_form': form,
                                           'modal_error': True})


class ProductDeleteView(View):
    def post(self, request, cat_id, product_id):
        with connection.cursor() as cursor:
            cursor.execute('''DELETE FROM cart_products WHERE product_id = "{}"'''.format(product_id))
            cursor.execute('''DELETE FROM transaction WHERE product_id = "{}"'''.format(product_id))
            cursor.execute('''DELETE FROM product WHERE product_id = "{}"'''.format(product_id))
            return redirect('category_products_view', cat_id=cat_id)


class ProductEditView(CategoryProductsView):
    def get(self, request, cat_id, product_id):
        product_select = Product.objects.raw('''SELECT * FROM product WHERE product_id = "{}"'''.format(product_id))
        product = list(product_select)[0]

        edit_product_form = ProductForm(initial={'product_name': product.product_name,
                                                 'product_specs': product.product_specs,
                                                 'product_price': product.product_price,
                                                 'number_in_stock': product.number_in_stock})

        return render(request,
                      template_name=self.template_name,
                      context={'product_form': edit_product_form,
                               'show_edit_modal': True})

    def post(self, request, cat_id, product_id):

        form = self.productForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:

                cursor.execute('''SELECT COUNT(*) FROM product
                                  WHERE product_name = "{}" AND category_id = "{}" AND product_id != "{}"'''
                               .format(data['product_name'], cat_id, product_id))

                (number_of_rows,) = cursor.fetchone()

                if number_of_rows == 0:

                    cursor.execute('''UPDATE product SET product_name = "{}", product_specs = "{}", 
                                                 product_price = "{}", number_in_stock = "{}" 
                                                 WHERE product_id = "{}"'''
                                   .format(data['product_name'], data['product_specs'],
                                           data['product_price'], data['number_in_stock'], product_id))

                    return redirect('category_products_view', cat_id=cat_id)
                else:
                    return render(request=request,
                                  template_name=self.template_name,
                                  context={'product_form': form,
                                           'modal_error': True,
                                           'show_edit_modal': True})


class SearchView(HomePageView):
    def post(self, request):

        form = self.searchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                if data['search_filter'][0] == 'C':
                    cursor.execute(
                        '''SELECT C.cat_name, S.store_name, C.cat_descr, S.store_id, C.cat_id
                          FROM store S, category C, store_categories SC 
                          WHERE SC.category_id IN 
                          (SELECT cat_id FROM category WHERE cat_name LIKE "%%{}%%")
                          AND S.store_id = SC.store_id
                          AND C.cat_id = SC.category_id'''.format(data['search_item']))

                    categories_result = cursor.fetchall()

                    return render(request=request,
                                  template_name=self.buyer_template_name,
                                  context={'categories_result': categories_result,
                                           'search_form': form})

                elif data['search_filter'][0] == 'S':
                    cursor.execute(
                        '''SELECT S.store_name, S.create_date, U.username, S.store_id 
                            FROM store S, user U WHERE S.store_name LIKE "%%{}%%" 
                            AND U.user_id = S.owner_id
                            '''.format(data['search_item']))

                    store_result = cursor.fetchall()

                    encryption = Encryption()

                    store_result = [(store[0], store[1], encryption.decrypt(store[2][2:-1].encode()), store[3])
                                    for store in store_result]

                    return render(request=request,
                                  template_name=self.buyer_template_name,
                                  context={'store_result': store_result,
                                           'search_form': form})

                else:
                    cursor.execute(
                        '''SELECT P.product_name, P.product_specs, P.product_price, 
                          P.number_in_stock, S.store_name, C.cat_name, P.product_id
                          FROM  product P, store_categories SC, store S, category C  
                          WHERE P.product_name LIKE "%%{}%%"
                          AND C.cat_id = P.category_id
                          AND SC.category_id = P.category_id 
                          AND S.store_id = SC.store_id'''.format(data['search_item']))

                    product_result = cursor.fetchall()

                    return render(request=request,
                                  template_name=self.buyer_template_name,
                                  context={'product_result': product_result,
                                           'search_form': form})


class SingleCategoryView(View):
    template_name = 'single_category_view.html'

    def get(self, request, cat_id):
        return self.custom_get_method(request, cat_id, 0)

    def post(self, request, cat_id):
        with connection.cursor() as cursor:
            product_id = int(request.POST['product_id'])
            cart_id = get_cart_id(request.session['user_id'])

            cursor.execute('''SELECT COUNT(*), is_checkedout FROM cart_products 
                            WHERE cart_id = "{}" AND product_id = "{}"'''.format(cart_id, product_id))

            (number_of_rows, is_checkedout) = cursor.fetchone()

            if number_of_rows == 0:
                cursor.execute('''INSERT INTO cart_products(cart_id, product_id, quantity, is_checkedout)
                                                  VALUES ("{}", "{}", {}, {})'''
                               .format(cart_id, product_id, 1, 0))
                return self.custom_get_method(request, cat_id, 1)
            else:
                if is_checkedout == 0:
                    return self.custom_get_method(request, cat_id, -1)
                else:
                    cursor.execute('''UPDATE cart_products SET quantity = 1, is_checkedout = 0
                                      WHERE cart_id = "{}" AND product_id = "{}"'''
                                   .format(cart_id, product_id))
                    return self.custom_get_method(request, 0)

    def custom_get_method(self, request, cat_id, add_type):
        my_products = Product.objects.raw('''SELECT * FROM product WHERE category_id = "{}" '''.format(cat_id))
        category_name = list(Category.objects.raw('''SELECT * FROM category WHERE cat_id = "{}"'''
                                                  .format(cat_id)))[0].cat_name

        return render(request=request,
                      template_name=self.template_name,
                      context={'my_products': my_products,
                               'category_name': category_name,
                               'add_type': add_type})


class SingleStoreView(View):
    template_name = 'single_store_view.html'

    def get(self, request, store_id):
        with connection.cursor() as cursor:
            store_name = list(Store.objects.raw('''SELECT * FROM store WHERE store_id = "{}"'''
                                                .format(store_id)))[0].store_name

            cursor.execute('''SELECT category_id FROM store_categories WHERE store_id = "{}"'''.format(store_id))
            result = cursor.fetchall()
            categories_id = np.asarray(result).reshape(-1)

            if not len(categories_id):
                return render(request=request,
                              template_name=self.template_name,
                              context={'store_name': store_name})

            my_categories = Category.objects.raw('''SELECT * FROM category WHERE cat_id IN ({})'''
                                                 .format(','.join(str(e) for e in categories_id.tolist())))

            return render(request=request,
                          template_name=self.template_name,
                          context={'my_categories': my_categories,
                                   'store_name': store_name})


class CartView(View):
    template_name = 'cart.html'

    def get(self, request):
        return self.custom_get(request, None)

    def custom_get(self, request, error_mess):
        with connection.cursor() as cursor:
            cart_id = get_cart_id(request.session['user_id'])

            cursor.execute('''SELECT P.product_name, P.product_price, CP.quantity, P.product_id
                              FROM product P, cart_products CP 
                              WHERE cart_id = "{}" AND P.product_id = CP.product_id AND CP.is_checkedout = 0'''
                           .format(cart_id))
            my_cart_results = cursor.fetchall()
            return render(request=request,
                          template_name=self.template_name,
                          context={'my_cart_results': my_cart_results,
                                   'error_mess': error_mess})


class CartEditView(CartView):
    def post(self, request, product_id):

        with connection.cursor() as cursor:
            cursor.execute('''SELECT P.number_in_stock, CP.quantity FROM product P, cart_products CP 
                              WHERE P.product_id = CP.product_id AND P.product_id = "{}" '''
                           .format(product_id))

            (number_in_stock, quantity,) = cursor.fetchone()

            if 'inc_btn' in request.POST:
                if number_in_stock == quantity:
                    return self.custom_get(request, "You can't order more than that")

                else:
                    cursor.execute('''UPDATE cart_products SET quantity={} WHERE product_id = "{}"'''
                                   .format(quantity + 1, product_id))
                    return self.custom_get(request, None)

            elif 'decr_btn' in request.POST:

                if quantity == 1:
                    return self.custom_get(request, "You can't order products less than 1 ")
                else:
                    cursor.execute('''UPDATE cart_products SET quantity={} WHERE product_id = "{}"'''
                                   .format(quantity - 1, product_id))
                    return self.custom_get(request, None)

            elif 'delete_btn' in request.POST:
                cart_id = get_cart_id(request.session['user_id'])
                cursor.execute('''DELETE FROM cart_products WHERE product_id = "{}" AND cart_id = "{}"'''
                               .format(product_id, cart_id))
                return self.custom_get(request, None)


class CheckoutView(CartView):
    def post(self, request):
        with connection.cursor() as cursor:
            transaction_date = datetime.date.today().strftime('%Y-%m-%d')
            buyer_id = request.session['user_id']
            cart_id = get_cart_id(request.session['user_id'])

            cursor.execute('''SELECT CP.product_id, CP.quantity FROM cart_products CP WHERE cart_id = "{}"
                              AND is_checkedout = 0'''.format(cart_id))
            my_cart_results = cursor.fetchall()

            for my_cart_item in my_cart_results:
                product_id = my_cart_item[0]
                quantity = my_cart_item[1]
                cursor.execute('''SELECT S.owner_id FROM product P, store_categories SC, store S 
                                      WHERE P.category_id = SC.category_id AND S.store_id = SC.store_id 
                                      AND product_id = "{}"'''.format(product_id))
                (seller_id,) = cursor.fetchone()

                cursor.execute(
                    '''INSERT INTO transaction(buyer_id, seller_id, product_id, quantity, transaction_date)
                        VALUES ("{}", "{}", "{}", "{}", "{}")'''
                        .format(buyer_id, seller_id, product_id, quantity, transaction_date))

                cursor.execute('''UPDATE cart_products SET is_checkedout = 1
                            WHERE cart_id = "{}" AND product_id = "{}"'''.format(cart_id, product_id))

            return redirect('homepage_view')


class OrderHistory(View):
    template_name = 'order_history.html'

    def get(self, request):
        with connection.cursor() as cursor:
            buyer_id = request.session['user_id']
            cursor.execute('''SELECT P.product_name, T.transaction_date, C.cat_name, S.store_name, T.transaction_date
                              FROM transaction T, product P, store S, category C 
                              WHERE T.buyer_id = "{}" AND P.product_id = T.product_id 
                              AND S.owner_id = T.seller_id AND C.cat_id = P.category_id '''.format(buyer_id))

            orders_result = cursor.fetchall()

            return render(request=request,
                          template_name=self.template_name,
                          context={'orders_result': orders_result})


class OrderReceiptsView(View):
    template_name = 'order_receipts.html'

    def get(self, request):
        with connection.cursor() as cursor:
            seller_id = request.session['user_id']
            cursor.execute('''SELECT P.product_name, T.transaction_date, U.username 
                              FROM transaction T, product P, user U WHERE T.seller_id = "{}" 
                              AND P.product_id = T.product_id AND T.buyer_id = U.user_id'''.format(seller_id))

            orders_result = cursor.fetchall()

            encryption = Encryption()

            orders_result = [(order[0], order[1], encryption.decrypt(order[2][2:-1].encode()))
                            for order in orders_result]

            return render(request=request,
                          template_name=self.template_name,
                          context={'orders_result': orders_result})
