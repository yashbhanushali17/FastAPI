#how can we export our pydantic model to json or dict

#pydantic give build in method to export our model to json or dict like .json() and .dict() method

from pydantic import BaseModel


class Address(BaseModel):
    
    city :str
    state:str
    pin:str

class Patient(BaseModel):
    name :str
    gender :str = "male"
    age:int
    address :Address # here we are using nested model address in patient model
address_info={'city':'ahemdabad','state':'gujrat','pin':'380015'}
address1= Address(**address_info)

patient_info={'name':'yash','gender':'male','age':21,'address':address1} # here we are passing address info dict in patient info dict

patient1=Patient(**patient_info)


print(patient1)
print(patient1.address) # here we can access address info like this
print(patient1.address.city) # here we can access city info like this


temp = patient1.model_dump()
print(temp) # this will give us dict of patient1 object
print(type(temp)) # this will give us type of temp variable which is dict


temp_json = patient1.model_dump_json()
print(temp_json) # this will give us json of patient1 object
print(type(temp_json)) # this will give us type of temp_json variable which is str because json is string format


#we can  control  the output like which field wants and which one not
temp = patient1.model_dump(include=['name','age']) # here we are including only name and age field in output
print(temp) # this will give us dict of patient1 object

temp = patient1.model_dump(exclude={'address'}) # here we are excluding address field in output
print(temp) # this will give us dict of patient1 object

temp = patient1.model_dump(exclude={'address':['state']}) # here we are excluding address field in output
print(temp) # this will give us dict of patient1 object

temp = patient1.model_dump(exclude_unset=True) #here this will not export the field which we dont have set in our info of patient like gender i dont pass it in info coz defualt i gave male n model so that unset field will not export in output