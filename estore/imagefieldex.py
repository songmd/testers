from django import forms
from django.db import models


# from .models import Picture

class ImgWidget(forms.ClearableFileInput):
    template_name = 'imgwidget2.html'

    class Media:
        css = {
            'all': ('css/dropify.css',)
        }
        js = ('js/jquery.min.js', 'js/dropify.js', 'js/docready.js')


class ImgSelectWidget(forms.Select):
    template_name = 'imgselect.html'

    # def get_context(self, name, value, attrs):
    #     context = super().get_context(name, value, attrs)
    #     urlmap = {}
    #     context['widget']['urlmap'] = urlmap;
    #     Picture.objects.get()
    #     print(context)
    #     return context
    class Media:
        js = ('js/jquery.min.js',)


class ImgSelectMultipleWidget(forms.SelectMultiple):
    template_name = 'imgselect2.html'

    # def get_context(self, name, value, attrs):
    #     context = super().get_context(name, value, attrs)
    #     urlmap = {}
    #     context['widget']['urlmap'] = urlmap;
    #     Picture.objects.get()
    #     print(context)
    #     return context
    class Media:
        js = ('js/jquery.min.js',)


class ImageFieldEx(models.ImageField):
    def formfield(self, **kwargs):
        kwargs['widget'] = ImgWidget
        return super(ImageFieldEx, self).formfield(**kwargs)


class OneToOneFieldEx(models.OneToOneField):
    def formfield(self, **kwargs):
        kwargs['widget'] = ImgSelectWidget
        return super(OneToOneFieldEx, self).formfield(**kwargs)


class ManyToManyFieldEx(models.ManyToManyField):
    def formfield(self, **kwargs):
        kwargs['widget'] = ImgSelectMultipleWidget
        return super(ManyToManyFieldEx, self).formfield(**kwargs)
