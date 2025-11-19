from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, MenuItem, GalleryImage, Contact

def home(request):
    categories = Category.objects.all()
    popular_items = MenuItem.objects.filter(is_popular=True, is_available=True)[:6]
    gallery_images = GalleryImage.objects.all()[:6]
    
    context = {
        'categories': categories,
        'popular_items': popular_items,
        'gallery_images': gallery_images,
    }
    return render(request, 'home.html', context)

def menu(request):
    categories = Category.objects.prefetch_related('menuitem_set').all()
    
    context = {
        'categories': categories,
    }
    return render(request, 'menu.html', context)

def gallery(request):
    images = GalleryImage.objects.all()
    
    context = {
        'images': images,
    }
    return render(request, 'gallery.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message
        )
        
        messages.success(request, 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.')
        return redirect('contact')
    
    return render(request, 'contact.html')

def kvkk(request):
    return render(request, 'kvkk.html')

def cookie_policy(request):
    return render(request, 'cookie_policy.html')

def terms_of_use(request):
    return render(request, 'terms_of_use.html')

def about(request):
    return render(request, 'about.html')