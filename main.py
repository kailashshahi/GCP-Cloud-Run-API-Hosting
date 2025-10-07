from fastapi import FastAPI
from pydantic import BaseModel
from typing import Type
import json
import os
from fastapi.middleware.cors import CORSMiddleware


class Student(BaseModel):
    id:str
    name:str
    address:str
    email:str
    


app=FastAPI()
# if your frontend domain is known, replace "*" with the actual origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path=os.path.join(os.getcwd(),"Database/student.json")

data=[{
        "id":"101",
        "name":"kailash singh",
        "address":"gurgoan",
        "email":"kailash.singh@indixpert.com"
        
    },
     {
        "id":"102",
        "name":"Indixpert",
        "address":"gurgoan",
        "email":"Indixpert@gmail.com"
        
    }
]

@app.get("/")
def CheckServerStatus():
    return {"message":"Indixpert - API- Server is working and active.....","statuscode":200}

@app.get("/test")
def GetStudentRegistration(studentid:str,email:str):
    try:
        if not studentid.isdigit():
            return {"error":"student id is not integer"}
          
        output={"message":"success","statuscode":200,"id":studentid,"email":email} 
        return output
    except Exception as e:
        return {"ERROR":e}
    
@app.get("/registration")
def GetStudentRegistration(): 
        data=ReadDBFromJson() 
        output={"message":"success","statuscode":200,"data":data}  
        return output
   
    
    
@app.post("/registration")
def StudentRegistration(student:Student):#variable : type (which type the data is int str or class)
    data=ReadDBFromJson()
    data.append(student.__dict__)
    WriteJsonInDB(data)
    return {"message":"Student Record Created Successfully","statuscode":200} 

@app.put("/registration/{studentid}")
def UpdateStudentData(studentid:str,student:Student):  
    data=ReadDBFromJson()
    for s in data:
        if s["id"]==studentid and student.id==studentid:# match both the ID because some time query string value could be change.
            s.update(student.__dict__)
            #s["name"]=student.name so on
    WriteJsonInDB(data)
    output={"message":"success","statuscode":200,"Data":data}       
    return output
            
    
    

@app.delete("/registration/{studentid}") #you can use email as well

def DeleteStudentData(studentid:str):  
    data=ReadDBFromJson()
    for s in data:
        if s["id"]==studentid:# match both the ID because some time query string value could be change
            data.remove(s) #remove the dictionary from Listdata
            #s["name"]=student.name so on
    WriteJsonInDB(data)
    output={"message":"success","statuscode":200,"Data":data}       
    return output


def ReadDBFromJson():
    
    if os.path.exists(path):
        with open(path,'r') as file:
            data=json.load(file)
            return data
    else:
        with open(path,'w') as file:
            file.write("[]")
            
            
def WriteJsonInDB(jsondata):
    with open(path,'w') as file:
        json.dump(jsondata,file,indent=2)
         