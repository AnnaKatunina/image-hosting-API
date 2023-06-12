from django.contrib import admin

from app.models import Plan, Account, Image, Thumbnail, ImageVersion


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


class ImageVersionInline(admin.TabularInline):
    model = ImageVersion
    extra = 0
    verbose_name = 'version'
    verbose_name_plural = 'versions'


class ImageAdmin(admin.ModelAdmin):
    inlines = (ImageVersionInline,)


admin.site.register(Plan, PlanAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Thumbnail, admin.ModelAdmin)
