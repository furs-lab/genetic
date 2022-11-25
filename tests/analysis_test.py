import pytest
from analysis import Analysis


@pytest.fixture
def test_filename():
    return "tst_analysis.xlsx"


def test_analysis_read(test_filename):
    Analysis.read(Analysis, test_filename)
    assert [Analysis.patient_sex,
            Analysis.patient_name,
            Analysis.patient_birthday,
            Analysis.number] == ["мужской",
                                 "Иванов Иван Иванович",
                                 "22/11/1999",
                                 "AB-0123"]


def test_analysis_read_nofile(test_filename):
    with pytest.raises(Exception) as error:
        Analysis.read(Analysis, "test_filename[1:]")
    assert 'Error: can not read excel file' == error.value.args[0]


def test_analysis_constructor(test_filename):
    an = Analysis(test_filename)
    assert [an.patient_sex,
            an.patient_name,
            an.patient_birthday,
            an.number] == ["мужской",
                           "Иванов Иван Иванович",
                           "22/11/1999",
                           "AB-0123"]


def test_analysis_data(test_filename):
    an = Analysis(test_filename)
    assert an.data.iloc[0].values.tolist() == ['NOS3(e)', 'rs1799983', 'G>T', 'G/G']


def test_analysis_panels_list(test_filename):
    an = Analysis(test_filename)
    an.get_panels()
    assert an.panels == ['hypertension', 'fat', 'smoke']


def test_analysis_get_panel_data(test_filename):
    an = Analysis(test_filename)
    df = an.get_panel_data('fat')
    assert df.iloc[:2].values.tolist() == [['NOS3', 'rs891512', 'G>A', 'G/A'], ['CYP2D6', 'rs3892097', 'C>T', 'C/T']]

def test_analysis_get_panel_data_nopanel(test_filename):
    an = Analysis(test_filename)
    df = an.get_panel_data('fvrt')
    assert df.iloc[:2].values.tolist() == []

def test_analysis_get_panel_data_length(test_filename):
    an = Analysis(test_filename)
    lengths = [an.get_panel_data('fat').shape[0], an.get_panel_data('smoke').shape[0],
               an.get_panel_data('hypertension').shape[0]]
    assert lengths == [4, 2, 34]


if __name__ == '__main__':
    pytest.main()
