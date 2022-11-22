from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class model_input(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: int


diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))


@app.post('/diabetes_prediction')
def diabetes_prediction(input_parameters: model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)

    pr = input_dictionary['Pregnancies']
    gl = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    st = input_dictionary['SkinThickness']
    il = input_dictionary['Insulin']
    bm = input_dictionary['BMI']
    dp = input_dictionary['DiabetesPedigreeFunction']
    ag = input_dictionary['Age']

    input_list = [pr, gl, bp, st, il, bm, dp, ag]

    prediction = diabetes_model.predict([input_list])

    if prediction[0] == 0:
        return "The person has no Diabetes."
    else:
        return "The person has Diabetes."
