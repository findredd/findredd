from django.contrib import admin
from main.models import UserDetail, UserPicture, UserSocialUrl, UserConfig, UserIssue, UserMessage, Certificate


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'name', 'blood_group', 'mobile_number', 'address', 'district', )
    ordering = ('username',)
    search_fields = ('username__username', 'status', 'name', 'blood_group', 'mobile_number', 'address', 'district', )


class UserPictureAdmin(admin.ModelAdmin):
    list_display = ('username', 'profile_picture', 'uploaded_at', )
    ordering = ('username', )
    search_fields = ('username__username', )


class UserSocialUrlAdmin(admin.ModelAdmin):
    list_display = ('username', 'website', 'facebook', 'twitter', 'instagram', )
    ordering = ('username', )
    search_fields = ('username__username', )


class UserConfigAdmin(admin.ModelAdmin):
    list_display = ('username', 'verified', 'blog', )
    ordering = ('username', )
    search_fields = ('username__username', )


class UserIssueAdmin(admin.ModelAdmin):
    list_display = ('username', 'status', 'category', 'reported_at', )
    ordering = ('reported_at', )
    search_fields = ('username__username', 'status', 'category', )


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at', )
    ordering = ('created_at', )
    search_fields = ('name', 'email', )


class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_number', 'certificate_image', 'uploaded_at', )
    ordering = ('uploaded_at', )
    search_fields = ('certificate_number', )


admin.site.register(UserDetail, UserDetailAdmin)
admin.site.register(UserPicture, UserPictureAdmin)
admin.site.register(UserSocialUrl, UserSocialUrlAdmin)
admin.site.register(UserConfig, UserConfigAdmin)
admin.site.register(UserIssue, UserIssueAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(Certificate, CertificateAdmin)
