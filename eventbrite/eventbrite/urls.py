"""
URL configuration for eventbrite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers
from user.views import*
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.urls import path,include
from django.contrib import admin
from django.contrib import admin
from django.contrib.admin import site
from booking.views import *
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from event.views import*
from user.views import*
from eventManagment.views import*
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/schema/',SpectacularAPIView.as_view(),name='api-schema'),
    path(
    'api/docs/',
    SpectacularSwaggerView.as_view(url_name='api-schema'),
    name='api-docs',
    ),
    # path('admin/', admin.site.urls),
    # user
    path('verify-mail/<uidb64>/<token>/',EmailVerificationQueryView.as_view(),name='verify_mail'),
    path('user/signup/',userViewSet.as_view({'post': 'create'}), name='signup'),
    path('user/login/',CustomTokenLoginView.as_view(), name='token'),
    # path('ProtectedView/',ProtectedView.as_view(), name='ProtectedView'),

    path('user/emailcheck/<str:email>/', EmailCheckView.as_view(), name='email-check'),
    path('user/reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('user/reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('user/reset-password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/reset-password/check-query/<uidb64>/<token>/', CustomPasswordResetCheckView.as_view(),name='password_reset_check'),
    path('user/reset-password/change_password/',CustomPasswordResetConfirmView.as_view(),name='password_reset_change'),
    path('user/reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # event
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/search/<str:event_name>', EventSearchView.as_view(), name='event_search'),
    path('events/type/<str:event_type>/', EventListtype.as_view(), name='event-list-by-type'),
    path('events/category/<str:event_Category>/', EventListCategory.as_view(), name='event-list-by-category'),
    path('events/sub_category/<str:event_sub_Category>/', EventListSupCategory.as_view(), name='event-list-by-sub_category'),
    path('events/ALL/', AllEventListView.as_view(), name='event-list-ALL'),
    path('events/online/', OnlineEventsAPIView.as_view(), name='online-events'),
    path('events/venue/<str:event_venue>/', EventListVenue.as_view(), name='event-list-by-venue'),
    path('events/ID/<str:event_ID>/', EventID.as_view(), name='event-list-by-ID'),
    path('events/interests-create/', UserInterestCreateAPIView.as_view(), name='user_interests_create'),
    path('events/for-you/', UserInterestEventsAPIView.as_view(), name='user-interests-events'),
    path('events/getuserinterests/', UserInterestAPIView.as_view(), name='user-interests'),
    path('events/today/', TodayEventsList.as_view(), name='today-events'),
    path('events/weekend/', WeekendEventsView.as_view(), name='weekend-events'),
    path('events/<int:event_id>/Tickets/', TicketCreateAPIView.as_view(), name='create_ticket'),
    path('events/TicketsPrice/<int:event_id>/', EventTicketPrice.as_view(), name='ticket_price_api'),
    path('events/free-events/', FreeTicketEventListView.as_view(), name='free_event_list'),
    path('events/drafte-vents/', DraftEventsAPIView.as_view(), name='Draft_event_list'),


    path('events/<int:event_id>/follow/', FollowEventView.as_view(), name='follow_event'),
    path('events/followed/', UserFollowedEvents.as_view(), name='followed_events'),
    path('events/following-events-count/',UserFollowedEventsCount.as_view(), name='user-events-following-count'),
    path('events/event-followers-count/<int:event_id>/', EventFollowersCount.as_view(), name='event-followers-count'),
    path('events/unfollow_event/<int:event_id>/', UnfollowEventView.as_view(), name='unfollow_event'),

    path('events/<int:event_id>/like/',LikeEventView.as_view(), name='like-event'),
    path('events/liked/', UserLikedEvents.as_view(), name='user-liked-events'),
    path('events/Liked-events-count/',UserLikedEventsCount.as_view(), name='user-events-following-count'),
    path('events/event-likes-count/<int:event_id>/',EventLikesCount.as_view(), name='event-Likes-count'),
    path('events/unlike_event/<int:event_id>/',UnlikeEventView.as_view(), name='unlike-event'),





    # path('book/<int:ticket_id>/',book_ticket, name='book_ticket'),


    #event management
    path('eventmanagement/userevents/<int:user_id>', UserListEvents.as_view(), name='user_list_events'),
    path('eventmanagement/UserPastEvents/<int:user_id>', UserListPastEvents.as_view(), name='user_list_past_events'),
    path('eventmanagement/UserUpcomingEvents/<int:user_id>', UserListUpcomingEvents.as_view(), name='user_list_upcoming_events'),
    path('eventmanagement/<int:event_id>/promocode/', PromoCodeCreateAPIView.as_view(), name='create_promocode'),
    path('eventmanagement/<int:event_id>/publish/' ,EventPublishView.as_view(), name='publish_event'),
    path('eventmanagement/<int:event_id>/add-attendee/' ,add_attendee, name='add-attendee'),
    path('eventmanagement/event/<int:event_id>/orders/', list_orders_by_event, name='list-orders-by-event'),
    path('eventmanagement/order/<int:order_id>/order-items/', list_orderitem_by_order, name='list-order-items-by-order-eventmanagement'),
    # path('events/upload',UploadImageView.as_view(),name='upload-image'),
    #booking
    path('booking/',include('booking.urls')),
    path('',include('rest_framework.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

