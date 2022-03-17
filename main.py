from string import whitespace
import mysql.connector as sql
from dataclasses import dataclass
import sys
import os

@dataclass
class Table:
    name : str
    header_names : list[str]
    header_types : list[str]

@dataclass
class Tournaments_Table (Table):
    name = "Tournaments"
    header_names = ["tourn_id", "name"   , "location", "year" ]
    header_types = ["int"     , "varchar(30)", "varchar(50)" , "char(4)"  ]

@dataclass
class Matches_Table (Table):
    name = "Matches"
    header_names = ["match_id", "tourn_id", "location", "team_id1" , "team_id2" , "Result"  ]
    header_types = ["int"     , "int"     , "varchar(50)", "int", "int", "char(1)" ]

@dataclass
class Teams_Table (Table):
    name = "Teams"
    header_names = ["team_id", "name"   , "captain", "wins", "losses" ]
    header_types = ["int"    , "varchar(20)", "varchar(20)", "int" , "int" ]


class AppData:
    column_width = 15
    view_mode = None 
    view_data = None
    tableName = None
    baseMenu = "".join([
    "Select your Next Action: \n",
    "\n",
    "(1) View Table \n",
    "(2) View Tournament Details \n",
    "(3) View Team Details \n",
    "(4) Add New Tournament \n",
    "(5) Add New Match\n",
    "\n",
    "Enter your next action : "
    ])
    
    selTable = "".join([
        "Select the Table you would like to view : \n",
        "\n",
        "(1) Tournaments \n",
        "(2) Teams \n",
        "(3) Matches \n",
        "\n",
        "Enter the table to view : "
    ])

    currMenu = baseMenu
    menuType = "base"
        

class App:
    table_tournament = Tournaments_Table
    table_match = Matches_Table
    table_team = Teams_Table

    def __init__(self):
        
        try :   self.cnx = sql.MySQLConnection(user='root', password = 'mayaank2004',
                                    host = 'localhost', database = 'Sport_Organizer')
        except: sys.exit("Failed to Connect to Database")

        self.cursor = self.cnx.cursor()
 
        self.data= AppData


    def init(self):
        self.createTable(App.table_tournament)
        self.createTable(App.table_match)
        self.createTable(App.table_team)

        self.createTableData()

    def reset(self):
        print("Resetting all data")
        self.deleteTable(App.table_tournament)
        self.deleteTable(App.table_match)
        self.deleteTable(App.table_team)

    def run(self):
        self.render()
        while True :
            self.WaitForInput()

    def close(self):
        self.cnx.close()

    def createTable(self, table: Table):
        command = "CREATE TABLE " + table.name + " ( "
        # id integer 
        # name char (5),

        assert len(table.header_names) == len(table.header_types), f"Incorrect header values in {table.name} "
        num_headers = len(table.header_names)
        
        for i in range(num_headers):
            command += table.header_names[i]
            command += " "
            command += table.header_types[i]
            if i != num_headers-1 : command += ", "
            
        command += ");"
        print(command)
        self.cursor.execute(command)

    def deleteTable(self, table: Table):
        command = "drop table " + table.name + ";"
        print (command)
        self.cursor.execute(command)

    def createTableData(self):
        print("Creating Data for Table")
        self.cursor.execute('INSERT INTO Tournaments VALUES \
            (1, "Mumbai League" , "Mumbai", "2019"  ), \
            (2, "Delhi League" , "Delhi", "2020"  ); \
        ')

        self.cursor.execute('INSERT INTO Teams VALUES \
            (1, "Hurricanes", "Ajay", 3, 1), \
            (2, "Strikers" , "Yash" , 1, 2),\
            (3, "Stars" , "Gaurav" , 1,2) ;\
        ')

        self.cursor.execute('INSERT INTO Matches VALUES \
            (1 , 1, "Thane", 1, 2, "W"),\
            (2 , 1, "Dadar", 2, 3, "L"),\
            (3 , 1, "Andheri", 1, 3, "W"),\
            (4 , 2, "Delhi", 1, 3, "W"),\
            (5 , 2, "Delhi", 1, 2, "L");\
        ')
        self.cnx.commit()

    def render(self):
        os.system('cls')

        # self.print_char(0,0,"+" + "-"*40 + "+")
        # self.print_char(0,3,"+" + "-"*40 + "+")
        # self.print_char(0,2,'|')
        # self.print_char(42,2,'|')
        print("="*40)
        print(" "*10 + "Sports Organizer" + " "*10)
        print("="*40)

        if self.data.view_mode == None:
            print("Not Viewing Anything Currently")
        
        elif self.data.view_mode == "table":
            title = self.data.view_data[0]
            headers = self.data.view_data[1]
            records=  self.data.view_data[2:]
            num_columns = len(headers)

            whitespace= ((self.data.column_width+3)*num_columns - len(title)-1)-3
            print("+"+("-"* ((self.data.column_width+3)*num_columns-1)) + "+")
            print("|", end = "")
            print(" "*(whitespace//2),title, " "*((whitespace+1)//2), "|")

            print("+"+("-"* (self.data.column_width+2) +"+")*num_columns )
            print("|", end = "")

            for i in range(num_columns):
                print(headers[i], " "*(self.data.column_width- len(headers[i])), "|", end = "")
            print()

            print("+"+("-"* (self.data.column_width+2) +"+")*num_columns)

            for j in range(len(records)):
                record = records[j]
                print("|", end = "")
                for i in range(num_columns):
                    print(record[i], " "*(self.data.column_width- len(str(record[i]))), "|", end = "")
                print()

            print("+"+("-"* (self.data.column_width+2) +"+")*num_columns)

        elif self.data.view_mode == "tourn":
            print("Tournament Information")
            print("-"*30)
            print("Tournament Id : ", self.data.view_data[0]  )
            print("Tournament Name : ", self.data.view_data[1]  )
            print("Played in : ", self.data.view_data[2]  )
            print("Year : ", self.data.view_data[3]  )

        elif self.data.view_mode == "team":
            num_wins = self.data.view_data[3]
            num_losses = self.data.view_data[4]
            print("Team Information")
            print("-"*30)
            print("Team Id : ", self.data.view_data[0]  )
            print("Team Name : ", self.data.view_data[1]  )
            print("Team Captain : ", self.data.view_data[2]  )
            print("Number of Wins : ", num_wins  )
            print("Number of Losses : ", num_losses  )
            print("Win Percentage : ", int(100*num_wins/(num_wins+num_losses)))

        elif self.data.view_mode == "add_tourn":
            print("Tournament Added Successfully")

        elif self.data.view_mode == "add_match":
            print("Match Added Successfully")
            print("Updated the statistics of the relevent teams")

        print("="*40)
        
        print(self.data.currMenu, end = "")


        # print("hi")

    def WaitForInput(self):
        inp = input()
        if self.data.menuType == "base":
            if inp == "1": # View table
                self.data.menuType = "table"
                self.data.currMenu = self.data.selTable
                self.data.view_mode = None
            
            elif inp == "2": # View Tournaments
                self.data.view_mode = None
                self.data.menuType = "tourn"
                self.loadTable(self.table_tournament)
                tourn_data = []
                for i in range(2,len(self.data.view_data)):
                    tourn = self.data.view_data[i]
                    tourn_data.append(f"({tourn[0]})  {tourn[1]} \n")
                
                self.data.currMenu = "".join(["Select Tournament to view : \n\n"] + \
                    tourn_data + ["\n Enter Tournament to view : "])
            
            elif inp == "3": # View Team
                self.data.view_mode = None
                self.data.menuType = "team"
                self.loadTable(self.table_team)
                team_data = []
                for i in range(2,len(self.data.view_data)):
                    team = self.data.view_data[i]
                    team_data.append(f"({team[0]})  {team[1]} \n")
                
                self.data.currMenu = "".join(["Select Team to view : \n\n"] + \
                    team_data + ["\n Enter Team to view : "])
            
            elif inp == "4": # Add Tournament
                self.data.view_mode = None
                self.data.menuType = "add_tourn"
                self.temp_data = {}
                self.loadTable(self.table_tournament)
                self.temp_data["id"] = len(self.data.view_data)-1
                self.temp_data["name"] = None
                self.data.currMenu = "".join([
                    "Creating New Tournament \n \n",
                    "Enter the tournament Name : "
                ])
            
            elif inp == "5": # Add Match
                self.data.view_mode = None
                self.data.menuType = "add_match"
                self.temp_data = {}
                self.loadTable(self.table_match)
                self.temp_data["match_id"] = len(self.data.view_data)-1
                self.temp_data["tourn_id"] = None
                self.data.currMenu = "".join([
                    "Creating New Match \n \n",
                    "Enter the tournament id in which match is held : "
                ])


        elif self.data.menuType == "table":
            self.data.view_mode = "table"
            if inp == "1": self.loadTable(self.table_tournament)
            elif inp == "2": self.loadTable(self.table_team)
            elif inp == "3": self.loadTable(self.table_match)
            self.data.menuType = "base"
            self.data.currMenu = self.data.baseMenu

        elif self.data.menuType == "tourn":
            self.data.view_mode = "tourn"
            for i in range(2, len(self.data.view_data)):
                record = self.data.view_data[i]
                if str(record[0]) == inp:
                    self.data.view_data = record
                    break
            self.data.menuType = "base"
            self.data.currMenu = self.data.baseMenu

        elif self.data.menuType == "team":
            self.data.view_mode = "team"
            for i in range(2, len(self.data.view_data)):
                record = self.data.view_data[i]
                print("Test",record)
                if str(record[0]) == inp:
                    self.data.view_data = record
                    break

            self.data.menuType = "base"
            self.data.currMenu = self.data.baseMenu

        elif self.data.menuType == "add_tourn":
            if self.temp_data["name"] == None:
                self.temp_data["name"] = inp
                self.data.currMenu += inp + "\n"
                self.data.currMenu += "Enter the tournament location : "
                self.temp_data["location"] = None

            elif self.temp_data["location"] == None :
                self.temp_data["location"] = inp
                self.data.currMenu += inp + "\n"
                self.data.currMenu += "Enter the tournament year : "
                self.temp_data["year"] = None

            elif self.temp_data["year"] == None :
                self.temp_data["year"] = inp
                self.data.currMenu += inp + "\n"

                self.data.currMenu = self.data.baseMenu
                self.data.menuType = "base"
                self.data.view_mode = "add_tourn"
                
                self.add_tourn()

        elif self.data.menuType == "add_match":
            if self.temp_data["tourn_id"] == None:
                self.temp_data["tourn_id"] = inp
                self.data.currMenu += inp + "\n"
                self.data.currMenu += "Enter the match location : "
                self.temp_data["location"] = None

            elif self.temp_data["location"] == None :
                self.temp_data["location"] = inp
                self.data.currMenu += inp + "\n"
                self.data.currMenu += "Enter the id of first team : "
                self.temp_data["id1"] = None

            elif self.temp_data["id1"] == None :
                self.temp_data["id1"] = inp
                self.data.currMenu += inp + "\n"
                self.data.currMenu += "Enter the id of second team : "
                self.temp_data["id2"] = None

            elif self.temp_data["id2"] == None :
                self.temp_data["id2"] = inp
                self.data.currMenu += inp + "\n"
                self.data.currMenu += "Enter the Result : "
                self.temp_data["result"] = None

            elif self.temp_data["result"] == None :
                self.temp_data["result"] = inp
                self.data.currMenu += inp + "\n"

                self.data.currMenu = self.data.baseMenu
                self.data.menuType = "base"
                self.data.view_mode = "add_match"
                
                self.add_match()

                


        self.render()

    def loadTable(self, table:Table):
        command = f"select * from {table.name}"
        self.cursor.execute(command)

        results = self.cursor.fetchall()
        self.data.view_data =[table.name]+ [tuple(table.header_names)]+results

    def add_tourn(self):
        command = f'Insert into {self.table_tournament.name} VALUES ({self.temp_data["id"]},"{self.temp_data["name"]}", "{self.temp_data["location"]}", "{self.temp_data["year"]}")'
        self.cursor.execute(command)
        self.cnx.commit()

    def add_match(self):
        command = f'Insert into {self.table_match.name} VALUES ({self.temp_data["match_id"]},"{self.temp_data["tourn_id"]}", "{self.temp_data["location"]}", "{self.temp_data["id1"]}" , "{self.temp_data["id2"]}" , "{self.temp_data["result"]}")'
        self.cursor.execute(command)
        self.cnx.commit()

        command = f"select * from {self.table_team.name} where team_id= {self.temp_data['id1']} "
        self.cursor.execute(command)
        team1 = self.cursor.fetchall()[0]
        self.cnx.commit()


        command = f"select * from {self.table_team.name} where team_id= {self.temp_data['id2']} "
        self.cursor.execute(command)
        team2 = self.cursor.fetchall()[0]
        self.cnx.commit()

        
        if self.temp_data['result'].lower() == 'w':
            command = f"update {self.table_team.name} set wins={team1[3]+1}    where team_id= {team1[0]} "
            self.cursor.execute(command)
            self.cnx.commit()

            command = f"update {self.table_team.name} set losses={team2[4]+1}    where team_id= {team2[0]} "
            self.cursor.execute(command)
            self.cnx.commit()
        
        if self.temp_data['result'].lower() == 'l':
            command = f"update {self.table_team.name} set losses={team1[4]+1}    where team_id= {team1[0]} "
            self.cursor.execute(command)
            self.cnx.commit()

            command = f"update {self.table_team.name} set wins={team2[3]+1}    where team_id= {team2[0]} "
            self.cursor.execute(command)
            self.cnx.commit()






if __name__ == "__main__" :
    app = App()
    # app.reset() # Delete all tables 
    # app.init() # Run only once to initialize data
    app.run()
    app.close()