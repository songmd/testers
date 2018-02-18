from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *
from functools import partial
from django.core import exceptions

from mptt.admin import MPTTModelAdmin
from django.db import models
from django.db.models import Q
from .imagefieldex import ImageFieldEx, ImgWidget
from django.forms.models import modelform_factory

from django import forms
from django.shortcuts import render
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.admin import helpers, widgets
from django.db.models import Q


# from guardian.admin import GuardedModelAdmin

class EstoreModelAdminMixin(object):

    def get_queryset(self, request):
        qs = super(EstoreModelAdminMixin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(owner=request.user) | Q(owner__isnull=True))

    def save_model(self, request, obj, form, change):
        # 超级用户写入的东西默认是给所有人看到
        if hasattr(obj, 'owner') and obj.owner is None and not request.user.is_superuser:
            obj.owner = request.user
        super(EstoreModelAdminMixin, self).save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return super(EstoreModelAdminMixin, self).has_add_permission(request) or request.user.is_staff

    def has_change_permission(self, request, obj=None):

        has_perm = super(EstoreModelAdminMixin, self).has_change_permission(request, obj)
        for_staff_show = request.user.is_staff and obj is None
        owner = getattr(obj, 'owner', None)
        is_owner_obj = owner is None or owner == request.user
        return has_perm or for_staff_show or is_owner_obj

    def has_delete_permission(self, request, obj=None):
        has_perm = super(EstoreModelAdminMixin, self).has_delete_permission(request, obj)
        if has_perm:
            return True
        for_staff_show = request.user.is_staff and obj is None
        owner = getattr(obj, 'owner', None)
        is_owner_obj = owner is None or owner == request.user
        return for_staff_show or is_owner_obj


csrf_protect_m = method_decorator(csrf_protect)


def _attr_text_field(attribute):
    return forms.CharField(label=attribute.name,
                           required=attribute.required)


def _attr_textarea_field(attribute):
    return forms.CharField(label=attribute.name,
                           widget=forms.Textarea(),
                           required=attribute.required)


def _attr_integer_field(attribute):
    return forms.IntegerField(label=attribute.name,
                              required=attribute.required)


def _attr_boolean_field(attribute):
    return forms.BooleanField(label=attribute.name,
                              required=attribute.required)


def _attr_float_field(attribute):
    return forms.FloatField(label=attribute.name,
                            required=attribute.required)


def _attr_date_field(attribute):
    return forms.DateField(label=attribute.name,
                           required=attribute.required,
                           widget=widgets.AdminDateWidget)


def _attr_datetime_field(attribute):
    return forms.fields.SplitDateTimeField(label=attribute.name,
                                           required=attribute.required,
                                           widget=widgets.AdminSplitDateTime)


def _attr_option_field(attribute):
    return forms.ModelChoiceField(
        label=attribute.name,
        required=attribute.required,
        queryset=attribute.option_group.options.all())


def _attr_multi_option_field(attribute):
    return forms.ModelMultipleChoiceField(
        label=attribute.name,
        required=attribute.required,
        queryset=attribute.option_group.options.all())


def _attr_entity_field(attribute):
    # Product entities don't have out-of-the-box supported in the ProductForm.
    # There is no ModelChoiceField for generic foreign keys, and there's no
    # good default behaviour anyway; offering a choice of *all* model instances
    # is hardly useful.
    return None


def _attr_numeric_field(attribute):
    return forms.FloatField(label=attribute.name,
                            required=attribute.required)


def _attr_file_field(attribute):
    return forms.FileField(
        label=attribute.name, required=attribute.required)


def _attr_image_field(attribute):
    return forms.ImageField(
        label=attribute.name, required=attribute.required)


@admin.register(ProductCategory)
class ProductCategoryAdmin(EstoreModelAdminMixin, MPTTModelAdmin):
    list_display = ('name', 'parent')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "parent":
            kwargs["queryset"] = ProductCategory.objects.filter(owner=request.user)

        return super(ProductCategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


from django.urls import reverse
from django.shortcuts import redirect


class SelectProductClassForm(forms.Form):
    product_class = forms.ChoiceField(label=_('选择商品种类'))


class ProductAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        new_fields = {}
        self.set_initial(kwargs)
        if len(args) == 2:  # post
            if kwargs['instance'] is None:  # add
                opts = self._meta
                instance = opts.model()
                instance.product_class = ProductClass.objects.get(pk=args[0]['product_class'])
                kwargs['instance'] = instance
                # self.instance = instance
        super(ProductAdminForm, self).__init__(*args, **kwargs)

        if self.instance.product_class is None:  # get #add
            self.instance.product_class = ProductClass.objects.get(pk=self.initial['product_class'])

        #
        # if hasattr(self, 'instance') and hasattr(self, 'initial') and 'product_class' in self.initial:
        #     self.instance.product_class = ProductClass.objects.get(pk=self.initial['product_class'])

    def _post_clean(self):
        """
        Set attributes before ModelForm calls the product's clean method
        (which it does in _post_clean), which in turn validates attributes.
        """
        print('_post_clean')
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attr_%s' % attribute.code
            # An empty text field won't show up in cleaned_data.
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.code, value)
        super(ProductAdminForm, self)._post_clean()

    def set_initial(self, kwargs):
        """
        Set initial data for the form. Sets the correct product structure
        and fetches initial values for the dynamically constructed attribute
        fields.
        """
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        self.set_initial_attribute_values(kwargs)

    def set_initial_attribute_values(self, kwargs):
        """
        Update the kwargs['initial'] value to have the initial values based on
        the product instance's attributes
        """
        instance = kwargs.get('instance')
        if instance is None:
            return
        for attribute in instance.product_class.attributes.all():
            try:
                value = instance.attribute_values.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                kwargs['initial']['attr_%s' % attribute.code] = value

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(EstoreModelAdminMixin, admin.ModelAdmin):
    FIELD_FACTORIES = {
        "text": _attr_text_field,
        "richtext": _attr_textarea_field,
        "integer": _attr_integer_field,
        "boolean": _attr_boolean_field,
        "float": _attr_float_field,
        "date": _attr_date_field,
        "datetime": _attr_datetime_field,
        "option": _attr_option_field,
        "multi_option": _attr_multi_option_field,
        "entity": _attr_entity_field,
        "numeric": _attr_numeric_field,
        "file": _attr_file_field,
        "image": _attr_image_field,
    }

    readonly_fields = ('product_class_read_only',)
    list_display = ('title', 'product_class', 'no', 'bar_code')
    list_display_links = ('title', 'product_class', 'no', 'bar_code')

    def get_urls(self):
        from django.urls import path
        info = self.model._meta.app_label, self.model._meta.model_name
        urlpattern = [path('selectproductclass/', self.select_product_class, name='%s_%s_select' % info)]
        return urlpattern + super(ProductAdmin, self).get_urls()

    @csrf_protect_m
    def select_product_class(self, request, form_url='', extra_context=None):
        context = dict(
            self.admin_site.each_context(request), )

        opts = self.model._meta
        app_label = opts.app_label
        context.update({
            'opts': opts,
            'app_label': app_label,
            'media': self.media,
        })


        choices = [('', '------------'), ]
        for ele in ProductClass.objects.filter(owner=request.user):
            choices.append((ele.id, ele))

        if request.method == 'POST':
            form = SelectProductClassForm(request.POST)
            form.fields["product_class"].choices = choices
            if form.is_valid():
                return redirect(
                    "%s?%s=%s" % (reverse('admin:estore_product_add'), 'product_class', form.data['product_class']))
        else:
            form = SelectProductClassForm()
            form.fields["product_class"].choices = choices

        context['form'] = form

        return render(request, 'select_product_class.html', context)

    def product_class_read_only(self, instance):
        # assuming get_full_address() returns a list of strings
        # for each line of the address and you want to separate each
        # line by a linebreak
        return instance.product_class

    product_class_read_only.short_description = _('商品种类')
    product_class_read_only.allow_tags = True

    def get_form(self, request, obj=None, **kwargs):

        if obj is not None:
            product_class = obj.product_class
        else:
            product_class = ProductClass.objects.get(pk=request.GET['product_class'])

        new_fields = {}
        for atrributes in product_class.attributes.all():
            # field_name = '{0}_groups'.format(atrributes.name.lower())
            field_name = 'attr_%s' % atrributes.code
            field = ProductAdmin.FIELD_FACTORIES[atrributes.type](atrributes)

            new_fields[field_name] = field

        form_class = modelform_factory(Product,
                                       form=ProductAdminForm, exclude=self.readonly_fields,
                                       formfield_callback=partial(self.formfield_for_dbfield, request=request))
        form_class.base_fields.update(new_fields)

        form_class.base_fields['product_class'].widget = forms.HiddenInput()

        return form_class

    def add_view(self, request, form_url='', extra_context=None):
        if 'product_class' not in request.GET and request.method == 'GET':
            return redirect(reverse('admin:estore_product_select'))
        return super(ProductAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def get_fieldsets(self, request, obj=None):
        if obj is not None:
            product_class = obj.product_class
        else:
            product_class = ProductClass.objects.get(pk=request.GET['product_class'])

        fields = []
        for atrributes in product_class.attributes.all():
            # field_name = '{0}_groups'.format(atrributes.name.lower())
            field_name = 'attr_%s' % atrributes.code
            fields.append(field_name)

        fieldsets = (
            (None, {
                'fields': (('title', 'product_class', 'product_class_read_only'), ('no', 'bar_code'), 'categories',),
            }),
            (_('属性'), {
                'fields': (name for name in fields),
            }),
            (_('详细展示'), {
                'fields': ('description', 'pics'),
                'classes': ('collapse',),
            }),
        )
        return fieldsets

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "pics":
            kwargs["queryset"] = Picture.objects.filter(owner=request.user)
        if db_field.name == "categories":
            kwargs["queryset"] = ProductCategory.objects.filter(owner=request.user)

        return super(ProductAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

class AttributeOptionInline(EstoreModelAdminMixin, admin.TabularInline):
    model = AttributeOption


@admin.register(AttributeOptionGroup)
class AttributeOptionGroupAdmin(EstoreModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'option_summary','owner')
    inlines = [AttributeOptionInline, ]


class ProductAttributeInline(EstoreModelAdminMixin, admin.TabularInline):
    template = 'tabular.html'
    model = ProductAttribute
    fields = ('name', 'required', 'code', 'type', 'option_group')

    @property
    def media(self):
        return super(ProductAttributeInline, self).media + forms.Media(css={'all': ('css/estore.css',)})


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "option_group":
            kwargs["queryset"] = AttributeOptionGroup.objects.filter(owner=request.user)

        return super(ProductAttributeInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ProductClass)
class ProductClassAdmin(EstoreModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'requires_shipping')
    inlines = [ProductAttributeInline]


@admin.register(Picture)
class PictureAdmin(EstoreModelAdminMixin, admin.ModelAdmin):
    list_display = ('desc', 'display_picture', 'display_path',)
    list_display_links = ('desc', 'display_picture', 'display_path',)


@admin.register(ShopInfo)
class ShopInfoAdmin(EstoreModelAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'type')
