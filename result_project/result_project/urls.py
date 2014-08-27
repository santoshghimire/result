from django.conf.urls import patterns, include, url
# from django.conf.urls.static import static
# from django.conf import settings
# from django.views.generic import TemplateView
from mainapp.views import FormView
from mainapp.tu_view import TUFormView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(
        r'^$',
        view=FormView.as_view(),
        name='form'
    ),
    url(
        r'^tu/$',
        view=TUFormView.as_view(),
        name='tuform'
    ),

    # Examples:
    # url(r'^$', 'result_project.views.home', name='home'),
    # url(r'^result_project/', include('result_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^admin/', include(admin.site.urls)),
    url(r'^slc/$', 'mainapp.slc.find_result'),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += patterns('',
#                             url(r'^__debug__/', include(debug_toolbar.urls)),
#                             )
