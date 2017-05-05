from quality import WineQuality
from flask import request, jsonify, render_template
from random import randint


class WineBase:

    def home(self):
        print('Home')
        # return render_template('Wine.html')
        html = open('templates/Wine.html', 'r').read()
        return html

    def predict_index(self):
        params = request.form
        print(params)
        data = str(params['desired'])

        quality_list = open('resources/winequality.txt')
        qualities = quality_list.readlines()

        index = []

        for line in qualities:
            if line[len(line) - 2:len(line) - 1] == data:
                index.append(line.split(';'))

        indices = index[randint(0, len(index))]
        indices.pop()
        resp = {'predictedIndex': indices}
        return jsonify(resp)

    def predict_wine(self):
        data = []
        params = request.form
        print(params)
        for key in params:
            print(params[key])
            data.append(float(params[key]))

        quality_calculator = self.quality_calculator

        try:
            quality = quality_calculator.estimate_quality(data)
            print(quality)
            resp = {'prediction': str(quality[0])}
            return jsonify(resp)
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
