from django.contrib import admin

from .models import ImprovementProposal


@admin.register(ImprovementProposal)
class ImprovementProposalAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'author', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('registration_number', 'author__username')