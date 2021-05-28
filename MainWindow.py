# !/usr/bin/env python3
# coding: utf-8
__author__ = "Shushanth Prabhu"
__email__ = "shushanth@gmail.com"
__version__ = "1.0"

# Built on Python 3.7.5
from tkinter import Frame, Label, messagebox, Menu, Button, Entry
from tkinter import Y, BOTH, TOP, LEFT, N, Toplevel, END
from tkinter.ttk import Notebook
from math import pow

# PROPERTIES OF AIR CONSTANT FOR NOW
n = 1.4


# TODO Units
# TODO Add status bar

class Equation_solver():
    """
    Collection of Methods to solve different Equations
    """

    def ideal_compression_for_p(self, p1, p2, t1, t2, n):
        """
        Solve Ideal Compression Law for Pressure
        :return:
        """
        if p1 == 0 and (p2 * t1 * t2) != 0:
            p1 = p2 * pow((t1 / t2), (n / (n - 1)))

        if p2 == 0 and (p1 * t1 * t2) != 0:
            p2 = p1 / pow((t1 / t2), (n / (n - 1)))

        if t1 == 0 and (p1 * p2 * t2) != 0:
            t1 = t2 * pow((p1 / p2), ((n - 1) / n))

        if t2 == 0 and (p1 * t1 * t2) != 0:
            t2 = t1 / pow((p1 / p2), ((n - 1) / n))

            # return p1, p2, t1, t2, n
        return p1, p2, t1, t2, n


class Entry_Property():
    """
        Class to store air properties
    """

    def __init__(self, name):
        self.text = name
        # self.default_value = default_value
        self.actual_value = 0

    def __repr__(self):
        """
        Returns Name of the field
        """
        return self.text


class Tab_Form():
    """
    A class containing different operations in a form.
    """

    def __init__(self, frame):
        self.property_list = []
        # self.label_list = []
        self.field_list = []
        self.frame = frame

    def add_property(self, name, default_value):
        """
        Function to add a property in the frame
        :param name: Name of property
        :param default_value: Default Value
        :return: None
        """
        property = Entry_Property(name)
        self.property_list.append(property)
        property.default_value = default_value

    def add_labels(self):
        """
        Populated all fields of Labels
        :return: None
        """
        row_count = 1
        for property in self.property_list:
            label = Label(self.frame, text=property.text)
            label.grid(row=row_count, column=0)
            row_count += 1

    def add_entries(self):
        """
        Populates all fields of Labels, Adds default value and size of Entry Box
        :return: None
        """
        row_count = 1
        for property in self.property_list:
            field = Entry(self.frame)
            field.grid(row=row_count, column=1, ipadx="50")
            field.insert(0, property.default_value)
            self.field_list.append(field)
            row_count += 1

    def clear_entries(self):
        """
        Cleares the form
        :return: None
        """
        i = 0
        while i < len(self.field_list):
            self.field_list[i].delete(0, END)
            self.field_list[i].insert(0, self.property_list[i].default_value)
            i += 1


class Tab_Ideal_Compression(Frame):
    """
    Class for each Tab
    """

    def __init__(self, nb):
        Frame.__init__(self, nb)
        self.parent = nb
        self.form = Tab_Form(self)

        # Property name, default value,
        self.form.add_property("Pressure 1", 0)
        self.form.add_property("Pressure 2", 0)
        self.form.add_property("Temperature 1", 0)
        self.form.add_property("Temperature 2", 0)

        # adding Labels and Forms
        self.form.add_labels()
        self.form.add_entries()

        button_accept = Button(self, text="Calculate", command=self.button_calculate)
        button_clear = Button(self, text="Clear", command=self.button_clear)
        button_accept.grid(row=6, column=0)
        button_clear.grid(row=6, column=1)

    def button_calculate(self):
        """
        Solves the Equation
        """
        p1 = float(self.form.field_list[0].get())
        p2 = float(self.form.field_list[1].get())
        t1 = float(self.form.field_list[2].get())
        t2 = float(self.form.field_list[3].get())

        eq = Equation_solver()
        p1, p2, t1, t2, n1 = eq.ideal_compression_for_p(p1, p2, t1, t2, n)
        self.form.field_list[0].delete(0, END)
        self.form.field_list[0].insert(0, p1)

        self.form.field_list[1].delete(0, END)
        self.form.field_list[1].insert(0, p2)

        self.form.field_list[2].delete(0, END)
        self.form.field_list[2].insert(0, t1)

        self.form.field_list[3].delete(0, END)
        self.form.field_list[3].insert(0, t2)

    def button_clear(self):
        """
        Clears the form with default values
        """
        self.form.clear_entries()


class Description_tab(Frame):
    """
    Placholder for other Tabs
    """

    # TODO Delete the class
    def __init__(self, nb):
        Frame.__init__(self, nb)
        self.parent = nb

        msg = ["Start Creating Widgets here-"]

        self.lbl = Label(self, wraplength='4i', justify=LEFT, anchor=N,
                         text=''.join(msg))
        self.lbl.pack()

        # widget
        self.btn = Button(self, text='Press')
        self.btn.pack()


class Gas_Dynamics_Calculator(Frame):
    """
    Main Window Class
    """

    def __init__(self, isapp=True, name='gas_dynamics_calculator'):
        Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)

        self.master.title('Gas Dynamics Calculator')
        self.master.iconbitmap('images//delete.png')
        self.isapp = isapp

        # CREATE WIDGETS
        self.create_panels()
        self.create_menu_panels()

        # ESC closes the widget.
        self.winfo_toplevel().bind('<Escape>', lambda x: self.master.destroy())

        self.flag_1 = False
        self.flag_2 = False

    def create_menu_panels(self):
        """
        Function creating menu panels
        :return: None
        """
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tearoff's
        self.menu = Menu(self.master, name='menu')
        self.build_submenus()
        self.master.config(menu=self.menu)
        # set up standard bindings for the Menu class
        # (essentially to capture mouse enter/leave events)
        # self.menu.bind_class('Menu', '<<MenuSelect>>', self.update_status)

    def build_submenus(self):
        """
        Function to add sub menus
        :return: None
        """
        self.add_options_menu()
        self.add_help_menu()
        # DELETE

    def add_options_menu(self):
        """
        Adding Options Menu
        :return: None
        """
        options_menu = Menu(self.menu, name='options_menu')

        self.menu.add_cascade(label='Options', menu=options_menu, underline=0)

        options_menu.add_command(label='Properties of Air',
                                 command=self.properties_of_air)

        self.add_sub_menu(options_menu)  # check buttons
        options_menu.add_separator()
        options_menu.add_command(label='Exit',
                                 command=self.exit_app)

    def esc_exit_app(self, event):
        """
        Escape closes the Widget
        :param event:
        :return:
        """
        if event:
            self.exit_app()

    def exit_app(self):
        """
        Are you sure prompt before exiting the Widget
        :return:
        """
        response = messagebox.askyesno(title="Exit", message="Are you sure you wish to Quit?")
        if response:
            self.master.destroy()

    def add_sub_menu(self, cascades):
        # build the Cascades->Check Buttons submenu
        check = Menu(cascades)
        cascades.add_cascade(label='Functionality Here', underline=0,
                             menu=check)
        check.add_checkbutton(label='Option 1 Here',
                              command=self.do_action_1)
        check.add_checkbutton(label='Option 2 Here',
                              command=self.do_action_2)

    def do_action_1(self):
        self.flag_1 = not self.flag_1

    def do_action_2(self):
        self.flag_2 = not self.flag_2

    def add_help_menu(self):
        """
        Adding Options Menu
        :return: None
        """
        disclaimer_msg = "THE AUTHORS DOES NOT WARRANT THE CORRECTNESS OF ANY RESULTS OBTAINED WITH THIS TOOL." \
                         + "IN NO EVENT WILL THE AUTHORS OR ANY OF ITS EMPLOYEES BE LIABLE TO YOU FOR DAMAGES," \
                         + "INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE" \
                         + "USE OR INABILITY TO USE THE SOFTWARE(INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA" \
                         + "BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES)."
        help_menu = Menu(self.menu, name='help_menu')
        self.menu.add_cascade(label='Help', menu=help_menu, underline=0)

        help_menu.add_command(label='Info',
                              command=self.show_help_menu_info_msg)

        help_menu.add_command(label='Disclaimer',
                              command=lambda: messagebox.showwarning(title="Disclaimer", message=disclaimer_msg))
        help_menu.entryconfig(0, bitmap='questhead', compound=LEFT)

    def show_help_menu_info_msg(self):
        """
        Display Info Message
        :return: None
        """
        copyright_symbol = u"\u00A9"
        window = Toplevel(self)

        info_msg = "A simple tool to calculate essential Gas Dynamic parameters " \
                   + "All Rights Reserved" + "\n"
        info_msg += "Code has the following dependencies-" + "\n"
        info_msg += "\t" + "Python v3.7.5" + "\n"

        panel = Label(window, text=info_msg)
        panel.grid(row=1, column=0)

        # img = Image.open('images//Logo.png')
        # img = img.resize((250, 80), Image.ANTIALIAS)
        # img = ImageTk.PhotoImage(img)
        # panel = Label(window, image=img)
        # panel.image = img
        panel.grid(row=1, column=0)

        ok_button = Button(window, text='Ok', command=window.destroy, width=10)
        ok_button.grid(row=2, column=0)
        ok_button.focus()

        # ESC closes the widget.
        window.winfo_toplevel().bind('<Escape>', lambda x: window.destroy())

    def properties_of_air(self):
        """ Menu to add or edit properties of Air"""
        pass

    def create_panels(self):
        demoPanel = Frame(self, name='demo')
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)

        # create the notebook
        nb = Notebook(demoPanel, name='notebook')

        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles thru tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()
        self.ideal_compression_work = Tab_Ideal_Compression(nb)
        nb.add(self.ideal_compression_work, text="Ideal Compression", underline=0, padding=2)

        self.description_tab = Description_tab(nb)
        nb.add(self.description_tab, text="Name of Tab", underline=2, padding=2)
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)


if __name__ == '__main__':
    Gas_Dynamics_Calculator().mainloop()
