from django.db import models
from datetime import date, time
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.postgres.fields import ArrayField
from datetime import datetime

# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app 
    """
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        user = self.model(email=self.normalize_email(email),name=name)
      #   user.is_staff=True
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email,  name, password=None):
      user = self.create_user(email=self.normalize_email(email),name=name,password=password)
      user.is_admin=True
      user.is_active=True
      user.is_staff=True
      user.is_superadmin=True
      user.save(using=self._db)
      return user


class CustomUser(AbstractBaseUser,PermissionsMixin):
   name = models.CharField(max_length=200, blank=True, null=True)
   email = models.EmailField(max_length=200, blank=True, null=True,unique=True)
   phone_number = models.BigIntegerField( blank=True, null=True,unique=True)
   otp = models.CharField(max_length=6, blank=True, null=True,unique=True)
   is_first_login = models.BooleanField(default=True)
   is_staff=models.BooleanField(default=True)
   is_active=models.BooleanField(default=True)
   is_admin=models.BooleanField(default=False)
   is_superadmin=models.BooleanField(default=False)
  
   objects = CustomUserManager()

   USERNAME_FIELD='email'
   REQUIRED_FIELDS=['password','name']

   
   def __str__(self):
      return self.email

   def has_perm(self,perm,obj=None):
      return self.is_admin

   def has_module_perms(self,add_label):
      return True

   class Meta:
       verbose_name_plural = "Create New User"
   
   
class UserToken(models.Model):
   user_id=models.IntegerField()
   token=models.CharField(max_length=235)
   created_at=models.DateTimeField(auto_now_add=True)
   expired_at=models.DateTimeField()


class userLocation(models.Model):
   location = models.CharField(max_length=200, blank=True, null=True)
   def __str__(self):
      return self.location
   class Meta:
       verbose_name_plural = "Location"

class userRole(models.Model):
   roleName = models.CharField(max_length=200, blank=True, null=True)
   def __str__(self):
      return self.roleName

   class Meta:
       verbose_name_plural = "Role"

class userDetails(models.Model):

   userName = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
   userLocation = models.ForeignKey(userLocation, on_delete=models.CASCADE, blank=True, null=True)
   userRole = models.ForeignKey(userRole, on_delete=models.CASCADE, blank=True, null=True)
   def __str__(self):
      return str(self.userName)

   class Meta:
       verbose_name_plural = "User detail"


class issueAgency(models.Model):
   agencyName = models.CharField(max_length=200, blank=True, null=True)
   def __str__(self):
      return str(self.agencyName)

   class Meta:
       verbose_name_plural = "Agency Name"

# def increment_number():
#     last_num = formData.objects.all().order_by('id').last()
#     if not last_num:
#          return '100001'
#     permit_no = last_num.permitnumber
#     # permit_int = int(permit_no.split('MAG')[-1])
#     new_permit_int = int(permit_no) + 1
#     new_permit_no = new_permit_int
#     return new_permit_no
CHOICES = (
    ("Suspend", "Suspend"),
    ("Hold", "Hold"),
    ("Terminate", "Terminate"),
    ("None", "None"),
)
# declaring a Student Model

class formData(models.Model):
   loggedPerson = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   # permitnumber = models.IntegerField(default=increment_number, blank=True, null=True)
   permitnumber = models.CharField(max_length=10, unique=True, blank=True, null=True)
   date = models.DateField()
   typeOfWork=ArrayField(models.CharField(max_length=500),blank=True, null=True)
   numberOfPerson = models.IntegerField()
   startTime = models.TimeField()
   endTime= models.TimeField()
   location = models.ForeignKey(userLocation, on_delete=models.CASCADE)
   equipment = models.CharField(max_length=200, blank=True, null=True)
   toolRequired = models.CharField(max_length=200, blank=True, null=True)
   workingAgency=models.ForeignKey(issueAgency, on_delete=models.CASCADE)
   workDescription = models.CharField(max_length=500, blank=True, null=True)
   ppeRequired = ArrayField(models.CharField(max_length=200), blank=True, null=True)
   other_ppe = models.CharField(max_length=255, blank=True, null=True, default="")

   person1 = models.ForeignKey(CustomUser, related_name="person1", on_delete=models.CASCADE)
   person2 = models.ForeignKey(CustomUser, related_name="person2", on_delete=models.CASCADE)
   person3= models.ForeignKey(CustomUser, related_name="person3", on_delete=models.CASCADE)

   verified_by_person1 = models.BooleanField(default=False, null=True)
   verified_by_person2 = models.BooleanField(default=False, null=True)
   verified_by_person3 = models.BooleanField(default=False, null=True)

   notify_person1 = models.BooleanField(default=True, null=True)
   notify_person2 = models.BooleanField(default=False, null=True)
   notify_person3 = models.BooleanField(default=False, null=True)

   newFlag = models.BooleanField(default=True, null=True,verbose_name="New Work Permit")
   oldFlag = models.BooleanField(default=False, null=True,verbose_name="Old Work Permit")
   tocloseFlag = models.BooleanField(default=False, null=True,verbose_name="Closed Work Permit")

   closedByLoggedUser = models.BooleanField(default=False,null=True)
   closedByPerson1 = models.BooleanField(default=False,null=True)
   closedByPerson2 = models.BooleanField(default=False, null=True)
   closedByPerson3 = models.BooleanField(default=False, null=True)

   completedFlag = models.BooleanField(default=False, null=True,verbose_name="Completed Work Permit")

   new_flag_date_created = models.DateField(null=True, blank=True)
   toclose_flag_date_created = models.DateField(null=True, blank=True)
   old_flag_date_created = models.DateField(null=True, blank=True)
   completed_flag_date_created = models.DateField(null=True, blank=True)

   approve_type = models.CharField(
       max_length=20,
       choices=CHOICES,
       default='None'
    )
   reason_for_status_type = models.CharField(max_length=500, blank=True, null=True)
   q1 = models.CharField(max_length=500, blank=True, null=True)
   q2 = models.CharField(max_length=500, blank=True, null=True)
   q3 = models.CharField(max_length=500, blank=True, null=True)
   q4 = models.CharField(max_length=500, blank=True, null=True)
   q5 = models.CharField(max_length=500, blank=True, null=True)
   q6 = models.CharField(max_length=500, blank=True, null=True)
   q7 = models.CharField(max_length=500, blank=True, null=True)
   q8 = models.CharField(max_length=500, blank=True, null=True)
   q9 = models.CharField(max_length=500, blank=True, null=True)
   q10 = models.CharField(max_length=500, blank=True, null=True)
   q11 = models.CharField(max_length=500, blank=True, null=True)
   q12 = models.CharField(max_length=500, blank=True, null=True)
   q13 = models.CharField(max_length=500, blank=True, null=True)
   q14 = models.CharField(max_length=500, blank=True, null=True)
   q15 = models.CharField(max_length=500, blank=True, null=True)
   q16 = models.CharField(max_length=500, blank=True, null=True)
   q17 = models.CharField(max_length=500, blank=True, null=True)

   rejectFlag = models.BooleanField(default=False, null=True, verbose_name="Rejected Work Permit")
   rejected_flag_date_created = models.DateField(null=True, blank=True)
   reject_reason = models.CharField(max_length=255, blank=True, null=True, default="None")

   created_at = models.DateField(auto_now_add=True)

   def save(self, *args, **kwargs):
       if self.newFlag == True and self.new_flag_date_created is None:
           self.new_flag_date_created = datetime.now()

       if self.oldFlag == True and self.old_flag_date_created is None:
           self.old_flag_date_created = datetime.now()

       if self.tocloseFlag == True and self.toclose_flag_date_created is None:
           self.toclose_flag_date_created = datetime.now()

       if self.completedFlag == True and self.completed_flag_date_created is None:
           self.completed_flag_date_created = datetime.now()

       if self.rejectFlag == True and self.rejected_flag_date_created is None:
           self.rejected_flag_date_created = datetime.now()

       super(formData, self).save(*args, **kwargs)

   def __str__(self): 
      return str(self.pk)

   class Meta:
       verbose_name_plural = "Work Permit"


class fcmTokenFirebase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=500,blank=True, null=True)
    device_id = models.CharField(max_length=255,blank=True, null=True)
    type = models.CharField(max_length=255,blank=True, null=True)
    language = models.CharField(max_length=255,blank=True, null=True)


class UserSession(models.Model):
    login_id= models.CharField(max_length=255,blank=True, null=True)
    current_login_user_email = models.CharField(max_length=255,blank=True, null=True)
    permit_id = models.CharField(max_length=255,blank=True, null=True)
    permit_initiator=models.CharField(max_length=255,blank=True, null=True)
    hod_id = models.CharField(max_length=255, blank=True, null=True)
    hod_encharge=models.CharField(max_length=255,blank=True, null=True)
    he_she_id = models.CharField(max_length=255, blank=True, null=True)
    he_she = models.CharField(max_length=255,blank=True, null=True)
    contractor_id = models.CharField(max_length=255, blank=True, null=True)
    contractor = models.CharField(max_length=255,blank=True, null=True)

class NotificationForUser(models.Model):
    user_name = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    form_id = models.ForeignKey(formData,on_delete=models.CASCADE)
    new_notification=models.BooleanField(default=False,null=True)
    close_notification=models.BooleanField(default=False,null=True)
    complete_notification=models.BooleanField(default=False,null=True)
    reject_notification = models.BooleanField(default=False, null=True)
    verified_by_all = models.BooleanField(default=False, null=True)
    closed_by_all = models.BooleanField(default=False, null=True)
    message = models.CharField(default="", max_length=255)

    def __str__(self):
        return self.user_name

class PermitNumber(models.Model):
    permit_number = models.IntegerField(unique=True)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)