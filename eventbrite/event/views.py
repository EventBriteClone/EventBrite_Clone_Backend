"""
This module contains several view classes for the events app.
class:EventCreateView: A viewset for creating an event instance.
class:AllEventListView: A viewset for retrieving all event instances.
class:EventSearchView: A viewset for searching event instances by title.
class:EventListtype: A viewset for retrieving event instances by type.
class:EventListCategory: A viewset for retrieving event instances by category.
class:EventListSupCategory: A viewset for retrieving event instances by sub-category.
class:EventListVenue: A viewset for retrieving event instances by venue.
class:OnlineEventsAPIView: A viewset for retrieving online event instances.
class:EventID: A viewset for retrieving event instances by ID.
class:UserInterestCreateAPIView: A viewset for creating an user Interests instance.
class:UserInterestAPIView: A viewset for retrive an user Interests instance.
class:UserInterestEventsAPIView: A viewset for retrieving event instances based on user Interests.
class:TodayEventsList: A viewset for retrieving event instances for today.
class:WeekendEventsView: A viewset for retrieving event instances for weekend.
class:TicketCreateAPIView: A viewset for create a new ticket for a given event
class:EventTicketPrice: A viewset for retrieve the ticket price for a given event.
"""
from event.forms import *
from django.db.models import Q
from django.shortcuts import render
from event.serializers import *
from user import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from event.models import event
from event.serializers import *
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.timezone import now
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from booking.models import *
from booking.serializers import *
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from booking.models import event, Ticket
from booking.serializers import TicketSerializer
import csv


class EventCreateView(generics.CreateAPIView):
    """
    A viewset for creating an event instance.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = eventSerializer
    queryset = event.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyPagination(PageNumberPagination):
    """
    A custom pagination class that extends the PageNumberPagination class.
    It sets the page size to 10 by default and overrides the get_paginated_response method to include some print statements and return the paginated response data.
    """
    page_size = 10
    def get_paginated_response(self, data):
        print(self.page)
        return super().get_paginated_response(data)


class AllEventListView(APIView):
    """
    A viewset for retrieving all event instances.
    """
    # permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def get(self, request, format=None):
        """
        This view should return a paginated list of all the events.
        """
        events = event.objects.all()
        paginator = self.pagination_class()
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = eventSerializer(paginated_events, many=True)
        response = paginator.get_paginated_response(serializer.data)
        response['count'] = paginator.page.paginator.count
        return response


class EventSearchView(generics.ListAPIView):
    """
    A viewset for searching event instances by title.
    """
    permission_classes = [IsAuthenticated]
    queryset = event.objects.all()
    serializer_class = eventSerializer

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the title specified in the URL parameter.
        """
        event_name = self.kwargs['event_name']
        return event.objects.filter(Title__icontains=event_name)


class EventListtype(generics.ListAPIView):
    """
    A viewset for retrieving event instances by type.
    """
    serializer_class = eventSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the type specified in the URL parameter.
        """
        event_type = self.kwargs['event_type']
        return event.objects.filter(type=event_type)


class EventListCategory(generics.ListAPIView):
    """
    A viewset for retrieving event instances by category.
    """
    serializer_class = eventSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the category specified in the URL parameter.
        """
        event_Category = self.kwargs['event_Category']
        return event.objects.filter(category_name=event_Category)


class EventListSupCategory(generics.ListAPIView):
    """
    A viewset for retrieving event instances by sub-category.
    """
    serializer_class = eventSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the sub-category specified in the URL parameter.
        """
        event_sub_Category = self.kwargs['event_sub_Category']
        return event.objects.filter(sub_Category=event_sub_Category)


class EventListVenue(generics.ListAPIView):
    """
    A viewset for retrieving event instances by venue.
    """
    serializer_class = eventSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the venue specified in the URL parameter.
        """
        event_venue = self.kwargs['event_venue']
        return event.objects.filter(venue_name=event_venue)


class OnlineEventsAPIView(APIView):
    """
    A viewset for retrieving event which the online is 'true' .
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        This view should return a list of all the online events.
        """
        events = event.objects.filter(online='True')
        serializer = eventSerializer(events, many=True)

        return Response(serializer.data)


class EventID(generics.ListAPIView):
    """
    A viewset for retrieving event instances by ID.
    """
    serializer_class = eventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the events
        for the sub-category specified in the URL parameter.
        """
        event_sub_ID = self.kwargs['event_ID']
        return event.objects.filter(ID=event_sub_ID)


class UserInterestCreateAPIView(CreateAPIView):
    """
    A viewset for creating an user Interests instance.
    """
    permission_classes = [IsAuthenticated]
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer


class UserInterestAPIView(generics.ListAPIView):
    """
    A viewset for retrive an user Interests instance.
    """
    permission_classes = [IsAuthenticated]
    queryset = UserInterest.objects.all()

    def list(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = UserInterestSerializer(queryset, many=True)
        return Response(serializer.data)


class UserInterestEventsAPIView(APIView):
    """
    A viewset for retrieving event instances based on user Interests.
    """
    permission_classes = [IsAuthenticated]
    """
    This function defines a GET request that retrieves a list of events based on the user's interests. 
    It first checks whether the user is authenticated, and if not, returns a 401 Unauthorized response. 
    If the user is authenticated, it retrieves the user's interests using the get_user_interests method and the events related to those interests using the get_events method. 
    Finally, it serializes the retrieved events using the eventSerializer class and returns the serialized data as a response using the Response class. 
    """

    def get(self, request, format=None):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Retrieve user interests
        user_interests = self.get_user_interests(request.user)
        # Retrieve events related to user interests
        events = self.get_events(user_interests)
        # Serialize data and return response
        serializer = eventSerializer(events, many=True)
        return Response(serializer.data)

    """
    This function retrieves the interests of a given user. It takes a user object as input, 
    and returns a queryset of UserInterest objects that match the given user. 
    """

    def get_user_interests(self, user):
        # Logic to retrieve user interests
        return UserInterest.objects.filter(user=user)
    """
    This function retrieves events related to a given set of user interests. It takes a queryset of UserInterest objects 
    as input, extracts the category and subcategory names from those objects, and returns a queryset of event objects 
    that belong to those categories. 
    """

    def get_events(self, user_interests):
        # Logic to retrieve events related to user interests
        categories = [ui.category_name for ui in user_interests]
        subcategories = [ui.sub_Category for ui in user_interests]
        return event.objects.filter(category_name__in=categories)
        # sub_Category__in=subcategories)


class TodayEventsList(generics.ListAPIView):
    """
    This class defines a GET request that returns a list of events happening today. 
    It uses the eventSerializer class for serialization. The get_queryset method is used to 
    retrieve the events happening on the current date and returns a queryset containing those events. 
    """
    serializer_class = eventSerializer

    def get_queryset(self):
        today = now().date()
        queryset = event.objects.filter(ST_DATE=today)
        return queryset


class WeekendEventsView(generics.ListAPIView):
    """
    This class defines a GET request that returns a list of events happening on the upcoming weekend. 
    It uses the eventSerializer class for serialization. The get_queryset method is used to retrieve 
    the events happening between Friday and Saturday of the upcoming weekend and returns a queryset containing those events. 
    """
    serializer_class = eventSerializer

    def get_queryset(self):
        today = timezone.now().date()
        # Find the date of the upcoming Friday
        friday = today + timezone.timedelta((4 - today.weekday()) % 7)
        # Find the date of the upcoming Saturday
        saturday = friday + timezone.timedelta(1)
        queryset = event.objects.filter(
            Q(ST_DATE__gte=friday) & Q(END_DATE__lte=saturday)
        )
        return queryset


class TicketCreateAPIView(generics.CreateAPIView):
    """
    This class defines a POST request to create a new ticket for a given event. It uses the TicketSerializer for serialization 
    and the Ticket model for database queries. The post method first checks if the specified event exists in the database, 
    then adds the event ID to the ticket data and attempts to create a new ticket using the serializer. If the serializer is 
    valid, the new ticket is saved and a success response is returned. Otherwise, an error response is returned with the 
    serializer errors.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def post(self, request, event_id):
        """
        A POST request to create a ticket object for a given event ID
        """
        try:
            Event = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response({'error': f'Event with id {event_id} does not exist.'}, status=HTTP_400_BAD_REQUEST)

        ticket_data = request.data.copy()
        ticket_data['event'] = Event.ID
        serializer = self.serializer_class(data=ticket_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class EventTicketPrice(APIView):
    """
    This class defines a GET request to retrieve the ticket price for a given event. It uses the event and Ticket models 
    for database queries. The get method first checks if the specified event exists in the database, then retrieves the 
    first ticket object associated with the event ID. If the ticket object exists, the ticket price is returned in a 
    success response. Otherwise, an error response is returned indicating that the ticket was not found.
    """
    def get(self, request, event_id):
        """
        Returns the ticket price for a given event.
        """
        try:
            event_obj = event.objects.get(ID=event_id)
        except event.DoesNotExist:
            return Response(status=404, data={'message': 'Event not found'})

        ticket_obj = Ticket.objects.filter(EVENT_ID=event_obj.ID).first()
        if ticket_obj:
            ticket_price = ticket_obj.PRICE
            return Response(status=200, data={'ticket_price': ticket_price})
        else:
            return Response(status=404, data={'message': 'Ticket not found'})

class FreeTicketEventListView(generics.ListAPIView):
    serializer_class = eventSerializer
    def get_queryset(self):
        return event.objects.filter(ticket_set__TICKET_TYPE='Free').distinct()
    
class DraftEventsAPIView(APIView):
    """
    A viewset for retrieving Draft events.
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        This view should return a list of all the draft events.
        """
        events = event.objects.filter(STATUS='Draft')
        serializer = eventSerializer(events, many=True)

        return Response(serializer.data)
