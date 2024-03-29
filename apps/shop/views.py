from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, OrderItem
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProducrtForm, OrderCreateForm
from django.contrib.auth.decorators import login_required


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, category__slug=slug, in_stock=True)
    return render(request, 'shop/product/detail.html', {'product':product})

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProducrtForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart' : cart})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.save()    
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'shop/order/created.html', {'order' : order})
    else:
        form = OrderCreateForm()
    return render(request, 'shop/order/create.html', {'cart' : cart, 'form' : form})
                                