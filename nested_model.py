from pydantic import BaseModel


class Address(BaseModel):
    
    city :str
    state:str
    pin:str

class Patient(BaseModel):
    name :str
    gender :str
    age:int
    address :Address # here we are using nested model address in patient model
address_info={'city':'ahemdabad','state':'gujrat','pin':'380015'}
address1= Address(**address_info)

patient_info={'name':'yash','gender':'male','age':21,'address':address1} # here we are passing address info dict in patient info dict

patient1=Patient(**patient_info)


print(patient1)
print(patient1.address) # here we can access address info like this
print(patient1.address.city) # here we can access city info like this