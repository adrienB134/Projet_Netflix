import json
import pandas as pd
import boto3
from io import StringIO


def lambda_handler(event, context):
    data = pd.read_json(event, orient="split")

    data.to_csv(
        "s3://netflix-bucket-jedha-lead/film.csv",
        storage_options={
            "key": "",
            "secret": "",
        },
    )

    return {
        "statusCode": 200,
    }
