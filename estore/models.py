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

import uuid


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
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)

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
        verbose_name_plural = _('图片')

    def __str__(self):
        return '%s||||%s' % (self.desc, self.picture.url)
        # return self.desc


class ProductCategory(MPTTModel):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)

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
            display = '%s->%s' % (pp.name, display)
            pp = pp.parent
        return display

    class Meta:
        verbose_name = _('商品分类')
        verbose_name_plural = _('商品分类')

#商户
class AppMerchant(models.Model):
    user = models.OneToOneField('auth.User', related_name='merchant', on_delete=models.CASCADE,verbose_name=_('关联用户'))
    type =   models.CharField(_('用户类型'),max_length=16, default='appmch',editable=False)
    mch_id = models.CharField(_('商户微信支付Id'),max_length=128, blank=True, null=True )
    mch_key = models.CharField(_('商户微信支付密钥'),max_length=128, blank=True, null=True )
    key_file = models.FileField(_('密钥文件'),blank=True, null=True,upload_to='cert')
    cert_file = models.FileField(_('证书文件'),blank=True, null=True,upload_to='cert')
    class Meta:
        verbose_name = _('商户')
        verbose_name_plural = _('商户')
    def __str__(self):
        return self.user.username

class AppCustomer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    belong = models.ForeignKey('ShopInfo', related_name='customers',on_delete=models.CASCADE, blank=True,null=True,verbose_name=_('所属店铺'))
    basket = models.OneToOneField('Basket',related_name='customer',on_delete=models.PROTECT,verbose_name=_('购物车'))
    phone_num = models.CharField(_('手机号'), max_length=16, blank=True, null=True)
    openid = models.CharField(_('微信OpenId'), max_length=128, blank=True, null=True)
    session_key = models.CharField(_('会话密钥'), max_length=128, blank=True, null=True)
    unionid = models.CharField(_('统一Id'), max_length=128, blank=True, null=True)
    user_info = models.TextField(_('用户信息'), max_length=512, blank=True, null=True)

    def display_id(self):
        return self.id.hex
    display_id.short_description = _('ID')

    class Meta:
        verbose_name = _('客户')
        verbose_name_plural = _('客户')
    def __str__(self):
        return self.id.hex

class ShopInfo(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_('所属商户'))

    name = models.CharField(max_length=32, verbose_name=_('店铺名称'))

    app_id = models.CharField(_('小程序id'),max_length=128, blank=True, null=True )

    app_secret = models.CharField(_('小程序密钥'),max_length=128, blank=True, null=True )


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

    banners = ManyToManyFieldEx(Picture, blank=True, related_name='banners',verbose_name=_('广告图片'))

    def display_id(self):
        return self.id.hex

    display_id.short_description = _('ID')

    class Meta:
        # name = '1'
        verbose_name = _('店铺')
        verbose_name_plural = _('店铺')
        # permissions = (("view", _("浏览")),)

    def __str__(self):
        return self.name

class Notice(models.Model):
    owner = models.ForeignKey(ShopInfo, related_name='notices',on_delete=models.CASCADE, verbose_name=_('所属店铺'))
    content = models.TextField(_('内容'),max_length=512,help_text=_('最多500个字符，250个汉字'))
    class Meta:
        # name = '1'
        verbose_name = _('公告')
        verbose_name_plural = _('公告')
        # permissions = (("view", _("浏览")),)

    def __str__(self):
        return self.content

class ProductAttributesContainer(object):
    """
    Stolen liberally from django-eav, but simplified to be product-specific

    To set attributes on a product, use the `attr` attribute:

        product.attr.weight = 125
    """

    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    def __init__(self, product):
        self.product = product
        self.initialised = False

    def initiate_attributes(self):
        values = self.get_values().select_related('attribute')
        for v in values:
            setattr(self, v.attribute.code, v.value)
        self.initialised = True

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            self.initiate_attributes()
            return getattr(self, name)
        raise AttributeError(
            _("%(obj)s has no attribute named '%(attr)s'") % {
                'obj': self.product.get_product_class(), 'attr': name})

    def validate_attributes(self):
        for attribute in self.get_all_attributes():
            value = getattr(self, attribute.code, None)
            if value is None:
                if attribute.required:
                    raise ValidationError(
                        _("%(attr)s attribute cannot be blank") %
                        {'attr': attribute.code})
            else:
                try:
                    attribute.validate_value(value)
                except ValidationError as e:
                    raise ValidationError(
                        _("%(attr)s attribute %(err)s") %
                        {'attr': attribute.code, 'err': e})

    def get_values(self):
        return self.product.attribute_values.all()

    def get_value_by_attribute(self, attribute):
        return self.get_values().get(attribute=attribute)

    def get_all_attributes(self):
        return self.product.product_class.attributes.all()

    def get_attribute_by_code(self, code):
        return self.get_all_attributes().get(code=code)

    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for attribute in self.get_all_attributes():
            if hasattr(self, attribute.code):
                value = getattr(self, attribute.code)
                attribute.save_value(self.product, value)


class Product(models.Model):
    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE, blank=True, null=True,
                              editable=False)

    belong = models.ForeignKey(ShopInfo, related_name='products', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('所属商铺'))

    product_class = models.ForeignKey('ProductClass', related_name='products', null=True, blank=True,
                                      on_delete=models.PROTECT, verbose_name=_('种类'))
    # product_class.hidden = True

    title = models.CharField(max_length=32, verbose_name=_('名称'))

    primary_pic = OneToOneFieldEx(Picture, blank=True, null=True, related_name='primary',verbose_name=_('首要图片'), on_delete=models.SET_NULL)

    price = models.FloatField(blank=True, null=True, verbose_name=_('价格'))
    off_price = models.FloatField(blank=True, null=True, verbose_name=_('折扣价格'))

    no = models.CharField(max_length=32, verbose_name=_('编号'), blank=True, null=True)

    bar_code = models.CharField(max_length=32, verbose_name=_('条码编号'), blank=True, null=True)

    categories = models.ManyToManyField('ProductCategory', blank=True, verbose_name=_('所属分类'))

    attributies = models.ManyToManyField('ProductAttribute', through='ProductAttributeValue', blank=True,
                                         verbose_name=_('属性'))

    rating = models.FloatField(_('评价'), null=True, blank=True, editable=False)

    description = models.TextField(max_length=512, blank=True, null=True, verbose_name=_('文字描述'),
                                   help_text=_('最多500个字符，250个汉字'))

    pics = ManyToManyFieldEx(Picture, blank=True, verbose_name=_('图片'))

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品')

    def __str__(self):
        return self.title

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.attr = ProductAttributesContainer(product=self)

    def clean(self):
        """
        Validate a product. Those are the rules:

        +---------------+-------------+--------------+--------------+
        |               | stand alone | parent       | child        |
        +---------------+-------------+--------------+--------------+
        | title         | required    | required     | optional     |
        +---------------+-------------+--------------+--------------+
        | product class | required    | required     | must be None |
        +---------------+-------------+--------------+--------------+
        | parent        | forbidden   | forbidden    | required     |
        +---------------+-------------+--------------+--------------+
        | stockrecords  | 0 or more   | forbidden    | 0 or more    |
        +---------------+-------------+--------------+--------------+
        | categories    | 1 or more   | 1 or more    | forbidden    |
        +---------------+-------------+--------------+--------------+
        | attributes    | optional    | optional     | optional     |
        +---------------+-------------+--------------+--------------+
        | rec. products | optional    | optional     | unsupported  |
        +---------------+-------------+--------------+--------------+
        | options       | optional    | optional     | forbidden    |
        +---------------+-------------+--------------+--------------+

        Because the validation logic is quite complex, validation is delegated
        to the sub method appropriate for the product's structure.
        """
        # getattr(self, '_clean_%s' % self.structure)()
        # if not self.is_parent:
        self.attr.validate_attributes()

    # def _clean_standalone(self):
    #     """
    #     Validates a stand-alone product
    #     """
    #     if not self.title:
    #         raise ValidationError(_("Your product must have a title."))
    #     if not self.product_class:
    #         raise ValidationError(_("Your product must have a product class."))
    #     if self.parent_id:
    #         raise ValidationError(_("Only child products can have a parent."))
    #
    # def _clean_child(self):
    #     """
    #     Validates a child product
    #     """
    #     if not self.parent_id:
    #         raise ValidationError(_("A child product needs a parent."))
    #     if self.parent_id and not self.parent.is_parent:
    #         raise ValidationError(
    #             _("You can only assign child products to parent products."))
    #     if self.product_class:
    #         raise ValidationError(
    #             _("A child product can't have a product class."))
    #     if self.pk and self.categories.exists():
    #         raise ValidationError(
    #             _("A child product can't have a category assigned."))
    #     # Note that we only forbid options on product level
    #     if self.pk and self.product_options.exists():
    #         raise ValidationError(
    #             _("A child product can't have options."))
    #
    # def _clean_parent(self):
    #     """
    #     Validates a parent product.
    #     """
    #     self._clean_standalone()
    #     if self.has_stockrecords:
    #         raise ValidationError(
    #             _("A parent product can't have stockrecords."))

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.get_title())
        super(Product, self).save(*args, **kwargs)
        self.attr.save()

    # Properties

    # @property
    # def is_standalone(self):
    #     return self.structure == self.STANDALONE
    #
    # @property
    # def is_parent(self):
    #     return self.structure == self.PARENT
    #
    # @property
    # def is_child(self):
    #     return self.structure == self.CHILD

    # def can_be_parent(self, give_reason=False):
    #     """
    #     Helps decide if a the product can be turned into a parent product.
    #     """
    #     reason = None
    #     if self.is_child:
    #         reason = _('The specified parent product is a child product.')
    #     if self.has_stockrecords:
    #         reason = _(
    #             "One can't add a child product to a product with stock"
    #             " records.")
    #     is_valid = reason is None
    #     if give_reason:
    #         return is_valid, reason
    #     else:
    #         return is_valid

    # @property
    # def options(self):
    #     """
    #     Returns a set of all valid options for this product.
    #     It's possible to have options product class-wide, and per product.
    #     """
    #     pclass_options = self.get_product_class().options.all()
    #     return set(pclass_options) or set(self.product_options.all())

    # @property
    # def is_shipping_required(self):
    #     return self.get_product_class().requires_shipping

    # @property
    # def has_stockrecords(self):
    #     """
    #     Test if this product has any stockrecords
    #     """
    #     return self.stockrecords.exists()

    # @property
    # def num_stockrecords(self):
    #     return self.stockrecords.count()

    def attributes_dict(self):
        ret = {}
        attributes = self.attribute_values.all()
        for attr in attributes:
            ret.update(attr.value_as_dict())
        return ret

    attributes_dict.short_description = _('attributes')

    @property
    def attribute_summary(self):
        """
        Return a string of all of a product's attributes
        """
        attributes = self.attribute_values.all()
        pairs = [attribute.summary() for attribute in attributes]
        return '{' + ", ".join(pairs) + '}'

    # def get_title(self):
    #     """
    #     Return a product's title or it's parent's title if it has no title
    #     """
    #     title = self.title
    #     if not title and self.parent_id:
    #         title = self.parent.title
    #     return title
    # get_title.short_description = pgettext_lazy(u"Product title", u"Title")

    # def get_product_class(self):
    #     """
    #     Return a product's item class. Child products inherit their parent's.
    #     """
    #     if self.is_child:
    #         return self.parent.product_class
    #     else:
    #         return self.product_class
    # get_product_class.short_description = _("Product class")

    # def get_is_discountable(self):
    #     """
    #     At the moment, is_discountable can't be set individually for child
    #     products; they inherit it from their parent.
    #     """
    #     if self.is_child:
    #         return self.parent.is_discountable
    #     else:
    #         return self.is_discountable

    # def get_categories(self):
    #     """
    #     Return a product's categories or parent's if there is a parent product.
    #     """
    #     if self.is_child:
    #         return self.parent.categories
    #     else:
    #         return self.categories
    # get_categories.short_description = _("Categories")

    # Images

    # def get_missing_image(self):
    #     """
    #     Returns a missing image object.
    #     """
    #     # This class should have a 'name' property so it mimics the Django file
    #     # field.
    #     return MissingProductImage()
    #
    # def get_all_images(self):
    #     if self.is_child and not self.images.exists():
    #         return self.parent.images.all()
    #     return self.images.all()

    # def primary_image(self):
    #     """
    #     Returns the primary image for a product. Usually used when one can
    #     only display one product image, e.g. in a list of products.
    #     """
    #     images = self.get_all_images()
    #     ordering = self.images.model.Meta.ordering
    #     if not ordering or ordering[0] != 'display_order':
    #         # Only apply order_by() if a custom model doesn't use default
    #         # ordering. Applying order_by() busts the prefetch cache of
    #         # the ProductManager
    #         images = images.order_by('display_order')
    #     try:
    #         return images[0]
    #     except IndexError:
    #         # We return a dict with fields that mirror the key properties of
    #         # the ProductImage class so this missing image can be used
    #         # interchangeably in templates.  Strategy pattern ftw!
    #         return {
    #             'original': self.get_missing_image(),
    #             'caption': '',
    #             'is_missing': True}

    # Updating methods

    # def update_rating(self):
    #     """
    #     Recalculate rating field
    #     """
    #     self.rating = self.calculate_rating()
    #     self.save()
    # update_rating.alters_data = True

    # def calculate_rating(self):
    #     """
    #     Calculate rating value
    #     """
    #     result = self.reviews.filter(
    #         status=self.reviews.model.APPROVED
    #     ).aggregate(
    #         sum=Sum('score'), count=Count('id'))
    #     reviews_sum = result['sum'] or 0
    #     reviews_count = result['count'] or 0
    #     rating = None
    #     if reviews_count > 0:
    #         rating = float(reviews_sum) / reviews_count
    #     return rating

    # def has_review_by(self, user):
    #     if user.is_anonymous:
    #         return False
    #     return self.reviews.filter(user=user).exists()

    # def is_review_permitted(self, user):
    #     """
    #     Determines whether a user may add a review on this product.
    #
    #     Default implementation respects OSCAR_ALLOW_ANON_REVIEWS and only
    #     allows leaving one review per user and product.
    #
    #     Override this if you want to alter the default behaviour; e.g. enforce
    #     that a user purchased the product to be allowed to leave a review.
    #     """
    #     if user.is_authenticated or settings.OSCAR_ALLOW_ANON_REVIEWS:
    #         return not self.has_review_by(user)
    #     else:
    #         return False
    #
    # @cached_property
    # def num_approved_reviews(self):
    #     return self.reviews.approved().count()
    #
    # @property
    # def sorted_recommended_products(self):
    #     """Keeping order by recommendation ranking."""
    #     return [r.recommendation for r in self.primary_recommendations
    #                                           .select_related('recommendation').all()]


class ProductClass(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)
    name = models.CharField(max_length=32, verbose_name=_('种类名称'))
    requires_shipping = models.BooleanField(_("是否运送"),
                                            default=True)

    class Meta:
        verbose_name = _('商品种类')
        verbose_name_plural = _('商品种类')

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)

    name = models.CharField(max_length=32, verbose_name=_('属性名称'))

    code = models.SlugField(max_length=32, verbose_name=_('属性编码'))

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
        ('', _('-------------')),
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
        verbose_name_plural = _('商品属性')

    def clean(self):
        if self.type in [ProductAttribute.OPTION, ProductAttribute.MULTI_OPTION] and self.option_group is None:
            raise ValidationError({'option_group': _('属性类型为选项或者多选项，必须指定所属选项组')})

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
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)

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
        if self.attribute.is_option and isinstance(new_value, six.string_types):
            # Need to look up instance of AttributeOption
            new_value = self.attribute.option_group.options.get(
                option=new_value)
        if self.attribute.is_multi_option:
            self.value_multi_option.set(new_value)
        else:
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

    def value_as_dict(self):
        return {self.attribute.code:str(self.value_as_text)}

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
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)

    name = models.CharField(_('名称'), max_length=32)

    # date_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('选项组')
        verbose_name_plural = _('选项组')

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
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, editable=False)

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
        verbose_name_plural = _('选项')





class Address(models.Model):
    phone_num = models.CharField(_('联系电话'), max_length=16, blank=True, null=True)
    addr = models.CharField(_('地址'), max_length=128)
    owner = models.ForeignKey(AppCustomer, related_name='addresses', on_delete=models.CASCADE,
                              verbose_name=_("客户"))


class Basket(models.Model):

    OPEN,   FROZEN, SUBMITTED = (
        "Open", "Saved", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )
    status = models.CharField(
        _("状态"), max_length=12, default=OPEN, choices=STATUS_CHOICES)

    date_created = models.DateTimeField(_("生成时间"), auto_now_add=True)
    date_submitted = models.DateTimeField(_("提交时间"), null=True, blank=True)

    def __str__(self):
        return self.customer.id.hex
    class Meta:
        verbose_name = _('购物车')
        verbose_name_plural = _('购物车')


class BasketLineUnit(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='lines', verbose_name=_("购物车"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='basket_lines', verbose_name=_("商品"))
    quantity = models.PositiveIntegerField(_('数量'), default=1)
    price = models.DecimalField(_('成交价格'), decimal_places=2, max_digits=12, null=True)
    date_created = models.DateTimeField(_("生成时间"), auto_now_add=True)


class Order(models.Model):
    number = models.CharField(
        _("订单号"), max_length=128, db_index=True, unique=True)

    basket = models.ForeignKey(Basket, verbose_name=_("购物车"),
                               null=True, blank=True, on_delete=models.SET_NULL)

    consumer = models.ForeignKey(AppCustomer, related_name='orders', null=True, blank=True,
                                 verbose_name=_("客户"), on_delete=models.SET_NULL)

    # Billing address is not always required (eg paying by gift card)
    shipping_address = models.ForeignKey(Address, null=True, blank=True, verbose_name=_("送货地址"),
                                         on_delete=models.SET_NULL)

    shipping_method = models.CharField(_("送货方式"), max_length=128, blank=True)

    shipping_code = models.CharField(_('快递单号'), blank=True, max_length=128, default="")

    status = models.CharField(_("订单状态"), max_length=100, blank=True)

    class Meta:
        verbose_name = _("订单")
        verbose_name_plural = _("订单")

# @todo 研究购物流程
# 显示产品列表  点添加按钮  显示添加结果  查看购物车细节  或者开始结账  收集结账必要的的信息（ 确认用户身份地址 输入支付 等等）
# 预览订单提交订单页面提交  返回确认结果
# 一系列的add和edit 增删改查
