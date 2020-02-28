# Class containing the main functionality i.e model
import os
import pandas as pd
import numpy as np
import itertools


class ReadWriteData:

    def __init__(self, input_file, annotation_file, output_file):
        self.input_file = input_file
        self.annotation_files = annotation_file
        self.output_file = output_file
        self.int_id = 0
        self.alpha_beta_df = pd.DataFrame(columns=['id', 'Alpha', 'Beta'])

    # Method to validate the input file
    def validate_input_file(self):
        extension = ''
        valid = True
        # Split the file name and verify each substring
        temp_input_file = self.input_file.split('/')
        new_input_file = temp_input_file[-1]
        new_input_file = new_input_file.split('.')

        if len(new_input_file) <= 1:
            valid = False
        else:
            extension = new_input_file[-1]
            if (extension != 'csv') and valid:
                valid = False

        return valid

    # Method to validate annotation file
    def validate_annotation_file(self):
        if self.annotation_files == '':
            print('Optional annotation file not given')
        return True

    # Method to create the initial dataframe with Alpha/ Beta
    def CreateIntList(self):
        a_df = pd.DataFrame(columns=['id', 'Alpha'])
        b_df = pd.DataFrame(columns=['id', 'Beta'])
        s_df = pd.DataFrame(columns=['id'])

        for file in self.input_file:
            df = pd.read_csv(file, header=0, index_col=False)

            # Get list of all SNPs
            mt = df.iloc[:, 1:].values.tolist()
            snps = list(itertools.chain(*mt))
            x_df = pd.DataFrame(snps, columns=['id'])
            s_df = s_df.append(x_df)

            # Check the order
            order = df.shape[1] - 1
            if (order < 1 or order > 4):
                print(file + ' must have 2 to 5 columns but it has ' +
                      str(order + 1) + ' columns')
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

            if (isAlpha):
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

    # Merge annotation files
    def ReadAnnotations(self):
        df = pd.read_csv(self.annotation_files[0], header=0, index_col=False, sep='\t')
        path = self.output_file
        if 'Variation ID' in df.columns[0]:
            pass
        else:
            print('The first annotation file must contain "Variant ID" column')
            exit(1)

        for i, file in enumerate(self.annotation_files):
            if i == 0:
                continue
            else:
                suffix = '_' + os.path.splitext(os.path.basename(file))[0]
                print(suffix)
                t_df = pd.read_csv(file, header=0, index_col=False, sep='\t')
                df = df.merge(t_df, on='Variation ID',
                              how='outer', suffixes=('', suffix))

        df.rename(columns={'Variation ID': 'id'}, inplace=True)
        df.to_csv(path + 'All.Annotations.csv', index=False)

        return df

    def AsNode(n_df, annot, path):

        e_df = pd.DataFrame(
            columns=['source', 'target', 'Alpha', 'Beta', 'id', 'order'])

        for i, r in n_df.iterrows():
            interaction = r['id']
            snps = interaction.split('#')
            order = r['order']
            # check for snp ids with #
            if (order != len(snps)):
                print(
                    'ERROR: Some SNP ids contain #. please change the SNP id in the interaction and annotation files and run the program again.')
                exit(1)

            if order > 1:
                e = r
                e['target'] = interaction
                for s in snps:
                    e['source'] = s
                    # print(dict(e))
                    e_df.loc[len(e_df)] = e

        n_df = n_df.merge(annot, on='id', how='left')

        e_df.to_csv(os.path.join(path, 'AsNode-Edge-DF.csv'), index=False)
        n_df.to_csv(os.path.join(path, 'AsNode-Node-DF.csv'), index=False)

        interaction_mode_dfs = [n_df, e_df]

        return interaction_mode_dfs

    def AsEdge(n_df, annot, path):

        e_df = pd.DataFrame(
            columns=['source', 'target', 'Alpha', 'Beta', 'id', 'order'])

        # list interaction nodes
        i_df = n_df[n_df['order'] > 1]

        for i, r in i_df.iterrows():
            interaction = r['id']
            snps = interaction.split('#')

            e = r

            pairs = [(snps[i], snps[j]) for i in range(len(snps))
                     for j in range(i + 1, len(snps))]
            for p in pairs:
                e['source'] = p[0]
                e['target'] = p[1]
                e_df.loc[len(e_df)] = e

        n_df = n_df[n_df['order'] == 1]

        n_df = n_df.merge(annot, on='id', how='left')

        e_df['interaction'] = e_df['id']
        e_df.to_csv(os.path.join(path, 'AsEdge-Edge-DF.csv') , index=False)
        n_df.to_csv(os.path.join(path, 'AsEdge-Node-DF.csv'), index=False)

        edge_mode_dfs = [n_df, e_df]

        return edge_mode_dfs

    # Method to write data in the correct format
    def get_correctly_formatted_dataframes(self, node_df, edge_df, int_order, interaction_or_edge):
        data_written_to_csv = True
        node_file_name = 'nodes.csv'
        edge_file_name = 'edges.csv'
        trans_edge_file_name = 'trans_edges.csv'
        trans_node_file_name = 'trans_nodes.csv'
        node_file_path = ''
        edge_file_path = ''

        user_given_output_path = self.output_file

        if user_given_output_path == '':
            # Check if directory exists
            directory = False
            if os.path.isdir('../SampleData/InteractionGraph/'):
                directory = True
            else:
                os.makedirs('../SampleData/InteractionGraph/')
                directory = True

            if directory:
                if interaction_or_edge == 1:
                    node_file_path = os.path.join('../SampleData/InteractionGraph/', node_file_name)
                    edge_file_path = os.path.join('../SampleData/InteractionGraph/', edge_file_name)
                elif interaction_or_edge == 2:
                    node_file_path = os.path.join('../SampleData/InteractionGraph/', trans_node_file_name)
                    edge_file_path = os.path.join('../SampleData/InteractionGraph/', trans_edge_file_name)
            else:
                print('Error: Could not find output directory')
        else:
            print('User given output path exists')
            if interaction_or_edge == 1:
                node_file_path = os.path.join(user_given_output_path, node_file_name)
                edge_file_path = os.path.join(user_given_output_path, edge_file_name)
            elif interaction_or_edge == 2:
                node_file_path = os.path.join(user_given_output_path, trans_node_file_name)
                edge_file_path = os.path.join(user_given_output_path, trans_edge_file_name)

        # DataFrames to send to Cytoscape
        correct_node_df = pd.DataFrame
        correct_edge_df = pd.DataFrame
        # TODO check the merging of the alpha, beta, count and annotation files
        # Pre-check for appending alpha and beta values for edge df
        if not os.path.isfile(node_file_path):
            print('No existing node file found. Creating a new file nodes.csv')
            new_node_df = self.check_node_duplicates(node_df, node_df)
        else:
            print('Existing node file found. Appending to node.csv')
            # Read in the existing DataFrame and check for duplicates
            existing_df = pd.read_csv(node_file_path)
            # Get a new DataFrame without any duplicated nodes
            new_node_df = self.check_node_duplicates(node_df, existing_df)

        # Check if files exist
        # Create a new file if there is no existing one
        # If exists then append to the existing file
        if not os.path.isfile(edge_file_path):
            print('No existing edges file found. Creating a new file edges.csv')
            new_edge_df = self.check_edge_duplicates(edge_df, edge_df, interaction_or_edge)
            if not new_edge_df.empty:
                new_edge_df = self.merge_association_to_edge_df(new_edge_df)
            new_edge_df.to_csv(edge_file_path, encoding='utf-8', index=False)
            correct_edge_df = new_edge_df
        else:
            print('Existing edges file found. Appending to edges.csv')
            # Read in the existing DataFrame and check for duplicates
            existing_df = pd.read_csv(edge_file_path)
            if existing_df.empty:
                print('The existing file is empty. Creating a new file edges.csv')
                new_edge_df = self.check_edge_duplicates(edge_df, edge_df, interaction_or_edge)
                new_edge_df = self.merge_association_to_edge_df(new_edge_df)
                new_edge_df.to_csv(edge_file_path, encoding='utf-8', index=False)
                correct_edge_df = new_edge_df
            else:
                # Get a new DataFrame without any duplicated edges
                print('The existing file is NOT empty. Appending to file edges.csv')
                new_edge_df = self.check_edge_duplicates(edge_df, existing_df, interaction_or_edge)
                new_edge_df = self.merge_association_to_edge_df(new_edge_df)
                os.remove(edge_file_path)
                new_edge_df.to_csv(edge_file_path, encoding='utf-8', index=False)
                correct_edge_df = new_edge_df

        connection_count_df = self.create_connection_count_df(correct_edge_df)

        if not os.path.isfile(node_file_path):
            print('No existing node file found. Creating a new file nodes.csv')
            new_node_df = self.check_node_duplicates(node_df, node_df)
            new_node_df = self.get_merged_new_node_df(new_node_df, connection_count_df)
            new_node_df = self.merge_df_with_annotations(new_node_df)
            new_node_df.to_csv(node_file_path, encoding='utf-8', index=False)
            correct_node_df = new_node_df
        else:
            print('Existing node file found. Appending to node.csv')
            # Read in the existing DataFrame and check for duplicates
            existing_df = pd.read_csv(node_file_path)
            # Get a new DataFrame without any duplicated nodes
            new_node_df = self.check_node_duplicates(node_df, existing_df)
            new_node_df = self.get_merged_new_node_df(new_node_df, connection_count_df)
            new_node_df = self.merge_df_with_annotations(new_node_df)
            os.remove(node_file_path)
            new_node_df.to_csv(node_file_path, encoding='utf-8', index=False)
            correct_node_df = new_node_df

        # Send the DataFrames (which were checked for duplication) to Cytoscape
        data_written = [correct_node_df, correct_edge_df, data_written_to_csv]

        return data_written

    # Method to read in data and write data from and to a csv file
    def get_dataframes(self, interaction_or_edge):
        read_write_done = True

        alpha_beta_df = self.CreateIntList()
        alpha_beta_df.to_csv(os.path.join(self.output_file, 'AB-DF.csv'), index=False)

        annotation_df = self.ReadAnnotations()

        user_given_output_path = self.output_file

        if user_given_output_path == '':
            # Check if directory exists
            directory = False
            if os.path.isdir('../SampleData/InteractionGraph/'):
                directory = True
            else:
                os.makedirs('../SampleData/InteractionGraph/')
                directory = True

            if directory:
                return_dfs = ''
                if interaction_or_edge == 1:
                    return_dfs = self.AsNode(alpha_beta_df, annotation_df, self.output_file)
                else:
                    return_dfs = self.AsEdge(alpha_beta_df, annotation_df, self.output_file)
            else:
                print('Error: Could not find output directory')
        else:
            print('User given output path exists')

        cytoscape_df = [return_dfs[0], return_dfs[1], read_write_done]

        return cytoscape_df
