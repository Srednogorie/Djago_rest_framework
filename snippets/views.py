# Writing regular Django views using our Serializer
# Let's see how we can write some API views using our new Serializer class.
# For the moment we won't use any of REST framework's other features, we'll just write the views as regular Django views.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# The root of our API is going to be a view that supports listing all the existing snippets, or creating a new snippet.
"""
# PATERRN 1 - List - "GET", "POST"
@csrf_exempt
def snippet_list(request):
    # List all code snippets, or create a new snippet.
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
"""
# We'll also need a view which corresponds to an individual snippet, and can be used to retrieve,
# update or delete the snippet.
"""
# PATTERN 1 - Detail - "GET", "PUT", "DELETE"
@csrf_exempt
def snippet_detail(request, pk):
    # Retrieve, update or delete a code snippet.
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
"""
# It's worth noting that there are a couple of edge cases we're not dealing with properly at the moment.
# If we send malformed json, or if a request is made with a method that the view doesn't handle,
# then we'll end up with a 500 "server error" response. Still, this'll do for now.


# Wrapping API views
# REST framework provides two wrappers you can use to write API views.
#
# The @api_view decorator for working with function based views.
# The APIView class for working with class-based views.
# These wrappers provide a few bits of functionality such as making sure you receive Request instances in your view,
# and adding context to Response objects so that content negotiation can be performed.
#
# The wrappers also provide behaviour such as returning 405 Method Not Allowed responses when appropriate,
# and handling any ParseError exception that occurs when accessing request.data with malformed input.
"""
# PATTERN 2 - List - "GET", "POST"
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    # List all code snippets, or create a new snippet.
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
# Our instance view is an improvement over the previous example.
# It's a little more concise, and the code now feels very similar to if we were working with the Forms API.
# We're also using named status codes, which makes the response meanings more obvious.
#
# Here is the view for an individual snippet, in the views.py module.
"""
# PATTERN 2 - Detail - "GET", "PUT", "DELETE"
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    # Retrieve, update or delete a code snippet.
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
# This should all feel very familiar - it is not a lot different from working with regular Django views.
#
# Notice that we're no longer explicitly tying our requests or responses to a given content type.
# request.data can handle incoming json requests, but it can also handle other formats.
# Similarly we're returning response objects with data, but allowing REST framework to render the response into the
# correct content type for us.

######################################CLASS BASED VIEWS############################################################
# Class-based Views
# We can also write our API views using class-based views, rather than function based views.
# This is a powerful pattern that allows us to reuse common functionality, and helps us keep our code DRY.
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

"""
# PATTERN 3 - List - 'GET', 'POST'
class SnippetList(APIView):
    # List all snippets, or create a new snippet.
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""
# So far, so good. It looks pretty similar to the previous case, but we've got better separation between the
# different HTTP methods. We'll also need to update the instance view:

"""
# PATTERN 3 - Detail - 'GET', 'PUT', 'DELETE'
class SnippetDetail(APIView):
    # Retrieve, update or delete a snippet instance.
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
# That's looking good. Again, it's still pretty similar to the function based view right now.


# Using mixins
# One of the big wins of using class-based views is that it allows us to easily compose reusable bits of behaviour.
# The create/retrieve/update/delete operations that we've been using so far are going to be pretty similar for any
# model-backed API views we create. Those bits of common behaviour are implemented in REST framework's mixin classes.

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

"""
# PATTERN 4 - List - 'GET', 'POST'
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
"""
# We'll take a moment to examine exactly what's happening here. We're building our view using GenericAPIView,
# and adding in ListModelMixin and CreateModelMixin.
# The base class provides the core functionality, and the mixin classes provide the .list() and .create() actions.
# We're then explicitly binding the get and post methods to the appropriate actions. Simple enough stuff so far.

"""
# PATTERN 4 - Detail - 'GET', 'PUT', 'DETAIL'
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""
# Pretty similar. Again we're using the GenericAPIView class to provide the core functionality, and adding in mixins
# to provide the .retrieve(), .update() and .destroy() actions.


# Using generic class-based views
# Using the mixin classes we've rewritten the views to use slightly less code than before, but we can go one step further.
# REST framework provides a set of already mixed-in generic views that we can use to trim down our views.py
# module even more.


from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import generics
from rest_framework import permissions

# PATTERN 5 - List - 'GET', 'POST'
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # It can be overriden even hire.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        print('Sending email...')

# PATTERN 5 - Detail - 'GET', 'PUT', 'DETAIL'
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    # Or more sophisticated things ...
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print('Check something before deleting the instance...')
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


# Right now we have endpoints for 'snippets' and 'users', but we don't have a single entry point to our API.
# To create one, we'll use a regular function-based view and the @api_view decorator we introduced earlier.
# Two things should be noticed here. First, we're using REST framework's reverse function in order to return
# fully-qualified URLs; second, URL patterns are identified by convenience names that we will declare later
# on in our snippets/urls.py.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format)
    })


from rest_framework import renderers
from rest_framework.response import Response

# Creating an endpoint for the highlighted snippets
# The other obvious thing that's still missing from our pastebin API is the code highlighting endpoints.
# Unlike all our other API endpoints, we don't want to use JSON, but instead just present an HTML representation.
# There are two styles of HTML renderer provided by REST framework, one for dealing with HTML rendered using templates,
# the other for dealing with pre-rendered HTML. The second renderer is the one we'd like to use for this endpoint.
# The other thing we need to consider when creating the code highlight view is that there's no existing concrete generic
# view that we can use. We're not returning an object instance, but instead a property of an object instance.
# Instead of using a concrete generic view, we'll use the base class for representing instances,
# and create our own .get() method.
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
