from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from artical.models import Author,Artical
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from django.contrib.auth.models import User
from artical.serializers import ArticalSerializer ,LogInSerializer,UserSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import TokenAuthentication

# Create your views here.


class ArticalView(APIView):
   
    def get(self,request,*args, **kwargs):
        articals=Artical.objects.all()
        serializer=ArticalSerializer(articals,many=True)
        return Response({"articals": serializer.data})
    
    def post(self,request):
        artical = request.data.get('artical')
        #create a artical from above data
        serializer=ArticalSerializer(data=artical)

        if serializer.is_valid(raise_exception=True):
            article_saved=serializer.save()
        return Response({"success": "Article '{}' created successfully".format(article_saved.title)})
        
    def put(self,request,pk):
        saved_data=get_object_or_404(Artical.objects.all(),pk=pk)
        data=request.data.get('artical')
        serializer=ArticalSerializer(instance=saved_data,data=data,partial=True)
        
        if serializer.is_valid(raise_exception=True):
            article_saved=serializer.save()
        return Response({"Success":"Article '{}' updated successfully".format(article_saved.title)})

    
    def delete(self,request,pk):
        #get the article with this pk
        article=get_object_or_404(Artical.objects.all(),pk=pk)
        article.delete()
        return Response({"message": "Artical with '{}' id deleted successfully".format(pk)},status=204)


       
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from rest_framework.authtoken.models import Token   
from rest_framework.authentication import TokenAuthentication     
class LogInView(APIView):

    def post(self,request):
        serializer=LogInSerializer(data=request.data)
        #if serailizer is valid then processed else raise exception then return to user directly
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        django_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"token":token.key},status=200)

    

class LogOutView(APIView):
    authentication_classes=(TokenAuthentication,)
    
    def post(self,request):
        django_logout(request)
        return Response(status=204)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer



class Register(APIView):
    def get(self,request):
        return Response({'Error':'No data in get call'})


    def post(self,request):
        serializer=UserSerializer(data=request.data,context={'request':request})
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            
            return Response({'Credential': {'username' : request.data.get('username'), 'password' : request.data.get('password')}})
        return Response({'Error':serializer.errors})
