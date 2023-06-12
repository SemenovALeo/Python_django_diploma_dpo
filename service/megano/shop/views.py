from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Product, Category


# Create your views here.
class productsPopular(APIView):
    def get(self, request: Request, category_slug=None) -> Response:
        products = Product.objects.get(available=True)

        print(products.__dict__)

        data = [
            {
                "id": products.id,
                "category": products.category_id,
                "price": products.price,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": products.name,
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                    {
                        "src": products.image.url,
                        "alt": "hello alt",
                    }
                ],
                # "tags": [
                #     {
                #         "id": 0,
                #         "name": "Hello world"
                #     }
                # ],
                "reviews": 5,
                "rating": 4.6
            }
        ]

        return Response(data)
