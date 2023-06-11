from django.contrib import admin

from app.models import Plan, Account, Image, Thumbnail


class ThumbnailInline(admin.TabularInline):
    model = Plan.thumbnails.through
    extra = 0
    verbose_name = 'thumbnail'
    verbose_name_plural = 'thumbnails'


class PlanAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'is_original_size', 'is_expiring_link',)
    inlines = (ThumbnailInline,)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan')


admin.site.register(Plan, PlanAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Image, admin.ModelAdmin)
admin.site.register(Thumbnail, admin.ModelAdmin)
