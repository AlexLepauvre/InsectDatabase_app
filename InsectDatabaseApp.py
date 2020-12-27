import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd
import sqlite3
import os
from PIL import ImageTk, Image
import numpy as np

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)


def popupmsg(message):
    """This function opens a small window displaying info"""

    # Create a window
    popup = tk.Tk()

    # Define function to exit window:
    def leavemini():
        popup.destroy()

    # Set window title:
    popup.wm_title("!")

    # Set label:
    label = ttk.Label(popup, text=message, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)

    # Set button
    B1 = ttk.Button(popup, text="Ok", command=leavemini)
    B1.pack()

    # Initiate callback loop
    popup.mainloop()


class InsectDataBaseApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Initialize tkinter:
        tk.Tk.__init__(self, *args, **kwargs)

        # Setting title and icon:
        tk.Tk.wm_title(self, "Insect database app")
        tk.Tk.iconbitmap(self, default="insect.ico")
        # Create container to populate:
        container = tk.Frame(self)

        # Packing the container:
        container.pack(side="top", fill="both", expand=True)

        # Basic configuration for the grids
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

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

        for F in (StartPage, CreateDataBasePage, ExpandDataBasePage, LoadDataBasePage, ExploreDataBase):
            # Initialize page:
            frame = F(container, self)
            # Add it to the frames dictionary:
            self.frames[F] = frame
            # Set grid parameters:
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the start page with show_frame method
        self.show_frame(StartPage)

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

    def load_data_base(self):
        # Selecting the database to load with browser
        self.database_file = filedialog.askopenfilename()

        # Creating the name of the table in the database:
        self.sql_table_name = "Collection"

        self.conn = sqlite3.connect(self.database_file)
        self.c = self.conn.cursor()

        # Creating the query:
        query = 'SELECT * FROM {}'.format(self.sql_table_name)

        # Executing query to get all the column names
        self.c.execute(query)

        # Listing the column names:
        self.database_column = [description[0] for description in self.c.description]

    def create_data_base(self):
        # Selecting the database to load with browser
        excel_file = filedialog.askopenfilename()

        # Loading the excel file
        excel_dataframe = pd.read_excel(excel_file, engine='openpyxl')

        # Converting all the strings to lower case to avoid non-consistency issues:
        for column in excel_dataframe:
            # Try and except statement in case of format issues:
            try:
                excel_dataframe[column] = excel_dataframe[column].str.lower()
            except:
                print("This column cannot be converted to lower case")

        # Creating the name of the data base:
        self.database_file = os.path.splitext(excel_file)[0] + ".db"

        # Creating the name of the table in the database:
        self.sql_table_name = "Collection"

        # Create connection to memory:
        cnx = sqlite3.connect(self.database_file)

        # Storing the excel file as a database:
        excel_dataframe.to_sql(name=self.sql_table_name, con=cnx)

        # Connecting to the database:
        self.conn = sqlite3.connect(self.database_file)
        self.c = self.conn.cursor()

        # Creating the query:
        query = 'SELECT * FROM {}'.format(self.sql_table_name)

        # Executing query to get all the column names
        self.c.execute(query)

        # Fetch all:
        self.database_column = [description[0] for description in self.c.description]

    def fetch_unique(self):
        """
        This function fetches the unique columns:
        :return:
        """

        # Creating the query of the table name:
        query = 'SELECT * FROM {}'.format(self.sql_table_name)

        # Connecting to the
        cursor = self.c.execute(query)

        # Listing all the columns:
        column_names = [description[0] for description in cursor.description]

        #
        unique = {}

        for columns in column_names:
            if columns == 'index':
                continue
            else:
                query = 'SELECT DISTINCT {} FROM {}'.format(columns, self.sql_table_name)
                cursor = self.c.execute(query)
                unique[columns] = cursor.fetchall()

        print(unique)


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
        load_database_button = ttk.Button(self, text="Load existing database",
                                          command=lambda: controller.show_frame(LoadDataBasePage))
        expand_database_button = ttk.Button(self, text="Expand database",
                                            command=lambda: controller.show_frame(ExpandDataBasePage))
        create_database_button.grid(row=1, column=0)
        load_database_button.grid(row=2, column=0)
        expand_database_button.grid(row=3, column=0)

        # Adding background image:
        image = Image.open('insect_bg.png')
        photo = ImageTk.PhotoImage(image.resize((600, 500), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.grid(row=0, column=1, rowspan=4)


class CreateDataBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Setting start page label:
        label = ttk.Label(self, text="Create database", font=LARGE_FONT)
        label.grid(row=0, column=0)

        # Creating the buttons:
        back_to_start_page_button = ttk.Button(self, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        create_data_base_page_button = ttk.Button(self, text="Create database from excel",
                                                  command=lambda: controller.create_data_base())
        explore_data_base_page_button = ttk.Button(self, text="Back to start page",
                                                   command=lambda: controller.update_frame(ExploreDataBase))

        back_to_start_page_button.grid(row=1, column=0)
        create_data_base_page_button.grid(row=2, column=0)
        explore_data_base_page_button.grid(row=3, column=0)

        # Adding background image:
        image = Image.open('insect_bg.png')
        photo = ImageTk.PhotoImage(image.resize((600, 500), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.grid(row=0, column=1, rowspan=4)


class LoadDataBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Setting start page label:
        label = ttk.Label(self, text="Create database", font=LARGE_FONT)
        label.grid(row=0, column=0)

        back_to_start_page_button = ttk.Button(self, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        select_data_base_button = ttk.Button(self, text="Select data base",
                                             command=lambda: controller.load_data_base())
        explore_data_base_page_button = ttk.Button(self, text="Explore database",
                                                   command=lambda: controller.show_frame(ExploreDataBase))

        back_to_start_page_button.grid(row=1, column=0)
        select_data_base_button.grid(row=2, column=0)
        explore_data_base_page_button.grid(row=3, column=0)

        # Adding background image:
        image = Image.open('insect_bg.png')
        photo = ImageTk.PhotoImage(image.resize((600, 500), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.grid(row=0, column=1, rowspan=4)


class ExpandDataBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Setting start page label:
        label = ttk.Label(self, text="Create database", font=LARGE_FONT)
        label.grid(row=0, column=0)

        back_to_start_page_button = ttk.Button(self, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        explore_data_base_page_button = ttk.Button(self, text="Back to start page",
                                                   command=lambda: controller.show_frame(ExploreDataBase))

        back_to_start_page_button.grid(row=1, column=0)
        explore_data_base_page_button.grid(row=2, column=0)

        # Adding background image:
        image = Image.open('insect_bg.png')
        photo = ImageTk.PhotoImage(image.resize((600, 500), Image.ANTIALIAS))
        label = tk.Label(self, image=photo)
        label.image = photo
        label.grid(row=0, column=1, rowspan=4)


class ExploreDataBase(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.bind("<<ShowFrame>>", self.on_show_frame)

        # Declaring the selection variable:
        self.selection = {}

        ################################################################################################################
        # Treeview Widget from https://gist.github.com/RamonWill/0686bd8c793e2e755761a8f20a42c762
        # Setting the widget for the database view:

        # Frame for TreeView
        frame1 = tk.LabelFrame(self, text="Excel Data")
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
        # Setting labels and buttons:
        label = ttk.Label(self, text="Exploring the database", font=LARGE_FONT)

        # Creating the buttons:
        back_to_start_page_button = ttk.Button(self, text="Back to start page",
                                               command=lambda: controller.show_frame(StartPage))
        unique_value_button = ttk.Button(self, text="Print unique",
                                         command=lambda: controller.fetch_unique())
        data_value_button = ttk.Button(self, text="Show table",
                                       command=lambda: self.show_selection(controller))

        ################################################################################################################
        # Creating the drop down menus frame:
        drop_down_frame = tk.LabelFrame(self, text="Options")
        drop_down_frame.place(relheight=0.7, relwidth=0.38, relx=0.01, rely=0.25)

        # Putting things on the page:
        label.place(rely=0, relx=0)
        back_to_start_page_button.place(rely=0.9, relx=0.02)
        unique_value_button.place(rely=0.05, relx=0.02)
        data_value_button.place(rely=0.1, relx=0.02)

    def on_show_frame(self, event):

        """
        This methods presents the different options to search through the database, based on the different columns
        numbers
        :param event:
        :return:
        """

        df = event.widget.master.master.database_column
        # Loading all the headers and so on from the table:
        columns_list = list(df.columns)

        # Position defaults:
        x = 0.1
        y = 0.28

        # Looping through all the headers to show them all as well as the options:
        for headers in columns_list:
            # Listing the different options from that list:
            drop_down_options = df[headers].unique()
            # TODO: Make that nicer, try except isn't the way to go here
            # Adding the option None in case the user doesn't want to select anything:
            try:
                drop_down_options = np.insert(drop_down_options, 0, "None", axis=0)

            except:
                try:
                    drop_down_options = np.insert(drop_down_options, 0, 0, axis=0)

                except:
                    print("The data format wasn't recognized")

            # Creating a stringvar for the value selected in the drop down menu:
            self.selection[headers] = tk.StringVar(self)
            self.selection[headers].set(drop_down_options[0])  # default value
            # Setting the label of the drop down menu:
            label = ttk.Label(self, text=headers, font=NORM_FONT)

            species_menu = ttk.OptionMenu(self, self.selection[headers], *drop_down_options)
            species_menu.place(relx=x, rely=y)
            label.place(relx=x - 0.075, rely=y)
            y = y + 0.05

            if y > 0.9:
                x = 0.25
                y = 0.28

    # Setting function to display the data base:
    def show_selection(self, controller):

        # First clearing the tree view from previous searches:
        self.table_frame.delete(*self.table_frame.get_children())

        # Initiating the query parameter:
        query_param = ""

        # Fetching all the retrieved values from the drop down menu to create the query:
        for entries in self.selection:
            # Not taking into account the options that weren't selected:
            if not self.selection[entries].get() == "None":
                if not self.selection[entries].get() == '0.0':
                    if not self.selection[entries].get() == '0':
                        # If there was already an option added, adding AND in between the two queries
                        if len(query_param) != 0:
                            query_param += 'AND '

                        # Expanding the query based on the selected options
                        query_param += entries
                        query_param += '='
                        query_param += "'"
                        query_param += self.selection[entries].get()
                        query_param += "'"
                        query_param += " "

        # Creating the query based on the retrieved values:
        query = 'SELECT * FROM {} WHERE {}'.format(controller.sql_table_name, query_param)

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


# Starting the app
app = InsectDataBaseApp()
# Setting the size:
app.geometry('800x500')
# initializing input loop:
app.mainloop()
