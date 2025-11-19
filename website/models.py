from django.db import models
from django.utils import timezone
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.price}₺"

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%d.%m.%Y')}"
    

    # Kullanıcı ziyaretlerini belirleme 

class PageVisit(models.Model):
    """Sayfa ziyaretlerini takip eder"""
    page_url = models.CharField(max_length=255, verbose_name="Sayfa URL")
    visit_date = models.DateTimeField(default=timezone.now, verbose_name="Ziyaret Tarihi")
    session_id = models.CharField(max_length=100, verbose_name="Oturum ID")
    time_spent = models.IntegerField(default=0, verbose_name="Geçirilen Süre (saniye)")
    
    class Meta:
        verbose_name = "Sayfa Ziyareti"
        verbose_name_plural = "Sayfa Ziyaretleri"
        ordering = ['-visit_date']
    
    def __str__(self):
        return f"{self.page_url} - {self.visit_date.strftime('%Y-%m-%d %H:%M')}"


class DailyStats(models.Model):
    """Günlük istatistikler"""
    date = models.DateField(unique=True, verbose_name="Tarih")
    total_visits = models.IntegerField(default=0, verbose_name="Toplam Ziyaret")
    unique_visitors = models.IntegerField(default=0, verbose_name="Tekil Ziyaretçi")
    avg_time_spent = models.IntegerField(default=0, verbose_name="Ortalama Süre (saniye)")
    
    class Meta:
        verbose_name = "Günlük İstatistik"
        verbose_name_plural = "Günlük İstatistikler"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.date} - {self.total_visits} ziyaret"