import pytest
from pandas import read_excel
import calculations
import database
from analysis import Analysis


@pytest.fixture
def test_filename():
    return read_excel("tst_analysis.xlsx").dropna()


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
    assert res == [0, 0, 106, 0, 0, 105]


def test_modify_genes_dict_all_panels(test_filename):
    analysis = Analysis(test_filename)
    analysis.sort_by_gens()
    genes_list = database.get_genes_for_risk(82)
    gt = calculations.calc_genotype(genes_list, analysis)
    res1 = calculations.modify_genes_dict(genes_list, gt)
    res = [len(rr['inter']) for rr in res1]
    database.stop()
    assert res == [0, 52, 106, 286, 294, 105]


if __name__ == '__main__':
    pytest.main()
