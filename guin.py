from tkinter import *

import pandas as pd
import os
import glob


class GuiWindow:
    def __init__(self):
        inputdata1 = StringVar()
        Label(root, text="Enter Subject Code:  ").grid(
            row=1, column=0, padx=10, pady=(50, 10))
        Entry(root, textvariable=StringVar(), width=40, font=('calibre', 10,
            'normal')).grid(row=1, column=1, columnspan=2, pady=(50, 10))
        Label(root, text="Enter name of Teacher:  ").grid(
            row=2, column=0, padx=10, pady=10)
        Entry(root, textvariable=inputdata1, width=40, font=(
            'calibre', 10, 'normal')).grid(row=2, column=1, columnspan=2, pady=10)
        Button(root, text="Generate Attendance", bg="green", fg="white",
            command=self.create_attendance).grid(row=3, column=0, padx=10, pady=10)

    def create_attendance(self):
        pathname = os.getcwd()
        filename = glob.glob(os.path.join(pathname, "*.csv"))

        # filename=glob.glob(os.path.join('/content/drive/MyDrive/attend/attenance_excel'+'/'+'/*csv'))

        list = []
        for colum in range(len(filename)):
            temp = pd.read_csv(filename[colum])
            list.append(temp)

        for i in range(len(list)):
            list[i]=list[i].replace(to_replace=['Left','Joined before'],value='Joined')
            list[i].drop_duplicates(subset=['Full Name','User Action'],keep='first',inplace=True)
            index_names=list[i][list[i]['Full Name']=='Domnic S'].index
            list[i].drop(index_names,inplace=True)
            list[i].drop_duplicates(subset=['Full Name','User Action'],keep='first',inplace=True)
            index_names=list[i][list[i]['Full Name']=='godan lal (Guest)'].index
            list[i].drop(index_names,inplace=True)
            list[i].drop_duplicates(subset=['Full Name','User Action'],keep='first',inplace=True)
            index_names=list[i][list[i]['Full Name']=='rahul mali (Guest)'].index
            list[i].drop(index_names,inplace=True)

        # list

        result = pd.concat(list)

        # result

        final=result['Full Name'].value_counts()

        self.final_output=final.reindex()

        self.final_output=self.final_output.reset_index()

        self.final_output

        self.final_output.rename(columns = {'index':'Students_Name'  , 'Full Name':'No._of_days_present'}, inplace = True)

        self.final_output['Total no. of days']=[23 for _ in range(len(self.final_output))]

        self.final_output['No. of days absent']= self.final_output['Total no. of days']- self.final_output['No._of_days_present']

        self.final_output['Attendance_percent'] = ((self.final_output['No._of_days_present'] /23)*100).round(2).astype(str) + '%'

        self.final_output=self.final_output.sort_values(by='Students_Name')

        self.final_output.reindex()

        self.final_output.to_excel('Attendance_Report.xlsx', sheet_name='sheet1', index=False)
        # print(self.final_output['Students_Name'])
        Label(root, text = "Report generated Successfully!!", fg='red').grid(row=3,column=1, padx=10) 

        Button(root, text="Get Specific Student\n Attendance Details", command=self.student_attendance).grid(row=4,column=0,padx=10, pady=(6,40))


    def student_attendance(self):
        self.clicked = StringVar()
        Label(root, text="Enter the Student Name: ").grid(row=5, column=0)
        Entry(root, textvariable=self.clicked, width=40).grid(row=5, column=1)
        Button(root, text="Submit", command=self.display_grid).grid(row=6, column=0, pady=10)


    def display_grid(self):
        details = self.final_output[self.final_output["Students_Name"]==self.clicked.get()]
        grows = len(details)
        gcols = len(list(details.columns))
        print(details)
        col = list(details.columns)
        for i,val in enumerate(col):
            Label(root,text=val).grid(row=7,column=i)
        for i in range(8, grows+8):
            for j in range(gcols):
                cell = Entry(root)
                # print(i,j)
                cell.grid(row=i,column=j)
                cell.insert(END, details.iloc[i-8][j])


root = Tk()
root.geometry("900x600")
root.title("Student Attendance Report")

mygui = GuiWindow()

root.mainloop()
