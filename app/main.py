# импортируем библиотеку для работы со случайными числами
import random

# импортируем класс для создания экземпляра FastAPI-приложения
from fastapi import FastAPI
from app.fast_api_handler import FastApiHandler

# создаём экземпляр FastAPI-приложения
app = FastAPI()

app.handler = FastApiHandler()

# обрабатываем запросы к корню приложения
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
# # обрабатываем запросы к специальному пути для получения предсказания модели
# # временно имитируем предсказание со случайной генерацией score
# @app.get("/api/churn/{user_id}")
# def get_prediction_for_item(user_id: str):
#     return {"user_id": user_id, "score": random.random()}
#
#
# @app.get("/service-status")
# def health_check():
#     return {"status": "ok"}
#
#
# @app.get("/api/credit/{client_id}")
# def is_credit_approved(client_id: int):
#     score = random.random()
#     if score < 0.8:
#         return {"approved": 0}
#     return {"approved": 1}


@app.post("/api/credit/")
def is_credit_approved(client_id: str, model_params: dict):
    """Функция определяет, выдать кредит или нет, на основании кредитного рейтинга клиента.

    Args:
        client_id (str): Идентификатор клиента.
        model_params (dict): Произвольный словарь с параметрами для модели.

    Returns:
        dict: Предсказание, выдаётся ли кредит.
    """

    all_params = {
        "client_id": client_id,
        "model_params": model_params
    }
    user_prediction = app.handler.handle(all_params)  # обращаемся к модели
    score = user_prediction["predicted_credit_rating"]  # получаем score
    if score >= 600:  # сравниваем с порогом
        approved = 1  # положительное решение, если выше
    else:
        approved = 0  # отрицательное решение, если ниже
    return {"client_id": client_id, "approved": approved}  # ответ
