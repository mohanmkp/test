from django.shortcuts import render, redirect,  HttpResponse
from .models import *
from .form import pointer_form, user_form, user_update_form
# import rasterio
# from rasterio.plot import reshape_as_image
# from io import BytesIOp
import asyncio
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dashboard.services.admin_decorator import admin_required
import folium
import os
from django.db.models import Q  
from folium.plugins import MousePosition
from folium import plugins
from PIL import Image
# import Image
from datetime import date, timedelta
from dashboard.services.lat_log import map_data
from django.http import HttpResponseRedirect
from django.contrib import messages
# from folium.features import CustomIcon
# css file
folium.folium._default_css.append(('leaflet_css', '/static/folium/leaflet.css'))
folium.folium._default_css.append(('bootstrap_css', '/static/folium/bootstrap.css'))
folium.folium._default_css.append(('bootstrap_theme_css', '/static/folium/bootstrap_theme.css'))
folium.folium._default_css.append(('awesome_markers_font_css', '/static/folium/font-awesome.min.css'))
folium.folium._default_css.append(('awesome_markers_css', '/static/folium/leaflet.awesome-markers.css'))
folium.folium._default_css.append(('awesome_rotate_css', '/static/folium/leaflet.awesome.rotate.css'))
folium.folium._default_css.append(('draw_css', '/static/folium/draw.css'))
folium.folium._default_css.append(('MousePosition_min_css', '/static/folium/L.Control.MousePosition.min.css'))
folium.folium._default_css.append(('measure_min-css', '/static/folium/leaflet-measure.min.css'))

# js file
folium.folium._default_js.append(('leaflet', '/static/folium/leaflet.js'))
folium.folium._default_js.append(('jquery', '/static/folium/jquery.js'))
folium.folium._default_js.append(('bootstrap', '/static/folium/bootstrap.js'))
folium.folium._default_js.append(('awesome_markers', '/static/folium/markers.js'))
folium.folium._default_js.append(('leaflet_draw', '/static/folium/draw.js'))
folium.folium._default_js.append(('Control_MousePosition_min', '/static/folium/L.Control.MousePosition.min.js'))
folium.folium._default_js.append(('measure_min', '/static/folium/measure.min.js'))





def Login(request, websocket_auth=False):
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            invalid = True
            return render(request, "dashboard/pages-login.html", locals())

    if request.user.is_authenticated:    
        return redirect("/")
    return render(request, "dashboard/pages-login.html", locals())


def Logout(request):
    logout(request)
    return redirect("/login")


@login_required(login_url='/login/')
def home(request):
    shp_dir = os.path.join(os.getcwd(), 'media', 'mapdata')
    m = folium.Map(location=[25.5464, 78.5742], zoom_start=5, height=700, width = 850)
    style_basin = {'fillColor': '#228B22', 'color': '#228B22'}
    style_river = {'color': 'blue'}
    g_file = "states_india.geojson"
    if "gfile" in request.POST:
        user_gfile = GeoFile.objects.get(user = request.user.id)
        filee = user_gfile.g_json_file
        final_file = list(str(filee).split("/"))

        g_file = final_file[1]

    folium.GeoJson(os.path.join(shp_dir, g_file), name='basin',
                   style_function=lambda x: style_basin).add_to(m)

    popup1 = folium.LatLngPopup()
    m.add_child(popup1)
    # mouser hover Coordinates
    formatter = "function(num) {return L.Util.formatNum(num, 5) + ' º ';};"

    MousePosition(
        position="topright",
        separator=" | Lon ",
        empty_string="NaN",
        lng_first=True,
        num_digits=20,
        prefix="Coordinates: Lat",
        lat_formatter=formatter,
        lng_formatter=formatter,
    ).add_to(m) 

    # marker
    # markers = Pointers.objects.filter(point_type="marker")
    #
    # try:
    #     for j in map_data:    
    #         folium.Marker(
    #             location=[j["lat"], j["lon"]],
    #             icon=DivIcon(
    #                 icon_size=(150, 36),
    #                 icon_anchor=(0, 0),
    #                 html='<div style="font-size: 10px; font-weight:bold;">%s</div>' % j["name"],
    #             ),
    #         ).add_to(m)
    #
    # except Exception as e:
    #     print("label not write because of", e)
    markers = ""
    try:
    
        if request.method == "POST":

            if "yesterday" in request.POST:
                print("yes yesterday called")
                yesterday = date.today() - timedelta(days=1)
                markers = Pointers.objects.filter(create_at__date = yesterday)
            elif "tommorow" in request.POST:
                print("yes yesterday called")
                yesterday = date.today() + timedelta(days=1)
                markers = Pointers.objects.filter(create_at__date = yesterday)
            
            
        
            else:
                get_date = request.POST.get("date")
            # newstr = get_date.replace("-", ",")
            # print(newstr)
                newlist = get_date.split("-")
                print(newlist)

                markers = Pointers.objects.filter(Q(create_at__date = date(int(newlist[0]), int(newlist[1]), int(newlist[2]))))
        
        else:
            markers = Pointers.objects.all()
    
        print(markers)
        for i in markers:
            print(i)
            # icon = CustomIcon('static/images/marker-icon.png', icon_size=(30, 30), icon_anchor=(15, 15))
            html = f"""
            <div style="width:200px">
                
                <h5> station id -- {i.station_id} </h5>
                <h5> Terminal id-- {i.terminal_id} </h5>
                <p>Delta to alpha delta to alpha</p>


            </div>
            """ 
            if i.filee:
                tif_path = f'media/{i.filee}'
                print(tif_path)

                tif_image = Image.open(tif_path)
                png_image = Image.new("RGB", tif_image.size, (255, 255, 255))
                png_image.paste(tif_image, mask=tif_image.split()[3])
                try:
                    png_image.save(f"static/folicon/tiffimage{i.id}.png", "PNG")
                except Exception as e:
                    print(e)

            popup = folium.Popup(html, max_width=30)
            if i.typee == "rain":
                icon_path = "static/folicon/flatrain.png"
            
            if i.typee == "avalanche":
                icon_path = "static/folicon/flatavalanche.png"
            
            if i.filee:
                icon_path = f"static/folicon/tiffimage{i.id}.png"


    # Create a DivIcon with the HTML content
            # icon = DivIcon(html=html)
            print(i.latitude, i.longitude)
            folium.Marker(
                location=[i.longitude, i.latitude], icon = folium.features.CustomIcon(icon_image=icon_path, icon_size=(30, 30))
            , popup=html).add_to(m)

        # if i.point_type == "marker":
        #     folium.Marker(location=[i.latitude, i.longitude],
        #                   icon=folium.Icon(color="green")).add_to(m)
    except Exception as e:
        print(e)

    # draw tools
    plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(m)

    #  measure tool
    plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles',
                           primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(m)

    folium.LayerControl(m)
    m._id = "1"
    m = m._repr_html_()


    return render(request, "dashboard/dashboard.html", locals())



@login_required(login_url='/login/')
def map_view(request):
    markers = Pointers.objects.filter(point_type="marker")
    labels = Pointers.objects.filter(point_type="label")
    return render(request, "map/map.html", locals())





@login_required(login_url='/login/')
def pointer(request, id=None, update_id=None):
    if id:
        p = Pointers.objects.get(id=int(id))
        p.delete()
        return redirect("/pointer/")

    if request.method == "POST":
        instance = get_object_or_404(Pointers, id=update_id)
        form = pointer_form(request.POST or None, instance=instance)
        if form.is_valid():
            form.save()
            updated = True

        else:
            not_add = True

    pointer_data = Pointers.objects.all()
    return render(request, "map/pointer_view.html", locals())


@login_required(login_url='/login/')
def Add_Pointer(request):
    form = pointer_form()
    print("hello from django form")
    if request.method == "POST":
        form = pointer_form(request.POST, request.FILES)

        if form.is_valid():
            data = form.cleaned_data
            
            print("hello")
            terminal_id = data["terminal_id"]
            print(terminal_id)
            form.save()
            added = True
            return HttpResponseRedirect(request.path_info)
        else:
            not_add = True
    return render(request, "map/pointer_add.html", locals())



view_user_kwargs = {
  "updated": False
}

@admin_required(login_url="/login/")
def view_all_user(request, delete_id=None, update_id=None, **kwargs):

    users = User.objects.all().order_by("-id")
    if delete_id:
        user = User.objects.filter(id=delete_id).first()
        user.delete()
        return redirect("/view-all-users/")

    elif update_id:
        usr = get_object_or_404(User, id=update_id)
        form = user_update_form(request.POST or None, instance=usr)
        if form.is_valid():
            form.save()
            view_user_kwargs["updated"] = True
        else:
            view_user_kwargs["not_update"] = True
        return redirect("/view-all-users/")
    else:
        view_user_kwargs["updated"] = False
        view_user_kwargs["not_update"] = False


    if "user_added" in request.session:
        user_added = True
        del request.session["user_added"]

    return render(request, "admin/view-all-user-details.html", locals())


@admin_required(login_url="/login/")
def add_new_user(request):
    if request.method == "POST":
        form = user_form(request.POST)
        if form.is_valid():
            usr = form.save()
            usr.set_password(form.cleaned_data['password'])
            usr.save()
            request.session["user_added"] = True
            return redirect("/view-all-users/")
        else:
            not_valid = True

    return render(request, "admin/add-new-user.html", locals())





@admin_required(login_url='/login/')
def user_profile(request, update_id=None):
    if request.method == "POST" and update_id:
        usr = get_object_or_404(User, id=update_id)
        form = user_update_form(request.POST or None, instance=usr)
        if form.is_valid():
            form.save()
            user_profile_edited = True
            return redirect("/user-profile/")
        else:
            user_profile_edited = False


    # password change
    elif request.method == "POST":
        password = request.POST["password"]
        new_password = request.POST["newpassword"]
        re_new_password = request.POST["renewpassword"]
        user = authenticate(username=request.user, password=password)
        if new_password == re_new_password:
            invalid_password = False
        else:
            invalid_password = True
        if user and invalid_password is False:
            usr = User.objects.get(username=request.user)
            usr.set_password(new_password)
            usr.save()
            login(request, usr)
            changed = True
        else:
            if user is None:
               incorrect = True


    return render(request, "dashboard/user-profile.html", locals())


def add_geo_json_file(request):
    try:
        if request.method == "POST":
            check_file= GeoFile.objects.filter(user = request.user).first()
        if check_file:
            check_file.delete()

        geofile = request.FILES.get("gfile")
        obj = GeoFile(user = request.user, g_json_file=geofile)
        obj.save()
        messages.success(request,"file added successfully")
        return redirect("/")
    except Exception as e:
        messages.error(request, "something went wrong")

    return render(request, "map/geojsonn.html")


def upload_tiff_file(request):
    if request.method == "POST":
        try:
            lat = request.POST.get("latitude")
            lon = request.POST.get("longitude")
            file = request.FILES.get("filee")

            obj = Pointers(latitude = lat, longitude = lon, filee = file)
            obj.save()
            messages.success(request, "added successfully")
            return redirect("/")    

        except Exception as e:
            messages.warning(request, "something went wrong")


    return render(request, "map/uploadtiff.html")
