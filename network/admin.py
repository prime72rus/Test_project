from django.contrib import admin
from django.utils.html import format_html
from network.models import Contact, Product, NetworkNode

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["email", "country", "city", "street", "house_number"]
    list_filter = ["country", "city"]
    search_fields = ["email", "country", "city"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "model", "release_date"]
    list_filter = ["release_date"]
    search_fields = ["name", "model"]

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ["name", "node_type", "supplier_link", "city", "debt", "created_at", "level"]
    list_filter = ["node_type", "contact__city", "contact__country"]
    search_fields = ["name", "contact__email"]
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html('<a href="{}">{}</a>',
                             f"/admin/network/networknode/{obj.supplier.id}/change/",
                             obj.supplier.name)
        return "Нет поставщика"
    supplier_link.short_description = "Поставщик"

    def city(self, obj):
        return obj.contact.city
    city.short_description = "Город"
    city.admin_order_field = "contact__city"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов.")
    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("contact", "supplier")
