import csv
import numpy as np


class CsvTable(object):
    """Represents a 2d-Table like in Spreadsheet-Software and in .csv-Files"""

    def __init__(self, rowNames, columnNames, titleElement, dataIsNumeric=True):
        """
          rowNames: List of strings: Names of the rows, excluding the Title-Row
          columnNames: List of strings: Names of the columns, excluding the Title-Column
          titleElement: string: Text in the TopLeft-TitleCorner (what is in the Title-Column/Title-Row)
        """
        self.TitleElement = titleElement
        self.RowNames = rowNames
        self.ColumnNames = columnNames

        if(dataIsNumeric):
            self.Data = np.zeros([len(columnNames), len(rowNames)])
        else:
            raise "Not Implemented"

    def GetColumnByName(self, coulmnName):
        return self.Data[self.ColumnNames.index(coulmnName), :]

    def GetColumnsByName(self, predicateFunc):
        """ predicateFunc a function deciding whether this element shall be selected (string) -> bool"""
        return self.Data[
            [i for i, x in enumerate(self.ColumnNames) if predicateFunc(x)],
            :
        ]


def readFile(filename, newline='\n', delimiter=';', dataIsNumeric=True, defaultValue=0):
    with open(filename, newline=newline) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        csvList = list(reader)

    result = CsvTable(
        rowNames=list(map(lambda x: x[0], csvList[1:])),
        columnNames=csvList[0][1:],
        titleElement=csvList[0][0],
        dataIsNumeric=dataIsNumeric
    )

    for dataRow in range(len(result.RowNames)):
        for dataColumn in range(len(result.ColumnNames)):
            csvValue = csvList[dataRow+1][dataColumn+1]
            try:
                result.Data[dataColumn, dataRow] = float(csvValue)
            except ValueError:
                if(dataIsNumeric == False):
                    result.Data[dataColumn, dataRow] = csvValue
                else:
                    result.Data[dataColumn, dataRow] = defaultValue

    return result
