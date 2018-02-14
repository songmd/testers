from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

from mptt.admin import MPTTModelAdmin
from django.db import models
from django.db.models import Q
from .imagefieldex import ImageFieldEx, ImgWidget

from django import forms
from django.shortcuts import render
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
csrf_protect_m = method_decorator(csrf_protect)

class ProductCategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent')

    # def save_form(self, request, form, change):
    #     form.owner = request.user
    #     super(GoodsCategoryAdmin, self).save_form(request, form, change)

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #
    #     obj.save()

    # def get_fields(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return ('owner', 'name', 'parent')
    #     return ['name', 'parent']
    #
    # def get_list_display(self, request):
    #     if request.user.is_superuser:
    #         return ('name', 'owner', 'parent')
    #     return ('name', 'parent')
    #
    # def get_queryset(self, request):
    #     qs = super(GoodsCategoryAdmin, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         qs = qs.filter(owner=request.user)
    #     return qs

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #
    #     if db_field.name == "parent":
    #         print('formfield_for_foreignkey')
    #         print(kwargs)
    #         kwargs["queryset"] = GoodsCategory.objects.filter(owner=request.user)
    #     # qs = kwargs["queryset"]
    #     # kwargs["queryset"] = qs.filter(owner=request.user)
    #     return super(GoodsCategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class AttributeInline(admin.TabularInline):
    model = ProductAttributeValue


class CategoryInline(admin.TabularInline):
    model = ProductCategory
    extra = 1


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 2


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'product_class', 'type')
    prepopulated_fields = {"code": ("name",)}


class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')


class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'requires_shipping')
    inlines = [ProductAttributeInline]


class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # inlines = [PictureInline]


# class ProductAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields': (('title','product_class', ), ('no', 'bar_code'),'categories', ),
#         }),
#         (_('详细展示'), {
#             'fields': ('description', 'pics'),
#             'classes':('collapse',),
#         }),
#     )

from django.urls import reverse
from django.shortcuts import redirect


class SelectProductClassForm(forms.Form):
    product_class = forms.ChoiceField(label=_('选择商品种类'))


class ProductAdmin(admin.ModelAdmin):

    def get_urls(self):
        from django.urls import path
        info = self.model._meta.app_label, self.model._meta.model_name
        urlpattern = [path('selectproductclass/', self.select_product_class,  name='%s_%s_select' % info)]
        return urlpattern+ super(ProductAdmin, self).get_urls()

    @csrf_protect_m
    def select_product_class(self, request, form_url='', extra_context=None):
        context = dict(
            self.admin_site.each_context(request), )

        opts = self.model._meta
        app_label = opts.app_label
        context.update({
            'opts': opts,
            'app_label': app_label,
            'media':self.media,
        })

        ProductClass.objects.all()
        choices = [('', '------------'), ]
        for ele in ProductClass.objects.all():
            choices.append((ele.id, ele))

        if request.method == 'POST':
            form = SelectProductClassForm(request.POST)
            form.fields["product_class"].choices = choices
            if form.is_valid():
                return redirect("%s?%s=%s" % (reverse('admin:estore_product_add'), 'product_class', form.data['product_class']))
        else:
            form = SelectProductClassForm()
            form.fields["product_class"].choices = choices

        context['form'] = form

        return render(request, 'select_product_class.html', context)

    def add_view(self, request, form_url='', extra_context=None):
        if 'product_class' not in request.GET and request.method == 'GET':
            return redirect(reverse('admin:estore_product_select'))
        return super(ProductAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    # date_hierarchy = 'date_created'
    # list_display = ('get_title', 'upc', 'get_product_class', 'structure',
    #                 'attribute_summary', 'date_created')
    # list_filter = ['structure', 'is_discountable']
    # raw_id_fields = ['parent']
    inlines = [AttributeInline, ]
    # prepopulated_fields = {"slug": ("title",)}
    # search_fields = ['upc', 'title']

    # def get_queryset(self, request):
    #     qs = super(ProductAdmin, self).get_queryset(request)
    #     return (
    #         qs
    #         .select_related('product_class', 'parent')
    #         .prefetch_related(
    #             'attribute_values',
    #             'attribute_values__attribute'))


class PictureAdmin(admin.ModelAdmin):
    pass
    # change_list_template = 'app_index_html'
    # form = PictureForm
    list_display = ('desc', 'display_picture', 'display_path',)
    list_display_links = ('desc', 'display_picture', 'display_path',)
    # formfield_overrides = {
    #     models.ImageField: {'widget': ImgWidget},
    # }


class AttributeOptionInline(admin.TabularInline):
    model = AttributeOption


class AttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline, ]


class SelectProductClassAdmin(admin.ModelAdmin):
    models = SelectProductClass

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = dict(
            self.admin_site.each_context(request), )
        ProductClass.objects.all()
        choices = [('', '------------'), ]
        for ele in ProductClass.objects.all():
            choices.append((ele.id, ele))

        if request.method == 'POST':
            form = SelectProductClassForm(request.POST)
            form.fields["product_class"].choices = choices
            form.is_valid()
        else:
            form = SelectProductClassForm()
            form.fields["product_class"].choices = choices

        context['form'] = form

        return render(request, 'select_product_class.html', context)

        # return TemplateResponse(request,'select_product_class.html',context)
        return super(SelectProductClassAdmin, self).change_view(request, object_id, form_url, extra_context)
        return redirect("%s?%s=%s" % (reverse('admin:estore_product_add'), 'product_class', '1'))


admin.site.register(ShopInfo, ShopInfoAdmin)

admin.site.register(ProductCategory, ProductCategoryAdmin)

admin.site.register(Picture, PictureAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductClass, ProductClassAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(AttributeOptionGroup, AttributeOptionGroupAdmin)
admin.site.register(AttributeOption)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(SelectProductClass, SelectProductClassAdmin)
