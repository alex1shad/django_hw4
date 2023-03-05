from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        for form in self.forms:
            is_main = form.cleaned_data.get('is_main')
            if is_main:
                is_main_count += 1
            if is_main_count > 1:
                raise ValidationError('Основной раздел должен быть один и только один!')
        if is_main_count == 0:
            raise ValidationError('Добавьте основной раздел!')
        return super().clean()


class TagInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset


class ArticleInline(admin.TabularInline):
    model = Scope
    extra = 1
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [TagInline, ]


@admin.register(Tag)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ArticleInline, ]
