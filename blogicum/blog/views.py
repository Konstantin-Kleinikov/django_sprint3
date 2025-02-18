from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import (
    Category,
    Post,
)
from .constants import NUMBER_OF_ROWS


def get_filtered_posts(post_id: int = None) -> QuerySet[Post]:
    """Возвращает QuerySet отфильтрованных записей блогов.

    Параметры:
            post_id (int): номер записи блога
    """
    if post_id:
        return get_object_or_404(
            Post,
            pk=post_id,
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
    else:
        return (Post.objects.select_related(
            'author',
            'location',
            'category',
        )
            .filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )
        )


def index(request):
    """Обрабатывает запрос к главной странице 'Лента записей'."""
    post_list = get_filtered_posts()[:NUMBER_OF_ROWS]

    return render(
        request,
        'blog/index.html',
        {'post_list': post_list}
    )


def post_detail(request, post_id: int):
    """Обрабатывает запрос к странице записи блога.

    Параметры:
            post_id (int): номер записи блога
    """
    post = get_filtered_posts(post_id)

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Обрабатывает запрос к странице публикаций блогов по категории.

    Параметры:
             category_slug (slug): название категории записей блога
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = (
        get_filtered_posts()
        .filter(category=category)
    )

    return render(request,
                  'blog/category.html',
                  {'category': category, 'post_list': post_list}
                  )
