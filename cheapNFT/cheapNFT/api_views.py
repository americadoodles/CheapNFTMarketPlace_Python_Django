from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import AuctionSerializer, AuctionListingSerializer, AuctionBidSerializer
from .models import Auction
from .utils.web3 import check_nft_ownable, check_nft_approvement, check_bidder_sig, check_token_allowance

@api_view(['GET', 'POST'])
def test(request):
    return Response("Ok!!!")


@api_view(['GET'])
def list(request):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 10

    pageInfo = AuctionListingSerializer(data=request.data)
    context = {'request', request}
    if pageInfo.is_valid():
        auctions = Auction.objects.all()
        result_page = paginator.paginate_queryset(auctions, request)
        serializers = AuctionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializers.data)


@api_view(['GET'])
def retrieve(request, pk):
    try:
        auctions = Auction.objects.get(id=pk)
        serializer = AuctionSerializer(auctions)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        raise NotFound("Auction object does not exist!!!")


@api_view(['POST'])
def create(request):
    serializer = AuctionSerializer(data=request.data)
    if serializer.is_valid():
        print(request.data['collection'])
        auctions = Auction.objects.filter(collection=request.data['collection'], token_id=request.data['token_id']).first()
        if auctions is not None:
            raise ValidationError("Auction object is already exist!!!")
        if check_nft_ownable(request.data['collection'], request.data['token_id'], request.data['creator']) is False:
            raise ValidationError("Creator is not owner of this NFT!!!")
        if check_nft_approvement(request.data['collection'], request.data['token_id'], request.data['creator']) is False:
            raise ValidationError("Creator should approve NFT to create auction!!!")
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def bid(request, pk):
    bidSerializer = AuctionBidSerializer(data=request.data)
    if bidSerializer.is_valid():
        try:
            amount = int(request.data['amount'])
            bidder_sig = request.data['bidder_sig']
            auction = Auction.objects.get(id=pk)
            serializer = AuctionSerializer(auction, data=request.data)
            if auction.amount is not None:
                if auction.amount >= amount:
                    raise ValidationError("Underpriced amount!!!")
            if check_nft_ownable(auction.collection, auction.token_id, auction.creator) is False or check_nft_approvement(auction.collection, auction.token_id, auction.creator) is False:
                raise ValidationError("Auction already finished!!!")
            bidder = check_bidder_sig(auction.collection, auction.payment_token, auction.token_id, amount, bidder_sig)
            if check_token_allowance(auction.payment_token, amount, bidder) is False:
                raise ValidationError("Invalid signature or insufficient payment token allowance!!!")
            serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
            raise NotFound("Can't find such auction!!!")
        except Exception:
            raise ValidationError("Invalid parameter!!!")
    return Response(bidSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
