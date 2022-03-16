import joblib
import numpy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sms
df=pd.read_csv("data.csv")
print(df)
print(df.isna().sum())
print(df.shape)
df=df.dropna(axis=1)
print(df.shape)
print(df.describe())
print(df.head())
print(df['diagnosis'].value_counts())
from sklearn.preprocessing import LabelEncoder
label_en_y=LabelEncoder()
df.iloc[:,1]=label_en_y.fit_transform(df.iloc[:,1].values)
print(df.head())
x=df.iloc[:,2:31].values
y=df.iloc[:,1].values
from sklearn.model_selection import train_test_split
Xtrain,Xtest,Ytrain,Ytest=train_test_split(x,y,test_size=0.20,random_state=0)
from sklearn.preprocessing import StandardScaler

Xtrain=StandardScaler().fit_transform(Xtrain)
Xtest=StandardScaler().fit_transform(Xtest)
def logModel(Xtrain,Ytrain):
    
    from sklearn.linear_model import LogisticRegression
    log=LogisticRegression(random_state=0)
    log.fit(Xtrain,Ytrain)
    from sklearn.tree import  DecisionTreeClassifier
    tree=DecisionTreeClassifier(random_state=0,criterion="entropy")
    tree.fit(Xtrain,Ytrain)

    from sklearn.ensemble import RandomForestClassifier
    forest=RandomForestClassifier(random_state=0,criterion="entropy",n_estimators=10)

    forest.fit(Xtrain,Ytrain)
  
    print("logistic",log.score(Xtrain,Ytrain))
    print("Decision",tree.score(Xtrain,Ytrain))
    print("RandomForest",forest.score(Xtrain,Ytrain))
    
    return log,tree,forest


model=logModel(Xtrain,Ytrain)    
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report 


for i in range(len(model)):
    print("model",i)
    
    
    print(classification_report(Ytest,model[i].predict(Xtest)))
    cf=confusion_matrix(Ytest,model[i].predict(Xtest))
    sms.heatmap()
    plt.show()

    print("Accurary: ",accuracy_score(Ytest,model[i].predict(Xtest)))
   
pred=model[2].predict(Xtest)    


from joblib import dump
dump(model[2],"cancer_prediction_md.joblib")
  
model2=joblib.load('D:/academic_projects\Breast-cancer-prediction-ML-Python-master\cancer_prediction_md.joblib')
prd=model2.predict(Xtest)[1]


if prd==1:
    print("M")
elif prd==0:
    print("B")    




