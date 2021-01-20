from django.contrib import admin
from django.urls import path, include
from django.conf import settings
# from django.shortcuts import redirect
from django.conf.urls.static import static
import category.views
from django.http import HttpResponse

from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from board.models import Board



info_dict = {
    'queryset': Board.objects.filter(),
    'date_field': 'created_at',
}

urlpatterns = [
    path('category/', include('category.urls', namespace='category')),
    path('board/', include('board.urls', namespace='board')),
    path('account/', include('account.urls', namespace='account')),
    path('tutorial/', include('tutorial.urls', namespace='tutorial')),
    path('', category.views.show_category, name='root'),
    path('sitemap.xml', sitemap, {'sitemaps': {'board': GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', lambda x: HttpResponse("User-Agent: *\nDisallow: /admin/\nDisallow: /account/\nAllow: /", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)