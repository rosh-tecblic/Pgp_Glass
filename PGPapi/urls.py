from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('rest_framework.urls')),

    path('locationapi', views.userLocationApiView.as_view(), name="userLocationAPI"),
    path('locationapi/<int:id>', views.userLocationIDApiView.as_view(), name="userLocationID"),

    path('roleapi', views.userRoleApiView.as_view(), name="userRoleAPI"),
    path('roleapi/<int:id>', views.userRoleIDApiView.as_view(), name="userRoleIDAPI"),

    # path('loginapi', views.userLoginApiView.as_view(), name="userLoginAPI"),
    # path('loginapi/<int:id>', views.userLoginIDApiView.as_view(), name="userLoginIDAPI"),

    path('userdetailapi', views.userDetailApiView.as_view(), name="userDetailID"),
    path('userdetailapi/<int:id>', views.userDetailIDApiView.as_view(), name="userDetailIDAPI"),

    path('formdataApi', views.formDataApiView.as_view(), name="formDataAPI"),
    path('edit/form/<int:id>', views.formDataIDApiView.as_view(), name="formDataIDAPI"),

    path('agencyapi', views.agencyNameApiView.as_view(), name="agencyapi"),

    path('filterapi/<str:locationname>', views.filterApiView.as_view(), name="filterapi"),

    path('newflagapi', views.newFlagApiView.as_view(), name="newFlagapi"),

    path('oldflagapi', views.oldFlagApiView.as_view(), name="oldFlagapi"),

    path('tocloseflagapi', views.closeFlagApiView.as_view(), name="closeFlagapi"),

    path('completedflagapi', views.completedFlagApiView.as_view(), name="completedFlagapi"),

    path('notificationtoverify', views.notificationToVerifyApiView.as_view(), name="notificationverifyapi"),

    path('notificationtoclose', views.notificationToCloseAPiView.as_view(), name="notificationcloseapi"),

    path('changetocloseflagapi', views.changeToCloseFlagApiView.as_view(), name="change"),

    path('changeoldflagapi', views.changeOldFlagApiView.as_view(), name="change"),

    path('changecompleteflag', views.changeCompleteFlagApiView.as_view(), name="changecompleteflag"),

    # path('closedbyloggeduser/<int:id>',views.closedByLoggedUserApiView.as_view(),name='completedbyloggeduser'),

    path('completedflag', views.completedFlagApiView.as_view(), name='completedflag'),

    path('verify/<int:id>', views.approvedByPersonFormApiView.as_view(), name="verify"),

    path('close/<int:id>', views.closedByPersonFormApiView.as_view(), name="close_work_permit"),

    path('completedtask', views.completedTaskApiView.as_view(), name='completedtask'),

    # path('extension/<int:id>',views.extensionView.as_view(),name='extension'),

    path('extendwork/<int:id>', views.updateExtensionApiView.as_view(), name='updateextension'),

    # path('user_login',views.userLogin.as_view(),name='userlogin'),
    path('reject/<int:id>', views.rejectFormApiView.as_view(), name='reject-form'),

    path('reject', views.rejectedFormListApiView.as_view(), name='rejected-from-list'),

    path('verifyotp', views.verifyOtpApiView.as_view(), name='verify-from-otp'),

    path('user_login', views.loginApiView.as_view(), name='userlogin'),

    path('user', views.userApiView.as_view(), name='user'),

    path('refresh', views.refreshApiView.as_view(), name='refresh'),

    path('logout', views.logoutApiView.as_view(), name='logout'),

    path('onetime/change_password', views.ResetPasswordApiView.as_view(), name='change-password'),

    path('chart', views.chartDataAPiView.as_view(), name='chart'),

    path('user_session', views.UserSessionApiView.as_view(), name='user-session'),

    path('change_password', views.PasswordChangeAPIView.as_view(), name='password'),

    path('inbox/notification', views.AllNotificationApiView.as_view(), name='allnotification'),

    path('inbox/notification/delete/<int:notification_id>', views.DeleteAllNotification.as_view(),
         name='delete-notification'),

    path('permitnumber', views.newPermitNoView.as_view(), name='permit_number'),

    path('generateworkpdf/<int:pk>', views.generatePdfOfWorkPermit, name='generateworkpdf'),

    path('faq', views.faqView.as_view(), name='faq'),

    path('exceldata', views.ExcelDataApiView.as_view(), name='exceldata'),

]