from fastapi import FastAPI
from fastapi.responses import JSONResponse 
from pydantic import BaseModel, Field, computed_field
from typing import Literal , Annotated
import pickle
import pandas as pd 
import sys

# Compatibility fix for sklearn version mismatch with _RemainderColsList
# This handles pickle files created with different sklearn versions
import sklearn.compose._column_transformer as ct_module

# Check if _RemainderColsList exists, if not create a compatibility class
if not hasattr(ct_module, '_RemainderColsList'):
    class _RemainderColsList(list):
        """Compatibility class for sklearn _RemainderColsList"""
        pass
    # Add to the module so pickle can find it
    ct_module._RemainderColsList = _RemainderColsList
    # Register in sys.modules for pickle's import system
    sys.modules['sklearn.compose._column_transformer._RemainderColsList'] = _RemainderColsList

# Custom unpickler to handle missing attributes gracefully
class CompatibleUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Handle _RemainderColsList specifically
        if module == 'sklearn.compose._column_transformer' and name == '_RemainderColsList':
            if not hasattr(ct_module, '_RemainderColsList'):
                class _RemainderColsList(list):
                    pass
                ct_module._RemainderColsList = _RemainderColsList
            return ct_module._RemainderColsList
        return super().find_class(module, name)

#import the ml model 
with open('model (1).pkl' , 'rb') as f:
    model = CompatibleUnpickler(f).load()

app = FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


#pydantic model to validate incoming data
class UserInput(BaseModel):
    
    age:Annotated[int , Field(..., gt=0 , lt=120, description='Age of the user')]
    weight : Annotated[float , Field(..., gt=0 , description='Weight of the user')]
    height: Annotated[float,Field(...,gt=0,description='Height of the user')]
    income_lpa: Annotated[float, Field(...,description='Annual salary of the user in lpa')]
    smoker: Annotated[bool , Field(...,description='Is user a smoker')]
    city: Annotated[str , Field(...,description='The city that the user belongs to')]
    occupation:Annotated[Literal['retired' , 'freelancer' , 'student' , 'government_job' , 'business_owner' , 'unemployed' , 'private_job' ] , Field(...,description='Occupation of the user')]


    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi> 30:
            return 'high'
        elif self.smoker and self.bmi > 27:
            return 'medium'
        else:
            return 'low'

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle_aged'
        else:
            return 'senior'
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else: 
            return 3

@app.post('/predict')
def perdict_permium(data : UserInput):

    input_df = pd.DataFrame([{
        'bmi' : data.bmi,
        'age_group' : data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier,
        'income_lpa' : data.income_lpa,
        'occupation' : data.occupation
    }])


    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code = 200 , content={'predicted_category':prediction})

