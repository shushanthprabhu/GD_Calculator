# !/usr/bin/env python3
# coding: utf-8

__author__ = "Shushanth Prabhu"
__version__ = "1.0"

# Built using Python 3.7.5

from tkinter import Frame, Label, messagebox, Menu, Button, Entry
from tkinter import Y, BOTH, LEFT, N, Toplevel, END, W, X, TclError  # TOP
from tkinter.ttk import Notebook, Combobox
from Equations import EquationSolver

# py installer --hidden-import=pkg_resources.py2_warn --one file --no console MainWindow_RC.py
# py installer MainWindow.spec


# PROPERTIES OF AIR CONSTANT FOR NOW
default_n = 1.4  # -
default_cp = 1005  # UNIT J/Kg K

# UNIT CONVERSION LIST
# FIRST IS SI UNIT, CONVERSION TO SI FROM CORRESPONDING POSITION FORMAT y= mx +c
# STORED AS (m,c)
# FOR EXAMPLE K -> C +273.15 -> 1,273.15
unit_list_pressure = ["Pa", "bar", "PSi"]
unit_pressure_conversion = [(1, 0), (100000, 0), (6894.757, 0)]
unit_list_temperature = ("K", "°C", "°F")
unit_temperature_conversion = [(1, 0), (1, 273.15),
                               (0.55555555555555555555555555555556, 255.37222222222222222222222222222)]


class GasDynamicsCalculatorError(Exception):
    """
    Base Class for any Error encountered in the Code
    """
    pass


class EntryProperty:
    """
    Class to store air properties
    """

    def __init__(self, name, property_type):
        self.text = name
        # self.default_value = default_value
        self.unit_input = 0
        self.type = property_type
        self.read_value = None
        self.actual_value = None

    def convert_to_si(self):
        """
        Converting Units to SI Units
        """
        try:
            unit = self.units.index(self.unit_input)
            if unit == 0:
                return self.read_value
            else:
                return self.read_value * self.conversion[unit][0] + self.conversion[unit][1]
        except GasDynamicsCalculatorError as error:
            error = str(error)
            raise GasDynamicsCalculatorError("Unit Conversion failed" + error)

    def convert_from_si(self):
        """
        Convert Units from SI
        """
        try:
            unit = self.units.index(self.unit_input)
            if unit == 0:
                return self.actual_value
            else:
                return (self.actual_value - self.conversion[unit][1]) / self.conversion[unit][0]
        except GasDynamicsCalculatorError as error:
            error = str(error)
            raise GasDynamicsCalculatorError("Unit Conversion failed" + error)

    @property
    def units(self):
        """
        Provide List of defined Units in a list
        """
        if self.type == "pressure":
            return unit_list_pressure
        elif self.type == "temperature":
            return unit_list_temperature

    @property
    def conversion(self):
        """
        Return List of Conversion Factors
        """
        if self.type == "pressure":
            return unit_pressure_conversion
        elif self.type == "temperature":
            return unit_temperature_conversion

    @property
    def default_unit(self):
        """
        Return SI unit
        """
        if self.type == "pressure":
            return unit_list_pressure[0]
        elif self.type == "temperature":
            return unit_list_temperature[0]

    def __repr__(self):
        """
        Returns Name of the field
        """
        return self.text


class TabForm(Frame):
    """
    A class containing different operations in a form.
    """

    def __init__(self, frame, status_bar_class):
        self.property_list = []
        self.status_bar_class = status_bar_class
        # self.label_list = []
        self.field_list = []
        self.unit_list = []
        self.frame = frame

    def add_property(self, name, property_type):
        """
        Function to add a property in the frame
        """
        item = EntryProperty(name, property_type)
        self.property_list.append(item)
        # item.default_value = item.default_value

    def arrange_form(self):
        """
        Populates all fields of Labels, Adds default value and size of Entry Box
        """
        row_count = 1
        for item in self.property_list:
            label = Label(self.frame, text=item.text)
            label.grid(row=row_count, column=0)

            field = Entry(self.frame)
            field.grid(row=row_count, column=1, ipadx="30")

            self.field_list.append(field)

            units = Combobox(self.frame, width=12, values=item.units, state="readonly")
            units.grid(column=3, row=row_count)
            units.current(0)
            self.unit_list.append(units)

            row_count += 1

    def clear_entries(self):
        """
        Clears the form
        """
        i = 0
        while i < len(self.field_list):
            self.field_list[i].delete(0, END)
            self.unit_list[i].set(self.property_list[i].default_unit)
            # self.field_list[i].insert(0, self.property_list[i].default_value)
            i += 1

    def get_input(self, form, position):
        """
        Performs sanity check of field read from a form.
        """
        if len(form.get()) == 0:
            return 0
        else:
            value = form.get()
        try:
            value.is_integer()
            return int(value)
        except AttributeError:
            try:
                value.isnumeric()
                return float(value)
            except ValueError:
                error_string = "Check values in " + str(self.property_list[position])
                raise GasDynamicsCalculatorError(error_string)

    @staticmethod
    def sanity_check(parameter_list):
        """
        Sanity Check of Input
        """
        # CHECK IF ONLY ONE VARIABLE IS MISSING
        count_zero = 0
        for item in parameter_list:
            if item == 0:
                count_zero += 1
        if count_zero == 0:
            raise GasDynamicsCalculatorError("One Input must be blank")
        elif count_zero > 1:
            raise GasDynamicsCalculatorError("More than One Input is not defined")
            # return False

        # IF ALL CONDITIONS ARE MET
        return True

    def put_output(self):
        """
        Updates the parameter list
        """
        i = 0
        while i != len(self.property_list):
            self.field_list[i].delete(0, END)
            self.property_list[i].read_value = self.property_list[i].convert_from_si()
            self.field_list[i].insert(0, round(self.property_list[i].read_value, 6))
            self.unit_list[i].set(self.property_list[i].unit_input)
            i += 1

    def read_form(self):
        """
        Function to read inputs  in the form
        """
        i = 0
        try:
            while i != len(self.property_list):
                self.property_list[i].read_value = self.get_input(self.field_list[i], i)
                self.property_list[i].unit_input = self.unit_list[i].get()
                self.property_list[i].actual_value = self.property_list[i].convert_to_si()
                i += 1
        except GasDynamicsCalculatorError as error:
            error = str(error)
            messagebox.showerror("Error", message=error)


class TabIdealCompression(Frame):
    """
    Class for each Tab
    """

    def __init__(self, nb, status_bar_class):
        Frame.__init__(self, nb)
        self.status_bar_class = status_bar_class
        self.parent = nb
        self.form = TabForm(self, self.status_bar_class)
        # Property name, default value,
        self.form.add_property("Pressure 1", "pressure")
        self.form.add_property("Pressure 2", "pressure")
        self.form.add_property("Temperature 1", "temperature")
        self.form.add_property("Temperature 2", "temperature")

        # adding Labels and Forms
        self.form.arrange_form()

        button_accept = Button(self, text="Calculate", command=self.button_calculate)
        button_clear = Button(self, text="Clear", command=self.button_clear)
        button_accept.grid(row=6, column=0)
        button_clear.grid(row=6, column=1)

    def button_calculate(self):
        """
        performs sanity check of the input
        Solves the Equation
        """
        eq = EquationSolver()
        self.form.read_form()
        p1 = self.form.property_list[0].actual_value
        p2 = self.form.property_list[1].actual_value
        t1 = self.form.property_list[2].actual_value
        t2 = self.form.property_list[3].actual_value
        try:
            self.form.sanity_check((p1, p2, t1, t2))
        except GasDynamicsCalculatorError as error:
            error = str(error)
            messagebox.showerror("Error", message=error)
        n = self.status_bar_class.properties_air_dict['n']
        p1, p2, t1, t2 = eq.ideal_compression_p_vs_t(p1, p2, t1, t2, n)
        self.form.property_list[0].actual_value = p1
        self.form.property_list[1].actual_value = p2
        self.form.property_list[2].actual_value = t1
        self.form.property_list[3].actual_value = t2
        self.form.put_output()

    def button_clear(self):
        """
        Clears the form with default values
        """
        self.form.clear_entries()


class DescriptionTab(Frame):
    """
    Placeholder for other Tabs
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


class GasDynamicsCalculator(Frame):
    """
    Main Window Class
    """

    def __init__(self, isapp=True, name='gas_dynamics_calculator'):
        Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)

        self.master.title('Gas Dynamics Calculator')
        self.master.iconbitmap('images//paper_airplane16X16.ico')
        self.isapp = isapp

        # CREATE WIDGETS
        self.create_panels()
        self.create_menu_panels()

        # ESC closes the widget.
        self.winfo_toplevel().bind('<Escape>', lambda x: self.master.destroy())
        # self.winfo_toplevel().bind('<Escape>', lambda x: self.exit_app())

        # DISABLE RESIZING
        self.winfo_toplevel().resizable(0, 0)

        # STATUS BAR
        self.status_bar = Label(self, text='Gas Dynamics Equation Calculator', borderwidth=1, font='Helv 10', anchor=W)
        self.status_bar.pack(side="left", fill=X)

        # INITIALIZE
        self.description_tab = None
        self.ideal_compression_work = None
        self.status = None

        # PROPERTIES OF AIR
        self.properties_air_dict = {
            'n': default_n,
            'Cp': default_cp
        }

        # # DELETE
        # self.flag_1 = False
        # self.flag_2 = False

    def create_panels(self):
        """
        Create Cascading Panels
        """
        # create the notebook
        nb = Notebook(self)

        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles through tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()

        self.ideal_compression_work = TabIdealCompression(nb, status_bar_class=self)
        nb.add(self.ideal_compression_work, text="Ideal Compression", underline=0, padding=2)
        self.ideal_compression_work.bind("<Enter>",
                                         lambda a: self.status_bar.configure(text="Isentropic Compression"))
        self.ideal_compression_work.bind("<Leave>", lambda a: self.status_bar.configure(text=" "))

        self.description_tab = DescriptionTab(nb)
        nb.add(self.description_tab, text="Name of Tab", underline=2, padding=2)
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)

    def create_menu_panels(self):
        """
        Function creating menu panels
        """
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tear off's
        # noinspection PyAttributeOutsideInit
        self.menu = Menu(self.master, name='menu')
        self.add_options_menu()
        self.add_help_menu()

        self.master.config(menu=self.menu)
        # set up standard bindings for the Menu class
        # (essentially to capture mouse enter/leave events)
        self.menu.bind_class('Menu', '<<MenuSelect>>', self.update_status)

    def add_options_menu(self):
        """
        Adding Options Menu
        """
        options_menu = Menu(self.menu, name='options_menu')
        self.menu.add_cascade(label='Options', menu=options_menu, underline=0)
        options_menu.add_command(label='Properties of Fluid', command=self.properties_of_air)

        # self.add_sub_menu(options_menu)  # check buttons
        options_menu.add_separator()
        options_menu.add_command(label='Exit', command=self.exit_app)

    def esc_exit_app(self, event):
        """
        Escape closes the Widget
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
        help_menu.entryconfig(0, bitmap="questhead", compound=LEFT)

    def show_help_menu_info_msg(self):
        """
        Display Info Message
        """
        # copyright_symbol = u"\u00A9"
        window = Toplevel(self)

        info_msg = "A simple tool to calculate essential Gas Dynamic parameters " \
                   + "All Rights Reserved" + "\n"
        info_msg += "Compiled using Python v3.7.5" + "\n"

        panel = Label(window, text=info_msg)
        panel.grid(row=1, column=0)

        ok_button = Button(window, text='Ok', command=window.destroy, width=10)
        ok_button.grid(row=2, column=0)
        ok_button.focus()

        # ESC closes the widget.
        window.winfo_toplevel().bind('<Escape>', lambda x: window.destroy())

    def properties_of_air(self):
        """
        Menu to add or edit properties of Air
        """
        window_network_options = Toplevel(self)
        window_network_options.title("Properties fo Air-")
        window_network_options.iconbitmap('images//paper_airplane16X16.ico')
        self.properties_of_air_form(window_network_options)

    def properties_of_air_form(self, window):
        """
        Form of global air porperties
        """
        option1 = Label(window, text="Enter Isentropic Compression -")
        option2 = Label(window, text="Enter Specific Heat of Fluid [J/kg.K-")

        # FIELD
        self.option1_field = Entry(window)
        self.option2_field = Entry(window)

        button_accept = Button(window, text="Accept", command=lambda: self.properties_of_air_accept(window))
        button_cancel = Button(window, text="Cancel", command=lambda: window.destroy())
        button_reset_default = Button(window, text="Reset Default", command=self.properties_of_air_default)

        # PLACEMENT
        option1.grid(row=1, column=0)
        option2.grid(row=2, column=0)

        self.option1_field.grid(row=1, column=1, ipadx="50")
        self.option2_field.grid(row=2, column=1, ipadx="50")

        button_accept.grid(row=3, column=0)
        button_cancel.grid(row=3, column=1)
        button_reset_default.grid(row=3, column=3)
        # button_reset_default.grid(row=3, column=2)

        self.option1_field.bind("<Return>", lambda a: self.option2_field.focus_set())
        self.option2_field.bind("<Return>", lambda a: button_accept.focus_set())

        self.option1_field.insert(0, str(self.properties_air_dict['n']))
        self.option2_field.insert(0, str(self.properties_air_dict['Cp']))

    def properties_of_air_accept(self, tab):
        """
        Change global air properties
        """
        self.properties_air_dict['n'] = float(self.option1_field.get())
        self.properties_air_dict['Cp'] = float(self.option2_field.get())
        tab.destroy()

    def properties_of_air_default(self):
        """
        Reset it to default air properties
        """
        self.option1_field.delete(0, END)
        self.option1_field.insert(0, str(default_n))
        self.option2_field.delete(0, END)
        self.option2_field.insert(0, str(default_cp))

    def update_status(self, evt):
        """
        Function to update the Status
        :param evt: Mouse Enter event
        """
        try:
            # triggered on mouse entry if a menu item has focus
            # (focus occurs when user clicks on a top level menu item)

            item = self.tk.eval('%s entrycget active -label' % evt.widget)
            self.status_bar.configure(foreground='black',
                                      text=item)
        except TclError:
            # no label available, ignore
            pass


if __name__ == '__main__':
    GasDynamicsCalculator().mainloop()
