from django.db import models

class User(models.Model):
    login=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    admin_rights=models.BooleanField()

class Patients(models.Model):
    polis_OMS=models.CharField(max_length=16)
    surname=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    patronymic=models.CharField(max_length=30, blank=True)
    gender=models.CharField(max_length=1)
    passport_data=models.TextField(max_length=255)
    SNILS=models.CharField(max_length=11)
    initial_inspection=models.BooleanField(blank=True)
    date_of_next_meet=models.DateField(null=True)
    work_phone=models.CharField(max_length=11)
    home_phone=models.CharField(max_length=11, blank=True)
    registration_address=models.TextField(max_length=255)
    residence_address=models.TextField(max_length=255)
    e_mail=models.CharField(max_length=255, blank=True)
    sector=models.IntegerField()
    place_of_work=models.TextField(max_length=255, blank=True)
    blood_type=models.IntegerField(null=True, blank=True)
    rhesus_factor=models.CharField(null=True,max_length=1, blank=True)

class Doctor(models.Model):
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=1)
    room_number = models.IntegerField()
    phone_number = models.CharField(max_length=11)
    subdivisions = models.CharField(max_length=50)
    def __str__(self):
        return self.surname+" "+self.name
    def get_room_number(self):
        return self.room_number

class Schedule(models.Model):
    id_doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    day = models.DateField()
    time_reception = models.IntegerField()
    start_hour =models.IntegerField()
    start_minute = models.IntegerField()
    end_hour = models.IntegerField()
    end_minute = models.IntegerField()
    def __int__(self):
        return self.id


class Reception(models.Model):
    id_Schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    day = models.DateField()
    reception_start_hour =models.IntegerField()
    reception_start_minute = models.IntegerField()
    reception_end_hour = models.IntegerField()
    reception_end_minute = models.IntegerField()
    status = models.BooleanField()
    patient_polis_OMS = models.CharField(max_length=150, blank=True)
    patient_FIO = models.CharField(max_length=16, blank=True)







