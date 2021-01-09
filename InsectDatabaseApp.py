import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import sqlite3
import os
from PIL import ImageTk, Image

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

def quit():
    quit()


def popupmsg(message):
    """This function opens a small window displaying info"""

    # Create a window
    popup = tk.Tk()

    # Set window title:
    popup.wm_title("!")

    # Set label:
    label = ttk.Label(popup, text=message, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    # Set button
    B1 = ttk.Button(popup, text="Ok", command=popup.destroy)
    B1.pack()

    # Initiate callback loop
    popup.mainloop()


class InsectDataBaseApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Initialize tkinter:
        tk.Tk.__init__(self, *args, **kwargs)

        # ----------------------------------------------------------
        # Position information:
        self.navigation_coordinates = [0.02, 0.7]
        self.navigation_size = [0.25, 0.25]
        self.current_options_coordinates = [0.02, 0.02]
        self.current_options_size = [0.4, 0.25]

        # Setting title and icon:
        tk.Tk.wm_title(self, "Insect database app")
        tk.Tk.iconbitmap(self, default="insect_logo.ico")
        self.geometry('1000x600')
        # Create container to populate:
        container = tk.Frame(self)

        # Packing the container:
        container.pack(side="top", fill="both", expand=True)

        # Basic configuration for the grids
        container.grid_rowconfigure(0, weight=1, pad=100)
        container.grid_columnconfigure(0, weight=1, pad=100)

        # Setting the menu bar
        menu_bar = tk.Menu(container)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        file_menu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet!"))
        menu_bar.add_cascade(label="File", menu=file_menu)

        tk.Tk.config(self, menu=menu_bar)

        # Initialize frames dictionary:
        self.frames = {}

        # Pre allocating:
        self.database_column = []

        for F in (StartPage, CreateDataBasePage, ExpandDataBasePage, ExploreDataBase, UpdateInsect):
            # Initialize page:
            frame = F(container, self)
            # Add it to the frames dictionary:
            self.frames[F] = frame
            # Set grid parameters:
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page with show_frame method
        self.show_frame(StartPage)

        # Connecting to the database:
        self.connect_data_base()

    def show_frame(self, cont):
        """
        This method just brings whatever page we want to the front, i.e. shows it
        :param cont: controls which frame to show
        :return:
        """
        # Select the frame to raise
        frame = self.frames[cont]
        # Raise that frame:
        frame.tkraise()

        # Creating the event for other processes:
        frame.event_generate("<<ShowFrame>>")

    def connect_data_base(self):
        """
        This function connects to the database if it exists:
        :return:
        """

        # Listing the files in directory and checking whether there are databases:
        databases_list = []
        for file in os.listdir("."):
            if file.endswith(".db"):
                databases_list.append(file)

        # Checking whether there is a data base:
        if len(databases_list) == 0:  # If there is no existing database, the user must select a file to create one:
            tk.messagebox.showwarning(title=None, message="There is no existing data base, please create one!")
            self.show_frame(CreateDataBasePage)
        elif len(databases_list) == 1:
            self.database_file = databases_list[0]
            # Creating the name of the table in the database:
            self.sql_table_name = "Insects"

            self.conn = sqlite3.connect(self.database_file)
            self.c = self.conn.cursor()

            # Creating the query:
            query = 'SELECT * FROM {}'.format(self.sql_table_name)

            # Executing query to get all the column names
            self.c.execute(query)

            # Listing the column names:
            self.database_column = [description[0] for description in self.c.description]
        elif len(databases_list) > 1:

            # Informing user that there is more than one database:
            tk.messagebox.showwarning(title=None, message="There is more than 1 database existing, please select one!")

            # Selecting the database to load with browser
            self.database_file = filedialog.askopenfilename()

            # Creating the name of the table in the database:
            self.sql_table_name = "Insects"

            self.conn = sqlite3.connect(self.database_file)
            self.c = self.conn.cursor()

            # Creating the query:
            query = 'SELECT * FROM {}'.format(self.sql_table_name)

            # Executing query to get all the column names
            self.c.execute(query)

            # Listing the column names:
            self.database_column = [description[0] for description in self.c.description]

    def create_data_base_from_excel(self, frame):
        # Checking that a name was selected:
        if len(frame.database_name_entry.get()) == 0:
            tk.messagebox.showerror(title=None,
                                    message="No table name entered! Please type in a table name!")
            return

        tk.messagebox.showinfo(title=None,
                               message='When creating a database from an excel file, please make sure that the reference column is titled "Ref" as later function depend on it!')

        # Selecting the database to load with browser
        excel_file = filedialog.askopenfilename()

        correct_format = 0
        # Looping until the correct file format is selected:
        while correct_format != 1:
            # Checking if the file format is corrects
            if excel_file.endswith(".xls") or excel_file.endswith(".xlsx") \
                    or not excel_file.endswith(".xlsm") or excel_file.endswith(".xlsb") \
                    or excel_file.endswith(".odf") or excel_file.endswith(".pdt") \
                    or excel_file.endswith(".csv"):
                # If the format is correct, while loop can be terminated:
                correct_format = 1
            else:
                # Showing a warning box and asking the user to select a new one:
                tk.messagebox.showwarning(title=None,
                                          message="This file format isn't accepted, please selected another file!")
                excel_file = filedialog.askopenfilename()

        # Loading the excel file
        if excel_file.endswith(".csv"):
            excel_dataframe = pd.read_csv(excel_file, sep=',')
        else:
            excel_dataframe = pd.read_excel(excel_file, engine='openpyxl', sheet_name=None)

        # Converting all the strings to lower case to avoid non-consistency issues:
        for column in excel_dataframe:
            # Try and except statement in case of format issues:
            try:
                excel_dataframe[column] = excel_dataframe[column].str.lower()
            except:
                print("This column cannot be converted to lower case")

        # Removing the spaces in the column names by underscores:
        excel_dataframe.columns = excel_dataframe.columns.str.replace(' ', '_')
        # Replacing all the potential weird characters in column names by underscores:
        excel_dataframe.columns = excel_dataframe.columns.str.replace('.', '_')
        excel_dataframe.columns = excel_dataframe.columns.str.replace(':', '_')
        excel_dataframe.columns = excel_dataframe.columns.str.replace('-', '_')
        excel_dataframe.columns = excel_dataframe.columns.str.replace('&', 'AND')

        # Creating the name of the data base:
        self.database_file = frame.database_name_entry.get() + ".db"

        # Creating the name of the table in the database:
        self.sql_table_name = "Insects"

        # Create connection to the created database:
        cnx = sqlite3.connect(self.database_file)

        # Setting progress bar:
        progress = ttk.Progressbar(frame.current_options_frame, length=100, mode='determinate')
        progress.grid(row=4, column=0)
        try:
            import time
            progress['value'] = 20
            frame.update_idletasks()
            time.sleep(0.2)
            # Converting the excel file to sql
            excel_dataframe.to_sql(name=self.sql_table_name, con=cnx, index=False)
            progress['value'] = 40
            frame.update_idletasks()
            time.sleep(0.2)
            progress['value'] = 60
            frame.update_idletasks()
            time.sleep(0.2)
            progress['value'] = 80
            frame.update_idletasks()
            time.sleep(0.2)
            progress['value'] = 100
            frame.update_idletasks()
            time.sleep(0.2)
            complete = ttk.Label(frame.current_options_frame, text='Complete!', font=LARGE_FONT)
            complete.grid(row=5, column=0)
        except:
            tk.messagebox.showerror(title=None,
                                    message="Failure! The database wasn't sucessfully created!")

        # Connecting to the database:
        self.conn = sqlite3.connect(self.database_file)
        self.c = self.conn.cursor()

        # Creating the query:
        query = 'SELECT * FROM {}'.format(self.sql_table_name)

        # Executing query to get all the column names
        self.c.execute(query)

        # Fetch all:
        self.database_column = [description[0] for description in self.c.description]

    def expand_data_base_from_excel(self, frame):
        # Selecting the database to load with browser
        excel_file = filedialog.askopenfilename()

        # Loading the excel file
        if excel_file.endswith(".csv"):
            excel_dataframe = pd.read_csv(excel_file, sep=',')
        else:
            excel_dataframe = pd.read_excel(excel_file, engine='openpyxl')

        # Converting all the strings to lower case to avoid non-consistency issues:
        for column in excel_dataframe:
            # Try and except statement in case of format issues:
            try:
                excel_dataframe[column] = excel_dataframe[column].str.lower()
            except:
                print("This column cannot be converted to lower case")

        # Removing the spaces in the column names by underscores:
        excel_dataframe.columns = excel_dataframe.columns.str.replace(' ', '_')
        # Replacing all the potential weird characters in column names by underscores:
        excel_dataframe.columns = excel_dataframe.columns.str.replace('.', '_')
        excel_dataframe.columns = excel_dataframe.columns.str.replace(':', '_')
        excel_dataframe.columns = excel_dataframe.columns.str.replace('-', '_')
        excel_dataframe.columns = excel_dataframe.columns.str.replace('&', 'AND')

        # Making sure that the column match:
        # First making sure there are the same number of entries

        if len(excel_dataframe.columns) == len(self.database_column):
            # Sorting the columns to make sure they are comparable:
            orderedExcelCol = list(excel_dataframe.columns)
            orderedDBHeaders = list(self.database_column)
            orderedExcelCol.sort()
            orderedDBHeaders.sort()
            ctr = 0
            for columns in orderedExcelCol:
                if columns != orderedDBHeaders[ctr]:
                    tk.messagebox.showerror(title=None,
                                            message="The column names in your table differs from he database. \nThese data cannot be appended!!")
                else:
                    ctr = ctr + 1
            # Setting the question marks for the query:
            q_marks = ""
            for i in range(len(self.database_column)):
                q_marks += "?"
                if i < (len(self.database_column)) - 1:
                    q_marks += ","

            # Creating the query:
            query = 'INSERT OR REPLACE INTO {} ({}) VALUES({})'.format(self.sql_table_name,
                                                                       ", ".join(self.database_column),
                                                                       q_marks)
            progress = ttk.Progressbar(frame.current_options_frame, length=100, mode='determinate')
            progress.grid(row=4, column=0)
            try:
                # Storing the excel file as a database:
                # The progress bar doesn't reflect anything, it just looks nice hehe
                import time
                self.conn.executemany(query, excel_dataframe.to_records(index=False))
                self.conn.commit()
                progress['value'] = 20
                frame.update_idletasks()
                time.sleep(0.2)
                progress['value'] = 40
                frame.update_idletasks()
                time.sleep(0.2)
                progress['value'] = 60
                frame.update_idletasks()
                time.sleep(0.2)
                progress['value'] = 80
                frame.update_idletasks()
                time.sleep(0.2)
                progress['value'] = 100
                frame.update_idletasks()
                time.sleep(0.2)
                complete = ttk.Label(frame.current_options_frame, text='Complete!', font=LARGE_FONT)
                complete.grid(row=5, column=0)
            except:
                tk.messagebox.showerror(title=None,
                                        message="The given entries couldn't be appended. Check format!")
        else:
            tk.messagebox.showerror(title=None,
                                    message="The number of columns of the table differ from the one in the database. \n These data cannot be appended!!")

    def create_data_base_manually(self, frame):
        # Checking that a name was selected:
        if len(frame.database_name_entry.get()) == 0:
            tk.messagebox.showerror(title=None,
                                    message="No table name entered! Please type in a table name!")
            return

        self.sql_table_name = "Insects"

        # Setting the connection:
        self.database_file = frame.database_name_entry.get() + ".db"
        self.conn = sqlite3.connect(self.database_file)
        self.c = self.conn.cursor()

        # Creating the database:
        self.c.execute("CREATE TABLE IF NOT EXISTS Insects(Ref TEXT UNIQUE, Ordre TEXT, G_Famille TEXT, Famille TEXT, "
                       "Genre TEXT, Sous_genre TEXT, Espece TEXT, Sous_espece TEXT, Male TEXT, Female TEXT, "
                       "Date TEXT, Capture_location TEXT, Region TEXT, Pays TEXT, Continent TEXT, Leg TEXT, "
                       "Auteur TEXT, Rangement TEXT, Boite TEXT)")

        data = []
        # Getting all the entered values:
        for entry in frame.entries:
            data.append(frame.entries[entry].get())

        # Adding the value to the database:
        self.c.execute("INSERT INTO Insects VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data)

        # Commiting the values to the database:
        self.conn.commit()

        # Getting the column names from the database directly
        # Creating the query:
        query = 'SELECT * FROM {}'.format(self.sql_table_name)

        # Executing query to get all the column names
        self.c.execute(query)

        # Listing the column names:
        self.database_column = [description[0] for description in self.c.description]

    def add_insect(self, frame):

        data = []
        query = 'INSERT INTO Insects VALUES('
        ctr = 0
        # Getting all the entered values:
        for entry in frame.entries:
            data.append(frame.entries[entry].get())
            query += '?'
            if ctr == len(frame.entries) - 1:
                query += ')'
            else:
                query += ','
                ctr = ctr + 1

        try:
            # Adding the value to the database:
            self.c.execute(query, data)
            # Commit the values to the database:
            self.conn.commit()
        except:
            tk.messagebox.showerror(title=None, message="Duplicates! An insect with this reference already exists!"
                                    "Please visit the page update database to edit exisiting entries")


class StartPage(tk.Frame):
    """
    First page presented when booting the app
    """

    # Initializing the start page classe
    def __init__(self, parent, controller):
        # Initializing tkinter:
        tk.Frame.__init__(self, parent)

        # Setting start page label:
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.grid(row=0, column=0)

        # Creating the buttons:
        create_database_button = ttk.Button(self, text="Create new database",
                                            command=lambda: controller.show_frame(CreateDataBasePage))
        load_database_button = ttk.Button(self, text="Explore database",
                                          command=lambda: controller.show_frame(ExploreDataBase))
        expand_database_button = ttk.Button(self, text="Expand database",
                                            command=lambda: controller.show_frame(ExpandDataBasePage))
        update_database_button = ttk.Button(self, text="Update database",
                                            command=lambda: controller.show_frame(UpdateInsect))
        create_database_button.place(rely=0.1, relx=0.02)
        load_database_button.place(rely=0.2, relx=0.02)
        expand_database_button.place(rely=0.3, relx=0.02)
        update_database_button.place(rely=0.4, relx=0.02)

        # Adding background image:
        image = Image.open('insect_bg.png')
        photo = ImageTk.PhotoImage(image.resize((600, 500), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(rely=0.05, relx=0.2, relheight=0.9, relwidth=0.75)


class CreateDataBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # In order to be able to edit the entry widgets, need to set focus on the window:
        self.bind("<<ShowFrame>>", self.force_focus)

        # Setting the page standard frames:
        navigation_frame = tk.LabelFrame(self, text="Navigation")
        navigation_frame.place(relheight=controller.navigation_size[0], relwidth=controller.navigation_size[1],
                               relx=controller.navigation_coordinates[0], rely=controller.navigation_coordinates[1])
        self.current_options_frame = tk.Frame(self)
        self.current_options_frame.place(relheight=controller.current_options_size[0],
                                    relwidth=controller.current_options_size[1],
                                    relx=controller.current_options_coordinates[0],
                                    rely=controller.current_options_coordinates[1])

        self.entries = {}
        # Setting start page label:
        label = ttk.Label(self.current_options_frame, text="Create database", font=NORM_FONT)
        label.grid(row=0, column=0, pady=20)

        # Creating the buttons:
        back_to_start_page_button = ttk.Button(navigation_frame, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        explore_database_button = ttk.Button(navigation_frame, text="Explore database",
                                             command=lambda: controller.show_frame(ExploreDataBase))
        create_data_base_page_button = ttk.Button(self.current_options_frame, text="Create database from excel",
                                                  command=lambda: controller.create_data_base_from_excel(self))
        save_to_database_button = ttk.Button(self, text="Add insect",
                                             command=lambda: controller.create_data_base_manually(self))

        # Setting an entry for the user to specify the name of the data base:
        self.database_name_entry = ttk.Entry(self.current_options_frame)
        database_name_label = ttk.Label(self.current_options_frame, text="Database_name:", font=NORM_FONT)

        # Placing the buttons:
        back_to_start_page_button.grid(row=0, column=0)
        explore_database_button.grid(row=1, column=0)

        database_name_label.grid(row=1, column=0)
        self.database_name_entry.grid(row=2, column=0, pady=10)
        create_data_base_page_button.grid(row=3, column=0)

        # --------------------------------------------------------------------------------------------------------------
        # Adding the options to create a database from scratch:
        database_param_frame = tk.LabelFrame(self, text="Manual database creation:")
        database_param_frame.place(relheight=0.75, relwidth=0.7, relx=0.28, rely=0.1)
        save_to_database_button.place(rely=0.85, relx=0.5, relwidth=0.2)

        # Adding all the options in the frame:
        # Setting the different entries:
        db_entries = ['Ref', 'Order', 'G_Famille', 'Famille', 'Genre', 'Sous_genre', 'Espece', 'Sous_espece', 'Male',
                      'Female', 'Date', 'Capture_location', 'Region', 'Pays', 'Continent', 'Leg', 'Auteur', 'Rangement',
                      'Boite']

        # Setting the initial position:
        x = 0
        y = 0

        # Creating one text box per entry of the database:
        for entry in db_entries:
            var = tk.StringVar(value=entry)
            label = ttk.Label(database_param_frame, text=entry + ": ", font=SMALL_FONT)
            self.entries[entry] = tk.Entry(database_param_frame, textvariable=var)
            label.grid(row=y, column=x, pady=10)
            self.entries[entry].grid(row=y, column=x + 1, pady=10)
            # If x is superior to 5, we have three entries so we go to the next row
            if x > 3:
                x = 0
                y = y + 1
            else:
                x = x + 2

    def force_focus(self, event):
        self.focus_force()


class ExpandDataBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.bind("<<ShowFrame>>", self.display_entries)

        # Setting the page standard frames:
        navigation_frame = tk.LabelFrame(self, text="Navigation")
        navigation_frame.place(relheight=controller.navigation_size[0], relwidth=controller.navigation_size[1],
                               relx=controller.navigation_coordinates[0], rely=controller.navigation_coordinates[1])
        self.current_options_frame = tk.Frame(self)
        self.current_options_frame.place(relheight=controller.current_options_size[0],
                                    relwidth=controller.current_options_size[1],
                                    relx=controller.current_options_coordinates[0],
                                    rely=controller.current_options_coordinates[1])

        self.entries = {}

        # Setting start page label:
        label = ttk.Label(self.current_options_frame, text="Expand database", font=LARGE_FONT)
        label.grid(row=0, column=0, pady=20)

        back_to_start_page_button = ttk.Button(navigation_frame, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        explore_data_base_page_button = ttk.Button(navigation_frame, text="Explore database",
                                                   command=lambda: controller.show_frame(ExploreDataBase))

        expand_from_excel_button = ttk.Button(self.current_options_frame, text="Expand from excel",
                                              command=lambda: controller.expand_data_base_from_excel(self))
        save_to_database_button = ttk.Button(self, text="Add insect",
                                             command=lambda: controller.add_insect(self))
        back_to_start_page_button.grid(row=0, column=0)
        explore_data_base_page_button.grid(row=1, column=0)
        expand_from_excel_button.grid(row=1, column=0)

        # Adding the options to create a database from scratch:
        self.database_param_frame = tk.LabelFrame(self, text="Manual database creation:")
        self.database_param_frame.place(relheight=0.85, relwidth=0.7, relx=0.28, rely=0.1)
        save_to_database_button.place(relx=0.6, rely=0.95)

    def display_entries(self, event):
        self.focus_force()

        db_entries = event.widget.master.master.database_column

        # Setting the initial position:
        x = 0
        y = 0

        # Creating one text box per entry of the database:
        for entry in db_entries:
            var = tk.StringVar(value=entry)
            label = ttk.Label(self.database_param_frame, text=entry + ": ", font=SMALL_FONT)
            self.entries[entry] = tk.Entry(self.database_param_frame, textvariable=var)
            label.grid(row=y, column=x, pady=10)
            self.entries[entry].grid(row=y, column=x + 1, pady=10)

            # If x is superior to 5, we have three entries so we go to the next row
            if x > 3:
                x = 0
                y = y + 1
            else:
                x = x + 2


class ExploreDataBase(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.bind("<<ShowFrame>>", self.show_database_parameters)

        # Declaring the selection variable:
        self.selection = {}

        navigation_frame = tk.LabelFrame(self, text="Navigation")
        navigation_frame.place(relheight=controller.navigation_size[0], relwidth=controller.navigation_size[1],
                               relx=controller.navigation_coordinates[0], rely=controller.navigation_coordinates[1])
        current_options_frame = tk.Frame(self)
        current_options_frame.place(relheight=controller.current_options_size[0],
                                    relwidth=controller.current_options_size[1],
                                    relx=controller.current_options_coordinates[0],
                                    rely=controller.current_options_coordinates[1])

        ################################################################################################################
        # Setting labels and buttons:
        label = ttk.Label(current_options_frame, text="Exploring the database", font=LARGE_FONT)

        # Creating the buttons:
        back_to_start_page_button = ttk.Button(navigation_frame, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        update_button = ttk.Button(navigation_frame, text="Update data base",
                                   command=lambda: controller.show_frame(UpdateInsect))
        show_table_button = ttk.Button(self, text="Show Insect",
                                       command=lambda: self.show_selection(controller))

        # Putting things on the page:
        label.grid(row=0, column=0)
        back_to_start_page_button.grid(row=0, column=0)
        update_button.grid(row=1, column=0)

        ################################################################################################################
        # Treeview Widget from https://gist.github.com/RamonWill/0686bd8c793e2e755761a8f20a42c762
        # Setting the widget for the database view:

        # Frame for TreeView
        frame1 = tk.LabelFrame(self, text="Database selection")
        frame1.place(relheight=0.95, relwidth=0.6, relx=0.4)

        # Placing the frame:
        self.table_frame = ttk.Treeview(frame1)
        self.table_frame.place(relheight=1,
                               relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        # Setting the scrollbars:
        tree_scroll_y = tk.Scrollbar(frame1, orient="vertical",
                                     command=self.table_frame.yview)  # command means update the yaxis view of the widget
        tree_scroll_x = tk.Scrollbar(frame1, orient="horizontal",
                                     command=self.table_frame.xview)  # command means update the xaxis view of the widget
        self.table_frame.configure(xscrollcommand=tree_scroll_x.set,
                                   yscrollcommand=tree_scroll_y.set)  # assign the scrollbars to the Treeview Widget
        # Packing the scroll bars into the frame:
        tree_scroll_x.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        tree_scroll_y.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        ################################################################################################################
        # Creating the drop down menus frame:
        self.drop_down_frame = tk.LabelFrame(self, text="Options")
        self.drop_down_frame.place(relheight=0.6, relwidth=0.38, relx=0.01, rely=0.06)
        show_table_button.place(rely=0.66, relx=0.17)

    def show_database_parameters(self, event):

        """
        This methods presents the different options to search through the database, based on the different columns
        numbers
        :param event:
        :return:
        """

        columns_list = list(event.widget.master.master.database_column)

        # Position defaults:
        x = 0
        y = 0

        # Looping through all the headers to show them all as well as the options:
        for headers in columns_list:
            # With sql, searching via index works differently, and we don't need it anyway, so we skip it:
            if headers == 'index':
                continue
            else:
                # Creating a query to fetch unique values in the specific columns:
                query = 'SELECT DISTINCT {} FROM {}'.format(headers, event.widget.master.master.sql_table_name)
                print(query)
                # Executing the query:
                cursor = event.widget.master.master.c.execute(query)
                # Listing the different options from that list:
                drop_down_options = cursor.fetchall()
                # Queries on sql database retrieves list of tuples. Therefore, need to convert the unique values to list
                drop_down_options = [item for t in drop_down_options for item in t]

                # TODO: Make that nicer, try except isn't the way to go here
                # Adding the option None in case the user doesn't want to select anything:
                drop_down_options.insert(0, "_")

                # Creating a stringvar for the value selected in the drop down menu:
                self.selection[headers] = tk.StringVar(self)
                self.selection[headers].set(drop_down_options[0])  # default value
                # Setting the label of the drop down menu:
                label = ttk.Label(self.drop_down_frame, text=headers, font=NORM_FONT)

                species_menu = ttk.OptionMenu(self.drop_down_frame, self.selection[headers], *drop_down_options)
                label.grid(row=y, column=x, pady=10)
                species_menu.grid(row=y, column=x + 1, pady=10)

                # If x is superior to 5, we have three entries so we go to the next row
                if x > 3:
                    x = 0
                    y = y + 1
                else:
                    x = x + 2

    # Setting function to display the data base:
    def show_selection(self, controller):

        # First clearing the tree view from previous searches:
        self.table_frame.delete(*self.table_frame.get_children())

        # Initiating the query parameter:
        query_param = ''

        # Fetching all the retrieved values from the drop down menu to create the query:
        for entries in self.selection:
            # Not taking into account the options that weren't selected:
            if not self.selection[entries].get() == "_":
                # If there was already an option added, adding AND in between the two queries
                if len(query_param) != 0:
                    query_param += 'AND '
                if len(query_param) == 0:
                    query_param += 'WHERE '

                # Expanding the query based on the selected options
                query_param += entries
                query_param += '='
                query_param += '"'
                query_param += self.selection[entries].get()
                query_param += '" '

        # Creating the query based on the retrieved values:
        query = "SELECT * FROM {} {}".format(controller.sql_table_name, query_param)

        # Fetch the queried data:
        data = pd.read_sql_query(query, controller.conn)

        # Get the columns names:
        self.table_frame["column"] = list(data)

        # Set the name of the thing:
        self.table_frame["show"] = "headings"

        for column in self.table_frame["columns"]:
            self.table_frame.heading(column, text=column)  # let the column heading = column name

        # Looping through the data to plot to insert them in the frame:
        for row in data.to_numpy().tolist():
            self.table_frame.insert("", "end",
                                    values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        return None


class UpdateInsect(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.bind("<<ShowFrame>>", self.display_entries)

        # Dividing the screen in frames:
        # First frame is for the option to go back and so on:
        # Setting the page standard frames:
        navigation_frame = tk.LabelFrame(self, text="Navigation")
        navigation_frame.place(relheight=controller.navigation_size[0], relwidth=controller.navigation_size[1],
                               relx=controller.navigation_coordinates[0], rely=controller.navigation_coordinates[1])
        current_options_frame = tk.Frame(self)
        current_options_frame.place(relheight=controller.current_options_size[0],
                                    relwidth=controller.current_options_size[1],
                                    relx=controller.current_options_coordinates[0],
                                    rely=controller.current_options_coordinates[1])

        # Placing a title frame for the options:
        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.place(relheight=0.65, relwidth=0.68, relx=0.3, rely=0.3)

        # Declaring the selection variable:
        self.selection = {}

        label = ttk.Label(current_options_frame, text="Update database", font=LARGE_FONT)
        label.grid(row=0, column=0, pady=20)

        # Adding the buttons:
        # Navigation:
        back_to_start_page_button = ttk.Button(navigation_frame, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        back_to_previous_page_button = ttk.Button(navigation_frame, text="Back to explore page",
                                                  command=lambda: controller.show_frame(ExploreDataBase))

        # Page options
        show_selection = ttk.Button(current_options_frame, text="Show Insect",
                                    command=lambda: self.show_insect(controller))
        save_changes = ttk.Button(self, text="Save changes",
                                  command=lambda: self.save_changes(controller))
        self.selected_insect = ttk.Entry(current_options_frame)
        entry_label = ttk.Label(current_options_frame, text="Insect reference", font=SMALL_FONT)

        # Placing these things:
        back_to_start_page_button.grid(row=0, column=0)
        back_to_previous_page_button.grid(row=1, column=0)

        show_selection.grid(row=1, column=0)
        self.selected_insect.grid(row=2, column=1)
        entry_label.grid(row=2, column=0)

        ################################################################################################################
        # Treeview Widget from https://gist.github.com/RamonWill/0686bd8c793e2e755761a8f20a42c762
        # Setting the widget for the database view:

        # Frame for TreeView
        frame1 = tk.LabelFrame(self, text="Data base")
        frame1.place(relheight=0.2, relwidth=0.68, relx=0.3, rely=0.1)
        save_changes.place(relx=0.6, rely=0.9)

        # Placing the frame:
        self.table_frame = ttk.Treeview(frame1)
        self.table_frame.place(relheight=1,
                               relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        # Setting the scrollbars:
        tree_scroll_x = tk.Scrollbar(frame1, orient="horizontal",
                                     command=self.table_frame.xview)  # command means update the xaxi view of the widget
        self.table_frame.configure(xscrollcommand=tree_scroll_x.set)  # assign the scrollbars to the Treeview Widget
        # Packing the scroll bars into the frame:
        tree_scroll_x.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget

    def display_entries(self, event):
        self.focus_force()
        # Getting the column names:
        db_entries = event.widget.master.master.database_column

        # Setting the initial position:
        x = 0
        y = 0

        self.insect_entries = {}
        self.entries = {}
        # Creating one text box per entry of the database:
        for entry in db_entries:
            self.insect_entries[entry] = tk.StringVar(value=entry)
            label = ttk.Label(self.options_frame, text=entry + ": ", font=NORM_FONT)
            self.entries[entry] = tk.Entry(self.options_frame, textvariable=self.insect_entries[entry])
            label.grid(row=y, column=x, pady=10)
            self.entries[entry].grid(row=y, column=x + 1, pady=10)

            if x > 3:
                x = 0
                y = y + 1
            else:
                x = x + 2

    def show_insect(self, controller):

        # First clearing the tree view from previous searches:
        self.table_frame.delete(*self.table_frame.get_children())

        # Searching the given reference into the database:
        try:
            query = 'SELECT * FROM {} WHERE Ref="{}"'.format(controller.sql_table_name,
                                                             self.selected_insect.get())
            insect = pd.read_sql_query(query, controller.conn)
            if insect.empty:
                tk.messagebox.showerror(title=None,
                                        message="No insect ith this reference number found!")
                return
        except:
            tk.messagebox.showwarning(title=None,
                                      message="There is no column called ref in your table!")
            return

        # Get the columns names:
        self.table_frame["column"] = list(insect)

        # Set the name of the thing:
        self.table_frame["show"] = "headings"

        for column in self.table_frame["columns"]:
            self.table_frame.heading(column, text=column)  # let the column heading = column name

        # Looping through the data to plot to insert them in the frame:
        for row in insect.to_numpy().tolist():
            self.table_frame.insert("", "end",
                                    values=row)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

        # Filling the entries by the values of the selected insect:
        for entries in self.insect_entries:
            self.insect_entries[entries].set(insect[entries][0])
        return None

    def save_changes(self, controller):
        data = []
        query = 'UPDATE Insects SET '
        ctr = 0
        # Getting all the entered values:
        for entry in self.insect_entries:
            if entry != "Ref":
                data.append(self.insect_entries[entry].get())
                query += (entry + "=")
                query += '?'
                if ctr == len(self.insect_entries) - 1:
                    continue
                else:
                    query += ','
                    ctr = ctr + 1
            else:
                ctr = ctr + 1

        query += ' WHERE Ref= "{}"'.format(self.insect_entries['Ref'].get())

        # Adding the value to the database:
        try:
            controller.c.execute(query, data)
        except:
            tk.messagebox.showerror(title=None,
                                    message="The update didn't work, make sure the reference column is named Ref!")

        # Commit the values to the database:
        controller.conn.commit()


# Starting the app
app = InsectDataBaseApp()
# initializing input loop:
app.mainloop()
