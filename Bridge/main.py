import mlflow.pyfunc
from fastapi import FastAPI
from typing import Dict
import pandas as pd
from surprise import Reader, Dataset, SVD

model_name = "Netflix_reco"
alias = "champion"
movie_database = pd.read_csv("s3://movie_titles.csv")
app = FastAPI()


@app.get("/predict")
async def predict(data: Dict):
    user = data["user_id"]
    last_seen_movie = data["last_seen_movie"]

    recommander = mlflow.pyfunc.load_model(f"models:/{model_name}@{alias}")

    # on filtre sur le dataset de base pour conserver uniquement les films non vus par l'user
    mask = (movie_database["Cust_Id"] != user) & (
        movie_database["Movie_Name"] != last_seen_movie
    )
    unseen_by_user = movie_database[mask]
    unseen_by_user = unseen_by_user["Movie_Id"].unique()

    # on conserve dans le dataset des titre de film, ceux qu'il n'a pas vus.

    unseen_by_user["Estimate_Score"] = unseen_by_user["Movie_Id"].apply(
        lambda x: recommander.predict(user, x).est
    )

    message = (
        unseen_by_user.sort_values("Estimate_Score", ascending=False)
        .head(10)
        .to_json(orient="split")
    )

    return message
