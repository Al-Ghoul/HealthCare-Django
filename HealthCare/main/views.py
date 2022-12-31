from django.shortcuts import render, redirect
from .forms import HealthCareUserForms, SymptomForms, SymptomSelectionForm, DaysForms
from .utils import cols, check_pattern, recurse, sec_predict, calc_condition, description_list, precautionDictionary


def MainView(request):
    request.session.flush()
    if request.method == 'POST':
        form = HealthCareUserForms(request.POST)
        if form.is_valid():
            request.session['name'] = form.cleaned_data['name']
            return redirect('SymptomsSearchView')
    else:
        form = HealthCareUserForms()
    context = {
        'title': '',
        'form': form,
    }
    return render(request, 'main/main.html', context)


def SymptomsSearchView(request):
    if not request.session.get('name', False):
        return redirect('Home')

    if request.method == 'POST':
        form = SymptomForms(request.POST)
        if form.is_valid():
            request.session['Symptom'] = form.cleaned_data['symptom'].lower()
            return redirect('SymptomsSelectionView')
    else:
        form = SymptomForms()
    context = {
        'title': request.session['name'],
        'form': form,
    }
    return render(request, 'main/Search.html', context)


def SymptomsSelectionView(request):
    if not request.session.get('Symptom', False):
        return redirect('SymptomsSearchView')
        
    symptomName = request.session['Symptom']
    feature_names = cols
    chk_dis = ",".join(feature_names).split(",")
    _, cnf_dis = check_pattern(chk_dis, symptomName)

    if (cnf_dis == []):
        return redirect('SymptomsSearchView')

    if request.method == 'POST':
        form = SymptomSelectionForm(request.POST)
        if form.is_valid():
            request.session['Symptom_num'] = form.cleaned_data['symptom_num']
            return redirect('SymptomsAnalyzeView')
    else:
        form = SymptomSelectionForm()

    context = {
        'title': '',
        'form': form,
        'Symptoms': cnf_dis
    }
    return render(request, 'main/Selection.html', context)


def SymptomsAnalyzeView(request):
    if not request.session.get('Symptom', False) or not request.session.get('Symptom_num', False):
        return redirect('SymptomsSearchView')

    symptomName = request.session['Symptom']
    feature_names = cols
    chk_dis = ",".join(feature_names).split(",")
    _, cnf_dis = check_pattern(chk_dis, symptomName)
    symp = None

    try:
        symp = cnf_dis[int(request.session['Symptom_num']) - 1]
    except:
        print("Enter valid symptom.")
        return redirect('Home')

    if request.method == 'POST':
        form = DaysForms(request.POST)
        if form.is_valid():
            request.session['symp'] = symp
            request.session['days'] = form.cleaned_data['num_days']
            return redirect('QuestionsView', 0)
    else:
        form = DaysForms()

    context = {
        'title': '',
        'form': form,
        'symp': symp
    }
    return render(request, 'main/Analyze.html', context)


def QuestionsView(request, answer):
    if not request.session.get('symp', False):
        return redirect('SymptomsSearchView')

    if not request.session.get('questions', False):
        recurse(request)
        request.session['current_question'] = 0
        request.session['questions_length'] = len(request.session['questions'])
        request.session['symptomps_list'] = []

    if answer == '1':
        request.session['symptomps_list'].append(
            request.session['questions'][request.session['current_question'] - 1])
    if request.session['current_question'] >= request.session['questions_length']:
        return redirect('ResultsView')

    context = {
        'title': '',
        'Question': request.session['questions'][request.session['current_question']],
    }
    request.session['current_question'] += 1
    return render(request, 'main/Questions.html', context)


def ResultsView(request):
    if not request.session.get('symptomps_list', False):
        return redirect('Home')
    second_prediction = sec_predict(request.session['symptomps_list'])
    condition_message = calc_condition(
        request.session['symptomps_list'], int(request.session['days']))
    present_disease = request.session['present_disease']
    present_disease_list = []
    other_present_disease_list = []
    if (present_disease[0] == second_prediction[0]):
        present_disease_list.append(present_disease[0])
        present_disease_list.append(description_list[present_disease[0]])
    else:
        present_disease_list.append(present_disease[0])
        other_present_disease_list.append(second_prediction[0])
        present_disease_list.append(description_list[present_disease[0]])
        present_disease_list.append(description_list[second_prediction[0]])
    precution_list = precautionDictionary[present_disease[0]]

    context = {
        'title': '',
        'Condition': condition_message,
        'PresetDiseases': present_disease_list,
        'OtherPresetDiseases': other_present_disease_list,
        'PreCautions': precution_list
    }
    return render(request, 'main/Results.html', context)
