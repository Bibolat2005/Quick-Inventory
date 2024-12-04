from datetime import date
from django.shortcuts import render
from .models import DailySale, Product, Transaction

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

from django.shortcuts import render

def profile(request):
    return render(request, 'inventory/profile.html')


from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now

def daily_sales(request):
    today = date.today()

    # Получаем продажи за текущий день
    sales = DailySale.objects.filter(sale_date=today)

    # Считаем общий доход и чистую прибыль
    total_income = sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_profit = sales.aggregate(
        total_profit=Sum(
            ExpressionWrapper(
                F('quantity') * (F('product__sale_price') - F('product__purchase_price')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )['total_profit'] or 0

    return render(request, 'inventory/daily_sales.html', {
        'sales': sales,
        'total_income': total_income,
        'total_profit': total_profit,
    })



def close_day(request):
    sales = DailySale.objects.filter(sale_date=now().date())
    total_income = sales.aggregate(total=Sum(F('quantity') * F('product__sale_price')))['total'] or 0
    return render(request, 'inventory/close_day.html', {
        'sales': sales,
        'total_income': total_income,
    })






