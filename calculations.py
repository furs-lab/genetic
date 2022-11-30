import logging


def calc_genotype(genes_list, analysis):
    genotypes_list = []
    genotypes = ['genotype' + str(i + 1) for i in range(3)]
    for gene in genes_list:
        res_df = analysis.data.loc[analysis.data['Gen'] == gene['name'], 'Result']
        if res_df.size == 0:
            genotypes_list.append('')
            logging.warning(f'gene \'{gene["name"]}\' is not found in analysis, genotype = \'\'')
            continue

        for genotype in genotypes:
            if res_df.values[0] == gene[genotype]:
                genotypes_list.append(genotype)
                logging.info(f'gene \'{gene["name"]}\', genotype = \'{genotype}\'')
                break

    return genotypes_list
