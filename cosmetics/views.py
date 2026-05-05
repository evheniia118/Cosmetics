from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.utils.translation import gettext as _
from .models import Product, UserSession
from .forms import ProductForm, RegisterForm


def logout_view(request):
    if request.user.is_authenticated:
        session_id = request.session.get('session_id')

        if session_id:
            try:
                session = UserSession.objects.get(id=session_id)

                login_time = session.login_time
                logout_time = timezone.now()

                duration = int((logout_time - login_time).total_seconds())

                session.logout_time = logout_time
                session.duration = duration
                session.save()

            except:
                pass

    logout(request)
    return redirect('login')


def product_list(request):
    query = request.GET.get('q')

    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    result_count = products.count()

    context = {
        'products': products,
        'result_count': result_count,
        'query': query
    }

    return render(request, 'product_list.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def product_create(request):

    if not request.user.groups.filter(name='manager').exists():
        return render(request, 'forbidden.html')

    form = ProductForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Product added successfully"))
        return redirect('cosmetics:product_list')

    return render(request, 'product_form.html', {'form': form})


@login_required
def product_update(request, id):

    if not request.user.groups.filter(name='manager').exists():
        return render(request, 'forbidden.html')

    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, _("Product updated"))
        return redirect('product_detail', id=id)

    return render(request, 'product_form.html', {'form': form})


@login_required
def product_delete(request, id):

    if not request.user.groups.filter(name='manager').exists():
        return render(request, 'forbidden.html')

    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, _("Product deleted"))
        return redirect('cosmetics:product_list')

    return render(request, 'product_confirm_delete.html', {'product': product})


@login_required
def product_edit(request, id):

    if not request.user.groups.filter(name='manager').exists():
        return render(request, 'forbidden.html')

    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=product)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('cosmetics:product_list')

    return render(request, 'product_form.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Registration successful"))
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})