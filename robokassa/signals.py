#coding: utf-8
from django.dispatch import Signal

result_received = Signal()
success_page_visited = Signal(providing_args=["InvId", "OutSum"])
fail_page_visited = Signal(providing_args=["InvId", "OutSum"])

