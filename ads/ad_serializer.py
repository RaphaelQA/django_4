from rest_framework import serializers

from ads.models import User, Ad, Category
from ads.user_serializers import UserDetailSerializer


class AdListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()

    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()

    )

    class Meta:
        model = Ad
        exclude = ['description']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer()

    class Meta:
        model = Ad
        fields = '__all__'


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        exclude = ['address', 'is_published']

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        ad.save()
        return ad


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        exclude = ['address', 'is_published']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.address = validated_data.get('address', instance.address)
        instance.image = validated_data.get('image', instance.image)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance




class AdDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']
