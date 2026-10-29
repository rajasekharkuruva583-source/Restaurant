from decimal import Decimal

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from app.forms import CheckoutForm, DishForm, ReviewForm
from app.models import Dish, Order, OrderItem


def create_dish(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Inserted Dish')
    else:
        form = DishForm()
    return render(request, 'create_dish.html', {'form': form})


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for Visiting Mine Restuarant')
        return render(request, 'create_review.html', {'form': form})
    return render(request, 'create_review.html', {'form': ReviewForm()})


def menu_view(request):
    context = {
        'breakfast_dishes': Dish.objects.filter(category='BREAKFAST', is_available=True),
        'veg_dishes': Dish.objects.filter(category='VEG', is_available=True),
        'nonveg_dishes': Dish.objects.filter(category='NON_VEG', is_available=True),
        'starters_dishes': Dish.objects.filter(category='STARTERS', is_available=True),
        'icecream_dishes': Dish.objects.filter(category='ICE_CREAM', is_available=True),
        'dishes': Dish.objects.filter(is_available=True),
    }
    return render(request, 'menu_view.html', context)


def menu_category(request, category):
    dishes = Dish.objects.filter(category=category.upper(), is_available=True)
    return render(request, 'menu_category.html', {
        'dishes': dishes,
        'category': category,
    })


def _get_session_quantities(request):
    quantities = request.session.get('selected_items', {})

    # Convert the old list format to the quantity dictionary format.
    if isinstance(quantities, list):
        converted = {}
        for dish_id in quantities:
            try:
                key = str(int(dish_id))
                converted[key] = converted.get(key, 0) + 1
            except (TypeError, ValueError):
                continue
        quantities = converted

    if not isinstance(quantities, dict):
        quantities = {}

    cleaned = {}
    for dish_id, quantity in quantities.items():
        try:
            key = str(int(dish_id))
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue
        if quantity > 0:
            cleaned[key] = quantity

    return cleaned


def update_selection(request):
    quantities = _get_session_quantities(request)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'clear':
            request.session['selected_items'] = {}
            return redirect('update_selection')

        try:
            dish_id = int(request.POST.get('dish_id'))
        except (TypeError, ValueError):
            return redirect('update_selection')

        dish = Dish.objects.filter(id=dish_id, is_available=True).first()
        if dish is None:
            return redirect('update_selection')

        key = str(dish_id)
        current_quantity = quantities.get(key, 0)

        if action == 'add':
            quantities[key] = current_quantity + 1
        elif action == 'remove':
            if current_quantity > 1:
                quantities[key] = current_quantity - 1
            else:
                quantities.pop(key, None)
        else:
            return redirect('update_selection')

        request.session['selected_items'] = quantities
        return redirect('update_selection')

    dishes = Dish.objects.filter(
        id__in=[int(dish_id) for dish_id in quantities],
        is_available=True
    ).order_by('id')

    selected_items = []
    subtotal = Decimal('0.00')
    total_plates = 0

    for dish in dishes:
        quantity = quantities.get(str(dish.id), 0)
        if quantity <= 0:
            continue
        dish.quantity = quantity
        dish.line_total = dish.price * quantity
        selected_items.append(dish)
        total_plates += quantity
        subtotal += dish.line_total

    return render(request, 'update_selection.html', {
        'selected_items': selected_items,
        'selected_count': total_plates,
        'subtotal': subtotal,
    })


def checkout(request):
    quantities = _get_session_quantities(request)
    if not quantities:
        return redirect('update_selection')

    dishes = Dish.objects.filter(
        id__in=[int(dish_id) for dish_id in quantities],
        is_available=True
    ).order_by('id')

    # Ignore stale IDs and calculate prices from the database, not the browser.
    order_lines = []
    subtotal = Decimal('0.00')
    total_plates = 0

    for dish in dishes:
        quantity = quantities.get(str(dish.id), 0)
        if quantity <= 0:
            continue
        line_total = dish.price * quantity
        order_lines.append({
            'dish': dish,
            'quantity': quantity,
            'unit_price': dish.price,
            'line_total': line_total,
        })
        subtotal += line_total
        total_plates += quantity

    if not order_lines:
        request.session['selected_items'] = {}
        return redirect('update_selection')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    customer_name=form.cleaned_data['customer_name'].strip(),
                    phone=form.cleaned_data['phone'],
                    order_type=form.cleaned_data['order_type'],
                    delivery_address=form.cleaned_data.get('delivery_address', '').strip()
                        if form.cleaned_data['order_type'] == 'DELIVERY' else '',
                    subtotal=subtotal,
                    total=subtotal,
                )

                for line in order_lines:
                    OrderItem.objects.create(
                        order=order,
                        dish=line['dish'],
                        dish_name=line['dish'].name,
                        quantity=line['quantity'],
                        unit_price=line['unit_price'],
                        line_total=line['line_total'],
                    )

            # Clear the cart only after the database transaction succeeds.
            request.session['selected_items'] = {}
            return redirect(
                'order_confirmation',
                order_number=str(order.order_number)
            )
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'form': form,
        'order_lines': order_lines,
        'selected_count': total_plates,
        'subtotal': subtotal,
    })


@require_GET
def order_confirmation(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'order_confirmation.html', {'order': order})
