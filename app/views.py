from django.shortcuts import render,redirect,reverse

# Create your views here.
from app.forms import *
from app.models import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

def create_dish(request):
    if request.method=='POST':
        form=DishForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Inserted Dish')
            # return redirect('menu_view')
    else:
        form=DishForm()
    return render(request,'create_dish.html',{'form':form})
        
def create_review(request):
    form=ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Thank you for Visiting Mine Restuarant')
        return HttpResponse('Invalid review')
    return render(request,'create_review.html',{'form':form})



def menu_view(request):
    breakfast_dishes=Dish.objects.filter(category='BREAKFAST',is_available=True)
    veg_dishes=Dish.objects.filter(category='VEG', is_available=True)
    nonveg_dishes=Dish.objects.filter(category='NON_VEG',is_available=True)
    starters_dishes=Dish.objects.filter(category='STARTERS',is_available=True)
    icecream_dishes=Dish.objects.filter(category='ICE_CREAM',is_available=True)
    dishes = Dish.objects.filter(is_available=True)
    selected_ids = request.session.get('selected_items', [])
    selected_items = Dish.objects.filter(id__in=selected_ids)



    d={'breakfast_dishes':breakfast_dishes,'veg_dishes':veg_dishes,'nonveg_dishes':nonveg_dishes,
        'starters_dishes':starters_dishes,'icecream_dishes':icecream_dishes,'dishes':dishes,'selected_items': selected_items
}
    return render(request,'menu_view.html',d)
    #return HttpResponse('Welcome')

def menu_category(request,category):
    dishes=Dish.objects.filter(category=category.upper(), is_available=True)
    d={'dishes':dishes, 'category':category}
    return render(request,'menu_category.html',d)
   

def update_selection(request):
    if request.method == 'POST':
        dish_id = int(request.POST.get('dish_id'))
        action = request.POST.get('action')
        selected = request.session.get('selected_items', [])

        if action == 'add' and dish_id not in selected:
            selected.append(dish_id)
        elif action == 'remove' and dish_id in selected:
            selected.remove(dish_id)

        request.session['selected_items'] = selected
    return redirect('menu_view')   # always go back to menu




