from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics

from .models import BlockCateInfo, BlockInfo, MpoolCateInfo, MpoolInfo
from .serializers import BlockCateSerializer, BlockSerializer, MpoolCateSerializer, MpoolSerializer

class Blockview(APIView):
    """
    Blockview
    """

    def get(self, request):
        """
        block view get method
        """

        q_set = BlockInfo.objects.all()
        s_set = BlockSerializer(instance=q_set, many=True)
        return Response(s_set.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        block view post method
        """

        s_set = BlockSerializer(data=request.data)
        if s_set.is_valid():
            s_set.save()
            return Response(data=s_set.data, status=status.HTTP_201_CREATED)
        return Response(data=s_set.errors, status=status.HTTP_400_BAD_REQUEST)

class BlockDeleteView(generics.DestroyAPIView):
    """
    BlockDeleteView
    """
    queryset = BlockInfo.objects.all()
    serializer_class = BlockSerializer

class  BlockCateView(generics.ListCreateAPIView):
    """
    BlockCateView
    """

    queryset = BlockCateInfo.objects.all()
    serializer_class = BlockCateSerializer

class Mpoolview(generics.ListCreateAPIView):
    """
    Mpoolview
    """

    queryset = MpoolInfo.objects.all()
    serializer_class = MpoolSerializer

class  MpoolCateView(generics.ListCreateAPIView):
    """
    MpoolCateView
    """
    
    queryset = MpoolCateInfo.objects.all()
    serializer_class = MpoolCateSerializer
    