from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import QuoteRequest
from .serializers import QuoteRequestSerializer

@api_view(['POST'])
def submit_quote(request):
    serializer = QuoteRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        pdf_url = '/media/quotes/sample_quote.pdf'

        return Response({
            'message': 'Quote submitted successfully!',
            'pdf_url': pdf_url
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
