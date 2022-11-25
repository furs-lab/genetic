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


def test_get_themes_id():
    res = [database.get_themes_id('НГ14-16'), database.get_themes_id('НГ 31 ген'),
           database.get_themes_id('80 Нутригенетика: избыточный вес и здоровье (max)')]
    database.stop()
    assert res == [[10], [10, 20, 28], [33, 34]]

def test_get_themes_id_no_such_panel():
    res = database.get_themes_id('jrgnrthjvgre')
    database.stop()
    assert res == []

if __name__ == '__main__':
    pytest.main()
