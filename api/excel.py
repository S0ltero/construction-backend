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
