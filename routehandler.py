from quality import WineQuality
from flask import request


class WineApi:

    def home(self):
        print('Home')
        return 'Home Page'

    def predict_wine(self):
        data = []
        params = request.form

        for key in params:
            data.append(int(params[key]))

        quality_calculator = self.quality_calculator

        try:
            quality = quality_calculator.estimate_quality(data)
            print(quality)
            return str(quality[0])
        except TypeError as e:
            return (e.args[0], 500)
        except ValueError as e:
            return (e.args[0], 500)
        except IOError as e:
            return (e.args[0], 500)
        except Exception as e:
            return (e.args[0], 500)
        else:
            print('Server response sent.')

    def __init__(self):
        self.quality_calculator = WineQuality()
