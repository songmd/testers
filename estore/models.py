from datetime import date, datetime
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from django.utils.translation import gettext_lazy as _

from .imagefieldex import ImageFieldEx, OneToOneFieldEx, ManyToManyFieldEx

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.files.base import File

# from django.core.exceptions import ValidationError
from django.utils import six

from mptt.models import MPTTModel, TreeForeignKey

from django.utils.html import format_html

from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)

    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)


class Picture(models.Model):
    # owner = models.ForeignKey('auth.User', related_name='pictures', on_delete=models.CASCADE, blank=True, null=True,
    #                           verbose_name=_('商户'))
    # picture = models.ImageField(upload_to='estorepics', blank=True, null=True, verbose_name=_('图片'))
    desc = models.CharField(max_length=32, verbose_name=_('描述'))
    picture = ImageFieldEx(upload_to='estorepics', verbose_name=_('图片'))

    def display_picture(self):
        return format_html('<image src="{}" height="80px"></image>',
                           self.picture.url)

    display_picture.allow_tags = True
    display_picture.short_description = _('预览')

    def display_path(self):
        return self.picture.url

    display_path.short_description = _('路径')

    # def born_in_fifties(self):
    #     return True
    # born_in_fifties.boolean = True

    class Meta:
        # name = '1'
        verbose_name = _('图片')
        verbose_name_plural = _('图片管理')

    def __str__(self):
        return '%s||||%s' % (self.desc, self.picture.url)
        # return self.desc


class ProductCategory(MPTTModel):
    # owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.SET_NULL, blank=True, null=True,
    #                           verbose_name=_('商户'))
    name = models.CharField(max_length=32, verbose_name=_('分类名称'))
    parent = TreeForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True,
                            null=True,
                            verbose_name=_('上级分类'))

    def __str__(self):
        display = self.name
        pp = self.parent
        while pp is not None:
            display = '%s->%s' % (pp.name,display)
            pp = pp.parent
        return display

    class Meta:
        verbose_name = _('商品分类')
        verbose_name_plural = _('商品分类管理')


class ShopInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('店铺名称'))

    # owner = models.ForeignKey('auth.User', related_name='shops', on_delete=models.CASCADE, blank=True, null=True,
    #                           verbose_name=_('商户'))

    type = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('店铺类型'),
                            help_text=_('自定义店铺类型，32个字符以内'))

    address = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('地址'))

    phone_num = models.CharField(max_length=11, blank=True, null=True, verbose_name=_('联系电话'))
    longitude = models.FloatField(blank=True, null=True, verbose_name=_('经度'))
    latitude = models.FloatField(blank=True, null=True, verbose_name=_('纬度'))

    # icon = ImageFieldEx(upload_to='shopinfo/icon', blank=True, null=True, verbose_name=_('店铺图标'))
    icon = OneToOneFieldEx(Picture, blank=True, null=True, verbose_name=_('店铺图标'), on_delete=models.SET_NULL)

    description = models.TextField(max_length=512, blank=True, null=True, verbose_name=_('店铺描述'),
                                   help_text=_('最多500个字符，250个汉字'))

    class Meta:
        # name = '1'
        verbose_name = _('店铺')
        verbose_name_plural = _('店铺管理')

    def __str__(self):
        return self.name


class Product(models.Model):
    # owner = models.ForeignKey('auth.User', related_name='goods', on_delete=models.CASCADE, blank=True, null=True,
    #                           verbose_name=_('商户'))

    product_class = models.ForeignKey('ProductClass', related_name='products', on_delete=models.PROTECT, verbose_name=_('种类'))

    title = models.CharField(max_length=32, verbose_name=_('名称'))

    no = models.CharField(max_length=32, verbose_name=_('编号'), blank=True, null=True)

    bar_code = models.CharField(max_length=32, verbose_name=_('条码编号'), blank=True, null=True)

    categories = models.ManyToManyField('ProductCategory', blank=True, verbose_name=_('所属分类'))

    attributies = models.ManyToManyField('ProductAttribute', through='ProductAttributeValue', blank=True, verbose_name=_('属性'))

    rating = models.FloatField(_('评价'), null=True, blank=True, editable=False)

    description = models.TextField(max_length=512, blank=True, null=True, verbose_name=_('文字描述'),
                                   help_text=_('最多500个字符，250个汉字'))

    pics = ManyToManyFieldEx(Picture, blank=True, verbose_name=_('图片'))

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品管理')

    def __str__(self):
        return self.title

class SelectProductClass(models.Model):
    product_class = models.ForeignKey(
        'ProductClass',
        blank=True,
        on_delete=models.CASCADE,
        related_name='selected',
        verbose_name=_("商品种类"))

class ProductClass(models.Model):
    # owner = models.ForeignKey('auth.User', related_name='goods_types', on_delete=models.CASCADE, blank=True, null=True,
    #                           verbose_name=_('商户'))
    name = models.CharField(max_length=32, verbose_name=_('种类名称'))
    requires_shipping = models.BooleanField(_("是否运送"),
                                            default=True)
    class Meta:
        verbose_name = _('商品种类')
        verbose_name_plural = _('商品种类管理')

    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('属性名称'))
    code = models.CharField(max_length=32, verbose_name=_('属性编码'))

    product_class = models.ForeignKey(
        'ProductClass',
        blank=True,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name=_("商品种类"))

    # Attribute types
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    RICHTEXT = "richtext"
    DATE = "date"
    DATETIME = "datetime"
    OPTION = "option"
    MULTI_OPTION = "multi_option"
    ENTITY = "entity"
    FILE = "file"
    IMAGE = "image"
    TYPE_CHOICES = (
        (TEXT, _("文字")),
        (INTEGER, _("整数")),
        (BOOLEAN, _("是/否")),
        (FLOAT, _("浮点数")),
        (RICHTEXT, _("富文本")),
        (DATE, _("日期")),
        (DATETIME, _("时间")),
        (OPTION, _("选项")),
        (MULTI_OPTION, _("多选项")),
        (ENTITY, _("实体")),
        (FILE, _("文件")),
        (IMAGE, _("图片")),
    )
    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_("类型"))

    option_group = models.ForeignKey(
        'AttributeOptionGroup',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='product_attributes',
        verbose_name=_("选项组"),
        help_text=_('如果属性类型是"选项"或者"多选项",需额外选择一个选项组'))
    required = models.BooleanField(_('是否必需'), default=False)


    class Meta:
        verbose_name = _('商品属性')
        verbose_name_plural = _('商品属性管理')

    def __str__(self):
        return self.name

    @property
    def is_option(self):
        return self.type == self.OPTION

    @property
    def is_multi_option(self):
        return self.type == self.MULTI_OPTION

    @property
    def is_file(self):
        return self.type in [self.FILE, self.IMAGE]


    def _save_file(self, value_obj, value):
        # File fields in Django are treated differently, see
        # django.db.models.fields.FileField and method save_form_data
        if value is None:
            # No change
            return
        elif value is False:
            # Delete file
            value_obj.delete()
        else:
            # New uploaded file
            value_obj.value = value
            value_obj.save()

    def _save_multi_option(self, value_obj, value):
        # ManyToMany fields are handled separately
        if value is None:
            value_obj.delete()
            return
        try:
            count = value.count()
        except (AttributeError, TypeError):
            count = len(value)
        if count == 0:
            value_obj.delete()
        else:
            value_obj.value = value
            value_obj.save()

    def _save_value(self, value_obj, value):
        if value is None or value == '':
            value_obj.delete()
            return
        if value != value_obj.value:
            value_obj.value = value
            value_obj.save()

    def save_value(self, product, value):  # noqa: C901 too complex
        # ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
        try:
            value_obj = product.attribute_values.get(attribute=self)
        except ProductAttributeValue.DoesNotExist:
            # FileField uses False for announcing deletion of the file
            # not creating a new value
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ProductAttributeValue.objects.create(
                product=product, attribute=self)

        if self.is_file:
            self._save_file(value_obj, value)
        elif self.is_multi_option:
            self._save_multi_option(value_obj, value)
        else:
            self._save_value(value_obj, value)

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    # Validators

    def _validate_text(self, value):
        if not isinstance(value, six.string_types):
            raise ValidationError(_("Must be str or unicode"))

    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_datetime(self, value):
        if not isinstance(value, datetime):
            raise ValidationError(_("Must be a datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))

    def _validate_entity(self, value):
        if not isinstance(value, models.Model):
            raise ValidationError(_("Must be a model instance"))

    def _validate_multi_option(self, value):
        try:
            values = iter(value)
        except TypeError:
            raise ValidationError(
                _("Must be a list or AttributeOption queryset"))
        # Validate each value as if it were an option
        # Pass in valid_values so that the DB isn't hit multiple times per iteration
        valid_values = self.option_group.options.values_list(
            'option', flat=True)
        for value in values:
            self._validate_option(value, valid_values=valid_values)

    def _validate_option(self, value, valid_values=None):
        if not isinstance(value, AttributeOption):
            raise ValidationError(
                _("Must be an AttributeOption model object instance"))
        if not value.pk:
            raise ValidationError(_("AttributeOption has not been saved yet"))
        if valid_values is None:
            valid_values = self.option_group.options.values_list(
                'option', flat=True)
        if value.option not in valid_values:
            raise ValidationError(
                _("%(enum)s is not a valid choice for %(attr)s") %
                {'enum': value, 'attr': self})

    def _validate_file(self, value):
        if value and not isinstance(value, File):
            raise ValidationError(_("Must be a file field"))

    _validate_image = _validate_file

class ProductAttributeValue(models.Model):
    """
    The "through" model for the m2m relationship between catalogue.Product and
    catalogue.ProductAttribute.  This specifies the value of the attribute for
    a particular product

    For example: number_of_pages = 295
    """
    attribute = models.ForeignKey(
        'ProductAttribute',
        on_delete=models.CASCADE,
        verbose_name=_("属性"))
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='attribute_values',
        verbose_name=_("商品"))

    value_text = models.TextField(_('文字'), blank=True, null=True)
    value_integer = models.IntegerField(_('整数'), blank=True, null=True)
    value_boolean = models.NullBooleanField(_('布尔值'), blank=True)
    value_float = models.FloatField(_('浮点数'), blank=True, null=True)
    value_richtext = models.TextField(_('富文本'), blank=True, null=True)
    value_date = models.DateField(_('日期'), blank=True, null=True)
    value_datetime = models.DateTimeField(_('时间'), blank=True, null=True)
    value_multi_option = models.ManyToManyField(
        'AttributeOption', blank=True,
        related_name='multi_valued_attribute_values',
        verbose_name=_("多选值"))
    value_option = models.ForeignKey(
        'AttributeOption',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("单选值"))


    def _get_value(self):
        value = getattr(self, 'value_%s' % self.attribute.type)
        if hasattr(value, 'all'):
            value = value.all()
        return value

    def _set_value(self, new_value):
        # if self.attribute.is_option and isinstance(new_value, six.string_types):
        #     # Need to look up instance of AttributeOption
        #     new_value = self.attribute.option_group.options.get(
        #         option=new_value)
        setattr(self, 'value_%s' % self.attribute.type, new_value)

    value = property(_get_value, _set_value)

    class Meta:
        # abstract = True
        # app_label = 'catalogue'
        unique_together = ('attribute', 'product')
        verbose_name = _('商品属性值')
        verbose_name_plural = _('商品属性值集合')

    def __str__(self):
        return self.summary()

    def summary(self):
        """
        Gets a string representation of both the attribute and it's value,
        used e.g in product summaries.
        """
        return u"%s: %s" % (self.attribute.name, self.value_as_text)

    @property
    def value_as_text(self):
        """
        Returns a string representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_text property and
        return something appropriate.
        """
        property_name = '_%s_as_text' % self.attribute.type
        return getattr(self, property_name, self.value)

    @property
    def _multi_option_as_text(self):
        return ', '.join(str(option) for option in self.value_multi_option.all())

    @property
    def _richtext_as_text(self):
        return strip_tags(self.value)



    @property
    def value_as_html(self):
        """
        Returns a HTML representation of the attribute's value. To customise
        e.g. image attribute values, declare a _image_as_html property and
        return e.g. an <img> tag.  Defaults to the _as_text representation.
        """
        property_name = '_%s_as_html' % self.attribute.type
        return getattr(self, property_name, self.value_as_text)

    @property
    def _richtext_as_html(self):
        return mark_safe(self.value)



class AttributeOptionGroup(models.Model):
    """
    Defines a group of options that collectively may be used as an
    attribute type

    For example, Language
    """
    name = models.CharField(_('名称'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('选项组')
        verbose_name_plural = _('选项组管理')

    # @property
    def option_summary(self):
        options = [o.option for o in self.options.all()]
        return ", ".join(options)

    option_summary.short_description = _('可选项')



class AttributeOption(models.Model):
    """
    Provides an option within an option group for an attribute type
    Examples: In a Language group, English, Greek, French
    """
    group = models.ForeignKey(
        'AttributeOptionGroup',
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name=_("选项组"))
    option = models.CharField(_('选项'), max_length=32)

    def __str__(self):
        return self.option

    class Meta:
        unique_together = ('group', 'option')
        verbose_name = _('选项')
        verbose_name_plural = _('选项管理')