from tkinter import *
from tkinter import ttk
from database import connect_to_db, get_notes, create_note, delete_notes

connect_to_db()

class App:
    def __init__(self):

        self.data = get_notes()

        self.root = Tk()
        
        self.root.title("Note Taker")

        self.text_label = Label(self.root, text="Enter text here")

        self.text_label.pack()

        self.text_stringvar = StringVar(self.root)
        self.text_stringvar.set("")

        self.text = Entry(self.root, textvariable=self.text_stringvar)
        self.text.pack(fill=BOTH)
        
        self.box = Frame(self.root)
        
        for x in range(2):
            self.box.columnconfigure(x, weight=1)
            
        self.scrollbar = Scrollbar(self.box)
        self.scrollbar.pack( side = RIGHT, fill=Y )    

        self.table = ttk.Treeview(
            self.box,
            columns=("id", "text"),
            show="headings",
            yscrollcommand=self.scrollbar.set,
        )

        self.table.heading("id", text="id")
        self.table.heading("text", text="Text")

        self.table.pack(fill=BOTH, side=LEFT,expand=True)
        self.scrollbar.config(command=self.table.yview)

        for note in self.data:
            self.table.insert(parent="", index=END, values=note)

        def save_note():
            try:
                text = self.text_stringvar.get()
                new_text = create_note(text)
                self.table.insert(parent="", index=END, values=new_text)

            except:
                top = Toplevel()
                top.geometry("180x100")
                top.title("Creation Failed")
                success_button = Button(
                    top, text="Note Creation Failed!", command=top.destroy
                )
                success_button.pack(fill=BOTH)
                top.mainloop()

        def delete_chosen_notes():
            try:
                row_list = []
                selected_rows = list(self.table.selection())
                
                if len(selected_rows) == 0:
                    top = Toplevel()
                    top.title("No Rows Selected!")
                    success_button = Button(
                        top, text="Choose a row to delete.", command=top.destroy
                    )
                    success_button.pack(fill=BOTH)
                    top.mainloop()
                    return
                    
                else:    
                    for row in selected_rows:
                        row_id = self.table.item(row)["values"][0]
                        row_list.append(row_id)
                        self.table.delete(row)
                        
                    row_tuple = tuple(row_list)
                    return delete_notes(row_tuple)
            except:
                top = Toplevel()
                top.title("Deletion Failed")
                success_button = Button(
                    top, text="Note Deletion Failed!", command=top.destroy
                )
                success_button.pack(fill=BOTH)
                top.mainloop()
                return

        self.box.pack(fill=BOTH)
        
        self.save_button = Button(self.root, text="Create", command=save_note)
        self.save_button.pack(fill=BOTH)

        self.delete_button = Button(
            self.root, text="Delete", command=delete_chosen_notes
        )
        self.delete_button.pack(fill=BOTH)

        self.root.mainloop()


if __name__ == "__main__":
    App()
