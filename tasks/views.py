# tasks/views.py
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from rest_framework.response import Response
from rest_framework import status

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.completed = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
