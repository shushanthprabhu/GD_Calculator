# !/usr/bin/env python3
# coding: utf-8
__email__ = "shushanth@gmail.com"
__version__ = "1.0"

# Built on Python 3.7.5
from tkinter import Frame, Label, messagebox, Menu, Button, Entry
from tkinter import Y, BOTH, TOP, LEFT, N, Toplevel, END
from tkinter.ttk import Notebook
from math import pow

# py installer --hidden-import=pkg_resources.py2_warn --one file --no console MainWindow_RC.py
# py installer MainWindow.spec
# ICON_MAKER http://www.rw-designer.com/online_icon_maker.php icon Maker

# PROPERTIES OF AIR CONSTANT FOR NOW
n = 1.4


# TODO Units
# TODO Add status bar
# Add equations /Nikhil
class GasDynamicsCalculatorError(Exception):
    """
    Base Class for Exception
    """
    pass


class EquationSolver:
    """
    Collection of Methods to solve different Equations
    """

    @staticmethod
    def ideal_compression_p_vs_t(p1, p2, t1, t2, g):
        """
        Solve Ideal Compression Law for Pressure
        """
        if p1 == 0 and (p2 * t1 * t2) != 0:
            p1 = p2 * pow((t1 / t2), (g / (g - 1)))

        if p2 == 0 and (p1 * t1 * t2) != 0:
            p2 = p1 * pow((t2 / t1), (g - 1) / g)

        if t1 == 0 and (p1 * p2 * t2) != 0:
            t1 = t2 * pow((p1 / p2), ((g - 1) / g))

        if t2 == 0 and (p1 * t1 * t2) != 0:
            t2 = t1 * pow((p2 / p1), ((g - 1) / g))

        return p1, p2, t1, t2, g


class EntryProperty:
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


class TabForm:
    """
    A class containing different operations in a form.
    """

    def __init__(self, frame):
        self.property_list = []
        # self.label_list = []
        self.field_list = []
        self.frame = frame

    def add_property(self, name, initial_value):
        """
        Function to add a property in the frame
        :param name: Name of property
        :param initial_value: Default Value
        :return: None
        """
        item = EntryProperty(name)
        self.property_list.append(item)
        item.default_value = initial_value

    def add_labels(self):
        """
        Populated all fields of Labels
        """
        row_count = 1
        for item in self.property_list:
            label = Label(self.frame, text=item.text)
            label.grid(row=row_count, column=0)
            row_count += 1

    def add_entries(self):
        """
        Populates all fields of Labels, Adds default value and size of Entry Box
        """
        row_count = 1
        for _ in self.property_list:
            field = Entry(self.frame)
            field.grid(row=row_count, column=1, ipadx="50")
            # field.insert(0, property.default_value)
            self.field_list.append(field)
            row_count += 1

    def clear_entries(self):
        """
        Clears the form
        """
        i = 0
        while i < len(self.field_list):
            self.field_list[i].delete(0, END)
            # self.field_list[i].insert(0, self.property_list[i].default_value)
            i += 1

    @staticmethod
    def _check_int_(number):
        try:
            number.is_integer()
            return int(number)
        except AttributeError:
            raise GasDynamicsCalculatorError("Not Integer")

    @staticmethod
    def _check_float_(number):
        try:
            number.isnumeric()
            return float(number)
        except ValueError:
            raise GasDynamicsCalculatorError("Not Float")

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
        # CHECK IF ANY INPUT IS FALSE
        # count_zero = 0
        # for item in parameter_list:
        #     if item == False:
        #         count_zero += 0
        # if not count_zero == 1:
        #     raise GasDynamicsCalculatorError("Input is missing")
        #     return False

        # CHECK IF ONLY ONE VARIABLE IS MISSING
        count_zero = 0
        for item in parameter_list:
            if item == 0:
                count_zero += 1
        if not count_zero == 1:
            raise GasDynamicsCalculatorError("More than One Input is not defined")
            # return False

        # IF ALL CONDITIONS ARE MET
        return True

    def put_output(self, parameter_list):
        """
        Updates the parameter list
        """
        i = 0
        while i != len(parameter_list):
            self.field_list[i].delete(0, END)
            self.field_list[i].insert(0, round(parameter_list[i], 3))
            i += 1


class TabIdealCompression(Frame):
    """
    Class for each Tab
    """

    def __init__(self, nb):
        Frame.__init__(self, nb)
        self.parent = nb

        self.form = TabForm(self)

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
        performs sanity check of the input
        Solves the Equation
        """
        eq = EquationSolver()
        p1 = p2 = t1 = t2 = None
        try:
            p1 = self.form.get_input(self.form.field_list[0], 0)
            p2 = self.form.get_input(self.form.field_list[1], 1)
            t1 = self.form.get_input(self.form.field_list[2], 2)
            t2 = self.form.get_input(self.form.field_list[3], 3)
        except GasDynamicsCalculatorError as error:
            error = str(error)
            messagebox.showerror("Error", message=error)
        try:
            self.form.sanity_check((p1, p2, t1, t2))
        except GasDynamicsCalculatorError as error:
            error = str(error)
            messagebox.showerror("Error", message=error)
        p1, p2, t1, t2, n1 = eq.ideal_compression_p_vs_t(p1, p2, t1, t2, n)
        self.form.put_output((p1, p2, t1, t2))

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

        self.flag_1 = False
        self.flag_2 = False

        self.description_tab = None
        self.ideal_compression_work = None

    def create_menu_panels(self):
        """
        Function creating menu panels
        """
        # create the main menu (only displays if child of the 'root' window)
        self.master.option_add('*tearOff', False)  # disable all tear off's
        # noinspection PyAttributeOutsideInit
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
        help_menu.entryconfig(0, bitmap="questhead", compound=LEFT)

    def show_help_menu_info_msg(self):
        """
        Display Info Message
        """
        # copyright_symbol = u"\u00A9"
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
        """
        Menu to add or edit properties of Air
        """
        pass

    def create_panels(self):

        demo_panel = Frame(self, name='demo')
        demo_panel.pack(side=TOP, fill=BOTH, expand=Y)

        # create the notebook
        nb = Notebook(demo_panel, name='notebook')

        # extend bindings to top level window allowing
        #   CTRL+TAB - cycles through tabs
        #   SHIFT+CTRL+TAB - previous tab
        #   ALT+K - select tab using mnemonic (K = underlined letter)
        nb.enable_traversal()
        self.ideal_compression_work = TabIdealCompression(nb)
        nb.add(self.ideal_compression_work, text="Ideal Compression", underline=0, padding=2)

        self.description_tab = DescriptionTab(nb)
        nb.add(self.description_tab, text="Name of Tab", underline=2, padding=2)
        nb.pack(fill=BOTH, expand=Y, padx=2, pady=3)


if __name__ == '__main__':
    GasDynamicsCalculator().mainloop()
