from rest_framework import serializers
from .models import Auction

class AuctionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    creator = serializers.CharField(required=True, allow_blank=False, max_length=42)
    collection = serializers.CharField(required=True, allow_blank=False, max_length=42)
    token_id = serializers.IntegerField(required=True)
    payment_token = serializers.CharField(required=True, allow_blank=False, max_length=42)
    bidder_sig = serializers.CharField(required=False, allow_blank=True, max_length=132, default=None)
    amount = serializers.IntegerField(required=False, default=None)

    class Meta:
        model = Auction
        fields = '__all__'


class AuctionListingSerializer(serializers.Serializer):
    offset = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False)


class AuctionBidSerializer(serializers.Serializer):
    bidder_sig = serializers.CharField(required=True, max_length=132)
    amount = serializers.IntegerField(required=True)