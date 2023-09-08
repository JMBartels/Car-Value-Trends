# -*- coding: utf-8 -*-
"""
@author: jbartels
"""

import numpy as np
from dash import Dash, html, Input, Output, dcc
import dash_daq as daq
import plotly.graph_objects as go


#Initial parameters 
conc = 0.1
MW = 100000
th_init = 1

#to prevent negative concentrations
def limit(num,minimum=0):
    if num <= minimum:
        return minimum
    else:
        return num

#Calculate the concentration profile for a given molecular weight, thickness, and drug concentration
#Returns the thickness and concentration profiles with 1 minute time steps, currently embed rate constant k (arb.)
def ConcProfile(MW, th_init, conc):
    k=5E5
    Rd = k*MW**(-3/2)
    t_half = 20
    
    t_length = 1001
    t = np.arange(0,t_length)

    
    Current_conc = 0
    conc_all = [0]
    th_all = []  

    
    for i in range(len(t)):
        if i == 0: #first cycle initiates the zero point 
            th_now = th_init
            th_prev = th_now
            th_all.append(th_now)

        else:
            th_now = limit(th_init - Rd*t[i]) #remove th by rate, determined by MW

            th_all.append(th_now) #make a list of th at each t

            loss_to_conc = Current_conc*(1/2)**((1)/t_half) # using (1) as the dt here

            Current_conc = loss_to_conc
            Current_conc = Current_conc + (th_prev-th_now)*conc #add conc from dissolved polymer
            conc_all.append(Current_conc)
            th_prev = th_now

    return conc_all, th_all




#Interactive Dashboard that recalculates and plots ConcProfile
# ___MAIN___
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(children=[
    
    html.Label('Membrane Design:', style={'color': 'lightblue', 'fontSize': 28}),
    html.Label(' '),
    daq.Knob(id='my-knob-1',
            value=100000,
            min=0,
            max=500000,
            label='Molecular weight (g/mol)',
            size=100,
            scale={'interval': 100000, 'labelInterval':1},
            ),
        
#     html.Br(),
    daq.Knob(id='my-knob-2',
            value=1,
            min=0,
            max=3,
            label='Thickness (a.u.)',
            style = {'font-size': 14, 'maxWidth': 300, 'width': 300},
            size =100,
            scale={'interval': 0.5, 'labelInterval':1}
            ), 
    
  
    daq.Knob(id='my-knob-3',
            value=1,
            min=0,
            max=3,
            label='Drug Concentration (g/cc)',
            size=100,
            scale={'interval': 0.5, 'labelInterval':1}
            )]),
    

    html.Div(children=[
        html.Br(),
        html.Div(id='plot1'),
        html.Br(),
#         html.Br(),
        html.Div(id='message1', style={'color': 'black', 'fontSize': 28, 'textAlign': 'center'}),
        html.Br(),
        html.Div(id='message2', style={'color': 'black', 'fontSize': 28, 'textAlign': 'center'})
    ])


], style={'display': 'flex', 'flex-direction':'row', "align-items":"flex-start"})




    
@app.callback([
Output('plot1', 'children'),
Output('message1', 'children'),
Output('message2', 'children')],
Input('my-knob-1', 'value'),
Input('my-knob-2','value'),
Input('my-knob-3', 'value'),
prevent_initial_call='initial_duplicate')

def render_plot(MW_value, th_value, conc_value):  

        conc_all, th_all = ConcProfile(MW_value, th_value, conc_value) #generate conc profile from inputs out as th_all and conc_all
        
        t_length = 1001
        t = np.arange(0,t_length)
        UCL = [0.06]*t_length
        LED = [0.013]*t_length
        
        Above_LED = np.subtract(np.array(conc_all), np.array(LED))
        firstIndex = next((index for index, value in enumerate(Above_LED) if value > 0), -1) #find index of first time conc becomes effective
        lastIndex = t_length - next((index for index, value in enumerate(reversed(Above_LED)) if value > 0), -1) #find index when conc stops being effective
        
        time_to_active = firstIndex
        time_spent_active = round((lastIndex - firstIndex)/24,2)

        msg1 = f'Onset of Action: {time_to_active} hours'
        msg2 = f'Duration of drug action: {time_spent_active} days'

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=conc_all, name='Active Conc.',line = dict(color='black', width=5)))
        fig.update_xaxes(range=[0, 480])
        fig.update_layout(
            autosize=False,
            width=750,height=500,
            xaxis_title="Time (hr)",
            yaxis_title="Active Drug Concentration",
            template='simple_white',
            font=dict(size=22))
        
        fig.add_trace(go.Scatter(x=t, y=UCL, name='Max Safety Conc.', line = dict(color='red', width=3, dash='dash')))
        fig.add_trace(go.Scatter(x=t, y=LED, name='Min. Effective Dose',line = dict(color='green', width=3, dash='dash')))
    
        return html.Div(dcc.Graph(figure=fig), id='plot1'), msg1, msg2



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)
