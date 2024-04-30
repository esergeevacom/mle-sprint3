"""Класс FastApiHandler, который обрабатывает запросы API."""

# импортируем класс модели
from catboost import CatBoostRegressor


class FastApiHandler:
    """Класс FastApiHandler, который обрабатывает запрос и возвращает предсказание."""

    def __init__(self):
        """Инициализация переменных класса."""

        # типы параметров запроса для проверки
        self.param_types = {
            "client_id": str,
            "model_params": dict
        }

        # Cписок необходимых параметров модели
        self.required_model_params = [
            'gender', 'Type', 'PaperlessBilling', 'PaymentMethod',
            'MonthlyCharges', 'TotalCharges'
        ]

        self.model_path = "../models/catboost_credit_model.bin"
        self.model_path = "../models/catboost_churn_model.bin"
        with open(self.model_path, 'rb') as f:
            print(f.read())
        self.load_credit_model(model_path=self.model_path)

    def load_credit_model(self, model_path: str):
        """Загружаем обученную модель предсказания кредитного рейтинга.

            Args:
            model_path (str): Путь до модели.
        """
        try:
            self.model = CatBoostRegressor()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

    def credit_rating_predict(self, model_params: dict) -> float:
        """Предсказываем кредитный рейтинг.

        Args:
            model_params (dict): Параметры для модели.

        Returns:
            float — кредитный рейтинг
        """
        return self.model.predict(list(model_params.values()))

    def check_required_query_params(self, query_params: dict) -> bool:
        """Проверяем параметры запроса на наличие обязательного набора.

                Args:
                    query_params (dict): Параметры запроса.

                Returns:
                    bool: True — если есть нужные параметры, False — иначе
                """
        if "client_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["client_id"], str):
            return False

        if not isinstance(query_params["model_params"], dict):
            return False
        return True

    def check_required_model_params(self, model_params: dict) -> bool:
        """Проверяем параметры пользователя на наличие обязательного набора.

        Args:
            model_params (dict): Параметры пользователя для предсказания.

        Returns:
            bool: True — если есть нужные параметры, False — иначе
        """
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False

    def validate_params(self, params: dict) -> bool:
        """Проверяем корректность параметров запроса и параметров модели.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
             bool: True — если проверки пройдены, False — иначе
        """
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False

        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True

    def handle(self, params):
        """Функция для обработки запросов API.

        Args:
            params (dict): Словарь параметров запроса.

        Returns:
            dict: Словарь, содержащий результат выполнения запроса.
        """
        try:
            # валидируем запрос к API
            if not self.validate_params(params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                model_params = params["model_params"]
                client_id = params["client_id"]
                print(f"Predicting for client_id: {client_id} and model_params:\n{model_params}")
                # получаем предсказания модели
                predicted_rating = self.credit_rating_predict(model_params)
                response = {
                    "client_id": client_id,
                    "predicted_credit_rating": predicted_rating
                }
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response


if __name__ == "__main__":

    # создаём тестовый запрос
    test_params = {
        "client_id": "123",
        "model_params": {
            "gender": 1.0,
            "Type": 0.5501916796819537,
            "PaperlessBilling": 1.0,
            "PaymentMethod": 0.2192247621752094,
            "MonthlyCharges": 50.8,
            "TotalCharges": 288.05,
            # "some_other_params": 1.0
        }
    }

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")
