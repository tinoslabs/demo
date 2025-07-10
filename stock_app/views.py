
from django.shortcuts import render, redirect
from .models import Product, Sale, ExtraSale
from .forms import ProductForm, SaleForm, ExtraSaleForm
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



def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('user_login')


def dashboard(request):
    products = Product.objects.all()
    sales = Sale.objects.all()
    return render(request, 'inventory/dashboard.html', {'products': products, 'sales': sales})


    


def display_products(request):
    products = Product.objects.all()

    # Total expense: sum of product_price * quantity
    total_expense = products.aggregate(
        total=Sum(F('product_price') * F('quantity'))
    )['total'] or 0

    return render(request, 'inventory/display_product.html', {
        'products': products,
        'total_expense': total_expense,
    })



def display_sales(request):
    sales = Sale.objects.select_related('product').all()
    total_profit = sales.aggregate(total=Sum('profit'))['total'] or 0
    total_loss = sales.aggregate(total=Sum('loss'))['total'] or 0
    return render(request, 'inventory/display_sales.html', {
        'sales': sales,
        'total_profit': total_profit,
        'total_loss': total_loss,
    })


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


def edit_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    products = Product.objects.all()

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('display_sales')
    else:
        form = SaleForm(instance=sale)

    return render(request, 'inventory/edit_sale.html', {'form': form, 'products': products, 'sale': sale})


def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    sale.delete()
    return redirect('display_sales')

    
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
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('display_products')  # Redirect to your product list page

    return render(request, 'inventory/edit_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)    
    product.delete()
    return redirect('display_products')

from django.db.models import F, Sum

def display_total_profit(request):
    total_profit = Sale.objects.aggregate(total=Sum('profit'))['total'] or 0
    sales = Sale.objects.select_related('product').all().order_by('-sale_date')
    return render(request, 'inventory/display_total_profit.html', {
        'sales': sales,
        'total_profit': total_profit
    })




def add_extra_sale(request):
    form = ExtraSaleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('display_extra_profit')
    return render(request, 'inventory/add_extra_sale.html', {'form': form})

def edit_extra_sale(request, pk):
    sale = get_object_or_404(ExtraSale, pk=pk)
    if request.method == 'POST':
        form = ExtraSaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('display_extra_profit')
    else:
        form = ExtraSaleForm(instance=sale)
    return render(request, 'inventory/edit_extra_sale.html', {'form': form, 'sale': sale})


def delete_extra_sale(request, pk):
    sale = get_object_or_404(ExtraSale, pk=pk)
    sale.delete()
    return redirect('display_extra_profit')

from django.db.models import F, Sum, ExpressionWrapper, DecimalField

def display_extra_profit(request):
    # Use a different name for annotation to avoid conflict with model field
    total_profit = ExtraSale.objects.annotate(
        computed_profit=ExpressionWrapper(
            (F('selling_price') - F('price')) * F('quantity_sold'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    ).aggregate(total=Sum('computed_profit'))['total'] or 0

    extra_sales = ExtraSale.objects.all()
    return render(request, 'inventory/display_extra_profit.html', {
        'extra_sales': extra_sales,
        'total_profit': total_profit
    })

    

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
    