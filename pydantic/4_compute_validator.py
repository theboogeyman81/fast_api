from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict


class Patient(BaseModel):
    name:str
    email:EmailStr
    age:int
    weight:float
    height:float
    married:bool
    allergies: List[str]
    contact_details:Dict[str,str]


    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi



def update_patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print(patient.bmi)
    print('updated')


patient_info = {
    'name':'pratham',
    'email':'abc@icici.com',
    'age': 78,
    'weight': 75.2,
    'height' : 1.72,
    'married' : True,
    'allergies' : ['pollen' , 'dust'],
    'contact_details':{'phone' : '234567891' , 'emergency' : '2453466232'}

}
    

patient1= Patient(**patient_info)

update_patient_data(patient1)