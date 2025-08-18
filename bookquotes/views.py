from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import QuoteRequest
from .serializers import QuoteRequestSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Todo
from .serializers import TodoSerializer, UserSerializer





# Set default admin credentials here
DEFAULT_ADMIN_USERNAME = "adminuser"
DEFAULT_ADMIN_PASSWORD = "Admin@123"

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if username != DEFAULT_ADMIN_USERNAME or password != DEFAULT_ADMIN_PASSWORD:
            return Response({'success': False, 'error': 'Invalid credentials'}, status=401)

        # Authenticate the default admin user (create if not exists)
        user, created = User.objects.get_or_create(username=DEFAULT_ADMIN_USERNAME)
        if created:
            user.set_password(DEFAULT_ADMIN_PASSWORD)
            user.save()

        # Generate tokens using super
        request.data['username'] = DEFAULT_ADMIN_USERNAME
        request.data['password'] = DEFAULT_ADMIN_PASSWORD
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        access_token = tokens['access']
        refresh_token = tokens['refresh']

        serializer = UserSerializer(user, many=False)

        res = Response()
        res.data = {'success': True}
        res.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            secure=True,
            samesite='None',
            path='/'
        )
        res.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=True,
            samesite='None',
            path='/'
        )
        res.data.update(tokens)
        return res

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

            res = Response()
            res.data = {'refreshed': True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='None',
                path='/'
            )
            return res
        except Exception as e:
            print(e)
            return Response({'refreshed': False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        res = Response()
        res.data = {'success': True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res
    except Exception as e:
        print(e)
        return Response({'success': False})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todos(request):
    user = request.user
    todos = Todo.objects.filter(owner=user)
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_logged_in(request):
    serializer = UserSerializer(request.user, many=False)
    return Response(serializer.data)









@api_view(['POST'])
def submit_quote(request):
    serializer = QuoteRequestSerializer(data=request.data)
    if serializer.is_valid():
        quote = serializer.save()  # Save instance and keep reference
        pdf_url = '/media/quotes/sample_quote.pdf'

        return Response({
            'message': 'Quote submitted successfully!',
            'pdf_url': pdf_url,
            'quote': QuoteRequestSerializer(quote).data 
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_all_quotes(request):
    quotes = QuoteRequest.objects.all().order_by('-submitted_at')
    serializer = QuoteRequestSerializer(quotes, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_quote(request, quote_id):
    try:
        quote = QuoteRequest.objects.get(id=quote_id)
        quote.delete()
        return Response({'message': 'Quote deleted successfully'}, status=status.HTTP_200_OK)
    except QuoteRequest.DoesNotExist:
        return Response({'error': 'Quote not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_all_quotes(request):
    QuoteRequest.objects.all().delete()
    return Response({'message': 'All quotes deleted successfully'}, status=status.HTTP_200_OK)
