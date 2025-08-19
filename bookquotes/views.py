from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import ContactRequest
from .serializers import ContactRequestSerializer

from .models import QuoteRequest, Todo
from .serializers import QuoteRequestSerializer, TodoSerializer, UserSerializer


# ---------------- AUTH VIEWS ----------------
DEFAULT_ADMIN_USERNAME = "adminuser"
DEFAULT_ADMIN_PASSWORD = "Admin@123"


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username != DEFAULT_ADMIN_USERNAME or password != DEFAULT_ADMIN_PASSWORD:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)

        user, created = User.objects.get_or_create(username=DEFAULT_ADMIN_USERNAME)
        if created:
            user.set_password(DEFAULT_ADMIN_PASSWORD)
            user.save()

        # Generate tokens
        request.data['username'] = DEFAULT_ADMIN_USERNAME
        request.data['password'] = DEFAULT_ADMIN_PASSWORD
        response = super().post(request, *args, **kwargs)

        tokens = response.data
        access_token = tokens['access']
        refresh_token = tokens['refresh']

        res = Response({'success': True, **tokens})
        res.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite="None",
            path='/'
        )
        res.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=False,
            samesite="None",
            path='/'
        )
        return res


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({'refreshed': False, 'error': 'No refresh token'}, status=400)

            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)

            tokens = response.data
            access_token = tokens['access']

            res = Response({'refreshed': True, **tokens})
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/'
            )
            return res
        except Exception as e:
            return Response({'refreshed': False, 'error': str(e)}, status=400)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todos(request):
    todos = Todo.objects.filter(owner=request.user)
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    res = Response({'success': True})
    res.delete_cookie('access_token', path='/', samesite='Lax')
    res.delete_cookie('refresh_token', path='/', samesite='Lax')
    return res


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_logged_in(request):
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data)


# ---------------- QUOTE VIEWS ----------------
@api_view(['POST'])
@permission_classes([AllowAny])
def submit_quote(request):
    """
    Submit a new quote. Public API.
    Returns a sample PDF link for download.
    """
    serializer = QuoteRequestSerializer(data=request.data)
    if serializer.is_valid():
        quote = serializer.save()

        # Serve a sample PDF for now
        pdf_url = '/media/quotes/sample_quote.pdf'

        return Response({
            'message': 'Quote submitted successfully!',
            'pdf_url': pdf_url,
            'quote': QuoteRequestSerializer(quote).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_all_quotes(request):
    quotes = QuoteRequest.objects.all().order_by('-submitted_at')
    serializer = QuoteRequestSerializer(quotes, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_quote(request, quote_id):
    try:
        quote = QuoteRequest.objects.get(id=quote_id)
        quote.delete()
        return Response({'message': 'Quote deleted successfully'}, status=200)
    except QuoteRequest.DoesNotExist:
        return Response({'error': 'Quote not found'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_quotes(request):
    QuoteRequest.objects.all().delete()
    return Response({'message': 'All quotes deleted successfully'}, status=200)


# ✅ Submit new contact form
@api_view(['POST'])
@permission_classes([AllowAny]) 
def submit_contact(request):
    serializer = ContactRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Contact submitted successfully"}, status=201)
    return Response(serializer.errors, status=400)

# ✅ Get all contacts (Admin only)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_contacts(request):
    contacts = ContactRequest.objects.all().order_by('-submitted_at')
    serializer = ContactRequestSerializer(contacts, many=True)
    return Response(serializer.data)

# ✅ Delete a single contact
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_contact(request, contact_id):
    try:
        contact = ContactRequest.objects.get(id=contact_id)
        contact.delete()
        return Response({"message": "Contact deleted successfully"}, status=200)
    except ContactRequest.DoesNotExist:
        return Response({"error": "Contact not found"}, status=404)

# ✅ Delete all contacts
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_contacts(request):
    ContactRequest.objects.all().delete()
    return Response({"message": "All contacts deleted successfully"}, status=200)

