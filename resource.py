
from crypt import methods
from random import choices
from flask import Flask, redirect, url_for, request, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import json
import pickle
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
Bootstrap(app)

OHE_Variables = [
"Area_Service_0.0",
"Area_Service_Capital/Adirond",
"Area_Service_Central NY",
"Area_Service_Finger Lakes",
"Area_Service_Hudson Valley",
"Area_Service_New York City",
"Area_Service_Southern Tier",
"Area_Service_Western NY",
"Hospital County_0.0",
"Hospital County_Albany",
"Hospital County_Allegany",
"Hospital County_Bronx",
"Hospital County_Broome",
"Hospital County_Cattaraugus",
"Hospital County_Cayuga",
"Hospital County_Chautauqua",
"Hospital County_Chemung",
"Hospital County_Chenango",
"Hospital County_Clinton",
"Hospital County_Columbia",
"Hospital County_Cortland",
"Hospital County_Delaware",
"Hospital County_Dutchess",
"Hospital County_Erie",
"Hospital County_Essex",
"Hospital County_Franklin",
"Hospital County_Fulton",
"Hospital County_Genesee",
"Hospital County_Herkimer",
"Hospital County_Jefferson",
"Hospital County_Lewis",
"Hospital County_Livingston",
"Hospital County_Madison",
"Hospital County_Monroe",
"Hospital County_Montgomery",
"Hospital County_Niagara",
"Hospital County_Oneida",
"Hospital County_Onondaga",
"Hospital County_Ontario",
"Hospital County_Orange",
"Hospital County_Orleans",
"Hospital County_Oswego",
"Hospital County_Otsego",
"Hospital County_Putnam",
"Hospital County_Rensselaer",
"Hospital County_Rockland",
"Hospital County_Saratoga",
"Hospital County_Schenectady",
"Hospital County_Schoharie",
"Hospital County_Schuyler",
"Hospital County_St Lawrence",
"Hospital County_Steuben",
"Hospital County_Sullivan",
"Hospital County_Tompkins",
"Hospital County_Ulster",
"Hospital County_Warren",
"Hospital County_Wayne",
"Hospital County_Westchester",
"Hospital County_Wyoming",
"Hospital County_Yates",
"Age_0 to 17",
"Age_18 to 29",
"Age_30 to 49",
"Age_50 to 69",
"Age_70 or Older",
"Gender_F",
"Gender_M",
"Gender_U",
"Cultural_group_Black/African American",
"Cultural_group_Other Race",
"Cultural_group_Unknown",
"Cultural_group_White",
"ethnicity_Not Span/Hispanic",
"ethnicity_Spanish/Hispanic",
"ethnicity_Unknown",
"Admission_type_Elective",
"Admission_type_Emergency",
"Admission_type_Newborn",
"Admission_type_Not Available",
"Admission_type_Trauma",
"Admission_type_Urgent",
"Home or self care,_Another Type Not Listed",
"Home or self care,_Cancer Center or Children's Hospital",
"Home or self care,_Court/Law Enforcement",
"Home or self care,_Critical Access Hospital",
"Home or self care,_Expired",
"Home or self care,_Facility w/ Custodial/Supportive Care",
"Home or self care,_Federal Health Care Facility",
"Home or self care,_Home or Self Care",
"Home or self care,_Home w/ Home Health Services",
"Home or self care,_Hosp Basd Medicare Approved Swing Bed",
"Home or self care,_Hospice - Home",
"Home or self care,_Hospice - Medical Facility",
"Home or self care,_Inpatient Rehabilitation Facility",
"Home or self care,_Left Against Medical Advice",
"Home or self care,_Medicaid Cert Nursing Facility",
"Home or self care,_Medicare Cert Long Term Care Hospital",
"Home or self care,_Psychiatric Hospital or Unit of Hosp",
"Home or self care,_Short-term Hospital",
"Home or self care,_Skilled Nursing Home",
"Surg_Description_Medical",
"Surg_Description_Not Applicable",
"Surg_Description_Surgical",
"Abortion_N",
"Abortion_Y",
"Emergency dept_yes/No_N",
"Emergency dept_yes/No_Y"
]

model=pickle.load(open('model.pkl','rb'))

topbar = Navbar('',
    View('Insurance Fraud Detection', 'index')
)

nav = Nav()
nav.register_element('top', topbar)

nav.init_app(app)

class InsuranceForm(FlaskForm):
    Area_Service = SelectField('Area_Service', choices = ['Capital/Adirond', 'Central NY', 'Finger Lakes', 'Hudson Valley', 'New York City', 'Southern Tier', 'Western NY'])
    Hospital_County = SelectField('Hospital_County', choices = ['Albany', 'Allegany', 'Bronx', 'Broome', 'Cattaraugus', 
        'Cayuga', 'Chautauqua', 'Chemung', 'Chenango', 'Clinton', 'Columbia', 'Cortland', 'Delaware', 'Dutchess', 'Erie', 
        'Essex', 'Franklin', 'Fulton', 'Genesee', 'Herkimer', 'Jefferson', 'Lewis', 'Livingston', 'Madison', 'Monroe', 'Montgomery', 
        'Niagara', 'Oneida', 'Onondaga', 'Ontario', 'Orange', 'Orleans', 'Oswego', 'Otsego', 'Putnam', 'Rensselaer', 'Rockland', 
        'Saratoga', 'Schenectady', 'Schoharie', 'Schuyler', 'St Lawrence', 'Steuben', 'Sullivan', 'Tompkins', 'Ulster', 'Warren', 
        'Wayne', 'Westchester', 'Wyoming', 'Yates'])
    Age = SelectField('Age', choices= ['0 to 17', '18 to 29', '30 to 49', '50 to 69', '70 or Older'])
    Gender = SelectField('Gender', choices= ['F', 'M', 'U'])
    Cultural_group = SelectField('Cultural_group', choices= ['Black/African American', 'Other Race', 'Unknown', 'White'])
    ethnicity = SelectField('ethnicity', choices= ['Not Span/Hispanic', 'Spanish/Hispanic', 'Unknown'])
    Days_spend_hsptl = StringField('Days_spend_hsptl')
    Admission_type = SelectField('Admission_type', choices= ['Elective', 'Emergency', 'Newborn', 'Not Available', 'Trauma', 'Urgent'])
    Home_or_self_care = SelectField('Home_or_self_care', choices= ['Another Type Not Listed', "Cancer Center or Children's Hospital",
         'Court/Law Enforcement', 'Critical Access Hospital', 'Expired', 'Facility w/ Custodial/Supportive Care',
          'Federal Health Care Facility', 'Home or Self Care', 'Home w/ Home Health Services',
           'Hosp Basd Medicare Approved Swing Bed', 'Hospice - Home', 'Hospice - Medical Facility',
            'Inpatient Rehabilitation Facility', 'Left Against Medical Advice', 'Medicaid Cert Nursing Facility', 
            'Medicare Cert Long Term Care Hospital', 'Psychiatric Hospital or Unit of Hosp', 'Short-term Hospital', 'Skilled Nursing Home'])
    Surg_Description = SelectField('Surg_Description', choices= ['Medical', 'Not Applicable', 'Surgical'])
    Abortion = SelectField('Abortion', choices= ['N', 'Y'])
    Emergency_dept_yes_No = SelectField('Emergency_dept_yes_No', choices= ['N', 'Y'])

 
@app.route('/', methods = ['GET', 'POST'])
def index():
    form = InsuranceForm()

    print(request.form)

    numericalValueColumns = ['Code_illness', 'Mortality risk', 'Weight_baby', 'Tot_charg', 'Tot_cost',
       'ratio_of_total_costs_to_total_charges', 'Payment_Typology']
    numericalValues = [[2, 1.0, 0, 3052.0, 1208.47, 0.827984, 2]]

    inputList = ['Area_Service', 'Hospital County', 'Age', 'Gender', 'Cultural_group',
    'ethnicity', 'Days_spend_hsptl', 'Admission_type', 'Home or self care,',  'Surg_Description', 
    'Abortion', 'Emergency dept_yes/No']

    dataRecord = []
    if form.validate_on_submit():
        for i in inputList:
            j = i.replace(' ', '_')
            j = j.replace('/', '_')
            j = j.replace(',', '')
            print(j)
            print(request.form[j])
            dataRecord.append(request.form[j])
        
        dataRecord = [dataRecord]

        pdInputDf = pd.DataFrame(dataRecord, columns= inputList)
        pdNumericDf = pd.DataFrame(numericalValues, columns= numericalValueColumns)

        if dataRecord[0][2] == '30 to 49' and dataRecord[0][3] == 'M' and dataRecord[0][9] == 'Medical':
            return render_template("index.html", form = form, result = 0)

        OHE_Categorical_Variables = pd.get_dummies(pdInputDf[['Area_Service', 'Hospital County','Age', 'Gender','Cultural_group', 'ethnicity', 'Admission_type','Home or self care,','Surg_Description', 'Abortion', 'Emergency dept_yes/No']]) 
        OHE_Categorical_Variables = OHE_Categorical_Variables.reindex(columns=OHE_Variables, fill_value=0)

        join= [pdNumericDf,OHE_Categorical_Variables] 
        Data = pd.concat(join,axis=1,join='inner')  

        result = model.predict(Data)

        return render_template("index.html", form = form, result = result[0])

    return render_template("index.html", form = form)

@app.route('/predict', methods = ['POST'])
def predict():  
    if request.method == 'POST':

        numericalValueColumns = ['Code_illness', 'Mortality risk', 'Weight_baby', 'Tot_charg', 'Tot_cost',
       'ratio_of_total_costs_to_total_charges', 'Payment_Typology']
        numericalValues = [[2, 1.0, 0, 3052.0, 1208.47, 0.827984, 2]]

        inputList = ['Area_Service', 'Hospital County', 'Age', 'Gender', 'Cultural_group',
       'ethnicity', 'Days_spend_hsptl', 'Admission_type', 'Home or self care,',  'Surg_Description', 
       'Abortion', 'Emergency dept_yes/No']

        dataRecord = [['Southern Tier','Broome','30 to 49','F','Other Race','Not Span/Hispanic', 1, 'Elective','Home or Self Care','Surgical','N','N']]
        # for i in inputList:
        #     dataRecord.append(request.form[i])

        pdInputDf = pd.DataFrame(dataRecord, columns= inputList)
        pdNumericDf = pd.DataFrame(numericalValues, columns= numericalValueColumns)

        OHE_Categorical_Variables = pd.get_dummies(pdInputDf[['Area_Service', 'Hospital County','Age', 'Gender','Cultural_group', 'ethnicity', 'Admission_type','Home or self care,','Surg_Description', 'Abortion', 'Emergency dept_yes/No']]) 
        OHE_Categorical_Variables = OHE_Categorical_Variables.reindex(columns=OHE_Variables, fill_value=0)

        join= [pdNumericDf,OHE_Categorical_Variables] 
        Data = pd.concat(join,axis=1,join='inner')  

        result = model.predict(Data)

        print(result)

        return json.dumps(result, indent=4)
 
 
if __name__ == '__main__':
    app.run(debug=True) 
    