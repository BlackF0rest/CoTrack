#!/usr/bin/env python3
import json

from nicegui import ui

def saveData(saveData:dict)->bool:
    try:
        with open('data.json', 'w') as saveFile:
            json.dump(saveData, saveFile)
        ui.notify('Saved')
    except Exception as e:
        ui.notify('Error Saving File!', category='error')
        return False
    return True

def readData()->dict:
    try:
        with open('data.json', 'r') as loadFile:
            data = json.load(loadFile)
        return data
    except Exception as e:
        ui.notify('Error Loading File!', category='error')

def genNewSerial()->int:
    lastID = max(item["id"] for item in runningData["rows"])
    return  lastID + 1
    

runningData = readData()

@ui.page("/editor")
def editorView():
    with ui.table(columns=runningData['columns'], rows=runningData['rows'], selection='multiple').classes('w-full') as table:
        with table.add_slot('top-left'):
            with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                ui.icon('search')
        with table.add_slot('top-right'):
            ui.button('Remove', on_click=lambda: (table.remove_rows(*table.selected), 
                    saveData(runningData))) \
                .bind_enabled_from(table, 'selected', backward=lambda val: bool(val))
            with ui.link(target=normalView):
                ui.button('Close View')

        with table.add_slot('bottom'):
            with table.row():
                with table.cell():
                    ui.button(on_click=lambda: (
                        table.add_rows({'id': genNewSerial(), 'name': new_name.value, 'descr': new_descr.value, 'flagged' : False}),
                        new_name.set_value(None),
                        new_descr.set_value(None),
                        saveData(runningData)
                    ), icon='add').props('flat fab-mini')
                with table.cell():
                    new_name = ui.input('Name')
                with table.cell():
                    new_descr = ui.input('Description')
        table.set_fullscreen(True)
        table.add_slot('body-cell-flag', '''
            <q-td key="flagged" :props="props">
                <q-badge :color="props.value < True ? 'red' : 'green'">
                    {{ props.value }}
                </q-badge>
            </q-td>
            ''')

def scannerInput(input, tableRef):
    print("8 Inputs")
    #TODO flag it
        
@ui.page('/')
def normalView():
    with ui.table(columns=runningData['columns'], rows=runningData['rows']).classes('w-full') as table:
        with table.add_slot('top-left'):
            inputRef = None
            inputRef = ui.input(placeholder='Scanner', on_change=lambda v: (scannerInput(v.value, table), inputRef.set_value(None),inputRef.update(), ui.notify("Scanned")) if v.value != None and len(v.value)==8 else inputRef.update()).bind_value(table, 'filter')
        with table.add_slot('top-right'):
            with ui.link(target=editorView):
                ui.button('Editor View')
        table.set_fullscreen(True)
        table.add_slot('body-cell-flag', '''
            <q-td key="flagged" :props="props">
                <q-badge :color="props.value < True ? 'red' : 'green'">
                    {{ props.value }}
                </q-badge>
            </q-td>
            ''')

ui.run()
editorView()