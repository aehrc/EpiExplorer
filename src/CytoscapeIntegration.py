# Class to send data to Cytoscape in the form of a json file
import os
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.cynetwork import CyNetwork
from IPython.display import Image
import json
import pandas as pd


class CytoscapeIntegration:
    def __init__(self, node_df, edge_df, core_details, interaction_or_edge):
        self.node_df = node_df
        self.edge_df = edge_df
        self.core_details = core_details
        self.interaction_or_edge = interaction_or_edge
        self.json_file_name = 'json_file.json'
        self.json_file_path = os.path.join('../SampleData/InteractionLists/', self.json_file_name)

    # Method to convert the DataFrames to a json object and save as a .json file
    def dataframe_to_json(self):

        # Create new node and edge dictionaries
        node_dic = self.node_df.to_dict('records')
        edge_dic = self.edge_df.to_dict('records')
        complete_node_list = []
        complete_edge_list = []

        # Add node_dic rows as new individual dictionaries to complete_node_list
        for i in range(len(node_dic)):
            temp_node_dic = {'data': node_dic[i], 'selected': False}
            complete_node_list.append(temp_node_dic)

        # Add edge_dic rows as new individual dictionaries to complete_edge_list
        for i in range(len(edge_dic)):
            temp_edge_dic = {'data': edge_dic[i], 'selected': False}
            complete_edge_list.append(temp_edge_dic)

        # Create dictionary containing both the node and edge data
        elements_dic = {'nodes': complete_node_list, 'edges': complete_edge_list}
        name_dic = {'name': 'Node_Edge_Network'}

        # Complete dictionary of data to be converted to json file
        full_dict = {'data': name_dic, 'elements': elements_dic}

        # Write data to json file in an ordered format
        with open(self.json_file_path, 'w') as outfile:
            json.dump(full_dict, outfile, sort_keys=True, indent=4)

    # When a style is changed in the GUI this method is called
    # TODO add code to filter data for network
    # TODO send the grayed out nodes 'to the back'
    def filter_data(self):
        print('Inside filter data')
        # Read the network in cytoscape
        # Get all the node details and styles
        # Change the styles according to core_details
        # Update the network
        return True

    # Method to create the network and add styles
    def cytoscape_successful(self, update):

        cytoscape_successful = True

        # Create client
        cy = CyRestClient()
        # Clear current session
        cy.session.delete()

        # Convert DataFrame to json file and save file
        self.dataframe_to_json()

        # Create network from json file
        node_edge_network = cy.network.create_from(self.json_file_path)

        cy.layout.apply(network=node_edge_network)

        # Add styles to the network
        my_style = cy.style.create('Epi_Explorer_style')

        # Discrete mappings for specific regions
        order_colour_key_value_pair = {
            '1': '#c99e10',
            '2': '#9b4f0f',
            '3': '#1e434c',
            '4': '#8d230f'
        }

        overlap_colour_key_value_pair = {
            'Protein_coding': '#c99e10',
            'Non_coding': '#9b4f0f',
            'Intergenic': '#1e434c'
        }

        edge_order_colour_key_value_pair = {
            '2': '#9b4f0f',
            '3': '#1e434c',
            '4': '#8d230f'
        }

        edge_order_size_key_value_pair = {
            '2': '5.0',
            '3': '3.0',
            '4': '1.0'
        }

        order_size_key_value_pair = {
            '1': '25.0',
            '2': '35.0',
            '3': '40.0',
            '4': '50.0'
        }

        order_shape_key_value_pair = {
            '1': 'Ellipse',
            '2': 'Diamond',
            '3': 'Triangle',
            '4': 'Hexagon'
        }

        type_colour_variation = [
            {
                'value': '1.0',
                'lesser': '#9b4f0f',
                'equal': '#9b4f0f',
                'greater': '#9b4f0f'
            },
            {
                'value': '20.0',
                'lesser': '#8d230f',
                'equal': '#8d230f',
                'greater': '#8d230f'
            }
        ]

        new_styles = {
            'NODE_FILL_COLOR': '#363636',
            'NODE_SIZE': 10,
            'NODE_BORDER_WIDTH': 0,
            'NODE_TRANSPARENCY': 255,
            'NODE_LABEL_COLOR': '#323334',

            'EDGE_WIDTH': 3,
            'EDGE_STROKE_UNSELECTED_PAINT': '#a9a9a9',
            'EDGE_LINE_TYPE': 'SOLID',
            'EDGE_TRANSPARENCY': 120,

            'NETWORK_BACKGROUND_PAINT': 'white'
        }

        my_style.update_defaults(new_styles)

        # If the GUI is being loaded for the first time
        # Then create network with 'default' styles
        if not update:
            # Add these styles only if the network type is Interaction
            if self.interaction_or_edge == 1:
                my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_FILL_COLOR',
                                                 mappings=order_colour_key_value_pair)

                my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SIZE',
                                                 mappings=order_size_key_value_pair)

                my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SHAPE',
                                                 mappings=order_shape_key_value_pair)

            my_style.create_discrete_mapping(column='order', col_type='String',
                                             vp='EDGE_STROKE_UNSELECTED_PAINT',
                                             mappings=edge_order_colour_key_value_pair)

            my_style.create_discrete_mapping(column='order', col_type='String', vp='EDGE_WIDTH',
                                             mappings=edge_order_size_key_value_pair)
        # TODO when reset/ submit same thing as what the user specified gets loaded
        elif update:
            print('Update styles')
            print(self.core_details)
            # TODO add code for the rest of the styles
            # TODO check if the column exists in the annotation file
            if 'node_colour' in self.core_details.columns:
                print('Styling node colour')
                update_type = self.core_details.at[0, 'node_colour']

                if update_type == 'Order' or update_type == 'Default':
                    my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_FILL_COLOR',
                                                     mappings=order_colour_key_value_pair)
                elif update_type == 'Type':
                    # https://github.com/cytoscape/cytoscape-automation/blob/master/for-scripters/Python/basic-fundamentals.ipynb
                    my_style.create_continuous_mapping(column='Alpha', col_type='Double', vp='NODE_FILL_COLOR', points=type_colour_variation)

                elif update_type == 'Overlap':
                    my_style.create_discrete_mapping(column='Overlap', col_type='String', vp='NODE_FILL_COLOR',
                                                     mappings=overlap_colour_key_value_pair)

            if 'node_size' in self.core_details.columns:
                print('Styling node size')
                update_type = self.core_details.at[0, 'node_size']

                if update_type == 'Order' or update_type == 'Default':
                    my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SIZE',
                                                     mappings=order_size_key_value_pair)

                elif update_type == 'Type':
                    # TODO add continuous mapping for Alpha/ Beta values
                    print('TODO')

            # Code for querying out data
            if 'query' in self.core_details.columns:
                if 'hide' in self.core_details.columns:
                    # TODO check if hide is set to True first omh
                    self.filter_data()

                if 'show' in self.core_details.columns:
                    self.filter_data()

                if 'highlight' in self.core_details.columns:
                    self.filter_data()

                if 'gray' in self.core_details.columns:
                    # Link: https://github.com/cytoscape/cytoscape-automation/blob/master/for-scripters/Python/advanced-view-api.ipynb

                    user_query = self.core_details.at[0, 'query']

                    if 'invert' in self.core_details.columns:
                        if self.core_details.at[0, 'invert'] != 0:
                            # TODO write code to modify query, basically the stuff I did below
                            print('Query needs to be modified')

                    # Get the network from cytoscape
                    view_id_list = node_edge_network.get_views()
                    my_style_2 = node_edge_network.get_view(view_id_list[0], format='json')
                    print(my_style_2)

                    # Get node and edge views as a dictionary
                    node_views_dict = my_style_2.get_node_views_as_dict()
                    edge_views_dict = my_style_2.get_edge_views_as_dict()

                    # Convert to pandas dataframe
                    node_view_df = pd.DataFrame.from_dict(node_views_dict, orient='index')
                    print(node_view_df)
                    print('_________')

                    # filter out the user desired data
                    filtered_df = node_view_df.query(user_query)

                    # Remove the filtered data and make a new df
                    new_df = node_view_df.merge(filtered_df, on='id')
                    print('this is the new df')
                    print(new_df)
                    node_view_df[(~node_view_df.id.isin(new_df.id))]

                    for index, row in filtered_df.iterrows():
                        row['NODE_FILL_COLOR'] = '#d3d3d3'

                    # combine the new DataFrame and the newly changed DataFrame with filters
                    new_df = new_df.merge(filtered_df, on='id')

                    my_style_2.batch_update_node_views(new_df)
                    Image(node_edge_network.get_png(height=400))
                    self.filter_data()

        cy.style.apply(my_style, node_edge_network)

        cy.layout.fit(network=node_edge_network)
        Image(node_edge_network.get_png(height=400))

        return cytoscape_successful
