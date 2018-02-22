from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance

class SnippetSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = ('owner','id', 'title', 'code', 'linenos', 'language', 'style')

class PictureSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = Picture
        fields = ('picture', 'desc')

class ProductAttributeSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = ProductAttribute
        # exclude=[]
        fields = ( 'code','attributie')

class NoticeSerializer(serializers.ModelSerializer):
    # snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = Notice
        fields = ('id','content')

class ShopInfoSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # icon = serializers.ReadOnlyField(view_name='picture-detail', format='json')
    banners = PictureSerializer(many=True)
    icon = PictureSerializer()
    notices = NoticeSerializer(many=True)
    serializers.StringRelatedField(many=True)
    class Meta:
        model = ShopInfo
        fields = ('id', 'name', 'owner', 'type', 'address', 'phone_num','longitude', 'latitude', 'icon', 'description','banners','notices')


class ProductSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    # icon = serializers.ReadOnlyField(view_name='picture-detail', format='json')
    pics = PictureSerializer(many=True)
    primary_pic = PictureSerializer()
    # attributies = ProductAttributeSerializer(many=True)
    # serializers.StringRelatedField(many=True)
    attributes = serializers.SerializerMethodField('get_attrbute_dict')
    class Meta:
        model = Product
        fields = ('title', 'attributes', 'description', 'pics','primary_pic','price','off_price')
    def get_attrbute_dict(self, obj):
        return obj.attributes_dict()

class BasketLineUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasketLineUnit
        exclude = []


class BasketSerializer(serializers.ModelSerializer):

    lines = BasketLineUnitSerializer(many=True)


    def update(self, instance, validated_data):
        # Update the book instance
        # instance.title = validated_data['title']
        # instance.save()
        #
        # # Delete any pages not included in the request
        # line_ids = [item['line_id'] for item in validated_data['lines']]
        # for page in instance.books:
        #     if page.id not in page_ids:
        #         page.delete()
        #
        # # Create or update page instances that are in the request
        # for item in validated_data['pages']:
        #     page = Page(id=item['page_id'], text=item['text'], book=instance)
        #     page.save()

        return instance
    class Meta:
        model = Basket
        fields = ('status','date_created','date_submitted','lines')


