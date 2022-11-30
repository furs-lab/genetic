import logging


def calc_genotype(genes_list, analysis):
    genotypes_list = []
    for gene in genes_list:
        res_df = analysis.data.loc[
            (analysis.data['Gen'] == gene['name']) & (analysis.data['RS'] == gene['rs_position']), 'Result']
        if res_df.size == 0:
            genotypes_list.append('')
            logging.warning(f'gene \'{gene["name"]}\' is not found in analysis, genotype = \'\'')
            continue

        for genotype in ['genotype' + str(i + 1) for i in range(3)]:
            if res_df.values[0] == gene[genotype]:
                genotypes_list.append(genotype)
                logging.info(f'gene \'{gene["name"]}\', genotype = \'{genotype}\'')
                break

    return genotypes_list


def modify_genes_dict(genes_list, genotypes_list):
    if len(genes_list) != len(genotypes_list):
        logging.warning(f'different lengths of genes_list and genotypes_list, modifications did not perform')
        return genes_list

    for gene, genotype in zip(genes_list, genotypes_list):
        if genotype != '':
            gene.update({'inter': gene['inter_' + genotype]})
        else:
            gene.update({'inter': ''})
            logging.warning(f'genotype for gene \'{gene["name"]}\' did not defined, return empty interpretation')
        for i in range(3):
            gene.pop('inter_genotype' + str(i+1))
    return genes_list
