"""Hospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from registry.views import Registry, MainRegistrator, MainMenuAdmin, custom_handler404, custom_handler500
from registry import views

urlpatterns = (
    path('admin/', admin.site.urls),
    path('', views.MainPatient, name = 'MainPatient'),
    path('registry/', Registry.as_view(), name='registry'),
    path('mainregistrator/', MainRegistrator.as_view(), name='MainRegistrator'),
    path('registratorsearch/', views.RegistratorSearch, name='RegistratorSearch'),
    path('makeanappointment/<int:reception_id>', views.MakeAnapPointment, name='MakeAnapPointment'),
    path('createnewpatientcard/', views.CreateNewPatientCard, name='CreateNewPatientCard'),
    path('mainmenuadmin/', MainMenuAdmin.as_view(), name='MainMenuAdmin'),
    path('admindoctorlist/', views.AdminDoctorList, name='AdminDoctorList'),
    path('newdoctor/', views.NewDoctor, name='NewDoctor'),
    path('adminschedule/', views.AdminSchedule, name='AdminSchedule'),
    path('newschedule', views.NewSchedule, name='NewSchedule'),
    path('adminschedule/', views.AdminSchedule, name='AdminSchedule'),
    path('receptionlist/', views.ReceptionList, name='ReceptionList'),
    path('editdoctor/<int:doctor_id>', views.EditDoctor, name='EditDoctor'),
    path('deletedoctor/<int:doctor_id>', views.DeleteDoctor, name='DeleteDoctor'),
    path('editpatient/<int:patient_id>', views.EditPatientCard, name='EditPatientCard'),
    path('deletepatient/<int:patient_id>', views.DeletePatient, name="DeletePatient"),
    path('deletereception/<int:reception_id>', views.DeleteReception, name='DeleteReception'),
    path('admindoctorlist/search/', views.SearchDoctor, name='SearchDoctor'),
    path('registratorsearch/search/', views.SearchPatient, name='SearchPatient'),
    path('adminschedule/search/', views.SearchSchedule, name='SearchSchedule'),
    path('receptionlist/search/', views.SearchReception, name='SearchReception')
)

handler404 = custom_handler404
handler500 = custom_handler500
