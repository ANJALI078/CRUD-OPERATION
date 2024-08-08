from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from Home.models import Entry
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Entry
from .serializers import EntrySerializer

# Create your views here.
def home(request):
    return render(request,"home.html")

def show(request):
    data = Entry.objects.all()
    return render(request,"show.html",{'data':data})

def send(request):
    if request.method == 'POST':
        ID = request.POST['id']
        data1 = request.POST['data1']
        data2 = request.POST['data2']
        Entry(ID = ID, data1 = data1, data2 = data2).save()
        msg = "Data store Successfully"
        return render(request,"home.html",{'msg':msg})
    else:
        return HttpResponse("<h1>404 - Not Found</h1>")


def delete(request):
    ID = request.GET['id']
    Entry.objects.filter(ID = ID).delete()
    return HttpResponseRedirect("show")

def edit(request):
    ID = request.GET['id']
    data1 = data2 = "Not Available"
    for data in Entry.objects.filter(ID=ID):
        data1 = data.data1
        data2 = data.data2
    return render(request,"edit.html",{'ID':ID,'data1':data1,'data2':data2})

def RecordEdited(request):
    if request.method == 'POST':
        ID = request.POST['id']
        data1 = request.POST['data1']
        data2 = request.POST['data2']
        Entry.objects.filter(ID=ID).update(data1=data1,data2=data2)
        return HttpResponseRedirect("show")
    else:
        return HttpResponse("<h1>404 - Not Found</h1>")
    

    # views.py



class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 201,
                'data': serializer.data,
                'message': 'Data stored successfully'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 400,
            'errors': serializer.errors,
            'message': 'Invalid data'
        }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'data': serializer.data,
                'message': 'Data updated successfully'
            })
        return Response({
            'status': 400,
            'errors': serializer.errors,
            'message': 'Invalid data'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'status': 204,
            'message': 'Data deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
