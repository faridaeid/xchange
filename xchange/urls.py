"""xchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from profiles.views import EditProfileView, LoginView, SignupView, StartPageView
from market.views import HomePageView, LogoutView, \
    CategoryAddView, CategoryDeleteView, \
    CategoryEditView, CategoryUpdateView, \
    CategoryProductsView, ProductAddView, \
    ProductDeleteView, ProductEditView, \
    SearchView, SingleCategoryView, SingleStoreView, \
    CartView, CartEditView, CheckoutView, OrderHistory, \
    OrderReceiptsView
from django.urls import path

urlpatterns = [
    path('', StartPageView.as_view(), name='start_view'),
    path('login/', LoginView.as_view(), name='login_view'),
    path('signup/', SignupView.as_view(), name='signup_view'),
    path('homepage/', HomePageView.as_view(), name='homepage_view'),
    path('homepage/logout', LogoutView.as_view(), name='logout_view'),
    path('homepage/edit', EditProfileView.as_view(), name='edit_profile_view'),
    path('homepage/order/history', OrderHistory.as_view(), name='order_history_view'),
    path('homepage/order/receipts', OrderReceiptsView.as_view(), name='order_receipts_view'),
    path('homepage/search', SearchView.as_view(), name='search_view'),
    path('homepage/cart', CartView.as_view(), name='cart_view'),
    path('homepage/cart/edit/<int:product_id>', CartEditView.as_view(), name='cart_edit_view'),
    path('homepage/cart/checkout', CheckoutView.as_view(), name='checkout_view'),
    path('homepage/store/<int:store_id>', SingleStoreView.as_view(), name='single_store_view'),
    path('homepage/category/<int:cat_id>', SingleCategoryView.as_view(), name='single_category_view'),
    path('homepage/category/add', CategoryAddView.as_view(), name='category_add_view'),
    path('homepage/category/delete/<int:cat_id>', CategoryDeleteView.as_view(), name='delete_category_view'),
    path('homepage/category/edit/<int:cat_id>', CategoryEditView.as_view(), name='category_edit_view'),
    path('homepage/category/update/<int:cat_id>', CategoryUpdateView.as_view(), name='category_update_view'),
    path('homepage/category/<int:cat_id>/products/', CategoryProductsView.as_view(),
         name='category_products_view'),
    path('homepage/category/<int:cat_id>/products/add', ProductAddView.as_view(), name='product_add_view'),
    path('homepage/category/<int:cat_id>/products/delete/<int:product_id>', ProductDeleteView.as_view(),
         name='product_delete_view'),
    path('homepage/category/<int:cat_id>/products/edit/<int:product_id>', ProductEditView.as_view(),
         name='product_edit_view'),
    path('admin/', admin.site.urls),
]
