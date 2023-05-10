"""
This module contains several function based views for the booking app.
function:list_ticket_classes_by_event: A FBV thst Return a list of all ticket classes for a given event.
function:check_promo_code: A FBV Check whether a promo code is valid for a given event.
function:create_order: A FBV that create order with its order items and Return the data saved.
function:confirm_order: a FBV that confirms the order by the sent token to user's email.
function:list_orders_by_user : a FBV that returns orders by user id.
function:list_orderitem_by_order : a FBV that return order items in an order by order id.
function:list_orderitem_by_user : a FBV that returns order items by user id.
"""
# class:discount_list: A view that returns a list of all discounts or creates a new discount.
# class:discount_pk: A view that returns a discounts object or update a new discount or delete it.

import itsdangerous
import requests
from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.http import Http404
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import generics, filters, status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from event.serializers import eventSerializer
from .models import *
from event.models import event as Event
from user.models import User
from eventbrite.settings import *
from rest_framework.authtoken.models import Token
from user.authentication import CustomTokenAuthentication
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from django.urls import reverse
from django.core.signing import TimestampSigner
from eventbrite.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


from django.utils import timezone
from django.http import QueryDict


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def list_ticket_classes_by_event(request, event_id):
    """
    Return a list of all ticket class for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A list of JSON objects representing the bookings for the given event.
    """

    # get all bookings for this event
    ticket_classes = TicketClass.objects.filter(event_id=event_id)
    serialized_Ticket_classes = TicketClassSerializer(
        ticket_classes, many=True)

    # return the data as a  list of JSON objects
    return Response(serialized_Ticket_classes.data)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def check_promocode(request, event_id):
    """
    Check whether a promocode is valid for a given event.

    :param request: HTTP request object.
    :param event_id: Event ID.
    :return: A JSON object indicating whether the promo code is valid.
    """
    print("start check promocode")
    print(request.query_params)
    try:
        promocode = request.query_params['promocode']
    except:
        return Response({"err": "missing promocode param"}, status=status.HTTP_400_BAD_REQUEST)
    print("promocode param found")

    now = timezone.now()
    print(now)

    discount = Discount.objects.filter(
        EVENT_ID=event_id, CODE=promocode).first()
    if not discount:
        return Response({'is_valid_promocode': False, "details": "not found"}, status=status.HTTP_200_OK)
    print("discount was found")

    if discount.Quantity_available is not None and discount.Quantity_available <= 0:
        return Response({'is_valid_promocode': False, "details": "quantity available = 0"}, status=status.HTTP_200_OK)
    print("availble quantity was found")

    if discount.Ends == 'scheduled' and discount.end_date is not None and discount.end_time is not None:
        if str(now.date()) > discount.end_date or (str(now.date()) == discount.end_date and str(now.time())[0:8] >= discount.end_time):
            return Response({'is_valid_promocode': False, "details": "promocode has expired"}, status=status.HTTP_200_OK)
    # print(now.date())
    # print(discount.end_date)
    # print(str(now.date()) > discount.end_date)

    # print(str(now.time())[0:8])
    # print(discount.end_time)
    # print(str(now.time())[0:8] >= discount.end_time)
    print("hasnt expired yet")

    serialized_discount = DiscountSerializer(discount)
    # print(serialized_discount)
    return Response({'is_valid_promocode': True, "discount": serialized_discount.data}, status=status.HTTP_200_OK)


# fees
@api_view(['POST'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request, event_id):
    """
    This view creates an order for an event with the specified event ID.
    user ID are received in the request data. A discount code may also be included.
    request data should look like this

        {
            "order_items":
            [
                {
                "ticket_class_id" : 1,	
                "quantity": 3 
                },
                {
                "ticket_class_id" : 2,	
                "quantity": 1 
                }
            ], 
            "promocode" : "DISCOUNT25" // optional

        }
    """
    # validate data

    # check sent event_id
    if not event.objects.filter(ID=event_id):
        return Response({"details": "no event exist with this ID"}, status=status.HTTP_400_BAD_REQUEST)
    # check if a promocode was sent and validate it
    promocode = request.data.get('promocode')
    if promocode:
        now = timezone.now()
        discount = Discount.objects.filter(
            EVENT_ID=event_id, CODE=promocode).first()
        if not discount:
            return Response({'is_valid_promocode': False, "details": "not found"}, status=status.HTTP_200_OK)
        if discount.Quantity_available is not None and discount.Quantity_available <= 0:
            return Response({'is_valid_promocode': False, "details": "quantity available = 0"}, status=status.HTTP_200_OK)
        if discount.Ends == 'scheduled' and discount.end_date is not None and discount.end_time is not None:
            if str(now.date()) > discount.end_date or (str(now.date()) == discount.end_date and str(now.time())[0:8] >= discount.end_time):
                return Response({'is_valid_promocode': False, "details": "promocode has expired"}, status=status.HTTP_200_OK)

    # get user data
    user_id = request.data.get('user_id')
    if not user_id:
        user_id = request.user.id
        print("user_id was got from the request ")

    # get order_items
    order_items = request.data.get('order_items')
    data = request.data
    print(data)
    if not order_items:
        return Response({"details": " no order_items list of object was sent"}, status=status.HTTP_400_BAD_REQUEST)

    # create empty order so that orderitem can point to it
    order = Order(user_id=request.user.id)
    # order.save()
    print("-------1--------")

    # for Calculate the order
    subtotal = 0.0
    amount_off = 0.0
    print("--------2-------")

    for item in order_items:

        item['order_id'] = order.ID
        try:
            item['ticket_price'] = TicketClass.objects.get(
                ID=item["ticket_class_id"]).PRICE
        except:
            ticket_class_id = item["ticket_class_id"]
            return Response({"details": f"no ticket class with this id. ticket_class_id = { ticket_class_id}"}, status=status.HTTP_400_BAD_REQUEST)

        item['user_id'] = user_id
        item['event_id'] = event_id
        print(item)

        order_item_serializer = OrderItemSerializer(data=item)
        if not order_item_serializer.is_valid():
            return Response({"details": f"order item serializer wasnt able to validate the data  {order_item_serializer.error_messages}"}, status=status.HTTP_400_BAD_REQUEST)
        order_item = order_item_serializer.save()
        print(order_item_serializer.is_valid())

        print("-----3----------")

        ticket_class = TicketClass.objects.get(
            ID=order_item_serializer.instance.ticket_class_id)

        print(ticket_class.PRICE)
        quantity = order_item_serializer.instance.quantity
        print(quantity)

        if int(ticket_class.capacity) - int(ticket_class.quantity_sold) < quantity:
            order.delete()
            # order_item.delete()
            return Response({"details": f"Not enough tickets available for ticket class id {order_item_serializer.instance.ticket_class_id}"}, status=status.HTTP_400_BAD_REQUEST)

        subtotal += ticket_class.PRICE * quantity

        # update ticket quantity sold
        quantity_sold_updated = int(ticket_class.quantity_sold) + quantity
        TicketClass.objects.filter(ID=ticket_class.ID).update(
            quantity_sold=str(quantity_sold_updated))

    # handel discount if a promocode was sent
    if promocode:
        order.discount_id = discount.ID
        amount_off = float(discount.Discountـpercentage)/100 * subtotal

        # decrement Quantity_available of the used promocode
        Quantity_available_updated = int(discount.Quantity_available) - 1
        Discount.objects.filter(ID=discount.ID).update(
            Quantity_available=str(Quantity_available_updated))

        print(discount.Discountـpercentage)
        print(type(discount.Discountـpercentage))

    fee = 0
    total = subtotal - amount_off + fee

    # Create the response
    order_response = {
        'tickets': order_items,
        'full_price': subtotal,
        'amount_off': amount_off,
        'fee': fee,
        'total': total
    }
    order.full_price = subtotal
    order.amount_off = amount_off
    order.total = total
    order.event_id = event_id
    order.fee = fee
    order.save()

    # send_confirmation_email(request._request,order)
    return Response(order_response, status=status.HTTP_201_CREATED)


def send_confirmation_email(request, order):
    """ 
    This function should construct the url with a token and send the link by mail to the user 
    """

    print("======confirmation mail=======")
    user = request.user

    # Generate a confirmation token
    signer = TimestampSigner()
    token = signer.sign(str(order.ID))
    # token = generate_confirmation_token(order.id)

    print(token)

    confirmation_url = request.build_absolute_uri(
        reverse('confirm-order', args=[token]))

    print("======1=======")

    # Build the confirmation URL
    # confirmation_url = request.build_absolute_uri(
    #     reverse('create-booking'))  # , args=[token]))

    # token, created = Token.objects.get_or_create(user=user)
    # confirmation_url = 'google.com'
    # confirmation_url = f"https://example.com/confirm-email/?token={token.key}"

    # Generate a QR code for the confirmation URL using the Google Charts API
    qr_code_url = f'https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={confirmation_url}'
    qr_code_image = requests.get(qr_code_url).content
    print("======2=======")

    # Send the confirmation email
    subject = 'Confirm your email address'
    message = f'Hi {user.first_name}, please click the link below or scan the QR code to confirm your booking:\n\n {confirmation_url} \n\n'
    from_email = 'no-reply@example.com'
    recipient_list = [user.email]
    print(recipient_list)
    mail = EmailMessage(subject, message, from_email,
                        recipient_list)
    print(EMAIL_HOST_USER)
    send_mail(subject=subject, message=message,
              from_email=from_email,
              fail_silently=False,
              recipient_list=recipient_list)
    print("======3=======")

    # ,content_type='image/png'
    mail.attach(filename='qrcode.png', content=qr_code_image)
    mail.send()
    # send_mail(message=mail, subject=subject,from_email=from_email,recipient_list=recipient_list , html_message=f'<p>{message}</p><img src="cid:qrcode">', fail_silently=False)
    # Render a response
    print("====== end of function =======")

    return Response({'status': 201}, status=201)


@api_view(['GET'])
def confirm_order(request, token):
    """
    This function confirms an order by taking a token as input and 
    returning a response indicating whether the order has been validated. 
    The token is used to retrieve the order ID, 
    which is then used to update the order object's is_validated field to True. 
    The function returns a response with the value of is_validated as True and a status code of 200 if successful.
    """

    print("=-=-=-=-= start confirm order==-=--=---=")

    signer = TimestampSigner()
    try:
        order_id = signer.unsign(token, max_age=86400)  # 86400 seconds = 1 day
    except signer.BadSignature:
        return Response({'details': 'Invalid token'})

    print("=-=-=-=-= mid confirm order==-=--=---=")
    print(id)
    order = Order.objects.get(ID=order_id)
    order.is_validated = True
    Order.objects.filter(ID=order_id).update(is_validated='True')

    # order.save()
    print("=-=-=-=-= end confirm order==-=--=---=")

    return Response({"is_validated": True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def list_orders_by_user(request, user_id):
    """
    Return a list of all orders for a given user.

    :param request: HTTP request object.
    :param user_id: User ID.
    :return: A list of JSON objects representing the bookings for the given user.
    """
    orders = Order.objects.filter(user_id=user_id)
    serialized_orders = OrderSerializer(orders, many=True)
    return Response(serialized_orders.data)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def list_orderitem_by_order(request, order_id):
    """

    """
    order_items = OrderItem.objects.filter(order_id=order_id)
    serialized_orderitems = OrderItemSerializer(order_items, many=True)
    return Response(serialized_orderitems.data)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def list_orderitem_by_user(request, user_id):
    """
    This function takes a user_id as input and returns a list of OrderItem objects
    associated with the given user. 
    It uses the OrderItemSerializer to serialize the data before returning it in the response.
    """
    order_items = OrderItem.objects.filter(user_id=user_id)
    serialized_orderitems = OrderItemSerializer(order_items, many=True)
    return Response(serialized_orderitems.data)


@api_view(['GET'])
@authentication_classes([CustomTokenAuthentication])
@permission_classes([IsAuthenticated])
def quantity_sold_out_of_total(request, event_id):
    """
    A view function that returns the ticket classes ids in an event associated with how many tickets were sold out of the total.
    It uses the TicketQuantityClassSerializer to serialize the data before returning it in the response.
    """
    try:
        Event = event.objects.get(ID=event_id)
        print(request.user.id)
    except event.DoesNotExist:
        return Response({'error': f'Event with id {event_id} does not exist.'}, status=HTTP_400_BAD_REQUEST)

    if str(request.user.id) != str(Event.User_id):
        return Response({'error': 'You are not authorized to create a ticket for this event.'}, status=HTTP_401_UNAUTHORIZED)
    ticket_classes = TicketClass.objects.filter(event_id=event_id)
    serialized_Ticket_classes = TicketQuantityClassSerializer(
        ticket_classes, many=True)
    return Response(serialized_Ticket_classes.data)
