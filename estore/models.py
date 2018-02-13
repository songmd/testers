from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

from django.utils.translation import gettext_lazy as _

from .imagefieldex import ImageFieldEx,OneToOneFieldEx,ManyToManyFieldEx

from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey

from django.utils.html import format_html

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
    owner = models.ForeignKey('auth.User', related_name='pictures', on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name=_('商户'))
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
        return '%s||||%s'% (self.desc, self.picture.url)
        # return self.desc


class GoodsCategory(MPTTModel):
    owner = models.ForeignKey('auth.User', related_name='categories', on_delete=models.SET_NULL, blank=True, null=True,
                              verbose_name=_('商户'))
    name = models.CharField(max_length=32, verbose_name=_('分类名称'))
    parent = TreeForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True,
                            null=True,
                            verbose_name=_('上级分类'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('商品分类')
        verbose_name_plural = _('商品分类管理')


class ShopInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('店铺名称'))
    owner = models.ForeignKey('auth.User', related_name='shops', on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name=_('商户'))
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


class Goods(models.Model):
    owner = models.ForeignKey('auth.User', related_name='goods', on_delete=models.CASCADE, blank=True, null=True,
                              verbose_name=_('商户'))
    name = models.CharField(max_length=32, verbose_name=_('名称'))

    no = models.CharField(max_length=32, verbose_name=_('编号'), blank=True, null=True)

    bar_code = models.CharField(max_length=32, verbose_name=_('条码编号'), blank=True, null=True)

    description = models.TextField(max_length=512, blank=True, null=True, verbose_name=_('描述'),
                                   help_text=_('最多500个字符，250个汉字'))

    pics = ManyToManyFieldEx(Picture, blank=True, verbose_name=_('图片'))

    class Meta:
        verbose_name = _('商品')
        verbose_name_plural = _('商品管理')

    def __str__(self):
        return self.name

