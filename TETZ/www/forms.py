from django import forms

from .models import ImprovementProposal


class ImprovementProposalForm(forms.ModelForm):
    class Meta:
        model = ImprovementProposal
        fields = [
            'department',
            'participation_coefficient',
            'current_situation',
            'current_situation_sketch',
            'proposed_solution',
            'solution_sketch',
            'expected_result',
            'ready_to_implement',
            'required_resources'
        ]
        widgets = {
            'current_situation': forms.Textarea(attrs={'rows': 4}),
            'proposed_solution': forms.Textarea(attrs={'rows': 4}),
            'expected_result': forms.Textarea(attrs={'rows': 3}),
            'required_resources': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'ready_to_implement': 'Готов внедрить решение самостоятельно',
        }