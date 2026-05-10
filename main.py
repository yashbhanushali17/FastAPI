from fastapi import  FastAPI,Path ,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field , computed_field
import json
from  typing import Annotated ,Literal ,Optional
app=FastAPI()

class Patient(BaseModel):

    id : Annotated[str,Field(...,description='Id of the patient' , examples=['p001'])]
    name : Annotated[str,Field(...,description='Name of patient')]
    city : Annotated[str,Field(...,description='city where patient lives')]
    age : Annotated[int,Field(...,gt=0,lt=120,description='age of patient between 0 to 120')]
    gender : Annotated[Literal['Male','Female','Other'],Field(...,description='gender of patient')]
    height : Annotated[float,Field(...,gt=0,description='hieght of patient in mtrs')]
    weight : Annotated[float,Field(...,gt=0,description='weight of patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def prediction(self)-> str:
        if self.bmi <18.5:
            return 'Underweight'
        elif self.bmi <25:
            return 'Normal'
        
        elif self.bmi <30:
            return 'Overweight'
        
        else:
            return 'Obese'
        
class PatientUpdate(BaseModel):
    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str],Field(default=None)]
    age : Annotated[Optional[int],Field(default=None,gt=0)]
    gender : Annotated[Optional[Literal['Male','Female','Other']],Field(default=None)]
    height : Annotated[Optional[float],Field(default=None,gt=0)]
    weight : Annotated[Optional[float],Field(default=None,gt=0)]

    


#we will create function for load data:

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)  #we give our data dict here in funtion and stored means dump it into our f which is our patient json file 


@app.get("/")
def hello():
    return {"message":"hello world"}

@app.get("/about")
def about():
    return{"message":"hey there"}

@app.get("/view")
def view():
    data=load_data()

    return data

#path function use for improve readability of code 
@app.get("/patient/{p_id}")
def patient_details(p_id:str =Path(...,description="this is for find patient from db", examples="p001")):
    data=load_data()
    if p_id in data:
        return data[p_id]
    raise HTTPException(status_code=404,detail="patient not found")

@app.get("/sort")
def sorted_data(order_by:str=Query(...,description="sort data basis of height,weight or bmi"),order:str=Query('asc',description='sort in asc or dsc')):
    valid_fields=['height','weight','bmi']

    if order_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f'invalid field select from{valid_fields}')
    if order not in ['asc','dsc']:
        raise HTTPException(status_code=400,detail='invalid order choose between asc or dsc')
    
    data=load_data()
    sort_order= True if order=="dsc" else False
    sorted_data= sorted(data.values(),key= lambda x:x.get(order_by,0),reverse=sort_order)

    return sorted_data


@app.post('/Create')
def create_patient(patient :Patient):
    #now the data we will get validated from Patient validation model and will be stored in patient
    
    #step -1 load existing data'

    data =load_data()

    # step -2 check if patient already exists

    if patient.id in data:
        raise HTTPException(status_code=400,detail='patient already exists')

    # step -3 if patient not exists add new patient

    #now for 3rd step we need to convert this patient object to json so we can create patient in our data
    data[patient.id]=patient.model_dump(exclude=['id'])

    #now we convert object into the the json and store it into the data dictory based of id
    # like we do in dict values will be stored based on id  id is our key 

    #now we need to convert that data dict to json again so we can complete http request
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})




#now for del and update operations in database of patients we will follow this steps :

    #1 new pydantic model for operations coz in patent pydantic model we have fields which are compulsory required but in this operations sometimes we just want to to edit few fields only so validation can be wrong if we use the other model 

    #2 new data will be validated and will update in existing data base


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update :PatientUpdate):
    
    data=load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,details='patient not found')
    
    else:
        existing_patient_info=data[patient_id] #this is data of our existing patient which user ask for by calling its patient id

        updated_patient_info=patient_update.model_dump(exclude_unset=True)#we change that patient_update object into dictnory so can update that data into our existing data info
        #we set exclude unset true beacause this will exclude the data which person didnt give to update this eill only get data in dict which user send to update

    #now for change the value in existing patient data we will run a loop  in update patient data so we can update that data in existing partient
    #  

    for key,value in updated_patient_info.items(): #this will run loop till all field which user wants to update nt get extracted like user want to change city and contact so key willl this city and contact and value will be its details so loop will run items times which will 2 pairs key  and value of city and contact

        #after getting that key and value we will store that in existing data info
        existing_patient_info[key]=value


        #after this loop we will have new dict of updated info of patient

        #existing_patient_info -> pydantic object of patient model which will again calculate new bmi and vedict with computed field ->updated bmi +verdict -> that object into dictnary again

        #for create object of pydantic model of patient we need id of our existing patient which is not in dict of our existing patient info 
        existing_patient_info['id']=patient_id #so we will get that patient id in our dict so we can create its patient pydantic object

        patient_pydantic_obj=Patient(**existing_patient_info)

        existing_patient_info=patient_pydantic_obj.model_dump(exclude='id') #now we not need our key name id in our updated values dict so we exclude while converting obj into dict again
      
        #now we will set that data into main data
        data[patient_id]=existing_patient_info

        #now we will save it in data of json

        save_data(data)

    return JSONResponse(status_code=200,content={'message ':'patient updated'})


#now delete end point

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient deleted'})