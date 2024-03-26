#!/usr/bin/env python3
import time
import json

from nicegui import ui

columns = [
    {'name': 'id', 'label': 'ID', 'field': 'id', 'required' : True},
    {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True},
    {'name': 'descr', 'label': 'Description', 'field': 'descr'},
]
rows = [
    {'id': 10000000, 'name': 'Part 1', 'descr':'', 'flagged':False},
    {'id': 10000001, 'name': 'Part 2', 'descr':'', 'flagged':False},
    {'id': 10000002, 'name': 'Part 3', 'descr':'', 'flagged':False},
    {'id': 10000003, 'name': 'Part 4', 'descr':'', 'flagged':False},
    {'id': 10000004, 'name': 'Part 5', 'descr':'', 'flagged':False},
    {'id': 10000005, 'name': 'Part 6', 'descr':'', 'flagged':False},
    {'id': 10000006, 'name': 'Part 7', 'descr':'', 'flagged':False},
]

with ui.table(columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-full') as table:
    with table.add_slot('top-left'):
        with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
            ui.icon('search')
    with table.add_slot('top-right'):
        ui.button('Remove', on_click=lambda: table.remove_rows(*table.selected)) \
            .bind_enabled_from(table, 'selected', backward=lambda val: bool(val))
    with table.add_slot('bottom'):
        with table.row():
            with table.cell():
                ui.button(on_click=lambda: (
                    table.add_rows({'id': time.time(), 'name': new_name.value, 'descr': new_descr.value}),
                    new_name.set_value(None),
                    new_descr.set_value(None),
                ), icon='add').props('flat fab-mini')
            with table.cell():
                new_name = ui.input('Name')
            with table.cell():
                new_descr = ui.input('Description')
    table.set_fullscreen(True)

class DataHandler:
    def __init__(self) -> None:
        pass

    def saveData(rows:list,columns:list)->bool:
        saveData = {
            'rows': rows,
            'columns': columns,
        }
        print(saveData)
        try:
            with open('data.json', 'w') as saveFile:
                json.dump(saveData, saveFile)
        except Exception as e:
            ui.notify('Error Saving File!', category='error')
            return False
        return True
ui.run()