import pandas as pd
import PIL.ImageFont as ImageFont
import qrcode
import os
import time
import shutil
from nicegui import ui
from typing import Union
from PIL import Image, ImageDraw
from timeloop import Timeloop
from datetime import timedelta
from fpdf import FPDF
import xlwings as xw
import asyncio

#app = xw.App()

def debug_print(message):
    """
    Prints a debug message in green color.

    :param message: The debug message.
    :type message: str
    """
    print("\033[92m" + str(message) + "\033[0m")

#TODO Focus on Scanner field

tl = Timeloop()

class InventoryManager:

    """
    A class for managing an inventory of items with unique serial numbers, names, descriptions, 
    and availability statuses.
    """

    qr_width = 1000

    def __init__(self):
        """
        Initializes the InventoryManager with the inventory data from the Excel file 
        Bauteileschrank.xlsx.
        """
        self.running_data = pd.read_excel('Verbrauchsmaterial_ELab_TRGE.xlsx', sheet_name='Verbrauchsmaterial', usecols={"id","Available","Name"}, dtype={'Available':bool}, engine='openpyxl')
        self.table = None
        self.input = None
        self.wb = None
        self.sht = None

    """def save_data(self):
        """""""
        Saves the current inventory data to existing Excel file.
        Runningdata contains the columns:
        id: The serial number of the item.
        Available: The availability status of the item.
        Name: The name of the item.
        """"""
        try:
            dataframe = pd.read_excel('Verbrauchsmaterial_ELab_TRGE.xlsx', sheet_name='Verbrauchsmaterial', dtype={'Available':bool})
            debug_print(dataframe)
        except Exception as e:
            print("Error Saving File! Error:\n" + str(e))
            ui.notify('Error Saving File!', category='error')"""

    def read_data(self):
        """
        Reads the inventory data from an Excel file.

        :return: The inventory data.
        :rtype: pd.DataFrame
        """
        try:
            self.running_data = pd.read_excel('Verbrauchsmaterial_ELab_TRGE.xlsx', sheet_name='Verbrauchsmaterial', dtype={'Available':bool}, usecols={"id","Available","Name"})
        except Exception as e:
            debug_print("Error Reading File! Error:\n"+str(e))
            ui.notify('Error Loading File!', category='error')

    """def gen_new_serial(self) -> int:
        """"""
        Generates a new serial number for the inventory.

        :return: The new serial number.
        :rtype: int
        """"""
        lastID = self.running_data['id'].max()
        debug_print("Generated new Serial: "+str(lastID + 1))
        return lastID + 1"""

    def update_availability(self, input: Union[str, list[dict[str, int]]], setting:bool=False):
        """
        Updates the availability of an item or a list of items.

        :param input: The serial number or list of items.
        :type input: Union[str, List[Dict[str, int]]
        :param setting: The availability setting.
        :type setting: bool
        """
        if input != None:
            if type(input) == str:
                debug_print("Updating String")
                self.running_data.loc[self.running_data['id']==int(input), 'Available'] = setting
            elif type(input) == list:
                debug_print("Updating List")
                for inp in input:
                    self.running_data.loc[self.running_data['id']==inp['id'], 'Available'] = setting
            try:
                app = xw.App()
                wb = xw.Book('Verbrauchsmaterial_ELab_TRGE.xlsx')
                sht = wb.sheets['Verbrauchsmaterial']
                if type(input) == str:
                    debug_print("Updating String")
                    for row in range(1, 1000):
                        if sht.range('A' + str(row)).value == int(input):
                            if setting == True:
                                sht.range('B' + str(row)).value = True
                                debug_print(input + " = True")
                            else:
                                sht.range('B' + str(row)).value = False
                                debug_print(input + " = False")
                            break
                elif type(input) == list:
                    debug_print("Updating List")
                    rownum = xw.Range('A1').current_region.last_cell.row
                    debug_print("Rownum: "+str(rownum))
                    for inp in input:
                        #debug_print("ID: "+str(inp['id']))
                        for row in range(1,rownum):
                            if sht.range('A' + str(row)).value == int(inp['id']):
                                if setting == True:
                                    sht.range('B' + str(row)).value = True
                                    debug_print(str(inp['id']) + " = True")
                                else:
                                    sht.range('B' + str(row)).value = False
                                    debug_print(str(inp['id']) + " = False")

            except Exception as e:
                ui.notify('Error Updating Availability!', category='error')
                debug_print("Error Updating Availability! Error:\n"+str(e))

            try:
                wb.save()
                wb.close()
            except Exception as e:
                debug_print("Error Saving File! Error:\n"+str(e))

            try:
                app.quit()
            except Exception as e:
                debug_print("Error Quitting Excel! Error:\n"+str(e))
            self.wb = None
            self.sht = None
            self.table.update_rows(self.running_data.loc[:].to_dict('records'))
            debug_print("Updated Availability Threading")
        
    def update_data(self):
        """
        Updates the data in the table.
        """
        self.read_data()
        self.table.update_rows(self.running_data.loc[:].to_dict('records'))
        self.table.update()
        debug_print("Updated Data")

    def gen_qr_code(self, serial:int, name:str):
        filename = f"barcodes/{serial}.png"

        debug_print("Generating QR-Code for single ID: "+str(serial))
        debug_print("Name: "+name)

        # Generate the QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(id)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Create a new image with the QR code and text
        width, height = img.size
        new_width = width + 1071
        new_height = height + 50
        new_img = Image.new("RGB", (new_width, new_height), "white")
        new_img.paste(img, (0, 0))

        # Add text to the image
        draw = ImageDraw.Draw(new_img)
        font = ImageFont.truetype("arial.ttf", 60)  # You may need to install a font
        if len(name) < 33:
            draw.text((width + 10, 50), name, font=font, fill="black")
        elif len(name) < 66:
            draw.text((width + 10, 50), name[:33], font=font, fill="black")
            draw.text((width + 10, 110), name[33:], font=font, fill="black")
        elif len(name) < 99:
            draw.text((width + 10, 50), name[:33], font=font, fill="black")
            draw.text((width + 10, 110), name[33:66], font=font, fill="black")
            draw.text((width + 10, 170), name[99:], font=font, fill="black")
        elif len(name) < 132:
            draw.text((width + 10, 50), name[:33], font=font, fill="black")
            draw.text((width + 10, 110), name[33:66], font=font, fill="black")
            draw.text((width + 10, 170), name[66:99], font=font, fill="black")
            draw.text((width + 10, 230), name[99:132], font=font, fill="black")
        else:
            ui.notify("Name is too long lengt:" + str(len(name)))

        draw.text((50, 300), str(serial), font=font, fill="black")

        #new_img.save(f"barcodes/{serial}_small.png")

        debug_print(new_img.size)

        middle_img = Image.new("RGB", (2156, 593), "white")
        middle_img.paste(new_img, (367, 38))
        #middle_img.save(f"barcodes/{serial}_mid.png")
                        
        big_img = Image.new("RGB", (2156, 728), "white")
        big_img.paste(new_img, (612, 38))
        #big_img.save(f"barcodes/{serial}_big.png")

        pdf = FPDF()
        pdf.set_line_width(0.5)
        pdf.add_page()
        pdf.rect(10, 10, 51.5, 14.5)
        pdf.image(new_img, x=0, y=10, w=51.5, keep_aspect_ratio=True)
        pdf.rect(10, 70, 80, 22)
        pdf.image(middle_img, x=0, y=70, w=80, keep_aspect_ratio=True)
        pdf.rect(10, 150, 80, 27)
        pdf.image(big_img, x=0, y=150, w=80, keep_aspect_ratio=True)
        pdf.output(f"barcodes/{serial}.pdf")

    def download_selected_qr_codes(self, id_list):
        """
        Downloads a QR code for each item with the given IDs.

        :param ids: The IDs of the items.
        :type ids: List[int]
        """
        for serial in id_list:
            shutil.copy(f"barcodes/{serial['id']}.pdf", f"download_temp/{serial['id']}.pdf")
        ui.download(shutil.make_archive('labels', 'zip', 'download_temp'))
        for filename in os.listdir('download_temp'):
            os.remove(f"download_temp/{filename}")
    
    def save_uploaded_file(self, file):
        """
        Saves an uploaded file to the inventory.

        :param file: The uploaded file.
        :type file: File
        """
        try:
            with open(file.name, 'wb') as f:
                f.write(file.content.read())
            debug_print("Uploaded File")
            self.update_data()
            for id in self.running_data['id']:
                if not os.path.exists(f"barcodes/{id}.png"):
                    self.gen_qr_code(id, self.running_data.loc[self.running_data['id']==id, 'Name'].values[0])
        except Exception as e:
            ui.notify('Error Uploading File!', category='error')
            debug_print(f"Error Uploading File! Error:{e}")

    def up_download_excel(self):
        """
        Uploads or downloads an Excel file with the inventory data. When Downloading it also exports the QR-Codes.
        """
        with ui.dialog() as dialog, ui.card():
            with ui.tabs() as tabs:
                ui.tab('up', label='Upload', icon='upload')
                ui.tab('down', label='Download', icon='download')
            with ui.tab_panels(tabs, value='up'):
                with ui.tab_panel('up'):
                    ui.upload(multiple=False, auto_upload=True, on_upload= lambda upload: self.save_uploaded_file(upload)).props('accept=.xlsx')
                with ui.tab_panel('down'):
                    ui.button('Download Excel', on_click=lambda: ui.download('Verbrauchsmaterial_ELab_TRGE.xlsx'))
                    #ui.button('Download QR-Codes', on_click=lambda: ui.download(shutil.make_archive('barcodes', 'zip', 'barcodes')))


        dialog.open()

    def run(self):
        """
        Starts the inventory management application.

        The application will run until it is manually stopped.
        """
        ui.run(port=80,title='CoTrack',dark=None)
        ui.open('/')
        #tl.start(block=False)

@tl.job(interval=timedelta(minutes=1))
def update():
    debug_print("Updating Data")
    inv.update_data()

inv = InventoryManager()

@ui.page('/')
def normal_view():
    """
    Displays the normal view of the inventory.
    """
    inv.table =  ui.table.from_pandas(inv.running_data).classes('w-full')
    inv.table.columns[1]['sortable'] = True
    inv.table.columns[0]['sortable'] = True
    with inv.table.add_slot('top-left'):
        inv.inputRef = ui.input(placeholder='Scanner').on('keydown.enter',lambda: (inv.update_availability(inv.inputRef.value, False), inv.inputRef.set_value(None))).props('type=search')
        inv.table.bind_filter_from(inv.inputRef, 'value')
        ui.button('Clear').on_click(lambda: (inv.inputRef.set_value(None)))
    with inv.table.add_slot('top-right'):
        with ui.link(target=editor_view):
            ui.button('Editor View')
    inv.table.set_fullscreen(True)
    inv.table.add_slot('body-cell-Available', '''
        <q-td key="Available" :props="props">
            <q-badge :color="props.value < true ? 'red' : 'green'">
                {{ props.value < true ? 'No' : 'Yes' }}
            </q-badge>
        </q-td>
        ''')

@ui.page('/editor')
def editor_view():
        """
        Displays the editor view of the inventory.
        """
        inv.table = ui.table.from_pandas(inv.running_data, selection='multiple').classes('w-full')
        inv.table.columns[1]['sortable'] = True
        inv.table.columns[0]['sortable'] = True
        with inv.table.add_slot('top-left'):
            inputRef = ui.input(placeholder='Search').on('keydown.enter',lambda: (inv.update_availability(inputRef.value, True), inputRef.set_value(None))).props('type=search')
            inv.table.bind_filter_from(inputRef, 'value')
            with inputRef.add_slot("append"):
                ui.icon('search')
        with inv.table.add_slot('top-right'):
            ui.button('Refresh',on_click=lambda: inv.update_data())
            ui.button('Upload/Download Excel', on_click=lambda: inv.up_download_excel())
            ui.button('Download QRs', on_click=lambda: inv.download_selected_qr_codes(inv.table.selected)).bind_enabled_from(inv.table, 'selected', backward=lambda val: bool(val))
            ui.button('Refill', on_click=lambda: (inv.update_availability(inv.table.selected, True), ui.update(inv.table))).bind_enabled_from(inv.table, 'selected', backward=lambda val: bool(val))
            #ui.button('Remove', on_click=lambda: (inv.delete_part(inv.table.selected))).bind_enabled_from(inv.table, 'selected', backward=lambda val: bool(val))
            with ui.link(target=normal_view):
                ui.button('Close View')

        #with inv.table.add_slot('bottom'):
        #    with inv.table.row():
        #        with inv.table.cell():
        #            ui.button(on_click=lambda: (
        #                inv.add_part(new_name.value),
        #                new_name.set_value(None),
        #            ), icon='add').props('flat fab-mini')
        #        with inv.table.cell():
        #            new_name = ui.input('Name')
        inv.table.set_fullscreen(True)
        inv.table.add_slot('body-cell-Available', '''
            <q-td key="Available" :props="props">
                <q-badge :color="props.value < true ? 'red' : 'green'">
                    {{ props.value < true ? 'No' : 'Yes' }}
                </q-badge>
            </q-td>
            ''')

inv.run() 