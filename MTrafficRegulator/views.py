from urllib.error import URLError

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from geopy import geocoders
from geopy.geocoders.googlev3 import GeocoderQueryError

from DTrafficControl import settings
from DTrafficControl.iotawrapper.iotawrapper import IOTAWrapper
from DTrafficControl.settings import GOOGLE_MAP_API_KEY_1


# Create your views here.
from MTrafficRegulator import forms
from MTrafficRegulator.models import TrafficNode


def get_geocode_address(address):
    g = geocoders.GoogleV3(api_key=GOOGLE_MAP_API_KEY_1)
    try:
        place_name, (longitude, latitude) = g.geocode(address.encode('utf-8'))
        return place_name, longitude, latitude
    except (URLError, GeocoderQueryError, ValueError):
        return None


@csrf_protect
def index(request):
    geo_addr_form = forms.AddressForm()

    search_traffic_node = None
    if request.POST:
        geo_addr_form = forms.AddressForm(request.POST)
        if geo_addr_form.is_valid():
            address = geo_addr_form.cleaned_data['place']
            place_name, latitude, longitude = get_geocode_address(address)

            search_traffic_node = TrafficNode()
            search_traffic_node.name = place_name
            search_traffic_node.address = address
            search_traffic_node.longitude = longitude
            search_traffic_node.latitude = latitude

    return render(
        request,
        'index.html',
        context={
            'form': geo_addr_form,
            'traffic_node': search_traffic_node,
            'g_api_key': settings.GOOGLE_MAP_API_KEY_1,
        }
    )


@csrf_exempt
def get_traffic_status(request):
    if request.POST and request.is_ajax():
        current_latitude = request.POST.get("latitude", None)
        current_longitude = request.POST.get("longitude", None)

        iota = IOTAWrapper()
        traffics = iota.get_traffic_status_within(2.5, latitude=current_latitude, longitude=current_longitude)

        return JsonResponse(traffics, safe=False)

    return HttpResponse(200)
