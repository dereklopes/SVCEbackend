from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from .models import User, Idea, Comment
from .serializers import IdeaSerializers, UserSerializers, CommnentSerializers
from django.http import HttpResponse
from rest_framework import generics
from filters import CommentFilter, UserFilter
from django_filters.rest_framework import DjangoFilterBackend




class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



#list all ideas
#ideas/
class IdeasList(generics.ListCreateAPIView):
    # list all ideas available

    queryset = Idea.objects.all()
    serializer_class = IdeaSerializers

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = IdeaSerializers(queryset, many=True)
        return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = IdeaSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


#comment/
#comment/?idea_id=..
class CommnentList(generics.ListCreateAPIView):
    # list all ideas available

    queryset = Comment.objects.all()
    serializer_class = CommnentSerializers
    filter_class = CommentFilter(generics.ListAPIView)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('ideaId' )  # filter the filed ideaId (in model)

    def get_queryset(self):
        queryset = Comment.objects.all()
        ideaid = self.request.query_params.get('idea_id', None)  #?idea_id=...
        if ideaid is not None:
            queryset = queryset.filter(ideaId=ideaid)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommnentSerializers(queryset, many=True)
        return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = CommnentSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


#user/
#user/?user_id=...
class UserList(generics.ListCreateAPIView):
    # list all ideas available

    queryset = User.objects.all()
    serializer_class = UserSerializers
    filter_class = UserFilter(generics.ListAPIView)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('userId')  # filter the filed userId (in model)

    def get_queryset(self):
        queryset = User.objects.all()
        userid = self.request.query_params.get('user_id', None)  # ?user_id=...
        if userid is not None:
            queryset = queryset.filter(userId=userid)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = UserSerializers(queryset, many=True)
        return JSONResponse(serializer.data)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = UserSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)