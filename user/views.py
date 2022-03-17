from django.http import HttpResponse
from django.shortcuts import render
from . models import Usertbl,Predict
from django.contrib.sessions.models import Session

# Create your views here.
def userreg(request):
    if request.method=="POST":
        fn=request.POST.get("fn")
        user=request.POST.get("usr")
        passw=request.POST.get("ps")
        eml=request.POST.get("eml")
        mb=request.POST.get("mb")
        obj=Usertbl.objects.create(fname=fn,username=user,password=passw,email=eml,mobile=mb)
        obj.save()
        return HttpResponse("<h4> Registrtion Successfully</h4> <a href='/login'>Login </a>")
    return render(request,'userreg.html')
def index(request):
    return render(request,'index.html')   
def login(req):
    if req.method=="POST":
        user=req.POST.get("usr")
        pss=req.POST.get("ps")
        req.session['username']=user  
        req.session['password']=pss
        obj=Usertbl.objects.filter(username=user,password=pss)
        for l in obj:
            idn=l.id
            nam=l.fname
        pr=Predict.objects.filter(id=idn)
        if obj:
            return render(req,'homepage.html',{'fname':nam,'data':pr,'url':"https://www.cancer.gov/types/mesothelioma/patient/mesothelioma-treatment-pdq"})
        else:
            return HttpResponse("Check Your Username and Password <a href='/'>Login</a>")    
def home(req):
    if req.session['username']!="" and req.session['password']!="":
        user=req.session['username']
        pss=req.session['password']
        obj=Usertbl.objects.filter(username=user,password=pss)
        for l in obj:
            idn=l.id
            nam=l.fname
        print(idn,"idno user")    
        pr=Predict.objects.all()
        return render(req,'homepage.html',{'fname':nam,'data':pr})
    else:
        return render(req,'index.html')    




def setData(request):
    if request.method=="POST":
        dt=[]
        dtn=[]
        v="inp"
        pnt=request.POST.get('pnt')
        for i in range(1,30):
            v2=v+str(i)
            dt.append(request.POST.get(v2))
        print(dt)    
        user=request.session['username']
        pss=request.session['password']
       
        obj=Usertbl.objects.filter(username=user,password=pss)
        for l in obj:
            idn=l.id
            print(idn)
       
        wcsv(dt)     
        result=modelexecution(dt)    
        print(result)
        if result==1:
            
            rs={'title':"Malignant","link":"https://www.medifee.com/list/best-cancer-hospital-in-india" ,"pic":"'images/abcdmoles.jpg'","About":"The term malignancy refers to the presence of cancerous cells that have the ability to spread to other sites in the body (metastasize) or to invade nearby (locally) and destroy tissues. Malignant cells tend to have fast, uncontrolled growth and do not die normally due to changes in their genetic makeup.Malignant cells that are resistant to treatment may return after all detectable traces of them have been removed or destroyed."}
           
            pr=Predict.objects.create(userid=idn,prediction='Malignant',patient=pnt) 
            pr.save()   
            return render(request,'result.html',{'result':rs,'valu':True})
        elif result==0:
           
            pr=Predict.objects.create(userid=idn,prediction='Benign ',patient=pnt) 
            pr.save()  
            abt="Benign refers to a condition, tumor, or growth that is not cancerous. This means that it does not spread to other parts of the body. It does not invade nearby tissue. Sometimes, a condition is called benign to suggest it is not dangerous or serious. In general, a benign tumor grows slowly and is not harmful."
            rs={'title':"benign","link":"https://www.medifee.com/list/best-cancer-hospital-in-india","About":abt}
            return render(request,'result.html',{'result':rs,'valu':False})


    else:
       
        return render(request,'prediction.html')   
def modelexecution(ls):
    import joblib
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sms
    df=pd.read_csv("inputdata.csv")
    # df1=pd.DataFrame(ls)
    # df2=pd.to_numeric(ls,downcast='float')
   
    df1=pd.DataFrame(ls)
    d=df.iloc[:,0:29].values
    print(df.isna().sum())
    print(df.shape)
    df=df.dropna(axis=1)
    print(df.shape)
    print(df.describe())
    print(df.head())

    print(d)
    lst=[]
    for i in df1:
        lst.append(i)



    df2=pd.to_numeric(lst,downcast="float")
    print(df2,"df2")
    
    model2=joblib.load('D:/academic_projects\Breast-cancer-prediction-ML-Python-master\cancer_prediction_md.joblib')    
    prd=model2.predict(df)
    return prd
def treatment(request):
    return render(request,'treatmentM.html')
def treatment2(request):
    return render(request,'treatB.html')

def wcsv(dat):
    head=["radius_mean","texture_mean","perimeter_mean","area_mean","smoothness_mean","compactness_mean","concavity_mean","concave points_mean","symmetry_mean","fractal_dimension_mean","radius_se","texture_se","perimeter_se","area_se","smoothness_se","compactness_se","concavity_se","concave points_se","symmetry_se","fractal_dimension_se","radius_worst","texture_worst","perimeter_worst","area_worst","smoothness_worst","compactness_worst","concavity_worst","concave points_worst","symmetry_worst","fractal_dimension_worst"]
    filename="inputdata.csv"
    with  open(filename,'w') as file:
        for header in head:
             file.write(str(header)+",")
        file.write('\n')     
        for dt in dat:
            file.write(str(dt)+",")
        file.write('\n')    

def logout(request):
    request.session['username']="nill"
    request.session['password']="nill"

    return render(request,"index.html")