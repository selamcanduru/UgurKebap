from django.contrib import admin
from .models import Category, MenuItem, GalleryImage, Contact
from django.contrib import admin
from django.db.models import Count, Avg
from django.utils.html import format_html
from datetime import datetime, timedelta
from .models import PageVisit, DailyStats

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'icon']
    list_editable = ['order']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_popular', 'is_available']
    list_filter = ['category', 'is_popular', 'is_available']
    list_editable = ['price', 'is_popular', 'is_available']
    search_fields = ['name', 'description']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at']
    list_filter = ['uploaded_at']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['name', 'phone', 'email', 'message', 'created_at']


    # Kullanıcı ziyaretleri denetimi

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ['page_url', 'visit_date', 'time_spent_display']
    list_filter = ['visit_date', 'page_url']
    search_fields = ['page_url', 'session_id']
    readonly_fields = ['page_url', 'visit_date', 'session_id', 'time_spent']
    date_hierarchy = 'visit_date'
    
    def time_spent_display(self, obj):
        minutes = obj.time_spent // 60
        seconds = obj.time_spent % 60
        return f"{minutes}dk {seconds}sn"
    time_spent_display.short_description = "Geçirilen Süre"
    
    def has_add_permission(self, request):
        return False  # Manuel eklemeyi engelle


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_visits', 'unique_visitors', 'avg_time_display']
    readonly_fields = ['date', 'total_visits', 'unique_visitors', 'avg_time_spent']
    date_hierarchy = 'date'
    
    def avg_time_display(self, obj):
        minutes = obj.avg_time_spent // 60
        seconds = obj.avg_time_spent % 60
        return f"{minutes}dk {seconds}sn"
    avg_time_display.short_description = "Ortalama Süre"
    
    def has_add_permission(self, request):
        return False
    
    def changelist_view(self, request, extra_context=None):
        # Özel istatistikler ekle
        extra_context = extra_context or {}
        
        # Bugün
        today = datetime.now().date()
        today_stats = DailyStats.objects.filter(date=today).first()
        
        # Bu hafta
        week_ago = today - timedelta(days=7)
        week_stats = DailyStats.objects.filter(date__gte=week_ago)
        
        # Bu ay
        month_ago = today - timedelta(days=30)
        month_stats = DailyStats.objects.filter(date__gte=month_ago)
        
        # Toplam
        total_visits = PageVisit.objects.count()
        total_unique = PageVisit.objects.values('session_id').distinct().count()
        
        # En popüler sayfalar
        popular_pages = PageVisit.objects.values('page_url').annotate(
            count=Count('id')
        ).order_by('-count')[:5]
        
        extra_context['today_visits'] = today_stats.total_visits if today_stats else 0
        extra_context['today_unique'] = today_stats.unique_visitors if today_stats else 0
        extra_context['week_visits'] = week_stats.aggregate(Count('total_visits'))['total_visits__count'] or 0
        extra_context['month_visits'] = month_stats.aggregate(Count('total_visits'))['total_visits__count'] or 0
        extra_context['total_visits'] = total_visits
        extra_context['total_unique'] = total_unique
        extra_context['popular_pages'] = popular_pages
        
        return super().changelist_view(request, extra_context=extra_context)