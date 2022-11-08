from store.models import Product
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','selling_price','discounted_price','brand','Category','product_image']

