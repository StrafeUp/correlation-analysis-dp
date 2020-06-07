import tkinter.messagebox as mb

import numpy as np
from flask import Blueprint, render_template, jsonify, request, redirect

import constants
import data_service

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/')
def hello_world():
    return render_template("index.html")


@api.route('/api/getData')
def get_data():
    try:
        data = data_service.get_all_factors_by_year(int(request.args.get('year')))
    except KeyError as e:
        mb.showerror("Error", "Invalid table format in newly added tables\nFix tables and relauch application")
    mat = np.corrcoef(data)
    return jsonify(corr=mat.tolist(), labels=constants.filenames)


@api.route('/api/getDataFromExcelByYear')
def get_region_to_factor_by_year():
    table_data = data_service.get_all_factors_map_regions(int(request.args.get('year')))
    return jsonify(table_data=table_data, table_header=constants.filenames)


@api.route('/api/getDataForBarChart')
def get_data_for_bar_chart():
    regions, factors = data_service.get_factor_points_for_barchart_by_year(request.args.get('factor'),
                                                                           int(request.args.get('year')))
    return jsonify(regions=regions, factors=factors)


@api.route('/api/getDataForLineChart')
def get_data_for_line_charts():
    factor_in_years, years = data_service.get_factor_points_for_linechart_by_year(request.args.get('region'),
                                                                                  request.args.get('factor'),
                                                                                  int(request.args.get('from')),
                                                                                  int(request.args.get('to')))

    return jsonify(factor_in_years=factor_in_years, years=years)


@api.route('/api/getFactorToEmptyYears')
def get_factor_to_empty_years():
    data_service.Parser()
    factor_to_years_dict = data_service.get_factor_to_empty_years()
    return jsonify(factor_to_years_dict)


@api.route('/api/getFactors')
def get_factors():
    data_service.Parser()
    return jsonify(constants.filenames)


@api.route('/api/getRegions')
def get_regions():
    data_service.Parser()
    return jsonify(constants.regions)


@api.route('/api/getYears')
def get_years():
    data_service.Parser()
    return jsonify(list(data_service.get_valid_years()))


@api.route('/api/redirect')
def reload_page():
    return redirect("/")
