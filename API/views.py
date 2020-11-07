import json

from django.contrib.auth import get_user_model
from django.db.models.functions import datetime
from django.utils import timezone
from rest_framework import authentication
# Create your views here.
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from marketplace.models import Product
from marketplace.serializers import ProductSerializer
from shoppingcart.extras import generate_order_id
from shoppingcart.models import OrderItem, Order, Transaction
from shoppingcart.serializers import OrderSerializer
from shoppingcart.views import get_user_pending_order
from users.models import User, Review, Vendor, Profile
from users.serializers import CreateUserSerializer, ProfileSerializer
from users.serializers import ReviewSerializer, AddReviewSerializer, UpgradeVendorSerializer


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class Home(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        model = Product
        products = []
        i = 0
        while i < 4:
            product = model.get_random(model)
            if product not in products:
                products.append(product)
                i += 1
        return products


class ProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(profile, many=False, context={"request": request})
        return Response(serializer.data)


class ItemDetailView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.filter(id=self.kwargs.get("id")).first()
            serializer = ProductSerializer(product, many=False, context={"request": request})
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data)


class AddToCartView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user_profile = get_object_or_404(Profile, user=request.user)
            json_data = json.loads(request.body)
            ids = json_data['item_id']
            n_product = int(json_data['item_quantity'])
            product = Product.objects.filter(id=ids).first()
            if product.quantity <= 0:
                product.available = False
                product.save()
            if product.quantity <= n_product:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)
            else:
                product.quantity -= n_product
                if product.quantity <= 0:
                    product.available = False
                product.save()
                order_item, state = OrderItem.objects.get_or_create(product=product, quantity=n_product)
                user_order, state = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
                user_order.items.add(order_item)
                if state:
                    user_order.ref_code = generate_order_id()
                    user_order.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class OrderDetailsView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        order = get_user_pending_order(request)
        if type(order) == int:
            return Response(False)
        serializer = OrderSerializer(order, many=False, context={"request": request})
        return Response(serializer.data)


class RemoveFromCartView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        try:
            json_data = json.loads(request.body)
            item_id = json_data['item_id']  # Surround with try catch
            item_to_delete = OrderItem.objects.filter(pk=item_id).first()
            n_item = item_to_delete.quantity
            item = item_to_delete.product
            item.quantity += n_item
            item.save()
            item_to_delete.delete()
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_200_OK)


class ShopView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        vendor_istance = get_object_or_404(User, username=request.user)
        vendor = Vendor.objects.filter(user=vendor_istance).first()
        products = Product.objects.filter(vendor=vendor).order_by('-date_added')
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class OthersShop(APIView):

    def get(self, request, *args, **kwargs):
        try:
            vid = self.kwargs.get('vid')
            vendor = Vendor.objects.filter(id=vid).first()
            products = Product.objects.filter(vendor=vendor).order_by('-date_added')
            serializer = ProductSerializer(products, many=True, context={"request": request})
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(serializer.data)


class DeleteItemView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        try:
            json_data = json.loads(request.body)
            product_id = json_data['id']
            item = Product.objects.filter(id=product_id).first()
            vendor = Vendor.objects.filter(user=request.user).first()
            if vendor == item.vendor:
                item.delete()
                return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UpdateItemView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def put(self, request, *args, **kwargs):
        try:
            item_id = self.kwargs.get("pk")
            item_instance = Product.objects.filter(id=item_id).first()
            user_vendor_instance = Vendor.objects.filter(user=request.user).first()
            if item_instance.vendor == user_vendor_instance:
                json_data = json.loads(request.body)
                item_instance.item = json_data['item']
                item_instance.description = json_data['description']
                item_instance.cost = json_data['cost']
                item_instance.quantity = json_data['quantity']
                item_instance.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class UpdateProfileView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def put(self, request, *args, **kwargs):
        user_id = self.kwargs.get("pk")
        profile_instance = Profile.objects.filter(id=user_id).first()
        if profile_instance.user == request.user:
            json_data = json.loads(request.body)
            profile_instance.money = json_data['money']
            profile_instance.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class AddItemView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user_vendor_instance = Vendor.objects.filter(user=request.user).first()
        if not user_vendor_instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        request.data["vendor"] = user_vendor_instance.id
        request.data["available"] = True
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_200_OK)


class ReviewView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            vendor_id = self.kwargs.get("vid")
            reviews = Review.objects.filter(reviewed_vendor=vendor_id)
            serializer = ReviewSerializer(reviews, many=True, context={"request": request})
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AddReviewView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user_instance = request.user
        vendor = Vendor.objects.filter(id=self.kwargs.get("vid")).first()
        request.data["reviewed_vendor"] = vendor.id
        request.data["posted_by"] = user_instance.id
        serializer = AddReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            vendor.ranksum += int(request.data["rank"])
            vendor.ranknum += 1
            vendor.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class SearchView(APIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(item__contains=self.kwargs.get("query"))
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class CategoryView(APIView):

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(category=self.kwargs.get("category"))
        serializer = ProductSerializer(products, many=True, context={"request": request})
        return Response(serializer.data)


class OrderListView(APIView):

    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        orders = Order.objects.filter(owner=user_profile).order_by('-date_ordered')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class IsVendorView(APIView):

    def get(self, request):
        isVendor = Vendor.objects.filter(user=request.user).first()
        if not isVendor:
            return Response(False)
        return Response(True)


class VendorUpgradeView(APIView):

    def post(self, request):
        request.data["user"] = request.user.id
        request.data["ranksum"] = 1
        request.data["ranknum"] = 1
        serializer = UpgradeVendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UpdateTransactionView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        order_to_purchase = get_user_pending_order(request)
        order_total = order_to_purchase.get_cart_total()
        user_profile = get_object_or_404(Profile, user=request.user)
        if user_profile.money < order_total:
            return Response(status=status.HTTP_403_FORBIDDEN)
        order_to_purchase.is_ordered = True
        order_to_purchase.date_ordered = timezone.now()
        order_to_purchase.save()
        order_items = order_to_purchase.items.all()
        order_items.update(is_ordered=True, date_ordered=timezone.now())
        user_profile.money = user_profile.money - order_total
        user_profile.save()
        for item in order_items:
            vendor = item.product.vendor
            p_quantity = item.quantity
            p_cost = item.product.cost
            v_instance = Profile.objects.filter(user=vendor.user).first()
            v_instance.money += (p_cost * p_quantity)
            v_instance.save()
        transaction = Transaction(profile=request.user.profile,
                                  order_id=order_to_purchase.id,
                                  amount=order_to_purchase.get_cart_total(),
                                  success=True)
        transaction.save()
        return Response(status=status.HTTP_200_OK)
