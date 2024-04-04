#!/usr/bin/env python3
import qrcode
import threading, traceback
import time
import pandas as pd

from nicegui import ui

table = None

def automaticRefresh(delay):
    nextTime = time.time() + delay
    while True:
        time.sleep(max(0,nextTime-time.time()))
        try:
            updateAvailability()
        except Exception:
            traceback.print_exc()
        nextTime += (time.time()-nextTime)//delay*delay+delay

def saveData(saveData:pd.DataFrame)->bool:
    try:
        saveData.to_excel(excel_writer='Bauteileschrank.xlsx', sheet_name='Tabelle', index=False)
    except Exception as e:
        ui.notify('Error Saving File!', category='error')
        return False
    return True

def readData()->pd.DataFrame:
    try:
        dataframe = pd.read_excel('Bauteileschrank.xlsx', sheet_name='Tabelle', dtype={'Available':bool})
        return dataframe
    except Exception as e:
        ui.notify('Error Loading File!', category='error')

def genNewSerial()->int:
    global runningData
    lastID = runningData['id'].max()
    return  lastID + 1

def updateAvailability(input=None, setting:bool=False):
    global table
    global runningData
    if input != None:
        if type(input) == str:
            runningData.loc[runningData['id']==int(input), 'Available'] = setting
        elif type(input) == list:
            for inp in input:
                runningData.loc[runningData['id']==inp['id'], 'Available'] = setting
        saveData(runningData)
    table.update_rows(runningData.loc[:].to_dict('records'))

def genBarcode(serialNum):
    #code = Code128(str(serialNum))
    outputFile = 'barcodes/' + str(serialNum)
    #code.save(str(outputFile))
    img = qrcode.make(serialNum)
    img.save(outputFile+'.png')
    #ui.download(outputFile+'.png')

def addRow(name, descr):
    global runningData
    newSerial = genNewSerial()
    runningData.loc[len(runningData)] = [newSerial,True,name,descr]
    genBarcode(newSerial)
    updateAvailability()

def deleteRow(input):
    global table
    global runningData
    if input != None:
        for inp in input:
            runningData = runningData[runningData['id']!=int(inp['id'])]
        saveData(runningData)
    table.update_rows(runningData.loc[:].to_dict('records'))
    table.update()

def downloadQrCodes(ids):
    for id in ids:
        filename = "barcodes/"+str(id['id'])+".png"
        ui.download(filename)

runningData = readData()

@ui.page("/editor")
def editorView():
    global runningData
    global table
    table = ui.table.from_pandas(runningData, selection='multiple').classes('w-full')
    with table.add_slot('top-left'):
        inputRef = ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').on('keydown.enter',lambda: (updateAvailability(inputRef.value, False),inputRef.set_value(None)))
        with inputRef.add_slot("append"):
            ui.icon('search')
    with table.add_slot('top-right'):
        ui.button('Refresh&Save',on_click=lambda: updateAvailability())
        ui.button('QR-Code/s', on_click=lambda: downloadQrCodes(table.selected)).bind_enabled_from(table, 'selected', backward=lambda val: bool(val))
        ui.button('Refilled', on_click=lambda: updateAvailability(table.selected, True)).bind_enabled_from(table, 'selected', backward=lambda val: bool(val))
        ui.button('Remove', on_click=lambda: (deleteRow(table.selected))).bind_enabled_from(table, 'selected', backward=lambda val: bool(val))
        with ui.link(target=normalView):
            ui.button('Close View')

    with table.add_slot('bottom'):
        with table.row():
            with table.cell():
                ui.button(on_click=lambda: (
                    addRow(new_name.value, new_descr.value),
                    new_name.set_value(None),
                    new_descr.set_value(None),
                    saveData(runningData)
                ), icon='add').props('flat fab-mini')
            with table.cell():
                new_name = ui.input('Name')
            with table.cell():
                new_descr = ui.input('Description')
    table.set_fullscreen(True)
    table.add_slot('body-cell-Available', '''
        <q-td key="Available" :props="props">
            <q-badge :color="props.value < true ? 'red' : 'green'">
                {{ props.value < true ? 'No' : 'Yes' }}
            </q-badge>
        </q-td>
        ''')
        
@ui.page('/')
def normalView():
    global table
    global runningData
    table =  ui.table.from_pandas(runningData).classes('w-full')
    with table.add_slot('top-left'):
        inp = None
        inputRef = ui.input(placeholder='Scanner').bind_value(table, 'filter').on('keydown.enter',lambda: (updateAvailability(inputRef.value, False),inputRef.set_value(None)))
    with table.add_slot('top-right'):
        with ui.link(target=editorView):
            ui.button('Editor View')
    table.set_fullscreen(True)
    table.add_slot('body-cell-Available', '''
        <q-td key="Available" :props="props">
            <q-badge :color="props.value < true ? 'red' : 'green'">
                {{ props.value < true ? 'No' : 'Yes' }}
            </q-badge>
        </q-td>
        ''')
        
threading.Thread(target=lambda: automaticRefresh(30))

ui.run(port=80,title='CoTrack',dark=None)
editorView()