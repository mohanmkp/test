from django.urls import path, include
from .import views
from .views import view_user_kwargs

urlpatterns = [
    path("", views.home, name="home page"),
    path("map/", views.map_view, name="map"),
    path("add-pointer/", views.Add_Pointer, name=" create pointer"),
    path('pointer/', include([
        path("<int:id>/", views.pointer),
        path("update/<int:update_id>/", views.pointer),
        path("", views.pointer),
    ])),
    path("login/", include([
        path("", views.Login, name="login-page"),
        path("<websocket_auth>/", views.Login, name="login-page"),
    ])),
    path("logout/", views.Logout, name="logout-page"),
    path("view-all-users/", include([
        path("", views.view_all_user, name="view_all_user", kwargs=view_user_kwargs),
        path("delete/<int:delete_id>/", views.view_all_user, name="delete_user"),
        path("update/<int:update_id>/", views.view_all_user, name="update_user"),
    ])),
    path("add-new-user/", views.add_new_user, name="add-new-user"),
    path("user-profile/", include([
        path("", views.user_profile, name="user-profile"),
        path("edit/<int:update_id>/", views.user_profile, name="user-profile-update"),
    ])),
    path("geojson", views.add_geo_json_file, name="geojson"),
    path("upload-tiff", views.upload_tiff_file, name="uploadtiff")
]
