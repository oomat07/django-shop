from django.urls import path
from . import views
app_name = 'shop'

urlpattern = [
    path('', views.product_list, name='product_list'),
    path('<slug:category>/', views.product_list, name='product_list_by_category')
]