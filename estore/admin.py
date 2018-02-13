from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import ShopInfo, GoodsCategory, Picture, Goods

from mptt.admin import MPTTModelAdmin
from django.db import models
from django.db.models import Q
from .imagefieldex import ImageFieldEx, ImgWidget

from django import forms


class GoodsCategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')

    # def save_form(self, request, form, change):
    #     form.owner = request.user
    #     super(GoodsCategoryAdmin, self).save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user

        obj.save()

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ('owner', 'name', 'parent')
        return ['name', 'parent']

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('name', 'owner', 'parent')
        return ('name', 'parent')

    def get_queryset(self, request):
        qs = super(GoodsCategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "parent":
            print('formfield_for_foreignkey')
            print(kwargs)
            kwargs["queryset"] = GoodsCategory.objects.filter(owner=request.user)
        # qs = kwargs["queryset"]
        # kwargs["queryset"] = qs.filter(owner=request.user)
        return super(GoodsCategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # inlines = [PictureInline]




class GoodsAdmin(admin.ModelAdmin):
    list_display = ('name', 'no', 'bar_code')
    # inlines = [GoodsPictureInline]
    # exclude = ('pics',)




class PictureAdmin(admin.ModelAdmin):
    pass
    # change_list_template = 'app_index_html'
    # form = PictureForm
    list_display = ('desc', 'display_picture', 'owner', 'display_path',)
    list_display_links = ('desc', 'display_picture', 'owner', 'display_path',)
    # formfield_overrides = {
    #     models.ImageField: {'widget': ImgWidget},
    # }


admin.site.register(ShopInfo, ShopInfoAdmin)

admin.site.register(GoodsCategory, GoodsCategoryAdmin)

admin.site.register(Picture, PictureAdmin)

admin.site.register(Goods)


