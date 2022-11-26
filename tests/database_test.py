import pytest
import database


def test_get_gene_function_one_arg():
    res = database.get_gene('ADRB2')
    database.stop()
    assert len(res) == 3


def test_get_gene_function_two_arg():
    res = database.get_gene('ADRB2', 'rs1042713')[0]['gene']
    database.stop()
    assert res == 'Адренергический рецептор 2'


def test_get_gene_function_no_such_gen():
    res = database.get_gene('jkbr3tvjhr4v')
    database.stop()
    assert res == []


def test_get_gene_function_no_such_rs():
    res = database.get_gene('ADRB2', 'huguvghv')
    database.stop()
    assert res == []


def test_get_themes():
    res1 = database.get_themes('НГ 31 ген')
    res2 = database.get_themes('НГ14-16')
    res3 = database.get_themes('cewevgebtebyt')
    res = [[item['id'] for item in res1], [item['id'] for item in res2], [item['id'] for item in res3]]
    database.stop()
    assert res == [[10, 20, 28], [10], []]


def test_get_themes_by_id():
    res1 = database.get_themes(13)
    res2 = database.get_themes(8)
    res3 = database.get_themes(1)
    res = [[item['id'] for item in res1], [item['id'] for item in res2], [item['id'] for item in res3]]
    database.stop()
    assert res == [[10, 20, 28], [10], []]


def test_get_subthemes():
    res1 = database.get_subthemes(10)
    res2 = database.get_subthemes(1)
    res = [[item['id'] for item in res1], [item['id'] for item in res2]]
    database.stop()
    assert res == [[7, 8, 17], []]


def test_get_risks():
    res = [rr['id'] for rr in database.get_risks(7)]
    database.stop()
    assert res == [17, 22, 24, 23, 30, 25, 27, 31, 32, 29]

def test_get_risks_no_such_subtheme():
    res = [rr['id'] for rr in database.get_risks(1)]
    database.stop()
    assert res == []


if __name__ == '__main__':
    pytest.main()
