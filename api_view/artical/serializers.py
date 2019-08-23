from rest_framework import serializers
from artical.models import Artical
from rest_framework import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class ArticalSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=200)
    description=serializers.CharField()
    body=serializers.CharField()
    author_id=serializers.IntegerField()

    def create(self,validated_data):
        return Artical.objects.create(**validated_data)


    def update(self,instance,validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.description=validated_data.get('description',instance.description)
        instance.body=validated_data.get('body',instance.body)
        instance.author_id=validated_data.get('author_id',instance.author_id)
        instance.save()
        return instance


class LogInSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):
        username=data.get('username')
        password=data.get('password')

        if username and password :
            #if username and password is available then chack user is authenticate or note
            user=authenticate(username=username,password=password)
            # user is active then login proceed
            if user:
                if user.is_active:
                    data["user"]=user
                else:
                    msg="user is deactivated"
                    raise exceptions.ValidationError(msg)
            else:
                msg="Unable to login with given credentail"
                raise exceptions.ValidationError(msg)
        else:
            msg="Must Provide username and password"
            raise exceptions.ValidationError(msg)
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','password')
        write_only_fields=('password',)
        read_only_fields=('id',)

    def create(self, validated_data):
        user=User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user