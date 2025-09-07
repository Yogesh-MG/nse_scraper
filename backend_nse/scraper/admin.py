from django.contrib import admin
from .models import OptionChain
import csv
from django.http import HttpResponse
# Register your models here.



def export_to_csv(modeladmin, request, queryset):
    """
    Custom admin action to export selected records to a CSV file.
    """
    # Get model fields dynamically
    field_names = [field.name for field in modeladmin.model._meta.fields]

    # Create the HTTP response for the CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={modeladmin.model._meta.model_name}_export.csv'

    # Add BOM for Excel compatibility (optional)
    response.write(u'\ufeff'.encode('utf8'))

    # Write the CSV
    writer = csv.writer(response)
    writer.writerow(field_names)  # header row

    for obj in queryset:
        row = [str(getattr(obj, field)) for field in field_names]
        writer.writerow(row)

    return response

export_to_csv.short_description = "Export selected items to CSV"

class customAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'symbol', 'current_price','expiry_date','CE_open_interest','CE_change_in_oi','CE_last_price','CE_bid_qty','CE_bid_price',
                    'CE_ask_price','CE_ask_qty','strike_price','PE_open_interest','PE_change_in_oi','PE_last_price','PE_bid_qty','PE_bid_price',
                    'PE_ask_price','PE_ask_qty')
    list_filter = ('symbol','timestamp')
    search_fields = ('strike_price', 'symbol')
    actions = [export_to_csv]

admin.site.register(OptionChain, customAdmin)
