import os,time
import numpy as np


def get_table():
    columns = []
    printable = " "*20+"|"
    while 1:
        new_column = input("Agregar columna (q para salir) -->")
        if new_column != "q":
            columns.append(new_column)
            printable += "{:20}|".format(new_column)
        else:
            printable += "\n"
            os.system("cls")
            break
    
    table,row = {},[]
    table["columns"] = columns
    print(printable+"\n")
    print()

    

    while 1:
        print("vueltaaaa")
        new_row = input("Nueva fila -->")
        printable += "{:20}|".format(new_row)
        os.system("cls")
        for i in columns:
            print(printable+"\n")
            row_value = input(f"{i} para {new_row}  -->")
            
            row.append(row_value)
            printable += "{:20}|".format(row_value)
            os.system("cls")
        
        table[new_row] = row
        another_row = input("Otra fila (y/n)?").lower()
        if another_row == "y":
            row = []
            printable += "\n"
            os.system("cls")
        else:
            print("Obteniendo tabla!")
            return table

def table():
    table = get_table()

    result = """
    <table class="table">
        <thead>
            <tr>
            <th scope="col">#</th>
    """
    body = "<tbody>"
    
    print(result)

    for k,v in table.items():
        if k == "columns":
            for c in table["columns"]:
                result += f"<th scope='col'>{c}</th>\n"
            result += "\n</tr>\n</thead>\n"
        else:
            body += f"\n<tr>\n<th scope='row'>{k}</th>"
            for c in v:
                body += f"<td>{c}</td>"
            body += "</tr>"
    body += "\n</tbody>\n</table>"
    return result + body
    


        

    


print(table())


 

"""
<table class="table">
  <thead>
    <tr>
      <th scope="col">#</th>
      <th scope="col">First</th>
      <th scope="col">Last</th>
      <th scope="col">Handle</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>Mark</td>
      <td>Otto</td>
      <td>@mdo</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>Jacob</td>
      <td>Thornton</td>
      <td>@fat</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td colspan="2">Larry the Bird</td>
      <td>@twitter</td>
    </tr>
  </tbody>
</table>
"""