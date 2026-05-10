#pydantic use for data validation

#pydantic works in three steps :

    #1: define pydantic model means define one class
        # here we will define ideal schema of data like we will provide data feilds its type can give, validations etc..

    #2: instantiate model with raw name like creatinf an object and it will be validated 

    #3: pass that model to our function using that object function will validate data


#example:
# now first have to install pydantic

#1st step import basemodel for create a class(model)

from pydantic import BaseModel

#here we did first step we defined our pydantic model and decided our basic schema that we want this values and in this datatpe we can apply validations here too

class Patient(BaseModel):
    name : str
    age : int


#2nd step:

#now create object with example data 
#we will create dictonary with raw data:
Patient_info={'name':'yash','age':21}#raw data dict
#now we will create object
patient1=Patient(**Patient_info) #we pass our raw data dict in that Patient class we use ** for unpack that dict and now our data will go to that class and if our data follow datatype we defined in that class like name should string and age should be int than that will be stored in patient1 variable



#3rd step:
# now we will send that class to our funtion 

# imagine it is just function which will be insert given data into database 
def insert_data(patient=Patient): #here we  created object of that class
    print(patient.name)
    print(patient.age)#we can pass our data like this to database with rules applied that data should be in give type
    print('inserted')

# now lets call function with object of patient1

insert_data(patient1) #if data we will be perfect data we will be inserted
#now like this we can create more function and can  reuse this model and can make changes in that model not have to make changes in all functions

# for example im creating a update function and will reuse this model in that
patient2_info={'name':'heref','age':'34'} #if u pass int in string pydantic automatically convert it into int
patient2=Patient(**patient2_info)
def update_data(patient=Patient): #here we  created object of that class
    print(patient.name)
    print(patient.age)#we can pass our data like this to database with rules applied that data should be in give type
    print('updated')

update_data(patient2)

