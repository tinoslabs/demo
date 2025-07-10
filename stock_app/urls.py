from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard', views.dashboard, name='dashboard'),
    

    
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
    
    path('edit_sale/<int:pk>/', views.edit_sale, name='edit_sale'),
    path('delete_sale/<int:pk>/', views.delete_sale, name='delete_sale'),

    path('add_expense/', views.add_expense, name='add_expense'),
    path('display_expense/', views.display_expense, name='display_expense'),
    path('edit_expense/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    
    path('edit_extra_sale/<int:pk>/', views.edit_extra_sale, name='edit_extra_sale'),
    path('delete_extra_sale/<int:pk>/', views.delete_extra_sale, name='delete_extra_sale'),
    
    path('add_extra_sale/', views.add_extra_sale, name='add_extra_sale'),
    path('display_extra_profit', views.display_extra_profit, name='display_extra_profit'),

    path('add_pur', views.add_pur, name='add_pur'),
    path('add_cat', views.add_cat, name='add_cat'),
      
    path('pro_list', views.pro_list, name='pro_list'),   
    path('brandlist/', views.brandlist, name='brandlist'),
    
    path('balance-stock/', views.display_balance_stock, name='display_balance_stock'),
    
    path('display-total-profit/', views.display_total_profit, name='display_total_profit'),
    
]