import uvicorn
import json
import pandas as pd
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, Request
import boto3
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


description = """
Affichage des prédictions de films pour les utilisateurs. 
"""


app = FastAPI(
    title="👨‍💼 Prediction app",
    description=description,
    version="0.1",
)

templates = Jinja2Templates(directory="./templates")
app.mount("/templates", StaticFiles(directory="./templates"), name="templates")


@app.get("/")
async def get_predictions(request: Request):
    URI_DU_FICHIER_S3 = "s3://netflix-bucket-jedha-lead/predictions.csv"
    bucket_name, object_key = URI_DU_FICHIER_S3.split("//")[1].split("/", 1)
    s3 = boto3.resource("s3")
    response = s3.Bucket(bucket_name).download_file(object_key, "predictions.csv")
    df = pd.read_csv("predictions.csv")

    response = {f"{df['Name'][i]}": df["link"][i] for i in range(0, 10)}

    return templates.TemplateResponse(
        "index.html", {"request": request, "response": response}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, reload=True)
