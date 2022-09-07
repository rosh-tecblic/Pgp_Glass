from rest_framework import serializers
from .models import *

class userLoginSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200)
    phone_number = serializers.CharField(max_length=200)

    class Meta:
        model = CustomUser
        fields= ['id','name','email','password','phone_number']

    def create(self, validated_data):
        return CustomUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

class userLocationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=200)
    class Meta:
        model = userLocation
        fields=['id','location']

    def create(self, validated_data):
        return userLocation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location',instance.location)
        instance.save()
        return instance

class userRoleSerializer(serializers.ModelSerializer):
    # user_role = serializers.PrimaryKeyRelatedField(read_only=False,
    #                                                queryset=userDetails.objects.all())
    roleName = serializers.CharField(max_length=200)
    class Meta:
        model = userRole
        fields=['id','roleName']

    def create(self, validated_data):
        return userRole.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.roleName = validated_data.get('roleName',instance.roleName)
        instance.save()
        return instance 

class userDetailSerializer(serializers.ModelSerializer):
    userName = serializers.SlugRelatedField(read_only=False,slug_field="name",
                                                   queryset=CustomUser.objects.all())
    userLocation = serializers.SlugRelatedField(read_only=False,slug_field="location",
                                                   queryset=userLocation.objects.all())
    userRole = serializers.SlugRelatedField(read_only=False,slug_field="roleName",
                                                   queryset=userRole.objects.all())

    class Meta:
        model = userDetails
        fields=('id','userName','userLocation','userRole')
        depth=1

    def create(self, validated_data):
        return userDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.userName = validated_data.get('userName',instance.userName)
        instance.userLocation = validated_data.get('userLocation', instance.userLocation)
        instance.userRole = validated_data.get('userRole', instance.userRole)
        instance.save()
        return instance

class issueAgencySerializer(serializers.ModelSerializer):
    agencyName = serializers.CharField(max_length=200)
    class Meta:
        model = issueAgency
        fields = ('id', 'agencyName')

    def create(self, validated_data):
        return issueAgency.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.agencyName = validated_data.get('agencyName',instance.agencyName)
        instance.save()
        return instance

class formDataSerializer(serializers.ModelSerializer):
    loggedPerson = serializers.SlugRelatedField(read_only=False,slug_field="name",
                                                   queryset=CustomUser.objects.all())
    date = serializers.DateField()
    typeOfWork = serializers.ListField(max_length=500)
    numberOfPerson = serializers.IntegerField()
    startTime = serializers.TimeField()
    endTime = serializers.TimeField()
    location = serializers.SlugRelatedField(read_only=False,slug_field="location",
                                                   queryset=userLocation.objects.all())
    equipment = serializers.CharField(max_length=200)
    toolRequired = serializers.CharField(max_length=200)
    workingAgency = serializers.SlugRelatedField(read_only=False,slug_field="agencyName",
                                                   queryset=issueAgency.objects.all())
    workDescription = serializers.CharField(max_length=500)
    ppeRequired = serializers.ListField(max_length=200)
    other_ppe = serializers.CharField(max_length=255,default="",allow_blank=True)
    person1 = serializers.SlugRelatedField(read_only=False,slug_field="name",
                                                   queryset=CustomUser.objects.all())
    person2 = serializers.SlugRelatedField(read_only=False,slug_field="name",
                                                   queryset=CustomUser.objects.all())
    person3 = serializers.SlugRelatedField(read_only=False,slug_field="name",
                                                   queryset=CustomUser.objects.all())

    permitnumber = serializers.CharField(max_length=500)

    q1 = serializers.CharField(default="",allow_blank=True)
    q2 = serializers.CharField(default="",allow_blank=True)
    q3 = serializers.CharField(default="",allow_blank=True)
    q4 = serializers.CharField(default="",allow_blank=True)
    q5 = serializers.CharField(default="",allow_blank=True)
    q6 = serializers.CharField(default="",allow_blank=True)
    q7 = serializers.CharField(default="",allow_blank=True)
    q8 = serializers.CharField(default="",allow_blank=True)
    q9 = serializers.CharField(default="",allow_blank=True)
    q10 = serializers.CharField(default="",allow_blank=True)
    q11 = serializers.CharField(default="",allow_blank=True)
    q12 = serializers.CharField(default="",allow_blank=True)
    q13 = serializers.CharField(default="",allow_blank=True)
    q14 = serializers.CharField(default="",allow_blank=True)
    q15 = serializers.CharField(default="",allow_blank=True)
    q16 = serializers.CharField(default="",allow_blank=True)
    q17 = serializers.CharField(default="",allow_blank=True)

    class Meta:
        model = formData
        fields = ('id','permitnumber','loggedPerson','date','typeOfWork','numberOfPerson','startTime','endTime','location',
                 'equipment','toolRequired','workingAgency','workDescription','ppeRequired','other_ppe',
                 'person1','person2', 'person3','closedByLoggedUser','closedByPerson1','closedByPerson2','closedByPerson3',
                  'verified_by_person1','verified_by_person2','verified_by_person3','reject_reason',
                  'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12',
                  'q13', 'q14', 'q15','q16','q17')

    def create(self, validated_data):
        return formData.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.date = validated_data.get('date',instance.date)
        instance.typeOfWork = validated_data.get('typeOfWork', instance.typeOfWork)
        instance.numberOfPerson = validated_data.get('numberOfPerson', instance.numberOfPerson)
        instance.startTime = validated_data.get('startTime', instance.startTime)
        instance.endTime = validated_data.get('endTime', instance.endTime)
        instance.location = validated_data.get('location', instance.location)
        instance.equipment = validated_data.get('equipment', instance.equipment)
        instance.toolRequired = validated_data.get('toolRequired', instance.toolRequired)
        instance.workDescription = validated_data.get('workDescription', instance.workDescription)
        instance.workingAgency = validated_data.get('workingAgency', instance.workingAgency)
        instance.ppeRequired = validated_data.get('ppeRequired', instance.ppeRequired)
        instance.other_ppe = validated_data.get('other_ppe', instance.other_ppe)
        instance.q1 = validated_data.get('q1', instance.q1)
        instance.q2 = validated_data.get('q2', instance.q2)
        instance.q3 = validated_data.get('q3', instance.q3)
        instance.q4 = validated_data.get('q4', instance.q4)
        instance.q5 = validated_data.get('q5', instance.q5)
        instance.q6 = validated_data.get('q6', instance.q6)
        instance.q7 = validated_data.get('q7', instance.q7)
        instance.q8 = validated_data.get('q8', instance.q8)
        instance.q9 = validated_data.get('q9', instance.q9)
        instance.q10 = validated_data.get('q10', instance.q10)
        instance.q11 = validated_data.get('q11', instance.q11)
        instance.q12 = validated_data.get('q12', instance.q12)
        instance.q13 = validated_data.get('q13', instance.q13)
        instance.q14 = validated_data.get('q14', instance.q14)
        instance.q15 = validated_data.get('q15', instance.q15)
        instance.q16 = validated_data.get('q16', instance.q16)
        instance.q17 = validated_data.get('q17', instance.q17)
        instance.save()
        return instance

class UserSessionSerializer(serializers.ModelSerializer):
    login_id= serializers.CharField()
    current_login_user_email = serializers.CharField()
    permit_id = serializers.CharField()
    permit_initiator=serializers.CharField()
    hod_id = serializers.CharField()
    hod_encharge=serializers.CharField()
    he_she_id = serializers.CharField()
    he_she = serializers.CharField()
    contractor_id = serializers.CharField()
    contractor = serializers.CharField()

    class Meta:
        model = formData
        fields = ('id','login_id','current_login_user_email','permit_id','permit_initiator',
                  'hod_id','hod_encharge','he_she_id','he_she','contractor_id','contractor')

    def create(self, validated_data):
        return UserSession.objects.create(**validated_data)

class NotificationForUserSerializer(serializers.ModelSerializer):
    user_name = serializers.SlugRelatedField(read_only=False,slug_field="name",
                                                   queryset=CustomUser.objects.all())

    form_id = formDataSerializer()
    new_notification=serializers.BooleanField(default=False)
    close_notification=serializers.BooleanField(default=False)
    complete_notification=serializers.BooleanField(default=False)
    reject_notification = serializers.BooleanField(default=False)
    verified_by_all = serializers.BooleanField(default=False)
    closed_by_all = serializers.BooleanField(default=False)
    message = serializers.CharField(default="")

    class Meta:
        model = NotificationForUser
        fields = ('id','user_name','form_id','new_notification','close_notification',
                  'reject_notification','verified_by_all','closed_by_all','complete_notification','message')

    def create(self, validated_data):
        return NotificationForUser.objects.create(**validated_data)

class PermitNumberSerializer(serializers.ModelSerializer):
    permit_number = serializers.IntegerField()

    class Meta:
        model = PermitNumber
        fields = ('id','permit_number')

    def create(self, validated_data):
        return PermitNumber.objects.create(**validated_data)


class FAQSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    answer = serializers.CharField()

    class Meta:
        model = FAQ
        fields = ('id','question','answer')

    def create(self, validated_data):
        return FAQ.objects.create(**validated_data)


class chartSerializer(serializers.Serializer):
    new_flag_count = serializers.IntegerField()
    toclose_flag_count = serializers.IntegerField()
    old_flag_count = serializers.IntegerField()
    completed_flag_count = serializers.IntegerField()
    rejected_flag_count=serializers.IntegerField()

    class Meta:
        fields=('new_flag_count','toclose_flag_count',
                'old_flag_count','completed_flag_count','rejected_flag_count')
