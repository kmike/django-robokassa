#coding: utf-8
try:
    from django.conf.urls.defaults import patterns, url
except ImportError:
    from django.conf.urls import patterns, url
    

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
