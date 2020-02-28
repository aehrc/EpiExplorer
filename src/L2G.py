import pandas as pd
import numpy as np
import itertools
import os

interactionFiles = ['/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.1.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.2.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.3.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.4.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.1.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.2.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.3.csv',
                    '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.4.csv']

annotationFiles = ['/home/arash/project/EpiExplorer/SampleData/AnnotationFiles/1KGen.txt',
                   '/home/arash/project/EpiExplorer/SampleData/AnnotationFiles/cadd.txt'
                   ]

# files = ['/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.4.csv']


def CreateIntList(files):
    a_df = pd.DataFrame(columns=['id', 'Alpha'])
    b_df = pd.DataFrame(columns=['id', 'Beta'])
    s_df = pd.DataFrame(columns=['id'])

    for file in files:
        df = pd.read_csv(file, header=0, index_col=False)

        # Get list of all SNPs
        mt = df.iloc[:, 1:].values.tolist()
        snps = list(itertools.chain(*mt))
        x_df = pd.DataFrame(snps, columns=['id'])
        s_df = s_df.append(x_df)

        # Check the order
        order = df.shape[1]-1
        if(order < 1 or order > 4):
            print(file + ' must have 2 to 5 columns but it has ' +
                  str(order+1) + ' columns')
            continue

        # Check for Alpha or Beta
        firstColName = df.columns[0]
        isAlpha = False
        if firstColName == 'Alpha':
            isAlpha = True
        elif firstColName == 'Beta':
            isAlpha = False
        else:
            print(
                'In ' + file + ' the first colunm name should be Alpha or Beta but it is: ' + firstColName)

        # name interactions
        df['id'] = df.iloc[:, 1:].agg('#'.join, axis=1)

        if(isAlpha):
            a_df = a_df.append(df[['id', 'Alpha']])
        else:
            b_df = b_df.append(df[['id', 'Beta']])

    # Merge Alpha and Beta
    ab_df = a_df.merge(b_df, on='id', how='outer').replace(np.nan, 0)

    # Merge extra SNP with ab_df
    ab_df = ab_df.merge(s_df.drop_duplicates(), on='id',
                        how='outer').replace(np.nan, 0)

    ab_df['order'] = 0
    for i, r in ab_df.iterrows():
        interaction = r['id']
        snps = interaction.split('#')
        order = len(snps)
        ab_df.at[i, 'order'] = order

    return ab_df


def ReadAnnotations(files, path):
    df = pd.read_csv(files[0], header=0, index_col=False, sep='\t')

    if 'Variation ID' in df.columns[0]:
        pass
    else:
        print('The first annotation file must contain "Variant ID" column')
        exit(1)

    for i, file in enumerate(files):
        if i == 0:
            continue
        else:
            suffix = '_'+os.path.splitext(os.path.basename(file))[0]
            print(suffix)
            t_df = pd.read_csv(file, header=0, index_col=False, sep='\t')
            df = df.merge(t_df, on='Variation ID',
                          how='outer', suffixes=('', suffix))

    df.rename(columns={'Variation ID': 'id'}, inplace=True)
    df.to_csv(path+'All.Annotations.csv', index=False)

    return df


def AsNode(n_df, annot, path):

    e_df = pd.DataFrame(columns=['s', 't', 'Alpha', 'Beta', 'id', 'order'])

    for i, r in n_df.iterrows():
        interaction = r['id']
        snps = interaction.split('#')
        order = r['order']
        # check for snp ids with #
        if(order != len(snps)):
            print('ERROR: Some SNP ids contain #. please change the SNP id in the interaction and annotation files and run the program again.')
            exit(1)

        if order > 1:
            e = r
            e['t'] = interaction
            for s in snps:
                e['s'] = s
                # print(dict(e))
                e_df.loc[len(e_df)] = e

    n_df = n_df.merge(annot, on='id', how='left')

    e_df.to_csv(path+'AsNode-Edge-DF.csv', index=False)
    n_df.to_csv(path+'AsNode-Node-DF.csv', index=False)


def AsEdge(n_df, annot, path):

    e_df = pd.DataFrame(columns=['s', 't', 'Alpha', 'Beta', 'id', 'order'])

    # list interaction nodes
    i_df = n_df[n_df['order'] > 1]

    for i, r in i_df.iterrows():
        interaction = r['id']
        snps = interaction.split('#')

        e = r

        pairs = [(snps[i], snps[j]) for i in range(len(snps))
                 for j in range(i+1, len(snps))]
        for p in pairs:
            e['s'] = p[0]
            e['t'] = p[1]
            e_df.loc[len(e_df)] = e

    n_df = n_df[n_df['order'] == 1]

    n_df = n_df.merge(annot, on='id', how='left')

    e_df.to_csv(path+'AsEdge-Edge-DF.csv', index=False)
    n_df.to_csv(path+'AsEdge-Node-DF.csv', index=False)


def DoItAll(interactionFiles, annotationFiles, path):

    ab_df = CreateIntList(interactionFiles)
    ab_df.to_csv(path+'AB-DF.csv', index=False)

    annot = ReadAnnotations(annotationFiles, path)

    AsNode(ab_df, annot, path)
    AsEdge(ab_df, annot, path)


DoItAll(interactionFiles, annotationFiles,
        '/home/arash/project/EpiExplorer/SampleData/InteractionGraph/')
