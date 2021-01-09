<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/insect_logo.ico">
    <img src="https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/insect_logo.ico" alt="Logo" width="80" height="80">
  </a>

# InsectDatabase_app
This application main goal is to create standardized databases for insects collectioners, who would like to document and reference the specimens in their collection in an ordered and concise fashion. The information about each insects are maintained in a SQL data base, living in the home directory of the application. The user interface provide with functions enabling the searching and filtering of the data base in the search of specific specimens. The search options are derived from the SQLlite database itself, making the application flexible for different formats. 
![alt text](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/Instructions_screenshots/Start%20page.PNG)

# I. Installation guide
In order to install the application on your computer, you should download the windows installer found here [here](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/dist/Les%20Robetes-0.1-amd64.msi). You should then follow the instructions and note the path to where the app gets installed. I still haven't figured out how to make ask for a shortcut on desktop. So go to whereever you installed the app and click on the file called InsectDatabaseApp to start the app.

# II. How to use

## First use
When using the application for the first time, you will be prompted with the warning that you need to create a new database. The application automatically loads the database found in the home directory and if no database exists yet, one needs to be created for the application to boot properly. This will only be relevant the first time you boot the app. After that, any time you start the application, the database found in the app home directory will be connected to automatically and you don't ned to worry about it!
![alt text](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/Instructions_screenshots/First%20use.PNG)

## Initializing database:
![alt text](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/Instructions_screenshots/First%20database%20creation.PNG)
When clicking on okay, you will be sent to the database creation page. You should first name the database. The name has only little relevance if you only plan to create a single database (which will be the best use in most cases). Once you gave it a name, you have to decide whether you want to add an insect manually or create a database from excel. When creating the database manually, simply fill out the fields in the Manual database creation frame and hit add insect once you are done. The options presented are hard coded in the app as a template.  By doing so, you will initialize the database. You can also add additional insects manually on this page. Alternatively, you can select an existing excel file to instantiate your database. This is the option you will want to choose if you have existing records of your insects and don't want to have to reenter things manually. Note that whatever columns you have in your excel table will be translated into columns in your SQLlite database. It is important your initial excel files are "clean" meaning that each columns are named uniquely and that you don't have weird characters (though most of the ones I could think off should be handeled). Also, it is really important that in your excel table one column is titled "ref" and that within this column, you have unique identifier for each line, as the app relies on this for later functionalities (it will be prompted to you when hitting the create daabase from excel button):  

If you press the button create database from excel, the browser will open, letting you choose the excel file of your choice.

## Exploring the database page:
Either way, you will have initiated your database. You can then hit the button Explore database, leading you to the "Exploring the database" page:
![alt text](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/Instructions_screenshots/Exploring%20the%20database.PNG)
On this page, you will see the different fields of your database. For each column, you have a drop down menu, listing all the different options within each columns. You should therefore set one of the column to whatever option you are interested in, and then hit the button show insect, which will make the selection appear in a table on the right. You can iterate upon your selection, in other words, you can make a new search after the first one, to find whatever you are looking for.

There are a few things one needs to be mindful of here. First of all, just like in excel, if your database is huge and you select option that results in an riduculously big chunk of your database being loaded, you will run into memory problem. In this program, whatever you want to see in the table on the right needs to be loaded in RAM. If what you are trying to load exceeds the capacity of your computer, things will crash, or be super slow. So try and avoid making too big of selections. The other thing to note is that the drop down menus are not influencing each other. So say you set one of the "left most" column to a value, the options of the next columns available in the drop down will not change to display only what is possible depending on the column you just set. And if you happen to set the values in two columns such that the database doesn't exist, nothing will be displayed!

These are really the core functions of the application: you can create and navigate your database. But there are other additional options that are also quite handy. 

## Expanding an existing database page:
Once you have instantiated your database, you will surely want to expand on it, either directly after the creation or later in time, as you go. To do so, you should navigate to the start page. In there, you should hit the button Expand database:
![alt text](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/Instructions_screenshots/Expand%20databse.PNG)
This page looks just the same as the create database, without the naming of hte database. Again, you can either add an insect manually or by selecting an excel file. To add an insect manually, simply fill out the fields. This option is quite handy to add a new insect you just acquired. Note that ideally, for any entry you make here, you should minimally enter a reference under Ref, otherwise you will run into troubles down the line. But if you have missing info at the time you are adding an insect to the database, you can always get back to it once you have more info (provided you entered a reference number to find it back ;)). If you want to append an existing excel file, just hit on expand from Excel. Note that the excel file you are trying to append need to have the same number of columns and the same columns in the same order as your existing database, otherwise it won't work. 

## Updating the database page:
In many cases, you might want to modify things you already entered in order to add more information or correct a mistake and so on. This is also possible. To do so, you must navigate to the page Update database:
![alt text](https://github.com/AlexLepauvre/InsectDatabase_app/blob/main/Instructions_screenshots/Update%20database.PNG)

 On this page, you must first enter the reference of the insect you want to modify (if you don't know, make sure you navigate to the explore data base page). Once you entered something under Insect reference hit show insect to show the specific insect in the database window on the right. At the same time, it will fill out the options with the entries found in the database. You can then change whatever you like and hit Save changes. Note that this is where the difference between creating the datbase manually vs from excel comes into play. SQLite primary key has the particularity to allow for only unique identifier. What this means is that with the manually created database, you will be enforced to have unique references (i.e. the same reference cannot occur twice), while from excel, you could have twice the same reference. If you do have twice the same reference, this step here will be problematic: the command to change an existing insect will be ambiguous, the software won't be able to know what you want to change exactly and will therefore throw an error. So in short, if you create your database from excel, you must be actively on the look out for double identifier, but if you do the manual creation, it won' let you mess it up!

## Additional information:
One thing I didn't touch into is what happens when you create an additional database. The databse let's you create as many database as you would like. I would not recommend doing so except if you have a very good reason (if you really want to have a completely different database with different columns). If you do so, the app will have different database files in its directory. Therefore, when booting the app, it will ask you which database you would like to work with. 

# III. A little history of this application

I (Alex Lepauvre) created this application for a friend who has an extensive collection of insects but limited knowledge in informatic and softwares. While this particular friend heard of databases and thought it could be a very useful addition to his documentation method, it remained out of his reach due to the inherent complexity for non-inititated people. Insect collectioners, while not the most numerous hobbyist could benefit of such technology for their archiving purposes. Indeed, some of them have baffling collections of several tenth of thousands of individuals, and for each they keep detailed taxonomical information as well as information specific to the individual (location of capture, information about the identifier, author...). Most of these collectioner seem to rely on excel table, who present the shortcoming of not having the option to load only parts of the files in memory. The size of some collection requires the use of several excel files, rendering search across the entire collection very cumbersome. This application offers them the option of hosting the entire information of their collection in one single database, enabling easy and efficient search, modifications, updating... Additionally, the built-in database template provides a good standardized basis that newly starting enthomologist, or even experienced ones who are looking to digitalize their records could rely onto to thoroughly document their possesions. 

Hopefully, a few passionated enthomologist will find this software useful and will be helped in their quest. 

This software is therefore entirely open source and can be modified as users see fit.

I would like to encourage each users to provide feedback regarding potential function they would like to see integrated, potential issues that need to be fixed. All users should also be aware that I am only a newby to software development and therefore cannot guarantee of the full safety of the application. You should therefore never destroy any existing documentation assuming the app is full proof. I will improve it as I go. 
