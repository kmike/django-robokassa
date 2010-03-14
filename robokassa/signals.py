#coding: utf-8
from django.dispatch import Signal

result_received = Signal(providing_args=["InvId", "OrdSum"])
success_page_visited = Signal(providing_args=["InvId", "OrdSum"])
fail_page_visited = Signal(providing_args=["InvId", "OrdSum"])

