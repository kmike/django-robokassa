#coding: utf-8
import django.conf.urls as urls
if getattr(urls, 'defaults', None):
    from django.conf.urls.defaults import *
else:
    from django.conf.urls import patterns, include, url

urlpatterns = patterns('robokassa.views',
    url(
          r'^result/$',
          'receive_result',
          name='robokassa_result'
    ),
    url(
          r'^success/$',
          'success',
          name='robokassa_success'
    ),
    url(
          r'^fail/$',
          'fail',
          name='robokassa_fail'
    ),
)
