# Controller class to join the View and the Model
from ReadWriteData import ReadWriteData
from CytoscapeIntegration import CytoscapeIntegration
from FormGUI import FormGUI


class Controller:
    def __init__(self):
        self.input_file = ''
        self.annotation_file = ''

    # Method to call forth the GUI
    def perform_form_functionality(self):
        controller = Controller()
        form = FormGUI(controller)
        form_details = form.form()

        return form_details

    # Method to call Model functionality from View
    # Takes the arguments: GUI filtering requirements, whether graph should be updated or if it's the first time,
    # If the network type is Interaction or Edge
    def perform_core_functionality(self, core_details, update, interaction_or_edge):
        global integration
        files_loaded = False
        if not update:
            # Validate input file
            input_files = core_details.iat[0, 0]
            input_files = input_files.split()
            for input_file in input_files:
                print(input_file)
                read_write_data = ReadWriteData(input_file, core_details.iat[0, 1], core_details.iat[0, 2])
                valid_input_file = read_write_data.validate_input_file()
                valid_annotation_file = read_write_data.validate_annotation_file()
                files_loaded = False
                if valid_input_file and valid_annotation_file:
                    print('The input file, {}, has been successfully validated.'
                          .format(input_file))

                    print('The annotation file, {}, has been successfully loaded.'
                          .format(core_details.iat[0, 1]))

                    files_loaded = True

                    # Get the node_df, edge_df and if the functions were successful
                    read_write_done = read_write_data.get_dataframes(interaction_or_edge)
                    if read_write_done[2]:
                        print(
                            'The input file, {}, has been successfully loaded '
                            'and the output file has been created successfully.'.format(
                                input_file))
                        print('Send data to Cytoscape.')

                        # Send the DataFrames in order to create the json file and create the network
                        if integration is None:
                            integration = CytoscapeIntegration(read_write_done[0], read_write_done[1],
                                                               interaction_or_edge)
                        # Call function and determine if cytoscape worked
                        cytoscape_successful = integration.cytoscape_successful(update, core_details)

                        if cytoscape_successful:
                            print('Successful creation of network!')
                        else:
                            print('Network creation unsuccessful, please make sure that Cytoscape is running in the background')
                    else:
                        print('Error has occurred in Read and/or Write of the file.')
                elif not valid_input_file:
                    print('Error found in input file format.')
                    files_loaded = False
                elif not valid_annotation_file:
                    print('Error found when loading the annotation file')
                    files_loaded = False
                print('___________________________________')
        elif update:
            print('Calliiinnggg update')
            cytoscape_successful = integration.cytoscape_successful(update, core_details)
            if cytoscape_successful:
                print('Successful creation of network!')
            else:
                print('Network creation unsuccessful, please make sure that Cytoscape is running in the background')

        return files_loaded


integration = None
