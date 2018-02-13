import xlsxwriter


def generate_xlsx(bewertungs_threads):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('Bewertungen.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Iterate over the data and write it out row by row.
    for index, element in bewertungs_threads:
        worksheet.write(row, col, index + 1)
        worksheet.write(row, col + 1, element.durchschnitt)
        worksheet.write(row, col + 2, element.stimmen)
        worksheet.write(row, col + 3, element.url)
        worksheet.write(row, col + 4, element.name)
        row += 1

    workbook.close()
