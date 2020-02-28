import pandas as pd
import numpy as np
import itertools

files = ['/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.1.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.2.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.3.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Alpha.4.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.1.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.2.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.3.csv',
         '/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.4.csv']

#files = ['/home/arash/project/EpiExplorer/SampleData/BitEpiOutputSmall/output.Beta.4.csv']


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

    return ab_df


def AsNode(n_df, path):
    n_df['order'] = 0
    e_df = pd.DataFrame(columns=['s', 't', 'Alpha', 'Beta', 'id', 'order'])

    for i, r in n_df.iterrows():
        interaction = r['id']
        snps = interaction.split('#')
        order = len(snps)

        n_df.at[i, 'order'] = order
        if order > 1:
            e = r
            e['t'] = interaction
            e['order'] = order
            for s in snps:
                e['s'] = s
                # print(dict(e))
                e_df.loc[len(e_df)] = e

    e_df.to_csv(path+'AsNode-Edge-DF.csv', index=False)
    n_df.to_csv(path+'AsNode-Node-DF.csv', index=False)


def DoItAll(files, path):

    ab_df = CreateIntList(files)
    AsNode(ab_df, path)


DoItAll(files, './')
