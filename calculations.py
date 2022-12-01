import logging
from random import uniform

import database

genotype_names = ['genotype1', 'genotype2', 'genotype3']
risk_levels_names = ['low', 'mid', 'high', 'upper']


def process_text(text):
    if text == None:
        logging.warning(f'\'None\' found when text from database processed, return \'\'')
        return ''
    text = text.replace('\n', '').replace('%', '\%')
    return text


def calc_genotype(genes_list, analysis):
    genotypes_list = []
    for gene in genes_list:
        res_df = analysis.data.loc[
            (analysis.data['Gen'] == gene['name']) & (analysis.data['RS'] == gene['rs_position']), 'Result']
        if res_df.size == 0:
            genotypes_list.append('')
            logging.warning(f'gene \'{gene["name"]}\', {gene["rs_position"]} is not found in analysis, genotype = \'\'')
            continue

        for genotype in genotype_names:
            if res_df.values[0] == gene[genotype]:
                genotypes_list.append(genotype)
                logging.info(f'gene \'{gene["name"]}\', {gene["rs_position"]}, genotype = \'{genotype}\'')
                break

    return genotypes_list


def calc_risk_values(risks_list, analysis):
    risk_values = []
    for risk in risks_list:
        # do some calculations or call some function for these calculations
        risk_values.append(uniform(0, 1.5 * float(risk['high_level'])))
        logging.info(f'calculate risk value \'{risk_values[-1]:.2f}\' for risk id: {risk["id"]}')

    return risk_values


def calc_risk_levels(risks_list, risk_values):
    risk_levels = []
    if len(risks_list) != len(risk_values):
        logging.warning(f'different lengths of risks_list and risk_values, return []')
        return []
    for risk, risk_value in zip(risks_list, risk_values):
        if risk_value <= float(risk['low_level']):
            risk_levels.append('low')
        elif float(risk['low_level']) < risk_value <= float(risk['mid_level']):
            risk_levels.append('mid')
        elif float(risk['mid_level']) < risk_value <= float(risk['high_level']):
            risk_levels.append('high')
        else:
            risk_levels.append('upper')
        logging.info(f'calculate risk level \'{risk_levels[-1]}\' for risk id: {risk["id"]}')
    return risk_levels


def modify_genes_dict(genes_list, genotypes_list):
    if len(genes_list) != len(genotypes_list):
        logging.warning(f'different lengths of genes_list and genotypes_list, modifications did not perform')
        return genes_list

    for gene, genotype in zip(genes_list, genotypes_list):
        if genotype in genotype_names:
            gene.update({'inter': process_text(gene['inter_' + genotype]),
                         'result': process_text(gene[genotype])})
            logging.info(f'interpretation for gene \'{gene["name"]}\', {gene["rs_position"]} is selected')
        else:
            gene.update({'inter': '', 'result': ''})
            logging.warning(f'genotype for gene \'{gene["name"]}\', {gene["rs_position"]} did not defined, return '
                            f'empty interpretation')

        gene.update({'genotype': genotype})
        for gt in genotype_names:
            del gene['inter_' + gt]

    return genes_list


def modify_risks_dict(risks_list, risk_values):
    risk_levels = calc_risk_levels(risks_list, risk_values)
    if len(risks_list) != len(risk_values):
        logging.warning(f'different lengths of risks_list and risk_values, modifications did not perform')
        return risks_list

    for risk, risk_value, risk_level in zip(risks_list, risk_values, risk_levels):
        risk.update({'inter': process_text(risk[risk_level + '_inter']),
                    'briefly': process_text(risk[risk_level + '_briefly']),
                    'recommendation': process_text(risk[risk_level + '_recommendation']),
                    'short_recommendation': process_text(risk[risk_level + '_short_recommendation'])})
        logging.info(f'interpretations and recommendations for risk id: {risk["id"]} are selected')

        risk.update({'risk_value': risk_value, 'risk_level': risk_level})
        for rn in risk_levels_names:
            del risk[rn + '_inter'], risk[rn + '_briefly'], risk[rn + '_recommendation'], \
                risk[rn + '_short_recommendation']

    return risks_list


def create_jinja2_dict(analysis):
    temp_vars = {'name': analysis.patient_name,
                 'birthday': analysis.patient_birthday,
                 'sex': analysis.patient_sex,
                 'analysis_number': analysis.number,
                 'analysis_date': '??/??/????',  # from there it should be taken?
                 'scandat': analysis.data
                 }
    logging.info(f'start creating dict for report for {analysis.patient_name}, analysis no. {analysis.number}')

    # !!!FOR TEST PURPOSES ONLY
    analysis.panels = ['Вит. Нов']  # !!!FOR TEST PURPOSES ONLY
    # !!!FOR TEST PURPOSES ONLY

    panels = []
    for panel in analysis.panels:
        themes = database.get_themes(panel)
        panels.append({"name": panel, "themes": themes})
        for theme in themes:
            subthemes = database.get_subthemes(theme['id'])
            theme.update({'subthemes': subthemes})
            for subthem in subthemes:
                risks = database.get_risks(subthem['id'])
                risks = modify_risks_dict(risks, calc_risk_values(risks, analysis))
                subthem.update({'risks': risks})
                for risk in risks:
                    genes = database.get_genes_for_risk(risk['id'])
                    genes = modify_genes_dict(genes, calc_genotype(genes, analysis))
                    risk.update({'genes': genes})

    temp_vars.update({'panels': panels})
    for theme in panels[0]['themes']:
        print(theme['name'])
    # for panel in panels:
    #     print(panel['name'])
    #     for theme in themes:
    #         print ('\t', theme['id'])
    #         for subtheme in theme['subthemes']:
    #             print('\t\t', subtheme['id'])
    #             for risk in subtheme['risks']:
    #                 print('\t\t\t', risk['id'])
    #                 for gene in risk['genes']:
    #                     print('\t\t\t\t', gene['id'])

    logging.info(f'dict created')
    return temp_vars
