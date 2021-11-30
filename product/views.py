import re
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import pagination
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
import math


class CategoryView(APIView,PageNumberPagination):
    serializer_class = CategorySerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get(self,request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CategoryDetailView(APIView):
    serializer_class = CategorySerializer

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = self.serializer_class(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class ProductListView(generics.ListAPIView):
#     serializer_class = ProductListSerializer
    

#     def get_queryset(self):
#         queryset = Product.objects.all()

#         q = self.request.query_params.get('q', None)
#         tags = self.request.query_params.get('tags')
#         criteria = self.request.query_params.get('properties')
#         in_stock = self.request.query_params.get('in_stock', None)
#         price_min = self.request.query_params.get('price_min', None)
#         price_max = self.request.query_params.get('price_max', None)

#         if q is not None:
#             queryset = queryset.filter(title__icontains=q)

#         if tags:
#             tags = tags.split(',')

#             for tag in tags:
#                 queryset = queryset.filter(tag_set__name__iexact=tag).distinct()

#         if criteria:
#             criteria = criteria.split(',')
#             values = PropertyValue.objects.filter(id__in=criteria)

#             grouped_values = defaultdict(list)
#             for value in values:
#                 grouped_values[value.property_id].append(value.id)

#             for key in grouped_values:
#                 values = grouped_values[key]
#                 queryset = queryset.filter(unit__value_set__in=values).distinct()

#         if in_stock == '1':
#             queryset = queryset.filter(unit__num_in_stock__gt=0).distinct()

#         if price_min is not None and price_min.isdigit():
#             queryset = queryset.filter(unit__price__gte=int(price_min)).distinct()

#         if price_max is not None and price_max.isdigit():
#             queryset = queryset.filter(unit__price__lte=int(price_max)).distinct()

#         return queryset


class ProductBySeller(APIView):
    def get(self,request,cName = ""):
        try:
            user_obj = User.objects.get(username = cName)
        except:
            raise Http404

        products = Product.objects.filter(seller=user_obj)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ProductSetPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'page': self.page.number,
                'has_prev': self.page.has_previous(),
                'has_next': self.page.has_next(),
            },
            'data': data,
            'total_pages': self.page.paginator.num_pages,
            'count':self.page.paginator.count
        })


class ProductView(APIView,ProductSetPagination):
    serializer_class = ProductSerializer

    def get_queryset(self,request):
        queryset = Product.objects.all()
        q = self.request.query_params.get('query', None)
        tags = self.request.query_params.get('tags','')
        order = self.request.query_params.get('order','newest')
        price_min = self.request.query_params.get('price_min', None)
        price_max = self.request.query_params.get('price_max', None)

        if q is not None:
            queryset = queryset.filter(title__icontains=q)

        if tags:
            tags = tags.split(',')
            tagId = [] 
            for tag in tags:
                if Category.objects.filter(cat_name=tag).exists():
                    cat_obj = Category.objects.get(cat_name=tag)
                    tagId.append(cat_obj.id)

            for id in tagId:
                queryset = queryset.filter(tag_set__id=id).distinct()



        if order == 'Price_By_Asc':
            queryset = queryset.order_by('price')
        elif order == 'Price_By_Desc':
            queryset = queryset.order_by('-price')
        elif order == 'newest':
            queryset = queryset.order_by('created_at')
        elif order == 'oldest':
            queryset = queryset.order_by('-created_at')

        if price_min is not None and price_min.isdigit():
            queryset = queryset.filter(price__gte=int(price_min)).distinct()
        if price_max is not None and price_max.isdigit():
            queryset = queryset.filter(price__lte=int(price_max)).distinct()
        return queryset


    def get(self, request, format=None):
        self.page_size_query_param = 'size'
        products = self.get_queryset(request)
        page = int(self.request.query_params.get('page',1))
        size = int(self.request.query_params.get('size',3))
        total_item = len(products)
        total_page = math.ceil(len(products)/size)
        if page > total_page:
            return Response({"message":"page Not exist",'total_page':total_page},status=status.HTTP_200_OK)
            self.page_query_param = 1

        results = self.paginate_queryset(products, request, view=self)
        serializer = self.serializer_class(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self,request):
        # serializer = self.serializer_class(data = request.data)
        # serializer.is_valid()
        validated_data = request.data
        title = validated_data.get('title',"")

        if Product.objects.filter(title=title).exists():
            return Response({'message':'title must be different'},status=status.HTTP_400_BAD_REQUEST)
        
        category_data = validated_data.pop('tags',[])

        digital = validated_data.pop('digital',False)
        user_obj = User.objects.get(username=validated_data['seller'])
        
        image = None
        if 'image' in validated_data:
            image = validated_data['image']
        
        description = ""
        if 'description' in validated_data:
            description = validated_data['description']
        

        product = Product.objects.create(title=validated_data['title'],
                price=validated_data['price'],
                seller = user_obj,
                image=image,
                description=description,
                digital=digital
            )
        for cat in category_data:
            cat_obj = Category.objects.get_or_create(cat_name=cat)[0]
            product.tag_set.add(cat_obj)
        product.save()
        serializer = self.serializer_class(product)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    


class ProductDetailView(APIView):
    serializer_class = ProductSerializer
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = self.serializer_class(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = self.serializer_class(snippet, data=request.data)
        serializer.is_valid()
        validated_data = request.data
        product = Product.objects.get(id=pk)
        try:
            product_obj = Product.objects.get(id=pk)
        except:
            raise Http404

        # edit title
        if 'title' in validated_data:
            title = validated_data.get('title',"")
            if  title != product_obj.title and Product.objects.filter(title=title).exists():
                return Response({'message':'title must be different'},status=status.HTTP_400_BAD_REQUEST)
            product.title = title
        
        # edit tags
        if 'tags' in validated_data:
            category_data = validated_data.pop('tags',[])
            for cat in category_data:
                cat_obj = Category.objects.get_or_create(cat_name=cat)[0]
                product.tag_set.add(cat_obj)
        # edit image 
        if 'image' in validated_data:
            product.image = validated_data['image']
        
        # edit description
        if 'description' in validated_data:
            product.description = validated_data['description']
        
        # edit price
        if 'price' in validated_data:
            product.price = validated_data['price']
        serializer = self.serializer_class(product)
        return Response(serializer.data)
        
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

