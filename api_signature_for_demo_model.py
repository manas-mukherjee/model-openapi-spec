from typing import Dict
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field

app = FastAPI()

class InputData(BaseModel):   
    entity_id: str = Field(..., example="ssn123", x_intuit_annotation={"required": True, "unique": True, "entity_identifier": True, "description": "The unique identifier of the for this input"})
    age: int
    income: int
    credit_score: int

class OutputData(BaseModel):
    prediction: int = Field(..., x_intuit_annotation={"description": "This is the prediction class"})
    prediction_proba: float

@app.post("/predict", response_model=OutputData, openapi_extra={"x-model-assetid": "12345abcde67890", "x-model-versionid": "1.1"})
def predict(data: InputData):
    try:
        prediction = 1 # prediction = model.predict(data)
        prediction_proba = 0.9
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return OutputData(prediction=prediction, prediction_proba=prediction_proba)

# --------------Code to generate openapi specification corresponding to the above predict function -------------#
from fastapi.openapi.utils import get_openapi
import yaml
openapi_schema = get_openapi(
    title="My ML model prediction API",
    version="1.0.0",
    routes=app.routes,
)

# Convert the dictionary to YAML format
yaml_data = yaml.dump(openapi_schema)
# print(f"type(yaml_data): {type(yaml_data)}")

import re

yaml_data_modified = re.sub("x_intuit_annotation","x-intuit_annotation",yaml_data)

yaml_data = yaml_data.replace("x_intuit_annotation", "x-intuit_annotation")
# Write the YAML data to a file
with open('model_code_openapi_2.yml', 'w') as f:
    f.write(yaml_data_modified)
