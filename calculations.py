import logging
from random import uniform

import config
import database
import plotrisk

genotype_names = ['genotype1', 'genotype2', 'genotype3']
risk_levels_names = ['low', 'mid', 'high', 'upper']


def process_text(text):
    if text == None:
        logging.warning(f'\'None\' found when text from database processed, return \'\'')
        return ''
    text = text.replace('\n', '').replace('%', '\%').replace('_', '\_')
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


def calc_risk_values(risk, analysis):
    val, val_max, val_min = 1, 1, 1
    genes_n = 0
    for gene in risk['genes']:
        if gene['genotype'] != '':
            val *= gene['deposit' + gene['genotype'].replace('genotype', '')]
            val_max *= max([gene['deposit' + str(i)] for i in range(1, 4)])
            val_min *= min([gene['deposit' + str(i)] for i in range(1, 4)])
            genes_n += 1

    if genes_n == 0:
        val, val_max, val_min = 0, 0, 0
        logging.warning(f'no genes to calculate risk {risk["id"]}, return zeros, {val=}, {val_max=}, {val_min=}')
    else:
        logging.info(f'risk for risk_id {risk["id"]} is calculated {val=}, {val_max=}, {val_min=}')

    risk = {'value': val,
            'value_max': val_max,
            'value_min': val_min}
    return risk


def calc_risk_levels(risks_list):
    risk_levels = []
    for risk in risks_list:
        if risk['value'] <= float(risk['low_level']):
            risk_levels.append('low')
        elif float(risk['low_level']) < risk['value'] <= float(risk['mid_level']):
            risk_levels.append('mid')
        elif float(risk['mid_level']) < risk['value'] <= float(risk['high_level']):
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

        gene['name'] = process_text(gene['name'])
        gene['rs_position'] = process_text(gene['rs_position'])
        for i in range(1, 4):
            gene['deposit' + str(i)] = float(gene['deposit' + str(i)])
            gene['freq' + str(i)] = float(gene['freq' + str(i)])
        gene.update({'genotype': genotype})
        for gt in genotype_names:
            del gene['inter_' + gt]
        del gene['_sa_instance_state']
    return genes_list


def modify_risks_dict(risks_list):
    risk_levels = calc_risk_levels(risks_list)
    for risk, risk_level in zip(risks_list, risk_levels):
        risk.update({'inter': process_text(risk[risk_level + '_inter']),
                    'briefly': process_text(risk[risk_level + '_briefly']),
                    'recommendation': process_text(risk[risk_level + '_recommendation']),
                    'short_recommendation': process_text(risk[risk_level + '_short_recommendation'])})
        logging.info(f'interpretations and recommendations for risk id: {risk["id"]} are selected')

        risk.update({'level': risk_level})
        for rn in risk_levels_names:
            del risk[rn + '_inter'], risk[rn + '_briefly'], risk[rn + '_recommendation'], \
                risk[rn + '_short_recommendation']
        del risk['_sa_instance_state']
    return risks_list


def create_tag_dict(analysis):
    temp_vars = {'name': analysis.patient_name,
                 'birthday': analysis.patient_birthday,
                 'sex': analysis.patient_sex,
                 'analysis_number': analysis.number,
                 'analysis_date': '??/??/????',  # from there it should be taken?
                 'scandat': analysis.data
                 }
    logging.info(f'start creating dict for report for {analysis.patient_name}, analysis no. {analysis.number}')

    # !!!FOR TEST PURPOSES ONLY
    analysis.panels = ['НГ14-16'] #['Вит. Нов']  # !!!FOR TEST PURPOSES ONLY
    # !!!FOR TEST PURPOSES ONLY

    panels = []
    for panel in analysis.panels:
        themes = database.get_themes(panel)
        panels.append({"name": panel, "themes": themes})
        for theme in themes:
            subthemes = database.get_subthemes(theme['id'])
            theme.update({'subthemes': subthemes})
            for subthem in subthemes:
                del subthem['_sa_instance_state']
                risks = database.get_risks(subthem['id'])
                for risk in risks:
                    genes = database.get_genes_for_risk(risk['id'])
                    genes = modify_genes_dict(genes, calc_genotype(genes, analysis))
                    risk.update({'genes': genes})
                    risk.update(calc_risk_values(risk, analysis))
                    risk.update({'fig_name': config.Path(config.files['template_path'], 'risk_' + str(risk['id']) + '.png').as_posix()})
                    plotrisk.plot_risk(risk['value_min'], risk['value_max'], risk['value'], risk['fig_name'])
                risks = modify_risks_dict(risks)
                subthem.update({'risks': risks})

    temp_vars.update({'panels': panels})

    # for theme in panels[0]['themes']:
    #     print(theme['name'])
    # for panel in panels:
    #     print(panel['name'])
    #     for theme in themes:
    #         print ('\t', theme['id'])
    #         for subtheme in theme['subthemes']:
    #             print('\t\t', subtheme['id'])
    #             for risk in subtheme['risks']:
    #                 print('\t\t\t', risk['id'])
    #                 for gene in risk['genes']:
    #                     print('\t\t\t\t', gene['name'])

    logging.info(f'dict created')
    return temp_vars
