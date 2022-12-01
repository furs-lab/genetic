import logging
from random import randint

genotype_names = ['genotype1', 'genotype2', 'genotype3']
risk_names = ['low', 'mid', 'high', 'upper']


def calc_genotype(genes_list, analysis):
    genotypes_list = []
    for gene in genes_list:
        res_df = analysis.data.loc[
            (analysis.data['Gen'] == gene['name']) & (analysis.data['RS'] == gene['rs_position']), 'Result']
        if res_df.size == 0:
            genotypes_list.append('')
            logging.warning(f'gene \'{gene["name"]}\' is not found in analysis, genotype = \'\'')
            continue

        for genotype in genotype_names:
            if res_df.values[0] == gene[genotype]:
                genotypes_list.append(genotype)
                logging.info(f'gene \'{gene["name"]}\', genotype = \'{genotype}\'')
                break

    return genotypes_list


def calc_risk(risks_list, analysis):
    risk_values = []
    for risk in risks_list:
        # do some calculations or call some function for these calculations
        risk_values.append(risk_names[randint(0, 3)])
        logging.info(f'calculate risk value \'{risk_values[-1]}\' for risk id: {risk["id"]}')

    return risk_values


def modify_genes_dict(genes_list, genotypes_list):
    if len(genes_list) != len(genotypes_list):
        logging.warning(f'different lengths of genes_list and genotypes_list, modifications did not perform')
        return genes_list

    for gene, genotype in zip(genes_list, genotypes_list):
        if genotype in genotype_names:
            gene.update({'inter': gene['inter_' + genotype], 'result': gene[genotype]})
            logging.info(f'interpretation for gene \'{gene["name"]}\' is selected')
        else:
            gene.update({'inter': '', 'result': ''})
            logging.warning(f'genotype for gene \'{gene["name"]}\' did not defined, return empty interpretation')

        gene.update({'genotype': genotype})
        for gt in genotype_names:
            del gene['inter_' + gt]

    return genes_list


def modify_risks_dict(risks_list, risk_values):
    if len(risks_list) != len(risk_values):
        logging.warning(f'different lengths of risks_list and risk_values, modifications did not perform')
        return risks_list

    for risk, risk_value in zip(risks_list, risk_values):
        if risk_value in risk_names:
            risk.update({'inter': risk[risk_value + '_inter'],
                         'briefly': risk[risk_value + '_briefly'],
                         'recommendation': risk[risk_value + '_recommendation'],
                         'short_recommendation': risk[risk_value + '_short_recommendation']})
            logging.info(f'interpretations and recommendations for risk id: {risk["id"]} are selected')
        else:
            risk.update({'inter': '', 'briefly': '', 'recommendation': '', 'short_recommendation': ''})
            logging.warning(f'risk value for risk id: {risk["id"]} did not defined, return empty interpretation')

        risk.update({'risk_value': risk_value})
        for rn in risk_names:
            del risk[rn + '_inter'], risk[rn + '_briefly'], risk[rn + '_recommendation'], \
                risk[rn + '_short_recommendation']

    return risks_list

def create_jinja2_dict(analysis):
    temp_vars = {'name': analysis.patient_name,
                 'birthday': analysis.patient_birthday,
                 'sex': analysis.patient_sex,
                 'analysis_number': analysis.number,
                 'analysis_date': '??/??/????', #from there it should be taken?
                 }

    return temp_vars