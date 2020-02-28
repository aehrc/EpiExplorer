# Class containing all the GUI functionality
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog
import pandas as pd
import webbrowser


class FormGUI:

    def __init__(self, controller):
        self.controller = controller
        self.hide_bool = False
        self.show_bool = False
        self.highlight_bool = False
        self.gray_bool = False
        self.reset_bool = False
        self.input_file_names = ''
        self.annotation_files = ''
        self.output_file_path = ''
        # Setting initial values as edge mode and not inverted
        self.var_interaction_or_edge = 1
        self.var_invert_or_not = 0

    # Method to get the invert of the query
    def invert_or_not(self, var_invert):
        if var_invert == 0:
            print('No inverting')
            self.var_invert_or_not = 0
        else:
            print('Invert')
            self.var_invert_or_not = 1

    # Method to check if mode is interaction or edge
    def check_interaction_or_edge(self, var_interaction):
        if var_interaction == 0:
            print('Loading network in Edge mode.')
            self.var_interaction_or_edge = 2
        else:
            print('Loading network in Interaction as a Node mode.')
            self.var_interaction_or_edge = 1

    # Method for the user to specify output file directory
    def select_output_file(self, root, output_file_entry):
        received_file = tkinter.filedialog.askdirectory(parent=root, title='Choose directory')
        self.output_file_path = received_file
        output_file_entry.insert(0, self.output_file_path)

    # Method for the user to specify annotation file paths
    def select_annotation_files(self, root, annotation_file_entry):
        received_files = tkinter.filedialog.askopenfilenames(parent=root, title='Choose a file/s')
        received_files = root.tk.splitlist(received_files)
        self.annotation_files = received_files
        annotation_file_entry.insert(0, self.annotation_files)

    # Method for the user to specify input file paths
    def select_input_files(self, root, input_file_entry):
        received_files = tkinter.filedialog.askopenfilenames(parent=root, title='Choose a file/s')
        received_files = root.tk.splitlist(received_files)
        self.input_file_names = received_files
        input_file_entry.insert(0, self.input_file_names)

    # Load files upon clicking load on the GUI
    def load_files(self, input_file, annotation_file, interaction_or_edge):
        # node_file_name = 'nodes.csv'
        # edge_file_name = 'edges.csv'
        # trans_edge_file_name = 'trans_edges.csv'
        # trans_node_file_name = 'trans_nodes.csv'
        #
        # node_file_path = os.path.join(self.output_file_path, node_file_name)
        # edge_file_path = os.path.join(self.output_file_path, edge_file_name)
        # trans_node_path = os.path.join(self.output_file_path, trans_node_file_name)
        # trans_edge_path = os.path.join(self.output_file_path, trans_edge_file_name)
        #
        # os.remove(node_file_path)
        # os.remove(edge_file_path)
        # os.remove(trans_node_path)
        # os.remove(trans_edge_path)

        details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, True]],
                                  columns=['input_file', 'annotation_file', 'output_file', 'reset'])
        # Call the validate function in Controller class
        valid = self.controller.perform_core_functionality(details_df, False, interaction_or_edge)
        if valid:
            messagebox.showinfo('Success', 'Check Cytoscape to view your network!')
        else:
            messagebox.showinfo('Error', 'Please input valid files')

    # Method to create the form
    def form(self):
        root = tk.Tk()
        root.title('EpiExplorer')

        # Add icon to the GUI
        # img_path = r'csiro.png'
        # imgicon = tk.Image('photo', file=img_path)
        # root.tk.call('wm', 'iconphoto', root._w, imgicon)

        # Main window colour scheme
        # Blue: '#00A9CE'
        # Dark blue: '#001D34'
        # Steel: '#757579'
        # Mist: '#DADBDC'

        canvas = tk.Canvas(root, height=720, width=640)
        canvas.pack()
        main_title = tk.Label(root, text='Welcome to EpiExplorer! A visualisation tool for SNP '
                                         'interactions.')
        main_title.place(relx=0.01, rely=0.035, relheight=0.05, relwidth=0.75)

        # logo = PhotoImage(file=img_path)
        # logo_resized = logo.subsample(10, 10)
        # photo_label = tk.Label(root, image=logo_resized)
        # photo_label.place(relx=0.8, rely=0.01, relheight=0.075, relwidth=0.25)

        # Frame to input files and load
        file_frame = tk.Frame(root, bg='#001D34', bd=5)
        file_frame.place(relx=0.5, rely=0.1, relwidth=0.95, relheight=0.2, anchor='n')

        input_file_title = tk.Label(file_frame, text='Input file/s: ')
        input_file_title.place(relx=0.01, rely=0.1, relheight=0.15, relwidth=0.25)

        input_file_entry = tk.Entry(file_frame)
        input_file_entry.insert('0', '../SampleData/BitEpiOutputSmall/output.Alpha.1.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Alpha.2.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Alpha.3.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Alpha.4.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Beta.1.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Beta.2.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Beta.3.csv '
                                     '../SampleData/BitEpiOutputSmall/output.Beta.4.csv')

        input_file_entry.place(relx=0.275, rely=0.1, relwidth=0.5, relheight=0.15)

        load_file_button = tk.Button(file_frame, bg='#DADBDC', text="Open",
                                     command=lambda: self.select_input_files(root, input_file_entry))
        load_file_button.place(relx=0.8, rely=0.1, relwidth=0.15, relheight=0.15)

        annot_file_title = tk.Label(file_frame, text='Annotation file/s: ')
        annot_file_title.place(relx=0.01, rely=0.3, relheight=0.15, relwidth=0.25)

        annot_file_entry = tk.Entry(file_frame)
        annot_file_entry.insert('0', '../SampleData/AnnotationFiles/1KGen.txt')
        annot_file_entry.place(relx=0.275, rely=0.3, relwidth=0.5, relheight=0.15)

        load_annot_file_button = tk.Button(file_frame, bg='#DADBDC', text="Open",
                                           command=lambda: self.select_annotation_files(root, annot_file_entry))
        load_annot_file_button.place(relx=0.8, rely=0.3, relwidth=0.15, relheight=0.15)

        output_file_title = tk.Label(file_frame, text='Output path: ')
        output_file_title.place(relx=0.01, rely=0.5, relheight=0.15, relwidth=0.25)

        output_file_entry = tk.Entry(file_frame)
        output_file_entry.insert('0', '../SampleData/InteractionGraph/')
        output_file_entry.place(relx=0.275, rely=0.5, relwidth=0.5, relheight=0.15)

        load_output_file_button = tk.Button(file_frame, bg='#DADBDC', text="Open",
                                            command=lambda: self.select_output_file(root, output_file_entry))
        load_output_file_button.place(relx=0.8, rely=0.5, relwidth=0.15, relheight=0.15)

        # Check button to specify Interaction or Edge network
        var_interaction = tk.IntVar()
        node_check_button = tk.Checkbutton(file_frame, text='Show Interaction as Nodes',
                                           variable=var_interaction,
                                           command=lambda: self.check_interaction_or_edge(
                                               var_interaction.get()))
        node_check_button.select()
        node_check_button.place(relx=0.01, rely=0.75, relwidth=0.35, relheight=0.2)

        load_button = tk.Button(file_frame, bg='#DADBDC', text="Load",
                                command=lambda: self.load_files(input_file_entry.get(), annot_file_entry.get(),
                                                                self.var_interaction_or_edge))
        load_button.place(relx=0.75, rely=0.75, relheight=0.2, relwidth=0.225)

        # Frame to specify styles for the network
        view_frame = tk.Frame(root, bg='#757579', bd=5)
        view_frame.place(relx=0.258, rely=0.31, relwidth=0.468, relheight=0.575, anchor='n')

        view_frame_title = tk.Label(view_frame, bg='#757579', text='Apply styles to SNPs.')
        view_frame_title.place(relx=0.04, rely=0.05, relheight=0.1, relwidth=0.95)

        node_colour_title = tk.Label(view_frame, bg='#DADBDC', justify='left', text='Node colour by: ')
        node_colour_title.place(relx=0.04, rely=0.2, relheight=0.1, relwidth=0.45)

        node_color_list = ['Order', 'Alpha', 'Beta']
        node_colour_variable = tk.StringVar(view_frame)
        node_colour_variable.set(node_color_list[0])

        node_colour_options = tk.OptionMenu(view_frame, node_colour_variable, *node_color_list,
                                            command=lambda x: self.node_colour(node_colour_variable.get(),
                                                                               input_file_entry.get(),
                                                                               annot_file_entry.get(),
                                                                               self.var_interaction_or_edge))
        node_colour_options.place(relx=0.525, rely=0.2, relheight=0.1, relwidth=0.45)

        node_size_title = tk.Label(view_frame, bg='#DADBDC', text='Node size by: ')
        node_size_title.place(relx=0.04, rely=0.35, relheight=0.1, relwidth=0.45)

        node_size_list = ['Order', 'Alpha', 'Beta']
        node_size_variable = tk.StringVar(view_frame)
        node_size_variable.set(node_color_list[0])

        node_size_options = tk.OptionMenu(view_frame, node_size_variable, *node_size_list,
                                          command=lambda x: self.node_size(node_size_variable.get(),
                                                                           input_file_entry.get(),
                                                                           annot_file_entry.get(),
                                                                           self.var_interaction_or_edge))
        node_size_options.place(relx=0.525, rely=0.35, relheight=0.1, relwidth=0.45)

        node_shape_title = tk.Label(view_frame, bg='#DADBDC', text='Node shape by: ')
        node_shape_title.place(relx=0.04, rely=0.5, relheight=0.1, relwidth=0.45)

        node_shape_list = ['Order', 'Alpha', 'Beta']
        node_shape_variable = tk.StringVar(view_frame)
        node_shape_variable.set(node_color_list[0])
        node_shape_options = tk.OptionMenu(view_frame, node_shape_variable, *node_shape_list,
                                           command=lambda x: self.node_shape(node_shape_variable.get(),
                                                                             input_file_entry.get(),
                                                                             annot_file_entry.get(),
                                                                             self.var_interaction_or_edge))
        node_shape_options.place(relx=0.525, rely=0.5, relheight=0.1, relwidth=0.45)

        edge_colour_title = tk.Label(view_frame, bg='#DADBDC', text='Edge colour by: ')
        edge_colour_title.place(relx=0.04, rely=0.65, relheight=0.1, relwidth=0.45)

        edge_colour_list = ['Order', 'Alpha', 'Beta']
        edge_colour_variable = tk.StringVar(view_frame)
        edge_colour_variable.set(edge_colour_list[0])
        edge_colour_options = tk.OptionMenu(view_frame, edge_colour_variable, *edge_colour_list,
                                            command=lambda x: self.edge_colour(edge_colour_variable.get(),
                                                                               input_file_entry.get(),
                                                                               annot_file_entry.get(),
                                                                               self.var_interaction_or_edge))
        edge_colour_options.place(relx=0.525, rely=0.65, relheight=0.1, relwidth=0.45)

        edge_thickness_title = tk.Label(view_frame, bg='#DADBDC', text='Edge thickness by: ')
        edge_thickness_title.place(relx=0.04, rely=0.8, relheight=0.1, relwidth=0.45)

        edge_thickness_list = ['Order', 'Alpha', 'Beta']
        edge_thickness_variable = tk.StringVar(view_frame)
        edge_thickness_variable.set(edge_thickness_list[0])
        edge_thickness_options = tk.OptionMenu(view_frame, edge_thickness_variable, *edge_thickness_list,
                                               command=lambda x: self.edge_thickness(edge_thickness_variable.get(),
                                                                                     input_file_entry.get(),
                                                                                     annot_file_entry.get(),
                                                                                     self.var_interaction_or_edge))
        edge_thickness_options.place(relx=0.525, rely=0.8, relheight=0.1, relwidth=0.45)

        # Frame to filter data
        filter_frame = tk.Frame(root, bg='#757579', bd=5)
        filter_frame.place(relx=0.74, rely=0.31, relwidth=0.468, relheight=0.575, anchor='n')

        filter_frame_title = tk.Label(filter_frame, bg='#757579', text='Query SNPs as shown below.')
        filter_frame_title.place(relx=0.04, rely=0.05, relheight=0.1, relwidth=0.95)

        filter_entry = tk.scrolledtext.ScrolledText(filter_frame)
        filter_entry.insert('insert', 'order == \'3\'')
        filter_entry.place(relx=0.05, rely=0.2, relwidth=0.925, relheight=0.3)

        # Check button to invert query
        var_invert = tk.IntVar()
        invert_check_button = tk.Checkbutton(filter_frame, text='Invert', bg='#DADBDC',
                                             variable=var_invert,
                                             command=lambda: self.invert_or_not(var_invert.get()))

        invert_check_button.place(relx=0.04, rely=0.85, relwidth=0.225, relheight=0.1)

        hide_button = tk.Button(filter_frame, bg='#DADBDC', text="Hide",
                                command=lambda: self.hide(input_file_entry.get(), annot_file_entry.get(),
                                                          self.var_interaction_or_edge,
                                                          filter_entry.get("1.0", tkinter.END),
                                                          self.var_invert_or_not))
        hide_button.place(relx=0.04, rely=0.55, relheight=0.1, relwidth=0.45)

        show_button = tk.Button(filter_frame, bg='#DADBDC', text="Show",
                                command=lambda: self.show(input_file_entry.get(), annot_file_entry.get(),
                                                          self.var_interaction_or_edge,
                                                          filter_entry.get("1.0", tkinter.END),
                                                          self.var_invert_or_not))
        show_button.place(relx=0.525, rely=0.55, relheight=0.1, relwidth=0.45)

        hl_button = tk.Button(filter_frame, bg='#DADBDC', text="Highlight",
                              command=lambda: self.highlight(input_file_entry.get(), annot_file_entry.get(),
                                                             self.var_interaction_or_edge,
                                                             filter_entry.get("1.0", tkinter.END),
                                                             self.var_invert_or_not))
        hl_button.place(relx=0.04, rely=0.7, relheight=0.1, relwidth=0.45)

        gray_button = tk.Button(filter_frame, bg='#DADBDC', text="Gray out",
                                command=lambda: self.grayout(input_file_entry.get(),
                                                             annot_file_entry.get(), self.var_interaction_or_edge,
                                                             filter_entry.get("1.0", tkinter.END),
                                                             self.var_invert_or_not))
        gray_button.place(relx=0.525, rely=0.7, relheight=0.1, relwidth=0.45)

        reset_button = tk.Button(filter_frame, bg='#DADBDC', text="Reset",
                                 command=lambda: self.reset(input_file_entry.get(),
                                                            annot_file_entry.get(), self.var_interaction_or_edge))
        reset_button.place(relx=0.3, rely=0.85, relheight=0.1, relwidth=0.45)

        help_button = tk.Button(filter_frame, bg='#DADBDC', text="Help",
                                command=lambda: self.help())
        help_button.place(relx=0.775, rely=0.85, relheight=0.1, relwidth=0.2)

        submit_button = tk.Button(root, text="Done", bg='#f0f0f0', command=lambda root=root: self.quit(root))
        submit_button.place(relx=0.3, rely=0.9, relheight=0.075, relwidth=0.35)

        root.mainloop()

    # Helper methods to update Cytoscape upon the press of buttons in the GUI
    def hide(self, input_file, annotation_file, interaction_or_edge, filter_entry, var_invert_or_not):
        self.hide_bool = True
        form_details_df = pd.DataFrame(
            [[input_file, annotation_file, self.output_file_path, self.hide_bool, filter_entry, var_invert_or_not]],
            columns=['input_file', 'annotation_file', 'output_file', 'hide', 'query', 'invert'])
        print('_______________________*^!@#_____________', filter_entry)
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def show(self, input_file, annotation_file, interaction_or_edge, filter_entry, var_invert_or_not):
        self.show_bool = True
        form_details_df = pd.DataFrame(
            [[input_file, annotation_file, self.output_file_path, self.show_bool, filter_entry, var_invert_or_not]],
            columns=['input_file', 'annotation_file', 'output_file', 'show', 'query', 'invert'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def highlight(self, input_file, annotation_file, interaction_or_edge, filter_entry, var_invert_or_not):
        self.highlight_bool = True
        form_details_df = pd.DataFrame(
            [[input_file, annotation_file, self.output_file_path, self.highlight_bool, filter_entry,
              var_invert_or_not]],
            columns=['input_file', 'annotation_file', 'output_file', 'highlight', 'query', 'invert'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def grayout(self, input_file, annotation_file, interaction_or_edge, filter_entry, var_invert_or_not):
        self.gray_bool = True
        form_details_df = pd.DataFrame(
            [[input_file, annotation_file, self.output_file_path, self.gray_bool, filter_entry, var_invert_or_not]],
            columns=['input_file', 'annotation_file', 'output_file', 'gray', 'query', 'invert'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def reset(self, input_file, annotation_file, interaction_or_edge):
        self.reset_bool = True
        form_details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, self.reset_bool]],
                                       columns=['input_file', 'annotation_file', 'output_file', 'reset'])
        self.controller.perform_core_functionality(form_details_df, False, interaction_or_edge)

    def help(self):
        messagebox.showinfo('Info', 'If you want to go to our wiki click ok!')
        webbrowser.open_new('https://github.com/aehrc/EpiExplorer/blob/master/README.md')
        pass

    def quit(self, root):
        root.quit()

    def node_colour(self, node_colour, input_file, annotation_file, interaction_or_edge):
        form_details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, node_colour]],
                                       columns=['input_file', 'annotation_file', 'output_file', 'node_colour'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def node_size(self, node_size, input_file, annotation_file, interaction_or_edge):
        form_details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, node_size]],
                                       columns=['input_file', 'annotation_file', 'output_file', 'node_size'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def node_shape(self, node_shape, input_file, annotation_file, interaction_or_edge):
        form_details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, node_shape]],
                                       columns=['input_file', 'annotation_file', 'output_file', 'node_shape'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def edge_colour(self, edge_colour, input_file, annotation_file, interaction_or_edge):
        form_details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, edge_colour]],
                                       columns=['input_file', 'annotation_file', 'output_file', 'edge_colour'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)

    def edge_thickness(self, edge_thickness, input_file, annotation_file, interaction_or_edge):
        form_details_df = pd.DataFrame([[input_file, annotation_file, self.output_file_path, edge_thickness]],
                                       columns=['input_file', 'annotation_file', 'output_file', 'edge_thickness'])
        self.controller.perform_core_functionality(form_details_df, True, interaction_or_edge)
