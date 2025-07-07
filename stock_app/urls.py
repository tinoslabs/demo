from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard', views.dashboard, name='dashboard'),
    
    path('add-category/', views.add_category, name='add_category'),
    path('display-categories/', views.display_categories, name='display_categories'),
    path('edit-category/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),
    
    path('user_login', views.user_login, name='user_login'),
    path('logout_user', views.logout_user, name='logout_user'),
     
    path('add-product/', views.add_product, name='add_product'),
    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('display-products/', views.display_products, name='display_products'),
    path('add-sale/', views.make_sale, name='add_sale'),
    path('display-sales/', views.display_sales, name='display_sales'),
    
    path('search-stock/', views.search_product_stock, name='search_stock'),
    path('autocomplete/', views.product_autocomplete, name='product_autocomplete'),
    path('', views.index, name='index'),
   
    path('add_pro',views.add_pro, name='add_pro'),
    path('add-purchase/', views.add_purchase, name='add_purchase'),
    path('edit-purchase/<int:pk>/', views.edit_purchase, name='edit_purchase'),
    path('delete-purchase/<int:pk>/', views.delete_purchase, name='delete_purchase'),
    
    path('display-purchases/', views.display_purchases, name='display_purchases'),
    path('add_pur', views.add_pur, name='add_pur'),
    path('add_cat', views.add_cat, name='add_cat'),
      
    path('pro_list', views.pro_list, name='pro_list'),   
    path('brandlist/', views.brandlist, name='brandlist'),
    
    path('balance-stock/', views.display_balance_stock, name='display_balance_stock'),
    
    path('display-total-profit/', views.display_total_profit, name='display_total_profit'),
    
]