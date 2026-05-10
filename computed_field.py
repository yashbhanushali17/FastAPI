from pydantic import BaseModel,EmailStr , computed_field
from typing import List , Dict

class Patient(BaseModel):
    name : str
    email : EmailStr
    age : int
    weight : float
    hieght:float
    married : bool
    allergies : list[str]
    contact_info :Dict[str,str]

    #computed field use to create field to get data from other fields not from user like from hieght and weight we can calculate bmi and return it in computed field
    @computed_field
    @property
    def bmi(self) -> float:
        bmi= round(self.weight/(self.hieght**2),2)
        return bmi


Patient_info={'name':'yash','email':'yash@icici.com','age':88,'weight':75,'hieght':1.75,'married':0,'allergies':['pollen','dust'],'contact_info':{'email':'xyz@gmail.com','phone':'9687675454','emergency':'9876543210'}}#raw data dict
#now we will create object
patient1=Patient(**Patient_info)

def insert_data(patient=Patient): #here we  created object of that class
    print(patient.name)
    print(patient.age)
    print(patient.bmi) # here we can access computed field like normal field

insert_data(patient1)