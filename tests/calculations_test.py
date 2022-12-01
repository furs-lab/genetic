import pytest

import calculations
import database
from analysis import Analysis


@pytest.fixture
def test_filename():
    return "tst_analysis.xlsx"


def test_calc_genotype_panel(test_filename):
    analysis = Analysis(test_filename)
    analysis.get_panel_data('fat')
    analysis.sort_by_gens()
    genes_list = database.get_genes_for_risk(82)
    res = calculations.calc_genotype(genes_list, analysis)
    database.stop()
    assert res == ['', '', 'genotype1', '', '', 'genotype2']


def test_calc_genotype_all_panels(test_filename):
    analysis = Analysis(test_filename)
    analysis.sort_by_gens()
    genes_list = database.get_genes_for_risk(82)
    res = calculations.calc_genotype(genes_list, analysis)
    database.stop()
    assert res == ['', 'genotype1', 'genotype1', 'genotype2', 'genotype3', 'genotype2']


def test_modify_genes_dict(test_filename):
    analysis = Analysis(test_filename)
    analysis.get_panel_data('fat')
    analysis.sort_by_gens()
    genes_list = database.get_genes_for_risk(82)
    gt = calculations.calc_genotype(genes_list, analysis)
    res1 = calculations.modify_genes_dict(genes_list, gt)
    res = [len(rr['inter']) for rr in res1]
    database.stop()
    assert res == [0, 0, 104, 0, 0, 102]


def test_modify_genes_dict_all_panels(test_filename):
    analysis = Analysis(test_filename)
    analysis.sort_by_gens()
    genes_list = database.get_genes_for_risk(82)
    gt = calculations.calc_genotype(genes_list, analysis)
    res1 = calculations.modify_genes_dict(genes_list, gt)
    res = [len(rr['inter']) for rr in res1]
    database.stop()
    assert res == [0, 52, 104, 281, 291, 102]


if __name__ == '__main__':
    pytest.main()
