from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ads.models import Category


class CatListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CatDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CatDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CatCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

class CatUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
