import numpy as np
import joblib

class ModelInterface:
    def __init__(self, model_path):
        """
        Initializes the model interface by loading the model from a pickle file.

        :param model_path: Path to the model's pickle file.
        """
        self.model = self._load_model(model_path)
        self.scaler = self._load_scaler("ml-model/scaler.pkl")

    def _load_model(self, model_path):
        """
        Loads the model from the pickle file.

        :param model_path: Path to the model's pickle file.
        :return: Loaded model.
        """
        try:
            with open(model_path, 'rb') as file:
                model = joblib.load(file)
            print(f"Model loaded successfully: {type(model)}")
            return model
        except FileNotFoundError:
            raise Exception(f"File not found: {model_path}")
        except Exception as e:
            raise Exception(f"Error loading the model: {e}")

    def _load_scaler(self, scaler_path):
        """
        Loads the model from the pickle file.

        :param model_path: Path to the model's pickle file.
        :return: Loaded model.
        """
        try:
            with open(scaler_path, 'rb') as file:
                scaler = joblib.load(file)
            print(f"Scaler loaded successfully: {type(scaler)}")
            return scaler
        except FileNotFoundError:
            raise Exception(f"File not found: {scaler_path}")
        except Exception as e:
            raise Exception(f"Error loading the model: {e}")

    def predict(self, input_data):
        """
        Makes a prediction using the loaded model.

        :param input_data: Input for the model (numpy array or list of lists).
        :return: Model's prediction.
        """
        try:
            # Convert input to a numpy array if necessary
            if not isinstance(input_data, np.ndarray):
                input_data = np.array(input_data)

            # Check if the model has a predict method
            if not hasattr(self.model, 'predict'):
                raise AttributeError("The loaded model does not have a 'predict' method.")

            # Make the prediction
            X_new_scaled = self.scaler.transform(input_data)
            predictions = self.model.predict(X_new_scaled)
            return predictions
        except Exception as e:
            raise Exception(f"Error during prediction: {e}")

# Example usage
if __name__ == "__main__":
    # Path to the model's pickle file
    model_path = "ml-model/model.pkl"

    # Create an instance of the model interface
    model_interface = ModelInterface(model_path)

    # Example input for the model
    input_data = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # Adapt this to your use case

    # Make a prediction
    try:
        predictions = model_interface.predict(input_data)
        print("Predictions:", predictions)
    except Exception as e:
        print(e)
