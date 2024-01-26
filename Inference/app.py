import mlflow
import mlflow.pyfunc
from fastapi import FastAPI
from typing import Dict
import pandas as pd
import os
from imdb import Cinemagoer
from surprise import Reader, Dataset, SVD

app = FastAPI()

mlflow.set_tracking_uri("https://mlflowjedhalead-a7146c8dff2f.herokuapp.com")
model_name = "Netflix_reco"
alias = "champion"


def treat_bad_lines(bad_line: list[str]) -> list[str] | None:
    return [bad_line[0], bad_line[1], f"{','.join(bad_line[2:])}"]


def search_image(film: str) -> str:
    ia = Cinemagoer()
    try:
        link = ia.search_movie(film)[0]["cover url"]
    except:
        link = film
    return link


@app.get("/")
async def index():
    return "hello!"


@app.get("/predict")
async def predict(user: int) -> None:
    movie_database = pd.read_csv(
        "/home/ubuntu/movie_titles.csv",
        encoding="ISO-8859-1",
        header=None,
        names=["Movie_Id", "Year", "Name"],
        on_bad_lines=treat_bad_lines,
        engine="python",
    )

    recommander = mlflow.sklearn.load_model(f"models:/{model_name}@{alias}")

    movie_database["Estimate_Score"] = movie_database["Movie_Id"].apply(
        lambda x: recommander.predict(user, x).est
    )
    movie_database = movie_database.sort_values("Estimate_Score", ascending=False).head(
        10
    )

    ia = Cinemagoer()

    movie_database["link"] = movie_database["Name"].apply(lambda x: search_image(x))

    movie_database[["Name", "link"]].to_csv(
        "s3://netflix-bucket-jedha-lead/predictions.csv",
        storage_options={
            "key": "",
            "secret": "",
        },
        index=False,
    )
    movie_database = movie_database["Name"].to_list()

    print(f"{movie_database}")
