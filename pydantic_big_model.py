from pydantic import BaseModel ,EmailStr,AnyUrl,Field ,field_validator ,model_validator
from typing import List ,Dict ,Optional ,Annotated

class Patient(BaseModel):
    #Annotated use for attach metadata like title ,description of field
    name : str =Annotated[str,Field(max_length=50,title='name of patient ',description='give name of patient here ')]
    email : EmailStr #here pydantic provides email validation by itself we not need to write email validation code 
    linkedin_url :AnyUrl #this will validate url by itself will not allow invalid url
    #for custom validation for specific requirement we use field function
    age : int =Field(gt=0,lt=100)#here we put vaidation that age should be greater than 0 and less than 100
    weight : Annotated[float , Field(gt=0,strict=True,description="weight must be greater than zero")] #here we will check that weight should be greater than 0 and strict will not allow number in string form in data like pydantic undertsand number in string and convert it into float bu strict restrict that behavoiur
    married : Annotated[bool,Field(default=None,description='is pateint married or not')]
    #why dont we just write allergies = List becoz that will not check that list data is string or not for check 2 validation that data should be in list and in string form we define like this List(str)
    allergies : Annotated[Optional[List[str]] ,Field(default=None,max_length=5)] #with optional we can make this field optional one if we will not fill this field it will get None in print # here we will take list of allergy from patient thats why we definr list of strings
    contact_info :Dict[str,str] # here we will take contact in dict like 2 strings : email : xy@gmail.com .dict of str

    @field_validator('email')
    @classmethod
    def email_validator(cls,value):
        valid_domains="icici.com" # we want to allow only email with this domain
        domain_name=value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('email domain must be icici.com')
        return value
    
    #we can also perform transormation using field validator 
    #field validator use for single field validation 
    @field_validator('name')
    @classmethod
    def name_validator(cls,value):
        return value.upper() # this will convert name into title case like yash will become Yash
    
#model_validator use for whole model validation like we want to check that if patient age is above 60 then emergency contact is required in contact info dict
    @model_validator(mode='after')
    def validate_emergency_contact(cls,model):
        if model.age>60 and 'emergency' not in model.contact_info:
            raise ValueError('emergency contact is required for patients above 60 years old')
        else:
            return model

Patient_info={'name':'yash','email':'yash@icici.com','linkedin_url':'https://www.linkedin.com/in/yash','age':88,'weight':75,'married':0,'allergies':['pollen','dust'],'contact_info':{'email':'xyz@gmail.com','phone':'9687675454','emergency':'9876543210'}}#raw data dict
#now we will create object
patient1=Patient(**Patient_info)



def insert_data(patient=Patient): #here we  created object of that class
    print(patient.name)
    print(patient.age)


insert_data(patient1)