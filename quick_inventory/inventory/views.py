from datetime import date
from django.shortcuts import render
from .models import DailySale, Product, Transaction

from django.shortcuts import render
from .models import ClosedDay, Product, Transaction

def dashboard(request):
    products = Product.objects.all()
    transactions = Transaction.objects.all()
    closed_days = ClosedDay.objects.all()  # Получаем все закрытые дни
    return render(request, 'inventory/dashboard.html', {'products': products, 'transactions': transactions, 'closed_days': closed_days})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import DailySaleForm, ProductForm

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


from django.shortcuts import render, redirect
from .models import Product, DailySale
from .forms import DailySaleForm
from django.utils.timezone import now

def daily_sales(request):
    today = now().date()  # Текущая дата

    # Получаем все продажи за текущий день
    sales = DailySale.objects.filter(sale_date=today)

    # Обработка формы при добавлении продажи
    if request.method == 'POST':
        form = DailySaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.sale_date = today
            sale.total_price = sale.quantity * sale.product.sale_price  # Считаем общую сумму продажи
            sale.save()

            # Обновляем количество товара в модели Product
            product = sale.product
            if product.quantity >= sale.quantity:
                product.quantity -= sale.quantity  # Уменьшаем количество товара
                product.save()  # Сохраняем изменения в базе данных
            else:
                form.add_error(None, "Недостаточно товара на складе")
                return render(request, 'inventory/daily_sales.html', {'form': form, 'sales': sales})

            return redirect('daily_sales')  # Перезагружаем страницу, чтобы увидеть обновления
    else:
        form = DailySaleForm()

    # Считаем итоговые доходы и прибыль
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
        'form': form,
        'today': today,  # Добавляем текущую дату в контекст
    })





from django.shortcuts import render
from .models import DailySale
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now

def close_day(request):
    today = now().date()  # Текущая дата

    # Получаем все продажи за сегодняшний день
    sales = DailySale.objects.filter(sale_date=today)

    # Считаем общий доход за день
    total_income = sales.aggregate(total=Sum(F('quantity') * F('product__sale_price')))['total'] or 0

    total_profit = sales.aggregate(
        total_profit=Sum(
            ExpressionWrapper(
                F('quantity') * (F('product__sale_price') - F('product__purchase_price')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )['total_profit'] or 0

    # Подготавливаем итоговый список проданных товаров
    sold_products = sales.values('product__name').annotate(total_quantity=Sum('quantity'))

    return render(request, 'inventory/close_day.html', {
        'sales': sales,
        'total_income': total_income,
        'total_profit': total_profit,
        'sold_products': sold_products,
        'today': today,  # Добавляем текущую дату в контекст
    })


from django.shortcuts import redirect
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.utils.timezone import now
from .models import DailySale, ClosedDay

def close_day(request):
    today = now().date()  # Текущая дата

    # Получаем все продажи за сегодняшний день
    sales = DailySale.objects.filter(sale_date=today)

    # Если продажи отсутствуют, выводим сообщение
    if not sales:
        print(f'Нет продаж для дня {today}')  # Выводим сообщение для отладки

    # Считаем общий доход и прибыль за день
    total_income = sales.aggregate(total=Sum(F('quantity') * F('product__sale_price')))['total'] or 0
    total_profit = sales.aggregate(
        total_profit=Sum(
            ExpressionWrapper(
                F('quantity') * (F('product__sale_price') - F('product__purchase_price')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )['total_profit'] or 0

    # Создаем объект ClosedDay
    closed_day = ClosedDay.objects.create(
        date=today,
        total_income=total_income,
        total_profit=total_profit
    )

    # Обновляем продажи, добавляя связь с ClosedDay
    sales.update(closed_day=closed_day)

    # Перенаправляем на страницу, где отображаются закрытые дни
    return redirect('dashboard')






def closed_day_detail(request, closed_day_id):
    closed_day = get_object_or_404(ClosedDay, id=closed_day_id)

    # Получаем все продажи, связанные с этим закрытым днем
    sales = closed_day.dailysale_set.all()  # Используем обратную связь для получения связанных продаж

    # Считаем общую сумму дохода и прибыли, если продажи есть
    total_income = sales.aggregate(total=Sum(F('quantity') * F('product__sale_price')))['total'] or 0
    total_profit = sales.aggregate(
        total_profit=Sum(
            ExpressionWrapper(
                F('quantity') * (F('product__sale_price') - F('product__purchase_price')),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )['total_profit'] or 0

    return render(request, 'inventory/closed_day_detail.html', {
        'closed_day': closed_day,
        'sales': sales,
        'total_income': total_income,
        'total_profit': total_profit,
    })














