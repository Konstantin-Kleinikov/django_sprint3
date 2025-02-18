from django.db import models


class CreatedPublishedModel(models.Model):
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class PostModel(CreatedPublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=256
    )

    class Meta:
        abstract = True
        default_related_name = '%(class)s_posts'

    def __str__(self):
        return self.title[:30]
