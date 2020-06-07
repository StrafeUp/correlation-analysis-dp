from pandas import *

import constants
from data_parser import Parser, get_factor_to_empty_years, years_set


def rescan_dat():
    Parser().rescan_data()


def get_factor_by_year(name, year):
    factor: DataFrame = Parser().data[name]
    return factor[year]


def get_all_factors_by_year(year):
    return [get_factor_by_year(x, year) for x in constants.filenames]


def get_all_factors_by_year_in_dict(year):
    return dict(zip(constants.filenames, get_all_factors_by_year(year)))


def get_all_factors_map_regions(year):
    regions_to_factors = dict(zip([x for x in constants.regions], [list() for el in constants.regions]))
    data_from_excel = get_all_factors_by_year_in_dict(year)

    for i, region_name in enumerate(constants.regions):
        for factor_name in constants.filenames:
            regions_to_factors[region_name].append(int(data_from_excel[factor_name][i]))
    return regions_to_factors


def get_factor_points_for_linechart_by_year(region, factor, year_from, year_to):
    region_index = list(constants.regions).index(region)
    years = [x for x in range(year_from, year_to + 1)]
    factor_values_in_year = list()
    for year in years:
        factor_values_in_year.append(int(get_factor_by_year(factor, year)[region_index]))

    return factor_values_in_year, years


def get_factor_points_for_barchart_by_year(factor, year):
    regions = list(constants.regions)
    factors = get_factor_by_year(factor, year)

    return regions, factors.tolist()


def get_empty_years():
    return get_factor_to_empty_years()


def get_valid_years():
    empty_years_set = set()
    factor_years_dict = get_empty_years()
    for factor in constants.filenames:
        empty_years_set.update(factor_years_dict[factor])

    return years_set - empty_years_set
