from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product, Order


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.valid_product_data = {
            "name": "Laptop",
            "description": "A high-performance laptop.",
            "price": 1000.00,
            "stock": 50
        }

    def test_create_product_success(self):
        url = "/products/"
        response = self.client.post(url, self.valid_product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()
        self.assertEqual(product.name, self.valid_product_data["name"])

    def test_get_products(self):
        Product.objects.create(**self.valid_product_data)
        url = "/products/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.valid_product_data["name"])


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.product1 = Product.objects.create(
            name="Laptop", description="A high-performance laptop.", price=1000.00, stock=50
        )
        self.product2 = Product.objects.create(
            name="Mouse", description="A wireless mouse.", price=20.00, stock=100
        )

    def test_create_order_success(self):
        url = "/orders/"
        order_data = {
            "products": [
                {"product_id": self.product1.id, "quantity": 2},
                {"product_id": self.product2.id, "quantity": 5}
            ]
        }
        response = self.client.post(url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(float(response.data["total_price"]), 2100.00)

    def test_create_order_insufficient_stock(self):
        url = "/orders/"
        order_data = {
            "products": [
                {"product_id": self.product1.id, "quantity": 200}  # Exceeds stock
            ]
        }
        response = self.client.post(url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient stock", response.data[0])

    def test_create_order_invalid_product(self):
        url = "/orders/"
        order_data = {
            "products": [
                {"product_id": 999, "quantity": 1}  # Non-existent product
            ]
        }
        response = self.client.post(url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("does not exist", response.data[0])
