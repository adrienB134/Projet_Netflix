import json
import pandas as pd
from io import StringIO
import requests


def lambda_handler(event, context):
    data = pd.read_json(event[0]["payload"]["value"], orient="split")

    data.to_csv(
        "s3://netflix-bucket-jedha-lead/film.csv",
        storage_options={
            "key": "",
            "secret": "",
        },
    )

    user = int(data["customerID"].iloc[0])

    requests.get(
        "http://ec2-13-36-178-62.eu-west-3.compute.amazonaws.com/predict",
        params={"user": user},
    )

    return {
        "statusCode": 200,
    }
