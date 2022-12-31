from django import forms


class HealthCareUserForms(forms.Form):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': '''
                    form-control
                    block
                    w-full
                    px-4
                    py-2
                    text-xl
                    font-normal
                    text-gray-700
                    bg-white bg-clip-padding
                    border border-solid border-gray-300
                    rounded
                    transition
                    ease-in-out
                    m-0
                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
        '''}))

    def clean_name(self):
        name = self.cleaned_data['name']
        if name == '':
            raise forms.ValidationError("Name can not be blank.")
        return name


class SymptomForms(forms.Form):
    symptom = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off', 'class': '''
                    form-control
                    block
                    w-full
                    px-4
                    py-2
                    text-xl
                    font-normal
                    text-gray-700
                    bg-white bg-clip-padding
                    border border-solid border-gray-300
                    rounded
                    transition
                    ease-in-out
                    m-0
                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
        '''}))

    def clean_symptom(self):
        symptom = self.cleaned_data['symptom']
        if symptom == '':
            raise forms.ValidationError("Symptom can not be blank.")
        return symptom


class SymptomSelectionForm(forms.Form):
    symptom_num = forms.CharField(widget=forms.NumberInput(
        attrs={'autocomplete': 'off', 'class': '''
                    form-control
                    block
                    w-full
                    px-4
                    py-2
                    text-xl
                    font-normal
                    text-gray-700
                    bg-white bg-clip-padding
                    border border-solid border-gray-300
                    rounded
                    transition
                    ease-in-out
                    m-0
                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
        '''}))

    def clean_symptom_num(self):
        symptom_num = self.cleaned_data['symptom_num']
        if symptom_num == '':
            raise forms.ValidationError("Symptom Number can not be blank.")
        return symptom_num


class DaysForms(forms.Form):
    num_days = forms.CharField(widget=forms.NumberInput(
        attrs={'autocomplete': 'off', 'class': '''
                    form-control
                    block
                    w-full
                    px-4
                    py-2
                    text-xl
                    font-normal
                    text-gray-700
                    bg-white bg-clip-padding
                    border border-solid border-gray-300
                    rounded
                    transition
                    ease-in-out
                    m-0
                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
        '''}))

    def clean_num_days(self):
        num_days = self.cleaned_data['num_days']
        if num_days == '':
            raise forms.ValidationError("Days can not be blank.")
        return num_days
