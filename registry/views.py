from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import HttpResponseNotFound, Http404, HttpResponse, HttpResponseRedirect
from registry.models import *
from django.views import View
from django.urls import reverse
from django.views.generic.list import ListView
from . import function
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from registry.templatetags.tags import get_doctor
from . import models


class Registry(View):
    def get(self, request):
        return render(request, "index.html")

    def post(self, request):
        login = request.POST.get("login")
        password = request.POST.get("password")
        user = function.Authorizate(login, password)
        if user is not None:
            request.session['login'] = login
            if(user.admin_rights==False):
                return HttpResponseRedirect(reverse('MainRegistrator'))
            else:
                return HttpResponseRedirect(reverse('MainMenuAdmin'))
        else:
            return render(request, "index.html")


class MainRegistrator(View):
    def get(self, request):
        return render(request, "mainmenuregistrator.html")

def MainPatient(request):
    if request.method == "GET":
        all_Schedule = Schedule.objects.all()
        start_minute = {object.pk: object.start_minute for object in all_Schedule}
        end_minute = {object.pk: object.end_minute for object in all_Schedule}
        for key in start_minute:
            if start_minute[key]==0:
                start_minute[key] = str("00")
        for key in end_minute:
            if end_minute[key]==0:
                end_minute[key] = str("00")
        paginator = Paginator(all_Schedule, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            schedules = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            schedules = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            schedules = paginator.page(paginator.num_pages)
        context = {
            'schedules':schedules,
            'start_minute': start_minute,
            'end_minute': end_minute,
        }
        return render(request, "mainpatient.html", context=context)
    if request.method == "POST":
        return HttpResponseRedirect(reverse('registry'))

def RegistratorSearch(request):
    if request.method == "GET":
        all_Patient = Patients.objects.all()
        paginator = Paginator(all_Patient, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            Cards = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            Cards = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            Cards = paginator.page(paginator.num_pages)
        context = {
            'Cards': Cards,
        }
        return render(request, 'registratorsearch.html', context=context)

def SearchPatient(request):
    if request.method == "GET":
        SearchPatient = request.GET.get('search')
        all_Patient = Patients.objects.filter(polis_OMS=SearchPatient)
        if not  SearchPatient:
            all_Patient = Patients.objects.all()
        context = {
            'Cards': all_Patient,
            'SearchPatient': SearchPatient
        }
        return render(request, 'registratorsearch.html', context=context)

def MakeAnapPointment(request, reception_id):
    all_Reception = Reception.objects.all()
    reception_start_minute = {object.pk: object.reception_start_minute for object in all_Reception}
    reception_end_minute = {object.pk: object.reception_end_minute for object in all_Reception}
    for key in reception_start_minute:
        if reception_start_minute[key] == 0:
            reception_start_minute[key] = str("00")
    for key in reception_end_minute:
        if reception_end_minute[key] == 0:
            reception_end_minute[key] = str("00")
    context = {
        'cards':Patients.objects.all(),
        'receptions': Reception.objects.filter(id=reception_id),
        'reception_start_minute': reception_start_minute,
        'reception_end_minute': reception_end_minute,
    }
    if request.method == "POST":
        patient_info = request.POST.get("patient")
        patient_FIO = patient_info.split()[2] + " " + patient_info.split()[3]
        patient_polis_OMS = patient_info.split()[1]
        status = True
        function.NewEdirReception(reception_id,patient_FIO,patient_polis_OMS,status)
        return HttpResponseRedirect(reverse('ReceptionList'))
    return render(request, "makeanappointment.html", context=context)

def DeleteReception(request, reception_id):
    if request.method == "GET":
        patient_FIO = ""
        patient_polis_OMS = ""
        status = False
        function.NewDeleteReception(reception_id,patient_FIO,patient_polis_OMS,status)
        return HttpResponseRedirect(reverse('ReceptionList'))

def CreateNewPatientCard(request):
    now_date = datetime.today()
    context = {
        'datetime_now': now_date
    }
    dont_valid = True
    if request.method == "GET":
        return render(request, "createnewpatientcard.html", context=context)
    if request.method == "POST":
        polis_OMS = request.POST.get("polis_OMS")
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        gender = request.POST.get("gender")
        passport_data = request.POST.get("passport_data")
        SNILS = request.POST.get("SNILS")
        initial_inspection = request.POST.get("initial_inspection")
        if initial_inspection is None:
            initial_inspection = False
        date_of_next_meet = request.POST.get("date_of_next_meet")
        if not date_of_next_meet:
            date_of_next_meet = None
        work_phone = request.POST.get("work_phone")
        home_phone = request.POST.get("home_phone")
        registration_address = request.POST.get("registration_address")
        residence_address = request.POST.get("residence_address")
        e_mail = request.POST.get("e_mail")
        sector = request.POST.get("sector")
        place_of_work = request.POST.get("place_of_work")
        blood_type = request.POST.get("blood_type")
        if not blood_type:
            blood_type = 0
        rhesus_factor = request.POST.get("rhesus_factor")
        if not polis_OMS:
            context["none_polis_OMS"] = "Поле Полис ОМС не заполнено"
            dont_valid = False
        if not surname:
            context["none_surname"] = "Поле Фамилия не заполнено"
            dont_valid = False
        if not name:
            context["none_name"] = "Поле Имя не заполнено"
            dont_valid = False
        if not passport_data:
            context["none_passport_data"] = "Поле Паспортные данные не заполнено"
            dont_valid = False
        if not SNILS:
            context["none_SNILS"] = "Поле СНИЛС не заполнено"
            dont_valid = False
        if not work_phone:
            context["none_work_phone"] = "Поле Рабочий телефон не заполнено"
            dont_valid = False
        if not registration_address:
            context["none_registration_address"] = "Поле Адрес прописки не заполнено"
            dont_valid = False
        if not residence_address:
            context["none_residence_address"] = "Поле Адрес проживания не заполнено"
            dont_valid = False
        if not sector:
            context["none_sector"] = "Поле Участок не заполнено"
            dont_valid = False
        if dont_valid==True:
            function.CreatePatient(polis_OMS,surname,name,patronymic,gender,passport_data,SNILS,initial_inspection,
                                           date_of_next_meet,work_phone,home_phone,registration_address,residence_address,
                                           e_mail,sector,place_of_work,blood_type,rhesus_factor)
            return HttpResponseRedirect(reverse('RegistratorSearch'))
        else:
            context["polis_OMS"] = polis_OMS
            context["surname"] = surname
            context["name"] = name
            context["patronymic"] = patronymic
            context["gender"] = gender
            context["passport_data"] = passport_data
            context["SNILS"] = SNILS
            context["work_phone"] = work_phone
            context["registration_address"] = registration_address
            context["residence_address"] = residence_address
            context["sector"] = sector
            context["date_of_next_meet"] = date_of_next_meet
            context["home_phone"] = home_phone
            context["e_mail"] = e_mail
            context["place_of_work"] = place_of_work
            context["blood_type"] = blood_type
            context["rhesus_factor"] = rhesus_factor
            return render(request, "createnewpatientcard.html", context=context)

class MainMenuAdmin(View):
     def get(self,request):
         return render(request, "mainmenuadmin.html")

def AdminDoctorList(request):
    if request.method == "GET":
        all_Doctor = Doctor.objects.all()
        paginator = Paginator(all_Doctor, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            doctors = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            doctors = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            doctors = paginator.page(paginator.num_pages)
        context = {
            'doctors': doctors
        }
        return render(request, "admindoctorlist.html", context=context)

def SearchDoctor(request):
    if request.method == "GET":
        doctor_name = request.GET.get('search')
        all_Dcotor = Doctor.objects.filter(surname=doctor_name)
        if not  doctor_name:
            all_Dcotor = Doctor.objects.all()
        context = {
            'doctors': all_Dcotor,
            'doctor_name': doctor_name
        }
        return render(request, 'admindoctorlist.html', context=context)


def NewDoctor(request):
    context = {}
    dont_valid = True
    if request.method == "GET":
        return render(request, "newdoctor.html")
    if request.method == "POST":
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        gender = request.POST.get("gender")
        room_number = request.POST.get("room_number")
        phone_number = request.POST.get("phone_number")
        subdivisions = request.POST.get("subdivisions")
        if not surname:
            context["none_surname"] = "Поле Фамилия не заполнено"
            dont_valid = False
        if not name:
            context["none_name"] = "Поле Имя не заполнено"
            dont_valid = False
        if not gender:
            context["none_gender"] = "Поле Пол не заполнено"
            dont_valid = False
        if not room_number:
            context["none_room_number"] = "Поле Номер кабинета не заполнено"
            dont_valid = False
        if not phone_number:
            context["none_phone_number"] = "Поле Номер телефона не заполнено"
            dont_valid = False
        if not subdivisions:
            context["none_subdivisions"] = "Поле Должность не заполнено"
            dont_valid = False
        if dont_valid == True:
            function.CreateDoctor(surname,name,patronymic,gender,room_number,phone_number,subdivisions)
            return HttpResponseRedirect(reverse('AdminDoctorList'))
        else:
            context["surname"] = surname
            context["name"] = name
            context["patronymic"] = patronymic
            context["gender"] = gender
            context["room_number"] = room_number
            context["phone_number"] = phone_number
            context["subdivisions"] = subdivisions
            return render(request, "newdoctor.html", context=context)

def AdminSchedule (request):
    if request.method == "GET":
        all_Schedule = Schedule.objects.all()
        start_minute = {object.pk: object.start_minute for object in all_Schedule}
        end_minute = {object.pk: object.end_minute for object in all_Schedule}
        for key in start_minute:
            if start_minute[key]==0:
                start_minute[key] = str("00")
        for key in end_minute:
            if end_minute[key]==0:
                end_minute[key] = str("00")
        paginator = Paginator(all_Schedule, 10)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            schedules = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            schedules = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            schedules = paginator.page(paginator.num_pages)
        context = {
            'schedules':schedules,
            'start_minute': start_minute,
            'end_minute': end_minute,
        }
        return render(request, "adminschedule.html", context=context)
    if request.method == "POST":
        return HttpResponseRedirect(reverse('AdminDoctorList'))

def SearchSchedule (request):
    if request.method == "GET":
        shedule_name = request.GET.get('search')
        for doc in Doctor.objects.filter(surname=shedule_name):
            all_Shedule = Schedule.objects.filter(id_doctor = doc.id)
        if not shedule_name:
            all_Shedule = Schedule.objects.all()
        start_minute = {object.pk: object.start_minute for object in all_Shedule}
        end_minute = {object.pk: object.end_minute for object in all_Shedule}
        for key in start_minute:
            if start_minute[key]==0:
                start_minute[key] = str("00")
        for key in end_minute:
            if end_minute[key]==0:
                end_minute[key] = str("00")
        context = {
            'schedules': all_Shedule,
            'shedule_name': shedule_name,
            'start_minute': start_minute,
            'end_minute': end_minute,
        }
        return render(request, 'adminschedule.html', context=context)

def NewSchedule(request):
    now_date = datetime.today()
    week = timedelta(7)
    in_weeks = now_date + week
    context = {
        'datetime_now': now_date,
        'in_weeks': in_weeks,
        'doctors': Doctor.objects.all()
    }
    dont_valid = True
    if request.method == "GET":
        return render(request, "newschedule.html", context=context)
    if request.method == "POST":
        id_doctor = request.POST.get("id_doctor")
        day = request.POST.get("day")
        time_reception = request.POST.get("time_reception")
        start_hour = request.POST.get("start_hour")
        start_minute = request.POST.get("start_minute")
        end_hour = request.POST.get("end_hour")
        end_minute = request.POST.get("end_minute")
        if not day:
            context["none_day"] = "Поле День не заполнено"
            dont_valid = False
        if not time_reception:
            context["none_time_reception"] = "Поле Время приема не заполнено"
            dont_valid = False
        if not start_hour or not start_minute or not end_hour or not end_minute:
            context["none_time"] = "Поле Времени не заполнено"
            dont_valid = False
        if dont_valid == True:
            time_reception=int(time_reception)
            start_hour=int(start_hour)
            start_minute=int(start_minute)
            end_hour=int(end_hour)
            end_minute=int(end_minute)
            function.CreateSchedule(Doctor.objects.get(id=id_doctor.split()[0]), day, time_reception, start_hour, start_minute, end_hour, end_minute)
            id_Schedule = Schedule.objects.get(id_doctor=id_doctor.split()[0], day=day)
            status = False
            function.CreateReceptions(id_Schedule, day, time_reception, start_hour, start_minute, end_hour, end_minute,status)
            return HttpResponseRedirect(reverse('AdminSchedule'))
        context["day"] = day
        context["time_reception"] = time_reception
        context["start_hour"] = start_hour
        if start_minute == 0:
            start_minute = str("00")
        context["start_minute"] = start_minute
        context["end_hour"] = end_hour
        if end_minute == 0:
            end_minute = str("00")
        context["end_minute"] = end_minute
        return render(request, "newschedule.html", context=context)
    if request.method == "POST":
        return HttpResponseRedirect(reverse('AdminDoctorList'))

def ReceptionList(request):
    if request.method == "GET":
        all_Reception = Reception.objects.all()
        reception_start_minute = {object.pk: object.reception_start_minute for object in all_Reception}
        reception_end_minute = {object.pk: object.reception_end_minute for object in all_Reception}
        for key in reception_start_minute:
            if reception_start_minute[key] == 0:
                reception_start_minute[key] = str("00")
        for key in reception_end_minute:
            if reception_end_minute[key] == 0:
                reception_end_minute[key] = str("00")
        paginator = Paginator(all_Reception, 11)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            receptions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            receptions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            receptions = paginator.page(paginator.num_pages)
        context = {
            'receptions': receptions,
            'reception_start_minute': reception_start_minute,
            'reception_end_minute': reception_end_minute,
        }
        return render(request, "receptionlist.html", context=context)

def SearchReception (request):
    global reception_name
    if request.method == "GET":
        reception_name = request.GET.get('search')
        all_Reception = Reception.objects.filter(day = reception_name)
        if not reception_name:
            all_Reception = Reception.objects.all()
        reception_start_minute = {object.pk: object.reception_start_minute for object in all_Reception}
        reception_end_minute = {object.pk: object.reception_end_minute for object in all_Reception}
        for key in reception_start_minute:
            if reception_start_minute[key] == 0:
                reception_start_minute[key] = str("00")
        for key in reception_end_minute:
            if reception_end_minute[key] == 0:
                reception_end_minute[key] = str("00")
        paginator = Paginator(all_Reception, 11)  # Show 25 contacts per page
        page = request.GET.get('page')
        try:
            receptions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            receptions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            receptions = paginator.page(paginator.num_pages)
        context = {
            'receptions': receptions,
            'reception_name': reception_name,
            'reception_start_minute': reception_start_minute,
            'reception_end_minute': reception_end_minute,
        }
        return render(request, 'receptionlist.html', context=context)

def EditDoctor(request, doctor_id):
    if request.method == "GET":
        context = {
            'doctors': Doctor.objects.filter(id=doctor_id),
        }
        return render(request, "editdoctor.html", context=context)
    if request.method == "POST":
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        gender = request.POST.get("gender")
        room_number = request.POST.get("room_number")
        phone_number = request.POST.get("phone_number")
        subdivisions = request.POST.get("subdivisions")
        function.NewEditDoctor(doctor_id,surname,name,patronymic,gender,room_number,phone_number,subdivisions)
        return HttpResponseRedirect(reverse('AdminDoctorList'))

def DeleteDoctor(request, doctor_id):
    if request.method == "GET":
        function.NewDeleteDoctor(doctor_id)
        return HttpResponseRedirect(reverse('AdminDoctorList'))

def EditPatientCard(request, patient_id):
    if request.method == "GET":
        now_date = datetime.today()
        context = {
            'datetime_now': now_date,
            'Cards': Patients.objects.filter(id=patient_id),
        }
        return render(request, "editpatientcar.html", context=context)
    if request.method == "POST":
        polis_OMS = request.POST.get("polis_OMS")
        surname = request.POST.get("surname")
        name = request.POST.get("name")
        patronymic = request.POST.get("patronymic")
        gender = request.POST.get("gender")
        passport_data = request.POST.get("passport_data")
        SNILS = request.POST.get("SNILS")
        initial_inspection = request.POST.get("initial_inspection")
        if initial_inspection is None:
            initial_inspection = False
        date_of_next_meet = request.POST.get("date_of_next_meet")
        if not date_of_next_meet:
            date_of_next_meet = None
        work_phone = request.POST.get("work_phone")
        home_phone = request.POST.get("home_phone")
        registration_address = request.POST.get("registration_address")
        residence_address = request.POST.get("residence_address")
        e_mail = request.POST.get("e_mail")
        sector = request.POST.get("sector")
        place_of_work = request.POST.get("place_of_work")
        blood_type = request.POST.get("blood_type")
        rhesus_factor = request.POST.get("rhesus_factor")
        function.NewEditPatient(patient_id,polis_OMS,surname,name,patronymic,gender,passport_data,SNILS,initial_inspection,
                                       date_of_next_meet,work_phone,home_phone,registration_address,residence_address,
                                       e_mail,sector,place_of_work,blood_type,rhesus_factor)
        return HttpResponseRedirect(reverse('RegistratorSearch'))

def DeletePatient(request, patient_id):
    if request.method == "GET":
        function.NewDeletePatient(patient_id)
        return HttpResponseRedirect(reverse('RegistratorSearch'))

def custom_handler404(request, exception):
    return HttpResponseNotFound('Ошибка 404, Страница не найдена! Возможно вы зашли в аккаунт!')


def custom_handler500(request):
    return HttpResponse("Ошибка 500, что-то сломалось на сервере!")