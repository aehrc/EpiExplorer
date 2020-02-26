# Class to send data to Cytoscape in the form of a json file
import os
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.cynetwork import CyNetwork
from IPython.display import Image
import json
import pandas as pd
from py2cytoscape.data.style import StyleUtil


class CytoscapeIntegration:

    def __init__(self, node_df, edge_df, interaction_or_edge):
        self.node_df = node_df
        self.edge_df = edge_df
        self.interaction_or_edge = interaction_or_edge
        self.json_file_name = 'json_file.json'
        self.json_file_path = os.path.join('../SampleData/InteractionGraph/', self.json_file_name)
        self.cy = CyRestClient()
        self.node_edge_network = None  # = self.cy.network.create_from(self.json_file_path)

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
    def cytoscape_successful(self, update, core_details):

        cytoscape_successful = True

        # Discrete mappings for specific regions
        order_colour_key_value_pair = {
            '1': '#c99e10',
            '2': '#9b4f0f',
            '3': '#1e434c',
            '4': '#8d230f'
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
            '1': '15.0',
            '2': '35.0',
            '3': '55.0',
            '4': '75.0'
        }

        order_shape_key_value_pair = {
            '1': 'Ellipse',
            '2': 'Diamond',
            '3': 'Triangle',
            '4': 'Hexagon'
        }

        type_colour_variation = [
            {
                'value': '0.0050',
                'lesser': '#1e434c',
                'equal': '#1e434c',
                'greater': '#1e434c'
            },
            {
                'value': '0.05',
                'lesser': '#f0f0f0',
                'equal': '#f0f0f0',
                'greater': '#f0f0f0'
            },
            {
                'value': '0.1',
                'lesser': '#8d230f',
                'equal': '#8d230f',
                'greater': '#8d230f'
            }
        ]

        type_shape_variation = [
            {
                'value': '0.0050',
                'lesser': 'Ellipse',
                'equal': 'Ellipse',
                'greater': 'Ellipse'
            },
            {
                'value': '0.1',
                'lesser': 'Hexagon',
                'equal': 'Hexagon',
                'greater': 'Hexagon'
            }

        ]

        node_type_size = StyleUtil.create_slope(min=0.001, max=0.01, values=(10, 50))

        edge_type_thickness = [
            {
                'value': '0.0050',
                'lesser': '1.0',
                'equal': '1.0',
                'greater': '1.0'
            },
            {
                'value': '0.05',
                'lesser': '3.0',
                'equal': '3.0',
                'greater': '3.0'
            },
            {
                'value': '0.1',
                'lesser': '5.0',
                'equal': '5.0',
                'greater': '5.0'
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

        # If the program is being loaded for the first time or the user wants to reset the network
        if not update:
            print('Creating network.')
            # Clear current session
            self.cy.session.delete()

            # Convert DataFrame to json file and save file
            self.dataframe_to_json()

            # Create network from json file
            self.node_edge_network = self.cy.network.create_from(self.json_file_path)

            self.cy.layout.apply(network=self.node_edge_network)

            # Add styles to the network
            my_style = self.cy.style.create('Epi_Explorer_style')

            # If the GUI is being loaded for the first time
            # Then create network with 'default' styles
            my_style.update_defaults(new_styles)

            # Add these styles only if the network type is Interaction
            if self.interaction_or_edge == 1:
                my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_FILL_COLOR',
                                                 mappings=order_colour_key_value_pair)

                my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SIZE',
                                                 mappings=order_size_key_value_pair)

                my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SHAPE',
                                                 mappings=order_shape_key_value_pair)

            # General styles for both modes of the network
            my_style.create_discrete_mapping(column='order', col_type='String',
                                             vp='EDGE_STROKE_UNSELECTED_PAINT',
                                             mappings=edge_order_colour_key_value_pair)

            my_style.create_discrete_mapping(column='order', col_type='String', vp='EDGE_WIDTH',
                                             mappings=edge_order_size_key_value_pair)

            self.cy.style.apply(my_style, self.node_edge_network)

        # If user wants to update according to a specific style/ query
        elif update:
            print('Update styles')
            my_style = self.cy.style.create('Epi_Explorer_style')
            my_style.update_defaults(new_styles)

            if 'node_colour' in core_details.columns:
                print('Styling node colour')
                update_type = core_details.at[0, 'node_colour']

                if update_type == 'Order':
                    my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_FILL_COLOR',
                                                     mappings=order_colour_key_value_pair)
                elif update_type == 'Alpha':
                    my_style.create_continuous_mapping(column='Alpha', col_type='Double', vp='NODE_FILL_COLOR',
                                                       points=type_colour_variation)
                elif update_type == 'Beta':
                    my_style.create_continuous_mapping(column='Beta', col_type='Double', vp='NODE_FILL_COLOR',
                                                       points=type_colour_variation)

                self.cy.style.apply(my_style, self.node_edge_network)

            if 'node_size' in core_details.columns:
                print('Styling node size')
                update_type = core_details.at[0, 'node_size']

                if update_type == 'Order':
                    my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SIZE',
                                                     mappings=order_size_key_value_pair)

                elif update_type == 'Alpha':
                    my_style.create_continuous_mapping(column='Alpha', col_type='Double', vp='NODE_SIZE',
                                                       points=node_type_size)
                elif update_type == 'Beta':
                    my_style.create_continuous_mapping(column='Beta', col_type='Double', vp='NODE_SIZE',
                                                       points=node_type_size)

                self.cy.style.apply(my_style, self.node_edge_network)

            if 'node_shape' in core_details.columns:
                print('Styling node shape')
                update_type = core_details.at[0, 'node_shape']

                if update_type == 'Order':
                    my_style.create_discrete_mapping(column='order', col_type='String', vp='NODE_SHAPE',
                                                     mappings=order_shape_key_value_pair)

                elif update_type == 'Alpha':
                    my_style.create_continuous_mapping(column='Alpha', col_type='Double', vp='NODE_SHAPE',
                                                       points=type_shape_variation)
                elif update_type == 'Beta':
                    my_style.create_continuous_mapping(column='Beta', col_type='Double', vp='NODE_SHAPE',
                                                       points=type_shape_variation)

                self.cy.style.apply(my_style, self.node_edge_network)

            if 'edge_colour' in core_details.columns:
                print('Styling edge colour')
                update_type = core_details.at[0, 'edge_colour']

                if update_type == 'Order' or update_type == 'Default':
                    my_style.create_discrete_mapping(column='order', col_type='String',
                                                     vp='EDGE_STROKE_UNSELECTED_PAINT',
                                                     mappings=edge_order_colour_key_value_pair)

                elif update_type == 'Alpha':
                    my_style.create_continuous_mapping(column='Alpha', col_type='Double',
                                                       vp='EDGE_STROKE_UNSELECTED_PAINT',
                                                       points=type_colour_variation)
                elif update_type == 'Beta':
                    my_style.create_continuous_mapping(column='Beta', col_type='Double',
                                                       vp='EDGE_STROKE_UNSELECTED_PAINT',
                                                       points=type_colour_variation)

                self.cy.style.apply(my_style, self.node_edge_network)

            if 'edge_thickness' in core_details.columns:
                print('Styling edge thickness')
                update_type = core_details.at[0, 'edge_thickness']

                if update_type == 'Order' or update_type == 'Default':
                    my_style.create_discrete_mapping(column='order', col_type='String', vp='EDGE_WIDTH',
                                                     mappings=edge_order_size_key_value_pair)

                elif update_type == 'Alpha':
                    my_style.create_continuous_mapping(column='Alpha', col_type='Double', vp='EDGE_WIDTH',
                                                       points=edge_type_thickness)
                elif update_type == 'Beta':
                    my_style.create_continuous_mapping(column='Beta', col_type='Double', vp='EDGE_WIDTH',
                                                       points=edge_type_thickness)

                self.cy.style.apply(my_style, self.node_edge_network)

            # Code for querying out data
            if 'query' in core_details.columns:
                if 'hide' in core_details.columns:
                    self.filter_data()

                if 'show' in core_details.columns:
                    self.filter_data()

                if 'highlight' in core_details.columns:
                    self.filter_data()

                if 'gray' in core_details.columns:
                    # Link: https://github.com/cytoscape/cytoscape-automation/blob/master/for-scripters/Python/advanced-view-api.ipynb

                    # Check if the gray out is set to True
                    if core_details.at[0, 'gray']:
                        user_query = core_details.at[0, 'query']
                        print('Querying the data using: ', user_query)

                        # Get the network from cytoscape
                        view_id_list = self.node_edge_network.get_views()
                        view1 = self.node_edge_network.get_view(view_id_list[0], fmt='view')
                        my_style_2 = self.node_edge_network.get_view(view_id_list[0])

                        # Get nodes and edges as a df
                        view_df = pd.DataFrame.from_dict(my_style_2, orient='index')
                        nodes_edge_df = view_df.iat[4, 0]

                        node_list = nodes_edge_df['nodes']
                        node_df = pd.DataFrame(node_list)
                        node_data_df = pd.DataFrame(node_df['data'])

                        correct_node_data_df = pd.DataFrame()

                        for index, row in node_data_df.iterrows():
                            correct_node_data_df = correct_node_data_df.append(node_data_df.iloc[index, 0],
                                                                               ignore_index=True)

                        # filter out the user desired data
                        filtered_df = correct_node_data_df.query(user_query).reset_index(
                            drop=True)

                        if 'invert' in core_details.columns:
                            if core_details.at[0, 'invert'] != 0:
                                # Invert
                                new_df = correct_node_data_df.merge(filtered_df, on=['id', 'name'])
                                filtered_df = correct_node_data_df[(~correct_node_data_df.id.isin(new_df.id))]

                        # Get node/edge views as a Python dictionary
                        node_views_dict = view1.get_node_views_as_dict()
                        # Convert it into Pandas DataFrame
                        nv_df = pd.DataFrame.from_dict(node_views_dict, orient='index')
                        # Extract specific Visual Property values...
                        node_location_df = nv_df['NODE_FILL_COLOR']
                        node_location_df = pd.DataFrame(node_location_df, columns=['NODE_FILL_COLOR'])
                        node_location_df['id'] = node_location_df.index
                        node_location_df = node_location_df.reset_index(drop=True)

                        convert_dict = {'id': int}

                        filtered_df = filtered_df.astype(convert_dict)
                        key_value_pair = {}
                        for index, row in filtered_df.iterrows():
                            filtered_id = filtered_df.at[index, 'id']
                            for index_node_loc, row_loc in node_location_df.iterrows():
                                node_loc_id = node_location_df.at[index_node_loc, 'id']
                                if filtered_id == node_loc_id:
                                    node_location_df.at[index_node_loc, 'NODE_FILL_COLOR'] = '#d3d3d3'
                                    key_value_pair[str(node_loc_id)] = '#d3d3d3'
                                else:
                                    key_value_pair[str(node_loc_id)] = node_location_df.at[
                                        index_node_loc, 'NODE_FILL_COLOR']

                        view1.update_node_views(visual_property='NODE_FILL_COLOR', values=key_value_pair)
                        Image(self.node_edge_network.get_png(height=400))
                        self.filter_data()

        self.cy.layout.fit(network=self.node_edge_network)
        Image(self.node_edge_network.get_png(height=400))

        return cytoscape_successful
