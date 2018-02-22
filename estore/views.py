from estore.models import Snippet, ShopInfo
from estore.serializers import *
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from estore.permissions import IsOwnerOrReadOnly

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PictureList(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetail(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


from rest_framework import renderers
from rest_framework.response import Response


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class ShopInfoList(generics.ListCreateAPIView):
    queryset = ShopInfo.objects.all()
    serializer_class = ShopInfoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopInfoDetail(generics.RetrieveAPIView):
    queryset = ShopInfo.objects.all()
    serializer_class = ShopInfoSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)

class ProductList(generics.ListAPIView):
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_queryset(self):
        shop_id = self.request.query_params.get('shop_id',None)
        if shop_id is None:
            return Product.objects.all().none()
        queryset = Product.objects.filter(belong=shop_id)
        return queryset

class BasketView(generics.RetrieveUpdateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

    def get_object(self):
        qs = self.get_queryset()
        obj = qs.get(customer__id=self.kwargs['pk'])
        return obj

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     # Delete any pages not included in the request
    #     basket = request.data
    #
    #     line_ids = [item['id'] for item in basket['lines'] if 'id' in item]
    #     for line in instance.lines.iterator:
    #         if line.id not in line_ids:
    #             line.delete()
    #
    #     # Create or update page instances that are in the request
    #     for item in basket['lines']:
    #         line = BasketLineUnit(id=item['id'], price=item['price'], quantity=item['quantity'],
    #                               product=item['product'],basket=instance)
    #         line.save()
    #     serializer = self.get_serializer(instance)
    #
    #
    #     return Response(serializer.data)
class BasketUnitView(generics.ListCreateAPIView):
    serializer_class = BasketLineUnitSerializer
    def get_queryset(self):
        return BasketLineUnit.objects.all().filter(basket__customer=self.kwargs['user_token'])

class BasketUnitDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = BasketLineUnitSerializer
    def get_queryset(self):
        return BasketLineUnit.objects.all().filter(basket__customer=self.kwargs['user_token'])

class RetCode(object):
    SUCCESS = '0000'
    INVALID_PARA = '0001'
    USER_NOT_EXIST = '0002'
    SHOP_NOT_EXIST = '0003'
    WXSRV_ERROR = '0004'
    SRV_EXCEPTION='0005'

# @api_view(['POST'])
from .models import AppCustomer
from django.contrib.auth import authenticate, login
import json
from django.http import HttpResponse

from .weixin import WxApi
import uuid

def customer_login(request):
    resp = {}
    js_code = request.GET.get('js_code',None)
    user_token = request.GET.get('user_token',None)
    shop_id = request.GET.get('shop_id',None)
    user_info = request.GET.get('user_info',None)


    try:
        if shop_id is None:
            resp['retcode'] = RetCode.INVALID_PARA
            return HttpResponse(json.dumps(resp), content_type="application/json")

        shop = ShopInfo.objects.get(pk=uuid.UUID(shop_id))
        if shop is None:
            resp['retcode'] = RetCode.SHOP_NOT_EXIST
            return HttpResponse(json.dumps(resp), content_type="application/json")

        # 有js_code 则user_token不生效
        if js_code is not None:
            wx_data = WxApi.get_openid(shop.app_id, shop.app_secret, js_code)
            if 'errcode' in wx_data:
                resp['retcode'] = RetCode.WXSRV_ERROR
                return HttpResponse(json.dumps(resp), content_type="application/json")
            try:
                customer = AppCustomer.objects.get(openid=wx_data['openid'], belong=shop)
                resp['user_token'] = customer.id.hex
            except AppCustomer.DoesNotExist:
                customer = AppCustomer.objects.create()
                customer.openid = wx_data['openid']
                customer.belong = shop
                resp['user_token'] = customer.id.hex
                customer.basket = Basket.objects.create()

            customer.session_key = wx_data['session_key']
            if 'unionid' in wx_data:
                customer.unionid = wx_data['unionid']
            if user_info:
                customer.user_info = user_info
            customer.save()

            # login(request, customer)
            resp['retcode'] = RetCode.SUCCESS
            return HttpResponse(json.dumps(resp), content_type="application/json")

        if user_token is not None:
            customer = AppCustomer.objects.get(pk=user_token, belong=shop)
            if customer is None:
                resp['retcode'] = RetCode.USER_NOT_EXIST
                return HttpResponse(json.dumps(resp), content_type="application/json")
            # login(request, customer)
            resp['retcode'] = RetCode.SUCCESS

            if user_info != customer.user_info:
                customer.user_info = user_info
                customer.save()

            return HttpResponse(json.dumps(resp), content_type="application/json")
    except BaseException as e:
        print(e)
        resp['retcode'] = RetCode.SRV_EXCEPTION
        return HttpResponse(json.dumps(resp), content_type="application/json")

    resp['retcode'] = RetCode.INVALID_PARA
    return  HttpResponse(json.dumps(resp), content_type="application/json")


