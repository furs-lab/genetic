from pandas import read_excel, DataFrame
import logging


class Analysis:
    raw_data = None
    data = None
    patient_name = None
    patient_birthday = None
    patient_sex = None
    panels = []
    number = None

    def __init__(self, fname):
        self.read(fname)

    def read(self, fname):
        Analysis.xls_file = fname
        try:
            Analysis.raw_data = read_excel(fname).dropna()
        except Exception:
            logging.exception('Error: can not read excel file')
            raise Exception('Error: can not read excel file')
        self.patient_name = self.raw_data["FIO"][0]
        self.patient_birthday = self.raw_data["DateOfBirthday"][0]
        self.patient_sex = 'мужской' if self.raw_data["Gender"][0] == 'male' else 'женский'
        self.number = self.raw_data["AnalysNo"][0]
        self.data = self.raw_data[['Gen', 'RS', 'Полиморфизм', 'Result']].copy()
        logging.info(f'read excel file \'{fname}\'')

    def get_panels(self):
        self.panels = []
        raw_panels = self.raw_data['BlockShifr'].unique()
        for pn in raw_panels:
            self.panels.extend(pn.replace(' ', '').split(','))
        self.panels = list(dict.fromkeys(self.panels))
        logging.info(f'get panels: {self.panels}')
        return self.panels

    def get_panel_data(self, panel):
        if panel not in self.panels:
            logging.warning(f'you want to create data for panel \'{panel}\' but it is not in panels: {self.panels}')
        self.data = (self.raw_data.loc[self.raw_data['BlockShifr'].str.contains(panel)])[
            ['Gen', 'RS', 'Полиморфизм', 'Result']].copy()
        logging.info(f'create data frame for panel \'{panel}\'')
        return self.data

    def sort_by_gens(self):
        self.data = self.data.sort_values(['Gen'])
        logging.info(f'sort data frame by \'Gen\'')
        return self.data
