import datetime
from datetime import timedelta
from twilio.rest import Client
import json
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_201_CREATED, \
    HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
import random
from PGPapi.authentication import JWTAuthentication, create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
from .serializers import *
from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework import permissions,exceptions
from rest_framework.permissions import IsAuthenticated
import requests
from .utils import *
# import pandas as pd
# Create your views here.

############# GET and POST REQUEST of userLocation MODEL ##############
try:
    def sendLiveNotification(token, body, title):
        payload = json.dumps({
            "to": token,
            "notification": {
                "body": body,
                "title": title
            }
        })

        headers = {
            'Authorization': 'key=AAAA41ZwfDE:APA91bERbr6SPGDhG15WB4000Kz919cXhdPA0dlAZus5e5go_waeiHs11fU4bExoJsVt6riIsxr6JtKfIdlkPtraEz2BBoPVGXbanValVH_Fswr05qjHaa0ZYni_ak4EqlGTVZliUYx3',
            'Content-Type': 'application/json'
        }
        sendnotification = requests.post('https://fcm.googleapis.com/fcm/send', data=payload, headers=headers)
        return sendnotification

    class userLocationApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args,**kwargs):
            print(request.user.id)
            get_language_from_query_string = request.GET.get('language')

            print('e',request.user)
            try:
                user_location= userLocation.objects.all()
                get_userlocation_data = userLocationSerializer(user_location, many=True)

                if get_language_from_query_string == 'hi_IN':
                    return JsonResponse({'data':get_userlocation_data.data,'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                else:
                    return JsonResponse({'data': get_userlocation_data.data, 'status': HTTP_200_OK}, safe=False,
                                        status=HTTP_200_OK)

            except:
                return JsonResponse({'error':get_userlocation_data.errors,'status':HTTP_400_BAD_REQUEST},status=HTTP_400_BAD_REQUEST)


        def post(self, request, *args,**kwargs):
            serializer=userLocationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  JsonResponse({'msg':'Data Created','status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    ############# GET, UPDATE, DELETE from ID of userLocation MODEL ##############
    class userLocationIDApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get_object(self, id):
            try:
                return userLocation.objects.get(pk=id)
            except userLocation.DoesNotExist:
                return JsonResponse(status=HTTP_400_BAD_REQUEST)

        def post(self, request, id,*args,**kwargs):
            location= self.get_object(id)
            serializer = userLocationSerializer(location, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data, 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def get(self, request, id):
            locationobj = self.get_object(id)
            serializer = userLocationSerializer(locationobj)
            return JsonResponse(serializer.data)

        def put(self, request, id,*args,**kwargs):
            user_location= self.get_object(id)
            serializer = userLocationSerializer(user_location, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data, 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def delete(self, request,id):
            deleteobj = self.get_object(id)
            deleteobj.delete()
            return JsonResponse({'msg':'Data Deleted','status':HTTP_204_NO_CONTENT},status=HTTP_204_NO_CONTENT)

    ############# GET and POST REQUEST of userRole MODEL ##############
    class userRoleApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args,**kwargs):
            try:
                user_role= userRole.objects.all()
                get_userRole_data = userRoleSerializer(user_role, many=True)
                return JsonResponse({'data':get_userRole_data.data,'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)
            except:
                return JsonResponse({'data': get_userRole_data.errors, 'status': HTTP_401_UNAUTHORIZED}, safe=False, status=HTTP_401_UNAUTHORIZED)

        def post(self, request, *args,**kwargs):
            serializer=userRoleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  JsonResponse({'msg':'Data Created', 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    ############# GET, UPDATE, DELETE from ID of userRole MODEL ##############
    class userRoleIDApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get_object(self, id):
            try:
                return userRole.objects.get(pk=id)
            except userRole.DoesNotExist:
                return JsonResponse(status=HTTP_400_BAD_REQUEST)

        def get(self, request, id):
            roleobj = self.get_object(id)
            serializer = userRoleSerializer(roleobj)
            return JsonResponse({'data':serializer.data,'status':HTTP_200_OK}, status=HTTP_200_OK)

        def post(self, request, id,*args,**kwargs):
            user_role= self.get_object(id)
            serializer = userRoleSerializer(user_role, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data,'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def put(self, request, id,*args,**kwargs):
            userRole= self.get_object(id)
            serializer = userRoleSerializer(userRole, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data,'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def delete(self, request,id):
            deleteobj = self.get_object(id)
            deleteobj.delete()
            return JsonResponse({'msg':'Data Deleted','status':HTTP_204_NO_CONTENT},status=HTTP_204_NO_CONTENT)

    # ############# GET and POST REQUEST of userDetails MODEL ##############
    # class userLoginApiView(APIView):
    #     def get(self, request, *args,**kwargs):
    #         user_login= CustomUser.objects.all()
    #         get_userdetail_data = userLoginSerializer(user_login, many=True)
    #         return JsonResponse(get_userdetail_data.data, safe=False, status=HTTP_200_OK)
    #
    #     def post(self, request, *args,**kwargs):
    #         serializer=userLoginSerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return  JsonResponse({'msg':'Data Created'}, status=HTTP_201_CREATED)
    #         return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
    #
    # ############# GET, UPDATE, DELETE from ID of userDetails MODEL ##############
    # class userLoginIDApiView(APIView):
    #     def get_object(self, id):
    #         try:
    #             return CustomUser.objects.get(pk=id)
    #         except CustomUser.DoesNotExist:
    #             return JsonResponse(status=HTTP_400_BAD_REQUEST)
    #
    #     def post(self, request, id,*args,**kwargs):
    #         user_login= self.get_object(id)
    #         serializer = userLoginSerializer(user_login, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return JsonResponse(serializer.data, status=HTTP_201_CREATED)
    #         return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
    #
    #     def get(self, request, id):
    #         getobj = self.get_object(id)
    #         serializer = userLoginSerializer(getobj)
    #         return JsonResponse(serializer.data, status=HTTP_200_OK)
    #
    #     def put(self, request, id,*args,**kwargs):
    #         userLogin= self.get_object(id)
    #         serializer = userLoginSerializer(userLogin, data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return JsonResponse(serializer.data, status=HTTP_201_CREATED)
    #         return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
    #
    #     def delete(self, request,id):
    #         deleteobj = self.get_object(id)
    #         deleteobj.delete()
    #         return JsonResponse({'msg':'Data Deleted'},status=HTTP_204_NO_CONTENT)

    ############# GET and POST REQUEST of userDetails MODEL ##############
    class userDetailApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args,**kwargs):
            try:
                user_detail= userDetails.objects.all()
                get_userdetail_data = userDetailSerializer(user_detail, many=True)
                return JsonResponse({'data':get_userdetail_data.data, 'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)
            except:
                return JsonResponse({'error': get_userdetail_data.errors, 'status': HTTP_400_BAD_REQUEST}, safe=False,
                                    status=HTTP_400_BAD_REQUEST)

        def post(self, request, *args,**kwargs):
            serializer=userDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return  JsonResponse({'msg':'Data Created', 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    ############# GET, UPDATE, DELETE from ID of userDetails MODEL ##############
    class userDetailIDApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get_object(self, id):
            try:
                return userDetails.objects.get(pk=id)
            except userDetails.DoesNotExist:
                return JsonResponse(status=HTTP_400_BAD_REQUEST)

        def get(self, request, id):
            getobj = self.get_object(id)
            serializer = userDetailSerializer(getobj)
            return JsonResponse({'data':serializer.data,'status':HTTP_200_OK}, status=HTTP_200_OK)

        def post(self, request, id,*args,**kwargs):
            user_detail= self.get_object(id)
            serializer = userDetailSerializer(user_detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data,'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def put(self, request, id,*args,**kwargs):
            userDetail= self.get_object(id)
            serializer = userDetailSerializer(userDetail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data, 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def delete(self, request,id):
            deleteobj = self.get_object(id)
            deleteobj.delete()
            return JsonResponse({'msg':'Data Deleted','status':HTTP_204_NO_CONTENT},status=HTTP_204_NO_CONTENT)



    ############# GET and POST REQUEST of Form MODEL ##############
    class formDataApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args,**kwargs):
            form_data= formData.objects.all()
            get_from_data = formDataSerializer(form_data, many=True)
            return JsonResponse({'data':get_from_data.data, 'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)

        def post(self, request):
            data={
                    "loggedPerson":request.user.name,
                    "permitnumber": request.data['permitnumber'],
                    "date":request.data['date'],
                    "typeOfWork":request.data['typeOfWork'],
                    "numberOfPerson":request.data['numberOfPerson'],
                    "startTime": request.data['startTime'],
                    "endTime":request.data['endTime'] ,
                    "location":request.data['location']  ,
                    "equipment": request.data['equipment'],
                    "toolRequired":request.data['toolRequired'],
                    "workingAgency": request.data['workingAgency'],
                    "workDescription": request.data['workDescription'],
                    "ppeRequired": request.data['ppeRequired'],
                    "other_ppe": request.data['other_ppe'],
                    "person1": request.data['person1'],
                    "person2":request.data['person2'],
                    "person3":request.data['person3'],

                    "q1": request.data['q1'],
                    "q2": request.data['q2'],
                    "q3": request.data['q3'],
                    "q4": request.data['q4'],
                    "q5": request.data['q5'],
                    "q6": request.data['q6'],
                    "q7": request.data['q7'],
                    "q8": request.data['q8'],
                    "q9": request.data['q9'],
                    "q10": request.data['q10'],
                    "q11": request.data['q11'],
                    "q12": request.data['q12'],
                    "q13": request.data['q13'],
                    "q14": request.data['q14'],
                    "q15": request.data['q15'],
                    "q16": request.data['q16'],
                    "q17": request.data['q17'],
            }
            print("----------------------------------------------------------------", request.data['permitnumber'])
            try:
                permit_number_exists = formData.objects.get(permitnumber=request.data['permitnumber'])
                print("----------------------------------------------------------------",permit_number_exists)
                return JsonResponse({'msg':'Permit Number Already Exists.', 'status':HTTP_400_BAD_REQUEST},
                                    status=HTTP_400_BAD_REQUEST)

            except formData.DoesNotExist:
                serializer = formDataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                    user_name = CustomUser.objects.get(name=request.data['person1'])

                    # print('CCCCCCC',b['fcm_token'])

                    form_id = formData.objects.get(id=serializer.data['id'])
                    NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                                                       new_notification=True, message="Waiting For Your Approvement")

                    desc=request.data['workDescription']

                    get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                    if get_fcm_token is not None:
                        response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                            f'{desc[0:90]}.........', 'Work Permit For Verification')
                        print("Verification Response",response_notification)
                    else:
                        print("PLEASE PASS FCM TOKEN")

                    return JsonResponse({'msg': 'Form Created','status':HTTP_200_OK}, status=HTTP_200_OK)

                return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    ############# GET, UPDATE, DELETE from ID of FORM MODEL ##############
    class formDataIDApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get_object(self, id):
            try:
                print("ID ++++", id)
                return formData.objects.get(pk=id)

            except formData.DoesNotExist:
                return JsonResponse(status=HTTP_400_BAD_REQUEST)

        def get(self, request, id):
            getobj = self.get_object(id)
            serializer = formDataSerializer(getobj)
            return JsonResponse(serializer.data, status=HTTP_200_OK)

        def put(self, request, id,*args,**kwargs):
            formDetail= self.get_object(id)
            print('FORMDATA === ', formDetail)
            serializer = formDataSerializer(formDetail, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data, 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors, 'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def post(self, request, id,*args,**kwargs):
            formDetail= self.get_object(id)
            serializer = formDataSerializer(formDetail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data, 'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def delete(self, request,id):
            deleteobj = self.get_object(id)
            deleteobj.delete()
            return JsonResponse({'msg':'Data Deleted','status':HTTP_204_NO_CONTENT},status=HTTP_204_NO_CONTENT)

    ############# GET and POST REQUEST of AGENCY MODEL ##############
    class agencyNameApiView(APIView):
        # authentication_classes = [JWTAuthentication]
        # permission_classes= [IsAuthenticated]
        def get(self, request, *args,**kwargs):
            agency_data= issueAgency.objects.all()
            get_agency_data = issueAgencySerializer(agency_data, many=True)
            return JsonResponse({'data':get_agency_data.data,'status':HTTP_200_OK}, safe=False,status=HTTP_200_OK)

        def post(self, request):
            serializer = issueAgencySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg': 'Data Created','status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    ############# GET, UPDATE, DELETE from ID of AGENCY MODEL ##############
    class issueAgencyDetailsApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get_object(self, id):
            try:
                return issueAgency.objects.get(pk=id)
            except issueAgency.DoesNotExist:
                return JsonResponse({'status':HTTP_400_BAD_REQUEST},status=HTTP_400_BAD_REQUEST)

        def get(self, request, id):
            getobj = self.get_object(id)
            serializer = issueAgencySerializer(getobj)
            return JsonResponse({'data':serializer.data,'status':HTTP_200_OK}, status=HTTP_200_OK)

        def post(self, request, id,*args,**kwargs):
            issue_agency= self.get_object(id)
            serializer = issueAgencySerializer(issue_agency, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data,'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def put(self, request, id,*args,**kwargs):
            issueAgencyDetail= self.get_object(id)
            serializer = issueAgencySerializer(issueAgencyDetail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data':serializer.data,'status':HTTP_201_CREATED}, status=HTTP_201_CREATED)
            return JsonResponse({'error':serializer.errors,'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

        def delete(self, request,id):
            deleteobj = self.get_object(id)
            deleteobj.delete()
            return JsonResponse({'msg':'Data Deleted','status':HTTP_204_NO_CONTENT},status=HTTP_204_NO_CONTENT)

    ############# FILTER DATA ACCORDING TO THE LOCATION SELECTED ##############
    class filterApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, locationname, *args, **kwargs):
            get_language_from_query_string = request.GET.get('language')

            try:
                loc =  userLocation.objects.get(location=locationname)

                user_details = userDetails.objects.filter(userLocation=loc.id)
                userDetail = userDetailSerializer(user_details, many=True)
                role1 = userDetails.objects.filter(userLocation=loc.id, userRole=1)
                role1_serializer = userDetailSerializer(role1, many=True)

                role2 = userDetails.objects.filter(userLocation=loc.id, userRole=2)
                role2_serializer = userDetailSerializer(role2, many=True)

                role3 = userDetails.objects.filter(userLocation=loc.id, userRole=3)
                role3_serializer = userDetailSerializer(role3, many=True)

                role4 = userDetails.objects.filter(userLocation=loc.id, userRole=4)
                role4_serializer = userDetailSerializer(role4, many=True)

                role = {
                    'permit_initiator': role1_serializer.data,
                    'area_owner': role2_serializer.data,
                    'contractor': role3_serializer.data,
                    'she_hes': role4_serializer.data
                }
                if get_language_from_query_string == 'hi_IN':
                    return JsonResponse({'role': role}, safe=False, status=HTTP_200_OK)
                else:
                    return JsonResponse({'role': role}, safe=False, status=HTTP_200_OK)
            except:
                return JsonResponse({'error': userDetail.errors, 'status': HTTP_400_BAD_REQUEST}, safe=False, status=HTTP_400_BAD_REQUEST)

    ############# FILTER DATA ACCORDING TO THE NEWFLAG SELECTED ##############
    class newFlagApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args, **kwargs):
            # #logged_person = CustomUser.objects.get(name=name)
            # form_data = formData.objects.filter(loggedPerson=request.user.id, newFlag = True)
            # serializer = formDataSerializer(form_data, many=True)
            # return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)
            try:
                get_language_from_query_string = request.GET.get('language')
                form_data = formData.objects.all().values()
                print("******************************",form_data)
                for data in form_data:
                    print('*****',request.user.id)
                    print('*************',data['loggedPerson_id'])
                    
                    if request.user.id == data['loggedPerson_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,newFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status = HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status = HTTP_200_OK)

                    if request.user.id == data['person1_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,newFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)


                    if request.user.id == data['person2_id']:
                        form_data = formData.objects.filter(newFlag=True, verified_by_person2=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person3_id']:
                        form_data = formData.objects.filter(newFlag=True, verified_by_person3=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
            except:
                return JsonResponse({'status':HTTP_400_BAD_REQUEST},status=HTTP_400_BAD_REQUEST)

    class oldFlagApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args, **kwargs):
            try:
                get_language_from_query_string = request.GET.get('language')
                form_data = formData.objects.all().values()
                print("******************************",form_data)
                for data in form_data:
                    print('*************',request.user.id)
                    print('*************',data['loggedPerson_id'])
                    if request.user.id == data['loggedPerson_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,oldFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person1_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,oldFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)


                    if request.user.id == data['person2_id']:
                        form_data = formData.objects.filter(person2 = request.user.id,oldFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person3_id']:
                        form_data = formData.objects.filter(person3 = request.user.id, oldFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)                
            except:
                return JsonResponse({'status':HTTP_400_BAD_REQUEST},status=HTTP_400_BAD_REQUEST)



            # get_language_from_query_string = request.GET.get('language')
            # try:
            #     form_data = formData.objects.filter(loggedPerson=request.user.id, oldFlag = True)
            #     serializer = formDataSerializer(form_data, many=True)
            #     if get_language_from_query_string=='hi_IN':
            #         return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, safe=False,
            #                             status=HTTP_200_OK)
            #     else:
            #         return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
            #                             status=HTTP_200_OK)
            #
            # except:
            #     return JsonResponse({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST}, safe=False, status=HTTP_400_BAD_REQUEST)

    class completedFlagApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args, **kwargs):

            try:
                get_language_from_query_string = request.GET.get('language')
                form_data = formData.objects.all().values()
                print("******************************",form_data)
                for data in form_data:
                    print('*************',request.user.id)
                    print('*************',data['loggedPerson_id'])
                    if request.user.id == data['loggedPerson_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,
                                                            completedFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person1_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,
                                                            completedFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person2_id']:
                        form_data = formData.objects.filter(person2=request.user.id,
                                                            completedFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person3_id']:
                        form_data = formData.objects.filter(person3=request.user.id,
                                                            completedFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
            except:
                return JsonResponse({'status':HTTP_400_BAD_REQUEST},status=HTTP_400_BAD_REQUEST)

            # get_language_from_query_string = request.GET.get('language')
            # try:
            #     form_data = formData.objects.filter(loggedPerson=request.user.id, completedFlag=True)
            #     print("**************************************",form_data)
            #     serializer = formDataSerializer(form_data, many=True)
            #     if get_language_from_query_string == 'hi_IN':
            #         return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
            #                             status=HTTP_200_OK)
            #     else:
            #         return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
            #                             status=HTTP_200_OK)
            # except:
            #     return JsonResponse({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST},
            #                         safe=False, status=HTTP_400_BAD_REQUEST)

    class closeFlagApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args, **kwargs):
            try:
                get_language_from_query_string = request.GET.get('language')
                form_data = formData.objects.all().values()
                print("******************************",form_data)
                for data in form_data:
                    print('*************',request.user.id)
                    print('*************',data['person2_id'])
                    if request.user.id == data['loggedPerson_id']:
                        form_data = formData.objects.filter(loggedPerson=request.user.id,
                                                            tocloseFlag=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person1_id']:
                        form_data = formData.objects.filter(tocloseFlag=True,
                                                            loggedPerson=request.user.id).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person2_id']:
                        form_data = formData.objects.filter(tocloseFlag=True,
                                                            closedByPerson2=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)

                    if request.user.id == data['person3_id']:
                        form_data = formData.objects.filter(tocloseFlag=True,
                                                            closedByPerson3=True).order_by('-id')
                        serializer = formDataSerializer(form_data, many=True)
                        if get_language_from_query_string == 'hi_IN':
                                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
                        else:
                            return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
                                                    status=HTTP_200_OK)
            except:
                return JsonResponse({'status':HTTP_400_BAD_REQUEST},status=HTTP_400_BAD_REQUEST)

            # get_language_from_query_string = request.GET.get('language')
            # try:
            #     form_data = formData.objects.filter(loggedPerson=request.user.id, tocloseFlag = True)
            #     serializer = formDataSerializer(form_data, many=True)
            #     if get_language_from_query_string == 'hi_IN':
            #         return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, safe=False,
            #                             status=HTTP_200_OK)
            #     else:
            #         return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False,
            #                             status=HTTP_200_OK)
            # except:
            #     return JsonResponse({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST},
            #                         safe=False, status=HTTP_400_BAD_REQUEST)

    # class notification(APIView):
    #     authentication_classes = [JWTAuthentication]
    #     permission_classes= [IsAuthenticated]
    #     def get(self, request):
    #         notification_data = formData.objects.filter(person1=request.user.id)
    #         if notification_data != None:
    #             form_filter_data = formDataSerializer(notification_data, many=True)
    #             return JsonResponse(form_filter_data.data, safe=False, status=HTTP_200_OK)
    #         else:
    #             return JsonResponse({"msg":"PROBLEM IN GET"}, status=HTTP_400_BAD_REQUEST)

    class notificationToVerifyApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request, *args, **kwargs):
            try:
                print("USERID============",request.user.id )
                notification_data = formData.objects.filter(Q(person1 = request.user.id, notify_person1=True) |
                                                            Q(person2 = request.user.id,  notify_person2=True)
                                                            )
                serializer = formDataSerializer(notification_data, many=True)
                return JsonResponse({'data':serializer.data , 'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)
            except:
                return JsonResponse({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST},
                                    safe=False, status=HTTP_400_BAD_REQUEST)

    class notificationToCloseAPiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def get(self, request, *args, **kwargs):
            print("USERID============", request.user.id)
            try:
                notification_data = formData.objects.filter(
                    Q(person1=request.user.id, closedByLoggedUser=True) |
                    Q(person2=request.user.id, closedByPerson1=True)
                )
                serializer = formDataSerializer(notification_data, many=True)
                return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, safe=False, status=HTTP_200_OK)
            except:
                return JsonResponse({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST},
                                    safe=False, status=HTTP_400_BAD_REQUEST)


    class changeOldFlagApiView(APIView):
        # authentication_classes = [JWTAuthentication]
        # permission_classes= [IsAuthenticated]
        def get(self, request):

            try:
                form_data = formData.objects.all()
                for data in form_data:
                    date_after_1_days = data.created_at + timedelta(days=1)
                    if date.today() >=date_after_1_days and data.oldFlag==False and \
                            data.tocloseFlag==False and data.completedFlag==False:

                        formData.objects.filter(id=data.id).update(oldFlag=True ,newFlag=False, tocloseFlag=False,
                                                                   completedFlag=False)
                return JsonResponse({"msg":"Old Flag Changed", 'status':HTTP_200_OK}, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    class changeToCloseFlagApiView(APIView):
        # authentication_classes = [JWTAuthentication]
        # permission_classes = [IsAuthenticated]

        def get(self, request):
            try:
                form_data = formData.objects.all()
                print(form_data)
                for data in form_data:
                    date_after_6_days = data.created_at + timedelta(days=6)
                    print("*********6567766",data.created_at)
                    print("***********",date_after_6_days)
                    print("***********1233",date.today())
                    if date.today() >=date_after_6_days and data.tocloseFlag==False and\
                            data.completedFlag==False:

                        print("hi------------")
                        formData.objects.filter(id=data.id).update(tocloseFlag=True, oldFlag=False, newFlag=False,
                                                                   completedFlag=False)
                return JsonResponse({"msg": "Close Flag Changed", "status":HTTP_200_OK}, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

            # try:
            #     form_data = formData.objects.all()
            #     for data in form_data:
            #         print("DATA======================",data.created_at)
            #         date_after_6_days = data.created_at + timedelta(days=6)
            #         print("DATE 6 days=============",date_after_6_days)
            #         print("Todays DATE =============", datetime.date.today())
            #         if datetime.date.today() >=date_after_6_days  :
            #            print("***************************************************",data.id)
            #            formData.objects.filter(id=data.id).update(tocloseFlag=True, oldFlag=False ,newFlag=False,
            #                                                       completedFlag=False)
            #     return JsonResponse({"msg":"To Close Flag Changed", 'status':HTTP_200_OK}, status=HTTP_200_OK)
            # except:
            #     return JsonResponse({"error": "Flag Not Changed",
            #                          'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    class changeCompleteFlagApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self,request):
            try:
                form_data=formData.objects.filter(tocloseFlag=True,person1=request.user.id)
                for data in form_data:
                    formData.objects.filter(id=data.id).update(completedFlag=True)
                return JsonResponse({"msg":"Completed Flag Changed", 'status':HTTP_200_OK}, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    # class closedByLoggedUserApiView(APIView):
    #     authentication_classes = [JWTAuthentication]
    #     permission_classes= [IsAuthenticated]
    #     def get(self,request,id):
    #         endTime = request.data.get('endTime')
    #         form_data=formData.objects.filter(tocloseFlag=True,loggedPerson=request.user.id)
    #         formData.objects.filter(id=id).update(closedByLoggedUser=True,endTime=endTime)
    #         return JsonResponse({"msg":"Closed By Logged User", 'status':HTTP_200_OK}, status=HTTP_200_OK)

    class approvedByPersonFormApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request,id):
            get_status = request.GET.get('get_status')
            remark = request.GET.get('remark')

            print('STATUS', get_status)
            form_data = formData.objects.filter(id=id).values()
            for data in form_data:
                print("jfhijrgijhijioy*************************8",data['id'])
                if request.user.id == data['person1_id']:

                    formData.objects.filter(id=data['id']).update(verified_by_person1=True,
                                                                      notify_person2=True,notify_person1=False)

                    user_name = CustomUser.objects.get(id=data['person2_id'])
                    print("USER",user_name.name)

                    person1_name= CustomUser.objects.get(id=data['person1_id'])


                    form_id = formData.objects.get(id=data['id'])
                    NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                                                       new_notification=True,
                                                       message="Waiting For Your Approvement")

                    NotificationForUser.objects.filter(user_name_id=person1_name.id,
                                                       form_id=form_id).update(message='Approved By You')


                    desc = data['workDescription']

                    print(desc)
                    get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                    if get_fcm_token is not None:
                        print("FCM TOKEN GET===============",get_fcm_token)
                        response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                     f'{desc[0:90]}.........',
                                                                     'Work Permit For Verification')
                        print("Verification Response",response_notification)
                    else:
                        print('PLEASE PASS FCM TOKEN')

                    return JsonResponse({'msg': 'Verified','status':HTTP_200_OK}, status=HTTP_200_OK)

                if request.user.id == data['person2_id']:
                    if get_status !=None:
                        if get_status == 'Suspend':
                            new_permit_data = formData.objects.last()
                            number = int(new_permit_data.permitnumber) + 1
                            print(number)
                            form_data = formData.objects.get(id=data['id'])

                            formData.objects.create(
                                permitnumber=number, loggedPerson=form_data.loggedPerson,date=form_data.date,
                                typeOfWork = form_data.typeOfWork,
                                numberOfPerson = form_data.numberOfPerson, startTime = form_data.startTime,
                                endTime=form_data.endTime, location =  form_data.location,
                                equipment = form_data.equipment, toolRequired=formData.toolRequired,
                                workingAgency=form_data.workingAgency, workDescription=form_data.workDescription,
                                ppeRequired = form_data.ppeRequired, other_ppe= form_data.other_ppe,
                                person1 = form_data.person1, person2=form_data.person2,person3=form_data.person3,
                                q1 = form_data.q1,q2 = form_data.q2,q3 = form_data.q3,q4 = form_data.q4,
                                q5 = form_data.q5,q6 = form_data.q6,q7 = form_data.q7,q8 = form_data.q8,
                                q9=form_data.q9,q10=form_data.q10,q11=form_data.q11,q12=form_data.q12,
                                q13=form_data.q13,q14=form_data.q14,q15=form_data.q15,q16=form_data.q16,
                                q17=form_data.q17
                            )
                            formData.objects.filter(id=data['id']).update(approve_type=get_status,
                                                                          verified_by_person2=False,
                                                                          reason_for_status_type=remark)

                            logged_person_name = CustomUser.objects.get(id=data['loggedPerson_id'])
                            print("LOGGED PERSON  IN SUSPEND === ", logged_person_name)
                            user_name_1 = CustomUser.objects.get(id=data['person1_id'])

                            print("user_name_1 IN SUSPEND === ", user_name_1)

                            form_id = formData.objects.get(id=data['id'])
                            NotificationForUser.objects.create(user_name=logged_person_name, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)

                            get_fcm_token_Log_person = fcmTokenFirebase.objects.filter(
                                user=logged_person_name).values().last()
                            NotificationForUser.objects.create(user_name=user_name_1, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)
                            get_fcm_token_person1 = fcmTokenFirebase.objects.filter(
                                user=user_name_1).values().last()

                            if get_fcm_token_Log_person is not None:
                                sendLiveNotification(get_fcm_token_Log_person['fcm_token'],
                                                     f'{remark[0:90]}.........',
                                                     f'Work Permit on {get_status}')

                            if get_fcm_token_person1 is not None:
                                sendLiveNotification(get_fcm_token_person1['fcm_token'],
                                                     f'{remark[0:90]}.........',
                                                     f'Work Permit on {get_status}')


                            return JsonResponse({'msg': 'Form Suspended', 'status': HTTP_200_OK}, status=HTTP_200_OK)

                        else:
                            formData.objects.filter(id=data['id']).update(approve_type=get_status,
                                                       verified_by_person2=False,reason_for_status_type = remark)

                            logged_person_name = CustomUser.objects.get(id=data['loggedPerson_id'])
                            user_name_1 = CustomUser.objects.get(id=data['person1_id'])

                            print("USER", logged_person_name.name)
                            form_id = formData.objects.get(id=data['id'])
                            NotificationForUser.objects.create(user_name=logged_person_name, form_id=form_id,
                                                                   new_notification=True,
                                                                   message=remark)

                            get_fcm_token_Log_person = fcmTokenFirebase.objects.filter(user=logged_person_name).values().last()
                            NotificationForUser.objects.create(user_name=user_name_1, form_id=form_id,
                                                                   new_notification=True,
                                                                   message=remark)
                            get_fcm_token_person1 = fcmTokenFirebase.objects.filter(
                                    user=user_name_1).values().last()

                            if get_fcm_token_Log_person is not None:
                                sendLiveNotification(get_fcm_token_Log_person['fcm_token'],
                                                                                 f'{remark[0:90]}.........',
                                                                                 f'Work Permit on {get_status}')


                            if get_fcm_token_person1 is not None:
                                sendLiveNotification(get_fcm_token_person1['fcm_token'],
                                                         f'{remark[0:90]}.........',
                                                         f'Work Permit on {get_status}')



                            return JsonResponse({'msg': get_status,'status':HTTP_200_OK}, status=HTTP_200_OK)

                    if get_status == None:
                        formData.objects.filter(id=data['id']).update(verified_by_person2=True, approve_type="None",
                                                                      reason_for_status_type= "",
                                                                      notify_person3=True,notify_person1=False)

                        user_name = CustomUser.objects.get(id=data['person3_id'])
                        print("USER",user_name.name)

                        person2_name= CustomUser.objects.get(id=data['person2_id'])

                        form_id = formData.objects.get(id=data['id'])
                        NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                                                       new_notification=True,
                                                       message="Waiting For Your Approvement")

                        NotificationForUser.objects.filter(user_name_id=person2_name.id,
                                                       form_id=form_id).update(message='Approved By You')
                        desc = data['workDescription']

                        print(desc)
                        get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                        if get_fcm_token is not None:
                            print("FCM TOKEN GET===============",get_fcm_token)
                            response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                     f'{desc[0:90]}.........',
                                                                     'Work Permit For Verification')
                            print("Verification Response",response_notification)
                        else:
                            print('PLEASE PASS FCM TOKEN')

                        return JsonResponse({'msg': 'Verified','status':HTTP_200_OK}, status=HTTP_200_OK)


                if request.user.id == data['person3_id']:
                    if get_status != None:
                        if get_status == 'Suspend':
                            new_permit_data = formData.objects.last()
                            number = int(new_permit_data.permitnumber) + 1
                            print(number)
                            form_data = formData.objects.get(id=data['id'])

                            formData.objects.create(
                                permitnumber=number, loggedPerson=form_data.loggedPerson,date=form_data.date,
                                typeOfWork = form_data.typeOfWork,
                                numberOfPerson = form_data.numberOfPerson, startTime = form_data.startTime,
                                endTime=form_data.endTime, location =  form_data.location,
                                equipment = form_data.equipment, toolRequired=formData.toolRequired,
                                workingAgency=form_data.workingAgency, workDescription=form_data.workDescription,
                                ppeRequired = form_data.ppeRequired, other_ppe= form_data.other_ppe,
                                person1 = form_data.person1, person2=form_data.person2,person3=form_data.person3,
                                q1 = form_data.q1,q2 = form_data.q2,q3 = form_data.q3,q4 = form_data.q4,
                                q5 = form_data.q5,q6 = form_data.q6,q7 = form_data.q7,q8 = form_data.q8,
                                q9=form_data.q9,q10=form_data.q10,q11=form_data.q11,q12=form_data.q12,
                                q13=form_data.q13,q14=form_data.q14,q15=form_data.q15,q16=form_data.q16,
                                q17=form_data.q17
                            )
                            formData.objects.filter(id=data['id']).update(approve_type=get_status,
                                                                          verified_by_person3=False,
                                                                          reason_for_status_type=remark)

                            logged_person_name = CustomUser.objects.get(id=data['loggedPerson_id'])
                            user_name_1 = CustomUser.objects.get(id=data['person1_id'])
                            user_name_2 = CustomUser.objects.get(id=data['person2_id'])

                            form_id = formData.objects.get(id=data['id'])
                            NotificationForUser.objects.create(user_name=logged_person_name, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)

                            get_fcm_token_logged_person = fcmTokenFirebase.objects.filter(
                                user=logged_person_name).values().last()

                            NotificationForUser.objects.create(user_name=user_name_1, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)
                            get_fcm_token_person1 = fcmTokenFirebase.objects.filter(
                                user=user_name_1).values().last()

                            NotificationForUser.objects.create(user_name=user_name_2, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)
                            get_fcm_token_person2 = fcmTokenFirebase.objects.filter(
                                user=user_name_2).values().last()

                            if get_fcm_token_logged_person is not None:
                                print("FCM TOKEN GET===============", get_fcm_token_logged_person)
                                response_notification = sendLiveNotification(get_fcm_token_logged_person['fcm_token'],
                                                                             f'{remark[0:90]}.........',
                                                                             f'Work Permit on {get_status}')
                                print("Verification Response", response_notification)

                            if get_fcm_token_person1 is not None:
                                print("FCM TOKEN GET===============", get_fcm_token_person1)
                                response_notification = sendLiveNotification(get_fcm_token_person1['fcm_token'],
                                                                             f'{remark[0:90]}.........',
                                                                             f'Work Permit on {get_status}')
                                print("Verification Response", response_notification)

                            if get_fcm_token_person2 is not None:
                                print("FCM TOKEN GET===============", get_fcm_token_person2)
                                response_notification = sendLiveNotification(get_fcm_token_person2['fcm_token'],
                                                                             f'{remark[0:90]}.........',
                                                                             f'Work Permit on {get_status}')
                                print("Verification Response", response_notification)

                            return JsonResponse({'msg': 'Form Suspended', 'status': HTTP_200_OK},
                                                status=HTTP_200_OK)

                        else:

                            formData.objects.filter(id=data['id']).update(approve_type=get_status,verified_by_person3=False,
                                                                          reason_for_status_type=remark)

                            logged_person_name = CustomUser.objects.get(id=data['loggedPerson_id'])
                            user_name_1 = CustomUser.objects.get(id=data['person1_id'])
                            user_name_2 = CustomUser.objects.get(id=data['person2_id'])

                            form_id = formData.objects.get(id=data['id'])
                            NotificationForUser.objects.create(user_name=logged_person_name, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)

                            get_fcm_token_logged_person = fcmTokenFirebase.objects.filter(user=logged_person_name).values().last()

                            NotificationForUser.objects.create(user_name=user_name_1, form_id=form_id,
                                                               new_notification=True,
                                                               message=remark)
                            get_fcm_token_person1 = fcmTokenFirebase.objects.filter(
                                user=user_name_1).values().last()

                            NotificationForUser.objects.create(user_name=user_name_2, form_id=form_id,
                                                                   new_notification=True,
                                                                   message=remark)
                            get_fcm_token_person2 = fcmTokenFirebase.objects.filter(
                                user=user_name_2).values().last()

                            if get_fcm_token_logged_person is not None:
                                print("FCM TOKEN GET===============", get_fcm_token_logged_person)
                                response_notification = sendLiveNotification(get_fcm_token_logged_person['fcm_token'],
                                                                            f'{remark[0:90]}.........',
                                                                            f'Work Permit on {get_status}')
                                print("Verification Response", response_notification)



                            if get_fcm_token_person1 is not None:
                                print("FCM TOKEN GET===============", get_fcm_token_person1)
                                response_notification = sendLiveNotification(get_fcm_token_person1['fcm_token'],
                                                                             f'{remark[0:90]}.........',
                                                                             f'Work Permit on {get_status}')
                                print("Verification Response", response_notification)



                            if get_fcm_token_person2 is not None:
                                print("FCM TOKEN GET===============", get_fcm_token_person2)
                                response_notification = sendLiveNotification(get_fcm_token_person2['fcm_token'],
                                                                             f'{remark[0:90]}.........',
                                                                             f'Work Permit on {get_status}')
                                print("Verification Response", response_notification)
                            return JsonResponse({'msg': get_status, 'status': HTTP_200_OK}, status=HTTP_200_OK)

                    # if get_status !=None:
                    #     formData.objects.filter(id=data['id']).update(approve_type=get_status,
                    #                                                   reason_for_status_type = reason)
                    #     user_name = CustomUser.objects.get(id=data['person3_id'])
                    #     print("USER", user_name.name)
                    #     form_id = formData.objects.get(id=data['id'])
                    #     print('FORM ID == ',form_id)
                    #     NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                    #                                        new_notification=True,
                    #                                        message=reason)
                    #     person3_name = CustomUser.objects.get(id=data['person3_id'])
                    #     NotificationForUser.objects.filter(user_name_id=person3_name.id,
                    #                                        form_id=form_id).update(message=reason)
                    #
                    #     return JsonResponse({'msg': get_status, 'status': HTTP_200_OK}, status=HTTP_200_OK)

                    if get_status == None:
                        formData.objects.filter(id=data['id']).update(verified_by_person3=True,notify_person1=False,
                                                                    approve_type = "None",reason_for_status_type = "",
                                                                    notify_person3=False,notify_person2=False)

                        NotificationForUser.objects.filter(form_id_id=id).update(verified_by_all=True, message='Verified By Everyone')
                        desc = data['workDescription']

                        user_name = CustomUser.objects.get(id=data['loggedPerson_id'])
                        get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                        if get_fcm_token is not None:
                            response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                     f'{desc[0:90]}.........',
                                                                     'Your Work Permit Is Verified By all.')
                            print('Verification By all Response',response_notification)
                        else:
                            print("PLEASE PASS FCM TOKEN")

                        return JsonResponse({'msg': 'Verified','status':HTTP_200_OK}, status=HTTP_200_OK)


    class closedByPersonFormApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]

        def get(self, request,id):
            print("*************************get*******")
            try:
                form_data = formData.objects.filter(id=id).values()
                print("INSIDE CLOSED.............!!!!!!!!")
                for data in form_data:
                    print("INSIDE FOR*********",data)
                    if request.user.id == data['person1_id']:
                        formData.objects.filter(id=data['id']).update(closedByPerson1=True)

                        user_name = CustomUser.objects.get(id=data['person2_id'])
                        form_id = formData.objects.get(id=data['id'])

                        person1_name = CustomUser.objects.get(id=data['person1_id'])

                        NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                                                           close_notification=True,message='Work Permit To Close')


                        NotificationForUser.objects.filter(user_name=person1_name.id,
                                                           form_id=form_id).update(message='Closed By You')



                        desc = data['workDescription']
                        get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                        if get_fcm_token is not None:
                            response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                         f'{desc[0:90]}.........',
                                                                         'Work Permit For closing.')
                            print('Closing Response',response_notification)
                        else:
                            print('PLEASE PASS FCM TOKEN')

                        return JsonResponse({'msg':'Closed successfully', 'status':HTTP_200_OK},
                                            status=HTTP_200_OK)

                    if request.user.id == data['person2_id']:
                        formData.objects.filter(id=data['id']).update(closedByPerson2=True)

                        user_name = CustomUser.objects.get(id=data['person3_id'])
                        form_id = formData.objects.get(id=data['id'])

                        person2_name = CustomUser.objects.get(id=data['person2_id'])

                        NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                                                           close_notification=True,message='Work Permit To Close')


                        NotificationForUser.objects.filter(user_name=person2_name.id,
                                                           form_id=form_id).update(message='Closed By You')



                        desc = data['workDescription']
                        get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                        if get_fcm_token is not None:
                            response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                         f'{desc[0:90]}.........',
                                                                         'Work Permit For closing.')
                            print('Closing Response',response_notification)
                        else:
                            print('PLEASE PASS FCM TOKEN')

                        return JsonResponse({'msg':'Closed successfully', 'status':HTTP_200_OK},
                                            status=HTTP_200_OK)


                    # else:
                    #     return JsonResponse({'msg': 'Enter Valid Form ID', 'status': HTTP_400_BAD_REQUEST},
                    #                         status=HTTP_400_BAD_REQUEST)

                    if request.user.id == data['person3_id']:
                        formData.objects.filter(id=data['id']).update(closedByPerson3=True,completedFlag=True,
                                                                      tocloseFlag=False, closedByLoggedUser=False,
                                                                      closedByPerson1=False,newFlag=False)

                        NotificationForUser.objects.filter(form_id_id=id).update(closed_by_all=True,
                                                                                 complete_notification=True)
                        user_name = CustomUser.objects.get(id=data['loggedPerson_id'])

                        person3_name = CustomUser.objects.get(id=data['person3_id'])

                        NotificationForUser.objects.filter(user_name=person3_name.id,
                                                           form_id=id).update(message='Closed By Everyone')

                        desc = data['workDescription']
                        get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                        if get_fcm_token is not None:
                            response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                         f'{desc[0:90]}.........',
                                                                         'Your Work Permit is now closed by all.')
                            print('Closed By All Response',response_notification)
                        else:
                            print('PLEASE PASS FCM TOKEN')
                        return JsonResponse({'msg': 'Closed successfully', 'status':HTTP_200_OK}, status=HTTP_200_OK)

                    if request.user.id == data['loggedPerson_id']:
                        formData.objects.filter(id=data['id']).update(closedByLoggedUser=True)

                        user_name = CustomUser.objects.get(id=data['person1_id'])
                        form_id = formData.objects.get(id=data['id'])
                        NotificationForUser.objects.create(user_name=user_name, form_id=form_id,
                                                           close_notification=True, message='Work Permit To Close')

                        desc = data['workDescription']
                        get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()
                        if get_fcm_token is not None:
                            response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                                         f'{desc[0:90]}.........',
                                                                         'Work Permit For Closing.')
                            print("Close Response",response_notification)
                        else:
                            print('PLEASE PASS FCM TOKEN')

                        return JsonResponse({'msg': 'Closed successfully', 'status':HTTP_200_OK}, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    class completedTaskApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def get(self, request):
            try:
                form_data = formData.objects.all().values()
                for data in form_data:
                    if request.user.id == data['person1_id']:
                        print("**************", data['id'])
                        form_data = formData.objects.filter(person1=data['person1_id']  ,completedFlag=True)
                        serializer = formDataSerializer(form_data, many=True)
                        return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, status=HTTP_200_OK)

                    if request.user.id == data['person2_id']:
                        print("**************", data['id'])
                        form_data = formData.objects.filter(person2=data['person2_id']  , completedFlag=True)
                        serializer = formDataSerializer(form_data, many=True)
                        return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, status=HTTP_200_OK)

                    if request.user.id == data['person3_id']:
                        print("**************", data['id'])
                        form_data = formData.objects.filter(person3=data['person3_id'] , completedFlag=True)
                        serializer = formDataSerializer(form_data, many=True)
                        return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, status=HTTP_200_OK)

                    if request.user.id == data['loggedPerson_id']:
                        print("**************",data['id'])
                        form_data = formData.objects.filter(loggedPerson = data['loggedPerson_id'] ,completedFlag=True)
                        serializer = formDataSerializer(form_data, many=True)
                        return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    # class extensionView(APIView):
    #     authentication_classes = [JWTAuthentication]
    #     permission_classes= [IsAuthenticated]
    #     def get(self,request,id):
    #         form_data=formData.objects.filter(id=id)
    #         serialized_data=formDataSerializer(form_data,many=True)
    #         return JsonResponse(serialized_data.data,safe=False)

    class rejectFormApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self, request, id):
            rejectreason = request.data.get('reject_reason')
            print(rejectreason)
            formData.objects.filter(id=id).update(verified_by_person1=False, verified_by_person2=False, oldFlag=False,
                                                  tocloseFlag=False, closedByLoggedUser=False, closedByPerson1=False,
                                                  completedFlag=False, newFlag=False, closedByPerson2=False,
                                                  closedByPerson3=False,verified_by_person3=False,
                                                  notify_person2=False, notify_person1=False, notify_person3=False,rejectFlag=True,
                                                  reject_reason=rejectreason)

            NotificationForUser.objects.filter(form_id_id=id).update(reject_notification=True,
                               new_notification=False, close_notification=False,
                               complete_notification=False,verified_by_all=False,closed_by_all=False,
                               message=f'Rejected By {request.user}')
            #status=f'Rejected By {request.user}'

            print("ID==================",id)
            data=formData.objects.filter(id=id).values()
            print("*************************", data[0]['loggedPerson_id'])
            user_name = CustomUser.objects.get(id=data[0]['loggedPerson_id'])
            second_user = CustomUser.objects.get(id=data[0]['person1_id'])

            get_fcm_token = fcmTokenFirebase.objects.filter(user=user_name).values().last()

            get_fcm_token_for_second_user = fcmTokenFirebase.objects.filter(user=second_user).values().last()
            print(get_fcm_token_for_second_user,"***************************************************")
            if get_fcm_token is not None:
                response_notification = sendLiveNotification(get_fcm_token['fcm_token'],
                                                             rejectreason,
                                                             f'Work Permit is Rejected by {request.user}')
                sendLiveNotification(get_fcm_token_for_second_user['fcm_token'],
                                                             rejectreason,
                                                             f'Work Permit is Rejected by {request.user}')
                print("Reject Response",response_notification)
            else:
                print('PLEASE PASS FCM TOKEN')

            return JsonResponse({'msg': 'Form Rejected'}, safe=False, status=HTTP_200_OK)

    class rejectedFormListApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def get(self, request):
            try:
                form_data = formData.objects.filter(loggedPerson=request.user.id,rejectFlag = True)
                serializer = formDataSerializer(form_data, many=True)
                return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, safe=False, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    class updateExtensionApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes= [IsAuthenticated]
        def put(self,request,id):

            try:
                startTime = request.data.get('startTime')
                print(startTime)
                endTime = request.data.get('endTime')
                formData.objects.filter(id=id).update(verified_by_person1=False,verified_by_person2=False,verified_by_person3=False,
                                                      oldFlag=False,tocloseFlag=False,  closedByLoggedUser=False,
                                                      closedByPerson1=False,closedByPerson2=False,closedByPerson3=False,
                                                      completedFlag=False,endTime=endTime,startTime=startTime,newFlag=True)

                return JsonResponse({"msg":"Work Extended","status":HTTP_200_OK}, status=HTTP_200_OK)
            except:
                return JsonResponse({"error": "Flag Not Changed",
                                     'status': HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)


    class chartDataAPiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        def get(self, request):

                if request.user.is_admin == True:
                    from_date =request.GET.get('from_date')
                    to_date = request.GET.get('to_date')
                    print(from_date)
                    print(to_date)

                    new_flag_date = formData.objects.filter(new_flag_date_created__range=[from_date,to_date])
                    print(new_flag_date)
                    old_flag_date = formData.objects.filter(old_flag_date_created__range=[from_date,to_date])
                    toclose_flag_date= formData.objects.filter(toclose_flag_date_created__range=[from_date, to_date])
                    completed_flag_date= formData.objects.filter(completed_flag_date_created__range=[from_date, to_date])
                    rejected_flag_date = formData.objects.filter(rejected_flag_date_created__range=[from_date, to_date])

                    data={
                        "new_flag_count":new_flag_date.count(),
                        "toclose_flag_count":toclose_flag_date.count(),
                        "old_flag_count":old_flag_date.count(),
                        "completed_flag_count":completed_flag_date.count(),
                        "rejected_flag_count":rejected_flag_date.count()
                    }
                    serializer = chartSerializer(data=data,many=True)
                    print(serializer.initial_data)

                    return JsonResponse(serializer.initial_data,safe=False, status=HTTP_200_OK)
                else:
                   return JsonResponse({'msg':'You are not authorized to view.'}, status=HTTP_400_BAD_REQUEST)

    class verifyOtpApiView(APIView):
        def post(self, request):
            phone_number=request.data['phone_number']
            print("**********************", phone_number)
            otp = request.data['otp']
            fcm_token = request.data['fcm_token']
            language = request.data['language']
            type = request.data['type']
            device_id = request.data['device_id']
            user = CustomUser.objects.filter(phone_number=phone_number).first()
            if user is None:
                return JsonResponse({"response":"Invalid User", "status":HTTP_401_UNAUTHORIZED}, status=HTTP_401_UNAUTHORIZED)

            else:
                if user.otp == otp:
                    access_token = create_access_token(user.id)
                    refresh_token = create_refresh_token(user.id)
                    UserToken.objects.create(
                        user_id=user.id,
                        token=refresh_token,
                        expired_at=datetime.utcnow() + timedelta(days=7)
                    )
                    fcmTokenFirebase.objects.create(
                        user_id=user.id,
                        fcm_token=fcm_token,
                        device_id=device_id,
                        language=language,
                        type=type.lower()
                    )

                    user_name = CustomUser.objects.get(phone_number=phone_number)
                    user_role = userRole.objects.get(roleName='SHE/EHS Incharge')
                    print('USER NAME==========', user_name.id)
                    safety_name = userDetails.objects.filter(userName=user_name.id, userRole=user_role.id).exists()
                    print("SAFETY==============", safety_name)

                    if safety_name == True:
                        role_name = "Safety"
                    else:
                        role_name = ""

                    response = Response()
                    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
                    response.data = {
                            'token' : access_token,
                            'user_id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'phone number': user.phone_number,
                            'fcm_token': fcm_token,
                            'device_id': device_id,
                            'language': language,
                            'type': type,
                            'is_fresh_login': user.is_first_login,
                            'role': role_name,
                            'status': HTTP_200_OK
                    }
                    return JsonResponse({"user_details":response.data}, status=HTTP_200_OK)
                else:
                    return JsonResponse({"msg":"Invalid Otp", 'status':HTTP_400_BAD_REQUEST}, status=HTTP_400_BAD_REQUEST)

    class loginApiView(APIView):
        def post(self,request):
                phone_number = request.data.get('phone_number')
                # request.session['phone_number']=phone_number
                if phone_number!=None:
                    user = CustomUser.objects.filter(phone_number=phone_number).first()
                    if user is None:
                        return JsonResponse({"response":"Invalid Phone Number", "status":HTTP_401_UNAUTHORIZED}, status=HTTP_401_UNAUTHORIZED)
                    else:
                        account_sid = 'AC484ae5245e66125e89a9d685d44301a0'
                        auth_token = '791fe6bb51c90aa617e4be72cfc6424e'
                        client = Client(account_sid, auth_token)
                        my_otp = random.randint(1111, 9999)

                        check_otp_exists = CustomUser.objects.filter(otp=my_otp)
                        print("*************************", check_otp_exists)
                        if check_otp_exists != None:
                            my_otp = random.randint(1111, 9999)
                            message = client.messages.create(
                                body=f"Hey Customer your OTP for PGP Login is {my_otp}",
                                from_='+19705947987',
                                to=f'+91{phone_number}'
                            )
                            CustomUser.objects.filter(phone_number=phone_number).update(otp=my_otp)
                            print(message.sid)
                            return JsonResponse({'msg': 'OTP SENT', "status":HTTP_200_OK}, status=HTTP_200_OK)
                        else:
                            message = client.messages.create(
                                body=f"Hey Customer your OTP for PGP Login is {my_otp}",
                                from_='+19896744452',
                                to=f'+91{phone_number}'
                            )
                            CustomUser.objects.filter(phone_number=phone_number).update(otp=my_otp)
                            print(message.sid)
                            return JsonResponse({'msg': 'OTP SENT', "status":HTTP_200_OK}, status=HTTP_200_OK)

                else:
                    email = request.data['email']
                    password = request.data['password']
                    fcm_token = request.data['fcm_token']
                    language = request.data['language']
                    type = request.data['type']
                    device_id = request.data['device_id']

                    # user=CustomUser.objects.filter(email=email).first()
                    user = authenticate(email=email, password=password)

                    # role = userDetails.objects.filter(userName_id=user.id).all().values()
                    #
                    # current_user_role={}
                    # for i in role:
                    #     rolename = userRole.objects.get(id=i['userRole_id'])
                    #     current_user_role['rolename'] =rolename
                    #     print(rolename)
                    # print(current_user_role)

                    if user is None:
                        return JsonResponse({"response":"Invalid Username And Password.", "status":HTTP_401_UNAUTHORIZED}, status=HTTP_401_UNAUTHORIZED)

                    user_name = CustomUser.objects.get(email = email)
                    user_role = userRole.objects.get(roleName='SHE/EHS Incharge')
                    print('USER NAME==========', user_name.id)
                    safety_name = userDetails.objects.filter(userName=user_name.id, userRole=user_role.id).exists()
                    print("SAFETY==============", safety_name)
                    user_role_contractor = userRole.objects.get(roleName='Contractor')
                    print('USER NAME==========', user_name.id)
                    contractor_safety_name = userDetails.objects.filter(userName=user_name.id, userRole=user_role_contractor.id).exists()
                    print("SAFETY==============", safety_name)
                    if safety_name == True:
                        role_name = "Safety"
                    else:
                        if contractor_safety_name == True:
                            role_name = "Contractor"
                        else:
                            role_name=""

                    access_token = create_access_token(user.id)
                    refresh_token=create_refresh_token(user.id)
                    UserToken.objects.create(
                            user_id=user.id,
                            token=refresh_token,
                            expired_at=datetime.utcnow() + timedelta(days=7)
                        )

                    fcmTokenFirebase.objects.create(
                        user_id=user.id,
                        fcm_token=fcm_token,
                        device_id=device_id,
                        language=language,
                        type= type.lower()
                    )

                    response = Response()
                    response.set_cookie(key='refresh_token',value=refresh_token,httponly=True)

                    response.data = {
                            'token' : access_token,
                            'user_id':user.id,
                            'name': user.name,
                            'email': user.email,
                            'phone number': user.phone_number,
                            'fcm_token': fcm_token,
                            'device_id': device_id,
                            'language': language,
                            'is_fresh_login':user.is_first_login,
                            'is_admin':user.is_admin,
                            'role':role_name,
                            # 'contractor_name':contractor_name,
                            'type': type,
                            'status': HTTP_200_OK
                    }
                    return JsonResponse({"user_details":response.data}, status=HTTP_200_OK)

    class userApiView(APIView):
        authentication_classes = [JWTAuthentication]
        def get(self,request):
            print(request)
            return Response(userLoginSerializer(request.user).data)

    class refreshApiView(APIView):
        def post(self,request):
            refresh_token=request.COOKIES.get('refresh_token')
            id = decode_refresh_token(refresh_token)
            access_token = create_access_token(id)

            if not UserToken.objects.filter(
                user_id=id,
                token=refresh_token,
                expired_at__gt=datetime.now(tz=datetime.timezone.utc)
            ).exists():
                raise exceptions.AuthenticationFailed('Unauthenticated')

            return Response({
                'token':access_token,
                'status': HTTP_200_OK
            })


    class logoutApiView(APIView):
        authentication_classes=[JWTAuthentication]
        def post(self,request):
            UserToken.objects.filter(user_id=request.user.id).delete()
            response = Response()
            response.delete_cookie(key='refresh_token')
            response.data={
                'msg':'success',
                'status': HTTP_200_OK
            }
            return response


    class ResetPasswordApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self, request):
            password = request.data['new_password']
            confirm_password = request.data['confirm_password']

            if password != confirm_password:
                return JsonResponse({'msg': 'Password Mismatch', 'status': HTTP_400_BAD_REQUEST},
                                    status=HTTP_400_BAD_REQUEST)

            else:
                CustomUser.objects.filter(id=request.user.id).update(password=make_password(password), is_first_login=False)
                return JsonResponse({'msg': 'Password Changed','status':HTTP_200_OK}, status=HTTP_200_OK)


    class UserSessionApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self, request):
            data = {
                "login_id": request.data['login_id'],
                "current_login_user_email": request.data['user_email'],
                "permit_id": request.data['permit_id'],
                "permit_initiator": request.data['permit_initiator_name'],
                "hod_id": request.data['hod_id'],
                "hod_encharge": request.data['hod_name'],
                "he_she_id": request.data['he_she_id'],
                "he_she": request.data['he_name'],
                "contractor_id": request.data['contractor_id'],
                "contractor": request.data['contractor_name']
            }
            serializer = UserSessionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'msg': 'Data Saved', 'status': HTTP_200_OK}, status=HTTP_200_OK)

            return JsonResponse({'error': serializer.errors, 'status': HTTP_400_BAD_REQUEST},
                                status=HTTP_400_BAD_REQUEST)


    class AllNotificationApiView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def get(self, request):
            user_name = CustomUser.objects.get(id=request.user.id)
            all_notifications = NotificationForUser.objects.filter(user_name=user_name)
            serializer = NotificationForUserSerializer(all_notifications, many=True)
            data={
                "Notification":serializer.data
            }
            return JsonResponse(data=data, safe=False, status=HTTP_200_OK)


    class DeleteAllNotification(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def delete(self, request, notification_id):
            try:
                delobj = NotificationForUser.objects.get(pk=notification_id)
                delobj.delete()
                return JsonResponse({"msg": "Notification Deleted."}, status=HTTP_200_OK)
            except:
                return JsonResponse({"msg": "Please enter valid id."}, status=HTTP_400_BAD_REQUEST)


    class PasswordChangeAPIView(APIView):
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self, request):
            pwd = request.user.password
            email = request.user
            old_password = request.data['old_password']

            user = authenticate(email=request.user, password=old_password)
            if user is not None:
                password = request.data['new_password']
                confirm_password = request.data['confirm_password']

                if password != confirm_password:
                    return JsonResponse({'msg': 'Password Mismatch', 'status': HTTP_400_BAD_REQUEST},
                                        status=HTTP_400_BAD_REQUEST)

                else:
                    CustomUser.objects.filter(id=request.user.id).update(password=make_password(password))
                    return JsonResponse({'msg': 'Password Changed Successfully', 'status':HTTP_200_OK},
                                        status=HTTP_200_OK)
            else:
                return JsonResponse({'msg': 'Please Check Your Password.', 'status':HTTP_400_BAD_REQUEST},
                                    status=HTTP_400_BAD_REQUEST)

    class newPermitNoView(APIView):
        def get(self, request, *args, **kwargs):
            new_permit_data = formData.objects.last()
            print(new_permit_data)
            if new_permit_data is None:
                data=10001
                return JsonResponse({'permit number': data}, status=HTTP_200_OK)

            data = int(new_permit_data.permitnumber) + 1
            return JsonResponse({'permit number': data}, status=HTTP_200_OK)

    ################################### generating pdf ##################################

    def generatePdfOfWorkPermit(request,pk):
        data = formData.objects.filter(id=pk)
        data_all = formData.objects.filter(id=pk).values()

        typeOfWork = data_all[0]['typeOfWork']

        ppeRequired = data_all[0]['ppeRequired']

        client_name =data_all[0]['permitnumber']
        filename = f'{client_name}'

        pdf = render_to_pdf('vaibhav.html', filename, {'data':data,
                                                                'typeOfWork':typeOfWork,
                                                                'ppeRequired':ppeRequired})

        # pdf = render_to_pdf('try1.html', filename,{'data':data,'equipment':flattenEquip,
        #                                                         'toolRequired':flattenTool,
        #                                                         'typeOfWork':flattentypeOfWork,
        #                                                         'ppeRequired':flattenpperequired})

        filename = f"{client_name}.pdf"
        response = HttpResponse(pdf, content_type='application/pdf')
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response

        # data = formData.objects.filter(id=pk)
        # data_all= formData.objects.filter(id=pk).values()
        # equipments = data_all[0]['equipment']
        # equipment = equipments.replace("\'","")
        # flattenEquip = equipment[1:-1]
        #
        # tool = data_all[0]['toolRequired']
        # tools = tool.replace("\'", "")
        # flattenTool = tools[1:-1]
        #
        # return render(request, 'workPermit.html', {'data':data,'equipment':flattenEquip,'toolRequired':flattenTool})

        # data = formData.objects.filter(id=pk)
        # data_all = formData.objects.filter(id=pk).values()
        # equipments = data_all[0]['equipment']
        # equipment = equipments.replace("\'", "")
        # flattenEquip = equipment[1:-1]
        #
        # tool = data_all[0]['toolRequired']
        # tools = tool.replace("\'", "")
        # flattenTool = tools[1:-1]
        #
        # # template_path = 'workPermit.html'
        # template_path = 'workpermit.html'
        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="Report.pdf"'
        # html = render_to_string(template_path, {'data': data, 'equipment': flattenEquip, 'toolRequired': flattenTool})
        # pisaStatus = pisa.CreatePDF(html, dest=response)
        # return response


    class faqView(APIView):
        def get(self, request, *args, **kwargs):
            faq_data = FAQ.objects.all()
            print(faq_data)
            serializer = FAQSerializer(faq_data,many=True)
            return JsonResponse({'data': serializer.data},safe=False, status=HTTP_200_OK)

    class ExcelDataApiView(APIView):
        def post(self,request):
            month = request.data['month']
            year = request.data['year']

            data = formData.objects.filter(date__month=month, date__year = year)
            print(data)
            serializer = formDataSerializer(data, many=True)
            return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, status=HTTP_200_OK)


            # month_year = request.data['month_or_year']
            # get_number = request.data['get_number']
            # print("=========++++++++++========++++++==========+++++++++",month_year)
            # if month_year == 'month':
            #     data = formData.objects.filter(date__month =get_number)
            #     serializer = formDataSerializer(data, many=True)
            #     return JsonResponse({'data':serializer.data, 'status':HTTP_200_OK}, status=HTTP_200_OK)
            #
            # elif month_year == 'year':
            #     data = formData.objects.filter(date__year=get_number)
            #     serializer = formDataSerializer(data, many=True)
            #     return JsonResponse({'data': serializer.data, 'status': HTTP_200_OK}, status=HTTP_200_OK)
            #
            # else:
            #     return JsonResponse({'msg': 'No data', 'status': HTTP_400_BAD_REQUEST},
            #                         status=HTTP_400_BAD_REQUEST)



    ###############vaibhav#################
    # from django.views.generic import View
    # class GeneratePdf(View):
    #     def get(self, request, *args, **kwargs):
    #         # data = formData.objects.filter(id=pk)
    #         data = {}
    #         # getting the template
    #         try:
    #             pdf = render_to_pdf('workPermit.html', data)
    #         except AttributeError:
    #         # counters is not a dictionary, ignore and move on
    #             pass
    #         if pdf:
    #             response = HttpResponse(pdf, content_type='application/pdf')
    #             filename = "HAHAHA.pdf"
    #             content = "attachment; filename='%s'" %(filename)
    #             response['Content-Dispostion'] = content
    #             return content
    #         # rendering the template
    #         return HttpResponse("Not Found")

except:
    raise Exception(HTTP_500_INTERNAL_SERVER_ERROR)

# def creating_user():
#         print('INSIDE EGT')
#         relative_path = os.path.dirname(os.path.realpath(__file__))
#         fname = "jambusar.xlsx"
#         path = os.path.join(relative_path, fname)
#         print('PATH=========', path)
#         df = pd.read_excel(path,'JBR-1')
#         print(df.columns)
#         print(df.shape[0])
#
#         # get_data = df[['Official Mail Id', 'Employee Name', 'Contact No']]
#         get_data = df[['Official Mail Id', 'EmpName', 'MobileNo']]
#
#         i = 0
#         print(i)
#         while i < 78:
#             print(get_data.iloc[i][1], get_data.iloc[i][0], get_data.iloc[i][2])
#             CustomUser.objects.create(email=str(get_data.iloc[i][0]).lower(),
#                                                name=get_data.iloc[i][1],
#                                                password=make_password('abc@1234'),
#                                                phone_number=get_data.iloc[i][2])
#             print('Data Added')
#             i += 1
# creating_user()