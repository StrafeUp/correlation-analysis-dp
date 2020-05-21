from pandas import *

import constants

files = ['data/' + x + '.xlsx' for x in constants.filenames]

dataframes_with_Nans = [read_excel(x) for x in files]  # Промежуточные значения, просто таблицы в виде объектов

dataframes = [x.dropna(axis=1, how='all') for x in
              dataframes_with_Nans]  # dropna - axis = 1 для выброса всех колонок с NaN, how=all - только колонки, где данные отсутствуют во всех полях

years_set = set()


class Parser:
    def __init__(self) -> None:
        super().__init__()
        self.data = dict(zip(constants.filenames, dataframes))

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Parser, cls).__new__(cls)
        return cls.instance


def get_factor_to_empty_years():
    years = {}
    empty_factors = dict(zip(constants.filenames, [list() for factor in constants.filenames]))

    for factor, dataframe in zip(constants.filenames, dataframes_with_Nans):
        years[factor] = [x for x in dataframe.columns.tolist() if type(x) == int]
        years_set.update(years[factor])  # Adding years to set to later get only viable years for graphs

    for factor, dframe in zip(constants.filenames, dataframes_with_Nans):
        for year in years[factor]:
            if dframe[year].isnull().values.any():
                empty_factors[factor].append(year)

    return empty_factors
