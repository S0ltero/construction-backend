import openpyxl
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment

from .models import Element


def insert_cells(ws: Worksheet, ws_row: int, cells: dict):
    """Insert cell value on row of `ws_row`, getted by column letter from `cells`"""
    for column in (ws.iter_cols(min_row=ws_row, min_col=1, max_col=8, max_row=ws_row)):
        for cell in column:
            letter = cell.column_letter
            if not cells.get(cell.column_letter):
                continue
            cell.value = cells[letter]["value"]
            cell.alignment = cells[letter].get("alignment", None)

    ws_row += 1

    return ws, ws_row


def foreman(project):
    stages = project["stages"]
    ws1_row = 1
    ws2_row = 1
    ws3_row = 1

    ws1_index = 1
    ws2_index = 1
    ws3_index = 1

    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "Список работ (Бригадир)"
    ws2 = wb.create_sheet("Список материалов (Бригадир)")
    ws3 = wb.create_sheet("Список общий (Бригадир)")

    for stage in stages:
        ws1.merge_cells(f"A{ws3_row}:H{ws3_row}")
        ws2.merge_cells(f"A{ws3_row}:H{ws3_row}")
        ws3.merge_cells(f"A{ws3_row}:H{ws3_row}")
        ws1[f"A{ws3_row}"] = ws2[f"A{ws3_row}"] = ws3[f"A{ws3_row}"] = f"Этап {stage['order']}. {stage['title']}"
        ws1[f"A{ws3_row}"].alignment = Alignment(horizontal="center")
        ws2[f"A{ws3_row}"].alignment = Alignment(horizontal="center")
        ws3[f"A{ws3_row}"].alignment = Alignment(horizontal="center")
        ws1_row += 1
        ws2_row += 1
        ws3_row += 1

        cells = {
            "B": {"value": "Наименование"}, 
            "C": {"value": "Кол-во"},
            "D": {"value": "ед-изм"}
        }
        ws1, ws1_row = insert_cells(ws1, ws1_row, cells)
        ws2, ws2_row = insert_cells(ws2, ws2_row, cells)
        ws3, ws3_row = insert_cells(ws3, ws3_row, cells)

        constructions = stage["constructions"]
        for count_construction, construction in enumerate(constructions, start=1):
            cells = {
                "A": {"value": f"{count_construction}. Конструкция"},
                "B": {"value": construction["title"]},
                "D": {"value": construction["measure"]}
            }
            ws1, ws1_row = insert_cells(ws1, ws1_row, cells)
            ws2, ws2_row = insert_cells(ws2, ws2_row, cells)
            ws3, ws3_row = insert_cells(ws3, ws3_row, cells)

            elements = construction["elements"]
            for element in elements:
                cells = {
                        "A": {
                            "value": None,
                            "alignment": Alignment(horizontal="right")
                        },
                        "B": {
                            "value": element["title"]
                        },
                        "C": {
                            "value": element["count"],
                            "alignment": Alignment(horizontal="right")
                        },
                        "D": {
                            "value": element["measure"]
                        }
                    }
                if element["type"] == Element.Type.JOB:
                    cells["A"]["value"] = f"{count_construction}.{ws1_index}"
                    ws1, ws1_row = insert_cells(ws1, ws1_row, cells)
                    ws1_index += 1
                elif element["type"] == Element.Type.MATERIAL:
                    cells["A"]["value"] = f"{count_construction}.{ws2_index}"
                    ws2, ws2_row = insert_cells(ws2, ws2_row, cells)
                    ws2_index += 1

                cells["A"]["value"] = f"{count_construction}.{ws3_index}"
                ws3, ws3_row = insert_cells(ws3, ws3_row, cells)
                ws3_index +=1 

            count_construction += 1

    return wb
