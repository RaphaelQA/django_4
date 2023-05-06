import location as location
from rest_framework import serializers

from ads.models import User, Location


class UserListSerializer(serializers.ModelSerializer):
    total_ads = serializers.IntegerField()
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',

    )

    class Meta:
        model = User
        fields = ['id', 'total_ads', 'first_name', 'last_name', 'username', 'role', 'age', 'locations']


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',

    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'role', 'age', 'locations']


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self.locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for loc_name in self.locations:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.locations.add(loc)
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'password', 'role', 'username', 'age', 'locations']


    def is_valid(self, raise_exception=False):
        self.locations = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def save(self):
        user = super().save()
        if self.locations:
            user.locations.clear()
            for loc_name in self.locations:
                loc, _ = Location.objects.get_or_create(name=loc_name)
                user.locations.add(loc)

        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
