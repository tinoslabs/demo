
from django.shortcuts import render, redirect
from .models import Product, Sale
from .forms import ProductForm, SaleForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "There was an error logging in, try again...")
            return redirect('user_login')
    return render(request, 'authenticate/login.html', {'form': True})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('index')


def dashboard(request):
    products = Product.objects.all()
    sales = Sale.objects.all()
    return render(request, 'inventory/dashboard.html', {'products': products, 'sales': sales})


def display_categories(request):
    categories = ProductCategory.objects.all()
    return render(request, 'inventory/display_category.html', {'categories': categories})

def add_category(request):
    form = ProductCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('display_categories')
    return render(request, 'inventory/add_category.html', {'form': form})

def edit_category(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('display_categories')
    else:
        form = ProductCategoryForm(instance=category)
    return render(request, 'inventory/edit_category.html', {'form': form, 'category': category})


def delete_category(request, pk):  
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()
    return redirect('display_categories')
    

def display_products(request):
    products = Product.objects.all()
    return render(request, 'inventory/display_product.html', {'products': products})



def display_sales(request):
    sales = Sale.objects.select_related('product').all().order_by('-sale_date')
    total_profit = sales.aggregate(total=Sum('profit'))['total'] or 0
    return render(request, 'inventory/display_sales.html', {
        'sales': sales,
        'total_profit': total_profit
    })


def display_purchases(request):
    purchases = Purchase.objects.all()
    return render(request, 'inventory/display_purchase.html', {'purchases': purchases})


def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('display_products')  # Make sure this route is defined in urls.py
    return render(request, 'inventory/add_product.html', {'form': form})


def make_sale(request):
    form = SaleForm(request.POST or None)
    products = Product.objects.all()
    if form.is_valid():
        form.save()
        return redirect('display_sales')
    return render(request, 'inventory/add_sale.html', {'form': form, 'products': products})


def add_purchase(request):
    form = PurchaseForm(request.POST or None)
    categories = ProductCategory.objects.all()
    if form.is_valid():
        form.save()
        return redirect('display_purchases')
    return render(request, 'inventory/add_purchase.html', {'form': form, 'categories': categories})


def edit_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        if form.is_valid():
            form.save()
            return redirect('display_purchases')
    else:
        form = PurchaseForm(instance=purchase)
    categories = ProductCategory.objects.all()
    return render(request, 'inventory/edit_purchase.html', {
        'form': form,
        'categories': categories,
        'purchase': purchase
    })
    
    
def delete_purchase(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    purchase.delete()
    return redirect('display_purchases')
    

# from django.db.models import Q

# def search_product_stock(request):
#     query = request.GET.get('q')
#     results = []
#     if query:
#         results = Product.objects.filter(
#             Q(product_code__icontains=query)
#         )
#     return render(request, 'inventory/search_product_stock.html', {
#         'query': query,
#         'results': results
#     })


# from django.http import JsonResponse

# def product_autocomplete(request):
#     term = request.GET.get('term', '')
#     product_codes = Product.objects.filter(product_code__icontains=term).values_list('product_code', flat=True).distinct()[:10]
#     return JsonResponse(list(product_codes), safe=False)

from django.db.models import Q
from django.http import JsonResponse
from .models import Product

def search_product_stock(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(Q(product_code__icontains=query))
    return render(request, 'inventory/search_product_stock.html', {
        'query': query,
        'results': results
    })

def product_autocomplete(request):
    term = request.GET.get('term', '')
    product_codes = Product.objects.filter(product_code__icontains=term).values_list('product_code', flat=True).distinct()[:10]
    return JsonResponse(list(product_codes), safe=False)

def display_balance_stock(request):
    from django.db.models import Sum
    products = Product.objects.all()
    total_quantity = products.aggregate(total=Sum('quantity'))['total'] or 0
    return render(request, 'inventory/display_balance_stock.html', {
        'products': products,
        'total_quantity': total_quantity
    })

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('display_products')
    else:
        form = ProductForm(instance=product)

    # ✅ This is what you're missing:
    purchases = Purchase.objects.all()

    return render(request, 'inventory/edit_product.html', {
        'form': form,
        'purchases': purchases
    })


from django.db.models import Sum

def display_total_profit(request):
    total_profit = Sale.objects.aggregate(total=Sum('profit'))['total'] or 0
    sales = Sale.objects.select_related('product').all().order_by('-sale_date')
    return render(request, 'inventory/display_total_profit.html', {
        'sales': sales,
        'total_profit': total_profit
    })

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)    
    product.delete()
    return redirect('display_products')
    

def index(request):
    return render(request,'index.html')

def brandlist(request):
    return render(request,'inventory/brandlist.html')

def add_pro(request):
    return render(request, 'admin_pages/addproduct.html')


def add_pur(request):
    return render(request, 'admin_pages/addpurchase.html')

def add_cat(request):
    return render(request, 'admin_pages/add_category.html')

def pro_list(request):
    
    return render(request, 'productlist.html')
    