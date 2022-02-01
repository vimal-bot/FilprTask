from rest_framework.decorators import api_view
from rest_framework.response import Response

from ttest.models import Customer, Order, Shipping

@api_view(['POST'])
def customer_view(request):
    if request.method == 'POST':
        customer_data = request.data
        customer_name = customer_data['name']
        customer_city = customer_data['city']
        customer_phone = customer_data['phone']
        customer_email = customer_data['email']
        customer = Customer(name=customer_name, city=customer_city, phone=customer_phone, email=customer_email)
        customer.save()
        return Response(customer_data)

@api_view(['POST'])
def order(request):
    if request.method == 'POST':
        purchase_data = request.data
        customer_id = purchase_data['customer_id']
        product_name = purchase_data['product_name']
        quantity = purchase_data['quantity']
        price = purchase_data['price']
        mrp = purchase_data['mrp']
        customer = Customer.objects.get(id=customer_id)
        order = Order(product_name=product_name, customer=customer, quantity=quantity, price=price, mrp=mrp)
        order.save()
        return Response(purchase_data)

@api_view(['POST'])
def shipping(request):
    if request.method == 'POST':
        shipping_data = request.data
        order_id = shipping_data['order_id']
        address = shipping_data['address']
        city = shipping_data['city']
        pin = shipping_data['pin']
        order = Order.objects.get(id=order_id)
        shipping = Shipping(address=address, city=city, pin=pin, order=order, customer=order.customer)
        shipping.save()
        return Response(shipping_data)

@api_view(['GET'])
def get_customers_shipping_by_city(request):
    if request.method == 'GET':
        city = request.GET.get('city')
        customers_ids = Customer.objects.filter(city=city).values_list('id', flat=True)
        shipping_data = Shipping.objects.filter(customer_id__in=customers_ids).values()
        return Response(shipping_data)

@api_view(['GET'])
def get_all_orders_by_all_customers(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        res = []
        for customer in customers:
            orders = Order.objects.filter(customer=customer)
            res.append({
                'customerId': customer.id,
                'name': customer.name,
                'city': customer.city,
                'phone': customer.phone,
                'email': customer.email,
                'orders': [{
                    'orderId': order.id,
                    'product_name': order.product_name,
                    'quantity': order.quantity,
                    'price': order.price,
                    'mrp': order.mrp,
                } for order in orders]
            })
        return Response(res)

@api_view(['GET'])
def get_all(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        res = []
        for customer in customers:
            tmp = {
                'customerId': customer.id,
                'name': customer.name,
                'city': customer.city,
                'phone': customer.phone,
                'email': customer.email,
            }

            orders = Order.objects.filter(customer=customer)
            for order in orders:
                shipping_data = Shipping.objects.filter(order=order).last()
                tmp['orders'] = [{
                    'orderId': order.id,
                    'product_name': order.product_name,
                    'quantity': order.quantity,
                    'price': order.price,
                    'mrp': order.mrp,
                    'shippingDetails': {
                        'address': shipping_data.address,
                        'city': shipping_data.city,
                        'pin': shipping_data.pin,
                    }
                }]
                res.append(tmp)
        return Response(res)
            