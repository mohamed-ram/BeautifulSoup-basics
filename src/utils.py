
def append_to_column(column, data_to_append):
    if column:
        column.append(data_to_append)
    else:
        column.append("None")


# clear all data.
def clear_data(data):
    for col, value in data.items():
        data[col] = []
