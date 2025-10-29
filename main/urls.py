from django.urls import path
from main.views import (
    show_main,
    show_product,
    register,
    login_user,
    logout_user,
    get_product_by_id_json,
    edit_product,
    add_product_ajax,
    edit_product_ajax,
    delete_product_ajax,
    login_ajax,
    register_ajax,
    get_products_json,
    
 








    
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("product/<int:id>/", show_product, name="show_product"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("get-products/", get_products_json, name="get_products_json"),
    path("create-product-ajax/", add_product_ajax, name="add_product_ajax"),
    path("edit-product-ajax-/<int:id>/", edit_product_ajax, name= "edit_product_ajax"),


    path('product-edit/<int:id>/', edit_product, name='edit_product'),
    path("get-product/<int:pk>/", get_product_by_id_json, name="get_product_by_id_json"),
    path('products-delete-ajax/<int:id>/', delete_product_ajax, name='delete_product_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),


    

]
