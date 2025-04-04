from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer

def book_list_view(request):
    books = Book.objects.all()
    return render(request, 'books_list.html', {'books': books})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request):
        """Create a new book"""
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error": "A book with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Update an existing book"""
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        """Partially update a book"""
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Get book by ID"""
        book = Book.objects.filter(pk=pk).first()
        if not book:
            return Response({"message": "No Data"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_by_title(self, request):
        """Get books by title"""
        title = request.query_params.get('title', None)
        if not title:
            return Response({'error': 'Title parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        books = Book.objects.filter(title__icontains=title)
        if not books.exists():
            return Response({"message": "No Data"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_by_author(self, request):
        """Get books by author"""
        author = request.query_params.get('author', None)
        if not author:
            return Response({'error': 'Author parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(author__icontains=author)
        if not books.exists():
            return Response({"message": "No Data"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_by_price(self, request):
        """Get books by price"""
        price = request.query_params.get('price', None)
        if not price:
            return Response({'error': 'Price parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            price = float(price)
        except ValueError:
            return Response({'error': 'Price must be a valid number'}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(price=price)
        if not books.exists():
            return Response({"message": "No Data"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def get_by_genre(self, request):
        """Get books by genre"""
        genre = request.query_params.get('genre', None)
        if not genre:
            return Response({'error': 'Genre parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(genre__icontains=genre)
        if not books.exists():
            return Response({"message": "No Data"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
