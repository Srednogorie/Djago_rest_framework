from django.contrib.auth.models import User, Group
from rest_framework import serializers
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    ### Many different types of representation available ###
    # When queryset argument isn't presented the UserSerializer is looking to find 'related_name' somewere
    # in the models. In this case the Snippet model is containing an owner ForeignKey pointing to 'auth.User'
    # and with 'related_name=snippets'. If we change our variable name to something different than snippets it wont work

    # StringRelatedField may be used to represent the target of the relationship using its __unicode__ method.
    #snippets = serializers.StringRelatedField(many=True)
    # PrimaryKeyRelatedField may be used to represent the target of the relationship using its primary key.
    #snippets = serializers.PrimaryKeyRelatedField(queryset=Snippet.objects.all(), many=True)
    # HyperlinkedRelatedField may be used to represent the target of the relationship using a hyperlink.
    # The HyperlinkedRelatedField and the HyperlinkedModelSerializer both require 'view_name'. It needs to be
    # detail view so it can get the object properties.
    snippets = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='snippet-detail')
    # SlugRelatedField may be used to represent the target of the relationship using a field on the target.
    #snippets = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    # Nested relationships can be expressed by using serializers as fields.
    #snippets = SnippetSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'email', 'groups', 'snippets')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')