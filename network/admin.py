from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from network.models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "model", "release_date"]


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "node_type",
        "supplier_link",
        "email",
        "country",
        "city",
        "street",
        "house_number",
        "debt",
        "created_at",
        "level",
    ]
    list_filter = ["city"]
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="{}">{}</a>',
                f"/admin/network/networknode/{obj.supplier.id}/change/",
                obj.supplier.name,
            )
        return "Нет поставщика"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(
            request, f"Задолженность очищена для {updated} объектов."
        )

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def save_model(self, request, obj, form, change):
        try:
            obj.full_clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)
            raise
