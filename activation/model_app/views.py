from rest_framework.views import APIView
from .serializer import Model, ModelSerial
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class ModelView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        post = Model.objects.all()
        serialized = ModelSerial(post, many=True)
        return Response(data = serialized.data, status = 200)
    
    def post(self, request):
        serializer = ModelSerial(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'details' : 'Changes saved Successfully.'})
        return Response({'details':'unexpected error occured or data is invalid.'})


