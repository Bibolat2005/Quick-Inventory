from django.shortcuts import render
from .models import Product, Transaction

def dashboard(request):
    products = Product.objects.all()
    transactions = Transaction.objects.all()
    return render(request, 'inventory/dashboard.html', {'products': products, 'transactions': transactions})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

from .forms import ProductForm

from django.shortcuts import render, redirect
from .models import Category, Product

def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        category_id = request.POST['category']
        quantity = int(request.POST['quantity'])
        purchase_price = float(request.POST['purchase_price'])
        sale_price = float(request.POST['sale_price'])

        category = Category.objects.get(id=category_id)
        Product.objects.create(
            name=name,
            category=category,
            quantity=quantity,
            purchase_price=purchase_price,
            sale_price=sale_price
        )
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'inventory/add_product.html', {'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST['name']
        category_id = request.POST['category']
        product.category = Category.objects.get(id=category_id)
        product.quantity = int(request.POST['quantity'])
        product.purchase_price = float(request.POST['purchase_price'])
        product.sale_price = float(request.POST['sale_price'])
        product.save()
        return redirect('dashboard')

    categories = Category.objects.all()
    return render(request, 'inventory/edit_product.html', {'product': product, 'categories': categories})


from django.shortcuts import render
from .models import Transaction

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'inventory/transaction_list.html', {'transactions': transactions})



