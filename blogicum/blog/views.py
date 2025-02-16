from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone

from .models import (
    Category,
    Post,
)


def index(request):
    """Обрабатывает запрос к главной странице 'Лента записей'."""
    try:
        post_list = (Post.objects.select_related(
            'author',
            'location',
            'category',
        )
            .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )
            .order_by('-pub_date')[:5]
        )
    except Post.DoesNotExist:
        raise Http404(
            'Не найдено ни одной опубликованной записи блогов.'
        )

    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id: int):
    """Обрабатывает запрос к странице записи блога.

    Параметры:
            post_id (int): номер записи блога
    """
    try:
        post = (Post.objects.select_related(
            'author',
            'location',
            'category',
        )
            .get(
            Q(pk=post_id)
            & Q(pub_date__lte=timezone.now())
            & Q(is_published=True)
            & Q(category__is_published=True)
        )
        )
    except Post.DoesNotExist:
        raise Http404(
            f'Не найдена страница с номером записи блога: {post_id}.'
        )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Обрабатывает запрос к странице публикаций блогов по категории.

    Параметры:
             category_slug (slug): название категории записей блога
    """
    try:
        category = Category.objects.get(
            slug=category_slug,
            is_published=True
        )
    except Category.DoesNotExist:
        raise Http404(f'Не найдена категория: {category_slug}'
                      )

    post_list = (Post.objects.filter(
        category=category,
        is_published=True
    )
        .select_related(
        'author',
        'location',
        'category',
    )
        .filter(
        is_published=True,
        pub_date__lte=timezone.now()
    )
        .order_by('-pub_date')
    )
    return render(request,
                  'blog/category.html',
                  {'category': category, 'post_list': post_list}
                  )
