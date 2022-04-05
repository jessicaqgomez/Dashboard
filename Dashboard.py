from dash import Dash, dash_table
import pandas as pd
from sqlalchemy import create_engine
import datetime

class DashboardNetoffice():
    def __init__(self):
        self.db = create_engine('postgresql://sugaruser:8JbJF0As&&T3t@54.156.158.155:6432/sugardb')
        self.df = pd.read_sql('select * from "RegresionNetoffice"', con=self.db)
        self.app = Dash(__name__)
        #app.layout = dash_table.DataTable(df.to_dict('records'),[{"name":i,"id":i} for i in df.columns],filter_action='native')
    def get_data(self):
        table = self.df.to_dict('records')
        comprobantes = ['numero_nota_credito', 'numero_factura', 'numero_recibo', 'numero_ingreso', 'numero_egreso',
                        'numero_orden_pago', 'numero_nota_debito', 'numero_factura_proveedor']
        lista = []
        temp = {}
        Comprobantes = ""
        for i in table:
            for key, value in i.items():
                if value != '' and key not in comprobantes:

                    if key == 'execution_date':
                        temp[key] = value.date()
                    elif key == 'execution_duration_minutes':
                        hours, minutes = divmod(value, 3600)
                        minutes, seconds = divmod(minutes, 60)
                        result = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)
                        temp[key] = result
                    else:
                        temp[key] = value
                elif key in comprobantes and value != '' and value is not None:
                    Comprobantes = Comprobantes  + str(key) + ": " + str(value)+ " | "
                    temp["comprobantes"] = Comprobantes.strip("|").strip().rstrip(" | ")

            #print(temp)
            #print("-------------------------------------------")
            lista.append(temp)
            temp = {}
            Comprobantes = ""
        return lista
    def get_columns(self):
        columnas = [
            {'name': 'id', 'id': 'id', 'type': 'numeric'},
            {'name': 'scenario', 'id': 'scenario', 'type': 'text'},
            {'name': ' fecha de ejecución ', 'id': 'execution_date', 'type': 'datetime'},
            {'name': 'status', 'id': 'status', 'type': 'text'},
            {'name': 'tiempo de duración', 'id': 'execution_duration_minutes', 'type': 'numeric'},
            {'name': 'comprobantes', 'id': 'comprobantes', 'type': 'text'},
            {'name': 'journal id', 'id': 'journal_id', 'type': 'text'},
            {'name': 'ambiente', 'id': 'ambiente', 'type': 'text'},
            {'name': 'base de datos', 'id': 'base_de_datos', 'type': 'text'},
        ]
        return columnas

if __name__ == '__main__':
    Dash = DashboardNetoffice()
    data = Dash.get_data()
    columns = Dash.get_columns()
    Dash.app.layout = dash_table.DataTable(data,columns=columns,filter_action='native', style_data_conditional=[
        {
            'if': {
                'column_id': 'status',
                'filter_query': '{status} eq "PASS"',

            },
            'backgroundColor': '#bbff54'
        },
        {
            'if': {
                'column_id': 'status',
                'filter_query': '{status} eq "FAIL"',

            },
            'backgroundColor': '#fd7057'
        },
        {
            'if': {
                'column_id': 'status',
                'filter_query': '{status} eq "NOT RUN"',

            },
            'backgroundColor': '#f9dd46'
        },

    ])
    Dash.app.run_server(debug=True)
