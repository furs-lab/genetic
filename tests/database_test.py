import pytest
import database


def test_get_gene_function_one_arg():
    res = database.get_gene_function('ADRB2')
    database.stop()
    assert len(res) == 3


def test_get_gene_function_two_arg():
    res = database.get_gene_function('ADRB2', 'rs1042713')
    database.stop()
    assert res == [
        'Бета-адренорецептор 2 типа.  Присутствует на мембранах клеток гладкой мускулатуры и в жировых клетках. Участвует в мобилизации жира из жировых клеток в ответ на гормоны (адреналин, норадреналин), стимулируют гликогенолиз в печени и выброс глюкозы в кровь для восполнения энергетических потребностей работы мышц.']


def test_get_gene_function_no_such_gen():
    res = database.get_gene_function('jkbr3tvjhr4v')
    database.stop()
    assert res == ['']


def test_get_gene_function_no_such_rs():
    res = database.get_gene_function('ADRB2', 'huguvghv')
    database.stop()
    assert res == ['']


def test_get_themes():
    res1 = database.get_themes('НГ 31 ген')
    res2 = database.get_themes('НГ14-16')
    res3 = database.get_themes('cewevgebtebyt')
    res = [[item['id'] for item in res1], [item['id'] for item in res2], [item['id'] for item in res3]]
    database.stop()
    assert res == [[10, 20, 28], [10], []]


def test_get_themes_id_by_id():
    res1 = database.get_themes(13)
    res2 = database.get_themes(8)
    res3 = database.get_themes(1)
    res = [[item['id'] for item in res1], [item['id'] for item in res2], [item['id'] for item in res3]]
    database.stop()
    assert res == [[10, 20, 28], [10], []]


def test_get_subthemes_id():
    res = [database.get_subthemes_id(10), database.get_subthemes_id(1)]
    database.stop()
    assert res == [[7, 8, 17], []]


if __name__ == '__main__':
    pytest.main()
