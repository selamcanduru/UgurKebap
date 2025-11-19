# website/middleware.py (yeni dosya oluştur)

from django.utils import timezone
from django.db import models
from .models import PageVisit, DailyStats
from datetime import datetime

class VisitorTrackingMiddleware:
    """Her sayfa ziyaretini kaydeder"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Sayfa yüklendiğinde
        response = self.get_response(request)
        
        # Admin panel ve static dosyaları hariç tut
        if not request.path.startswith('/admin/') and not request.path.startswith('/static/'):
            # Session ID al veya oluştur
            if not request.session.session_key:
                request.session.create()
            session_id = request.session.session_key
            
            # Ziyareti kaydet
            PageVisit.objects.create(
                page_url=request.path,
                session_id=session_id,
                visit_date=timezone.now()
            )
            
            # Günlük istatistikleri güncelle
            self.update_daily_stats()
        
        return response
    
    def update_daily_stats(self):
        """Günlük istatistikleri günceller"""
        today = datetime.now().date()
        
        # Bugünkü ziyaretler
        today_visits = PageVisit.objects.filter(
            visit_date__date=today
        )
        
        total_visits = today_visits.count()
        unique_visitors = today_visits.values('session_id').distinct().count()
        
        # Ortalama süre hesapla (eğer varsa)
        avg_time = today_visits.exclude(time_spent=0).aggregate(
            models.Avg('time_spent')
        )['time_spent__avg'] or 0
        
        # Günlük istatistiği oluştur veya güncelle
        DailyStats.objects.update_or_create(
            date=today,
            defaults={
                'total_visits': total_visits,
                'unique_visitors': unique_visitors,
                'avg_time_spent': int(avg_time)
            }
        )