from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from event.models import event
from event.serializers import eventSerializer
from django.contrib.auth import get_user_model


class EventListSubCategoryTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='ismail',
            email='ziad@gmail.com',
            password='512002',)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.event_sub_Category = 'pop'
        self.event1 = event.objects.create(
            ID=1,
            User_id=1,
            Title='Online Event 1',
            organizer='Organizer 1',
            Summery='Summary 1',
            Description='Description 1',
            type='Type 1',
            category_name='Category 1',
            sub_Category= self.event_sub_Category ,
            venue_name='Venue 1',
            ST_DATE='2023-04-15',
            END_DATE='2023-04-15',
            ST_TIME='09:00:00',
            END_TIME='10:00:00',
            online='True',
            CAPACITY=50,
            STATUS='Live',
            image=None
        )
        self.event2 = event.objects.create(
            ID=2,
            User_id=2,
            Title='Online Event 2',
            organizer='Organizer 2',
            Summery='Summary 2',
            Description='Description 2',
            type='Type 2',
            category_name='Category 2',
            sub_Category='Sub-category 2',
            venue_name='Venue 2',
            ST_DATE='2023-04-16',
            END_DATE='2023-04-16',
            ST_TIME='10:00:00',
            END_TIME='11:00:00',
            online='False',
            CAPACITY=100,
            STATUS='Live',
            image=None
        )
    def test_get_events_by_sub_Category(self):
        """
        Test retrieving events by sub_Category.
        """
        url = reverse('event-list-by-sub_category',
                      kwargs={'event_sub_Category': self.event_sub_Category})
        response = self.client.get(url,follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        event_data = response.data[0]
        serializer = eventSerializer(self.event1)
        self.assertEqual(event_data, serializer.data)

    def test_get_events_by_non_exist_sub_Category(self):
        """
        Test retrieving events by a sub_Category that does not exist.
        """
        nonexistent_sub_Category = 'nonexistent sub_Category'
        url = reverse('event-list-by-sub_category',
                      kwargs={'event_sub_Category': nonexistent_sub_Category})
        response = self.client.get(url,follow=True)
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
