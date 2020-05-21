import pandas
import webbrowser
from flask import Flask

from views.api import api

app = Flask(__name__)

if __name__ == '__main__':
    pandas.set_option('display.max_rows', 500)
    pandas.set_option('display.max_columns', 500)
    pandas.set_option('display.width', 1000)

    # print(data_service.get_factor_by_year('zkp', 2010))

    app.debug = True
    app.register_blueprint(api)
    # webbrowser.open('0.0.0.0:8080', new=0)
    app.run(host='0.0.0.0', port=8080)

    #todo Front end fields, years, years with errors, ip and port configs
