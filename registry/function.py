from registry.models import *

def Authorizate(login,password):
    try:
        authorizate = User.objects.get(login=login, password=password)
        return authorizate
    except User.DoesNotExist:
        return None

def CreatePatient(polis_OMS,surname,name,patronymic,gender,passport_data,SNILS,initial_inspection,date_of_next_meet,
                  work_phone,home_phone,registration_address,residence_address,e_mail,sector,place_of_work,blood_type,
                  rhesus_factor):
    Patients.objects.create(polis_OMS=polis_OMS,surname=surname,name=name,patronymic=patronymic,gender=gender,
                            passport_data=passport_data,SNILS=SNILS,initial_inspection=initial_inspection,
                            date_of_next_meet=date_of_next_meet,work_phone=work_phone,home_phone=home_phone,
                            registration_address=registration_address,residence_address=residence_address,
                            e_mail=e_mail,sector=sector,place_of_work=place_of_work,blood_type=blood_type,
                            rhesus_factor=rhesus_factor)

def CreateDoctor(surname,name,patronymic,gender,room_number,phone_number,subdivisions):
    Doctor.objects.create(surname=surname,name=name,patronymic=patronymic,gender=gender,room_number=room_number,
                          phone_number=phone_number, subdivisions=subdivisions)

def CreateSchedule(id_doctor, day, time_reception, start_hour, start_minute, end_hour, end_minute):
    Schedule.objects.create(id_doctor=id_doctor, day=day, time_reception=time_reception, start_hour=start_hour,
                            start_minute=start_minute, end_hour=end_hour, end_minute=end_minute)

def CreateReceptions(schedule_id,day,time_reception,start_hour,start_minute,end_hour,end_minute,status):
    while start_hour<end_hour or (start_hour==end_hour and start_minute!=end_minute):
        reception_start_hour = start_hour
        reception_start_minute = start_minute
        start_minute+=time_reception
        if(start_minute>=60):
            start_hour+=1
            start_minute-=60
        reception_end_hour = start_hour
        reception_end_minute = start_minute
        Reception.objects.create(id_Schedule=schedule_id, day=day,  reception_start_hour=reception_start_hour,
                                 reception_start_minute=reception_start_minute, reception_end_hour=reception_end_hour,
                                 reception_end_minute=reception_end_minute,status=status)

def NewEditDoctor(doctor_id,surname,name,patronymic,gender,room_number,phone_number,subdivisions):
    Doctor.objects.filter(id=doctor_id).update(surname=surname,name=name,patronymic=patronymic,gender=gender,room_number=room_number,
                          phone_number=phone_number, subdivisions=subdivisions)

def NewDeleteDoctor(id):
    Doctor.objects.get(id=id).delete()

def NewEditPatient(patient_id,polis_OMS,surname,name,patronymic,gender,passport_data,SNILS,initial_inspection,date_of_next_meet,
                  work_phone,home_phone,registration_address,residence_address,e_mail,sector,place_of_work,blood_type,
                  rhesus_factor):
    Patients.objects.filter(id=patient_id).update(polis_OMS=polis_OMS,surname=surname,name=name,patronymic=patronymic,gender=gender,
                            passport_data=passport_data,SNILS=SNILS,initial_inspection=initial_inspection,
                            date_of_next_meet=date_of_next_meet,work_phone=work_phone,home_phone=home_phone,
                            registration_address=registration_address,residence_address=residence_address,
                            e_mail=e_mail,sector=sector,place_of_work=place_of_work,blood_type=blood_type,
                            rhesus_factor=rhesus_factor)

def NewDeletePatient(id):
    Patients.objects.get(id=id).delete()

def NewEdirReception(reception_id,patient_FIO,patient_polis_OMS,status):
    Reception.objects.filter(id=reception_id).update(status=status, patient_polis_OMS=patient_polis_OMS,
                                                     patient_FIO=patient_FIO)

def NewDeleteReception(reception_id,patient_FIO,patient_polis_OMS,status):
    Reception.objects.filter(id=reception_id).update(status=status, patient_polis_OMS=patient_polis_OMS,
                                                     patient_FIO=patient_FIO)