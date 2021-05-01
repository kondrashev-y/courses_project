from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import render

from products.models import Comments, Product

User = get_user_model()
from django.contrib.contenttypes.models import ContentType


def get_children(qs_child):
    res = []
    for comment in qs_child:
        c = {
            'id': comment.id,
            'text': comment.text,
            'timestamp': comment.timestamp.strftime('%Y-%m_%d %H:%m'),
            'author': comment.user.first_name,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent
        }
        if comment.children.exists():
            c['children'] = get_children(comment.children.all())
        res.append(c)
    return res


def create_comments_tree(qs):
    res = []
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.text,
            'timestamp': comment.timestamp.strftime('%Y-%m_%d %H:%m'),
            'author': comment.user.first_name,
            'is_child': comment.is_child,
            'parent_id': comment.get_parent
        }
        if comment.children:
            c['children'] = get_children(comment.children.all())
        if not comment.is_child:
            res.append(c)
    return res


