from django.shortcuts import render
from django.contrib import messages
from rest_framework.response import Response
from rest_framework import status
from .forms import ApprovalForm
import pandas as pd
import joblib


def approvereject(unit):
    try:
        model = joblib.load("D:\\BankBuddy Intern\\Loan Management\\loan_model.pkl")
        scaler = joblib.load("D:\\BankBuddy Intern\\Loan Management\\scalers.pkl")
        X = scaler.transform(unit)
        y_pred = model.predict(X)
        y_pred = (y_pred > 0.55)
        new_df = pd.DataFrame(y_pred, columns=['Status'])
        new_df = new_df.replace({True: 'Approved', False: 'Rejected'})
        return (new_df['Status'][0])
    except ValueError as e:
        return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)

def ohevalue(df):
    ohe_col = joblib.load("D:\\BankBuddy Intern\\Loan Management\\allcol.pkl")
    cat_column = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area']
    df_processed = pd.get_dummies(df, columns=cat_column)
    new_dict = {}
    for i in ohe_col:
        if i in df_processed.columns:
            new_dict[i] = df_processed[i].values
        else:
            new_dict[i] = 0
    
    new_df = pd.DataFrame(new_dict)
    return new_df



# Create your views here.
def customerForm(request):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            Dependants = form.cleaned_data['Dependants']
            ApplicantIncome = form.cleaned_data['ApplicantIncome']
            CoapplicatIncome = form.cleaned_data['CoapplicatIncome']
            LoanAmount = form.cleaned_data['LoanAmount']
            Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
            Credit_History = form.cleaned_data['Credit_History']
            Gender = form.cleaned_data['Gender']
            Married = form.cleaned_data['Married']
            Education = form.cleaned_data['Education']
            Self_Employed = form.cleaned_data['Self_Employed']
            Property_Area = form.cleaned_data['Property_Area']
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            # print(ohevalue(df))
            loanStatus = approvereject(ohevalue(df))
            messages.success(request, loanStatus)

    form = ApprovalForm()
    return render(request, 'myform.html', {'form': form})