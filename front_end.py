import dash_mantine_components as dmc
from dash import Dash
import help_wordle as wordle
from dash_extensions import Keyboard
from dash_extensions.enrich import Input, Output, State, html

app = Dash()

allowed_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

app.layout = html.Div([
    Keyboard(
        captureKeys=['Enter', 'Delete', 'Backspace'] + allowed_letters,
        id='keyboard',
    ),
    dmc.MantineProvider(
        dmc.Center(
            style={'height': 500, 'width': '100%'},
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Group(
                                    children=[
                                        dmc.Button(
                                            '',
                                            id=f'{j+1},{i+1}',
                                            color='gray',
                                            #variant='outline',
                                            w=50,
                                            h=50
                                        ) for i in range(5)
                                    ]
                                ) for j in range(6)
                            ]
                        ),
                        dmc.List(
                            id='word_list',
                            type='ordered',
                            size='md',
                            withPadding=False
                        )
                    ]
                )
            ]
        )
    ),
    html.Div(['' for i in range(6)], id='guesses', style={'display':'none'}),
    html.Div('', id='guess', style={'display':'none'}),
    html.Div(1, id='row', style={'display':'none'}),
    html.Div(['gray' for i in range(30)], style={'display':'none'}),
    html.Div(00000, id='colors', style={'display':'none'}),
    html.Div(wordle.open_words('words.txt'), id='words', style={'display':'none'})
])

@app.callback(
    Output('guesses', 'children'),
    Output('guess', 'children'),
    Output('row', 'children'),
    Input('keyboard', 'n_keydowns'),
    Input('row', 'children'),
    Input('guess', 'children'),
    Input('guesses', 'children'),
    State('keyboard', 'keydown'),
)
def track_typing(_, row, guess, guesses, event):
    if event:
        key = event['key']
        if key in allowed_letters:
            guesses[row-1] = guesses[row-1] + key.upper()
        if key in ['Delete', 'Backspace']:
            guesses[row-1] = guesses[row-1][:-1]
        if key == 'Enter':
            if len(guesses[row-1]) == 5:
                guess = guesses[row-1]
                row += 1
    return guesses, guess, row

@app.callback(
    Output('word_list', 'children'),
    Input('words', 'children')
)
def update_suggestions(words):
    if len(words) >= 10:
        return [dmc.ListItem(f'{word}') for word in words[0:10]]
    else:
        return [dmc.ListItem(f'{word}') for word in words]

@app.callback(
    Output('words', 'children'),
    Input('words', 'children'),
    Input('guess', 'children'),
    Input('row', 'children'),
    [Input(f'{j+1},{i+1}', 'color') for j in range(6) for i in range(5)],
)
def update_words(words, guess, row, 
                color11, color12, color13, color14, color15, color21, color22, color23, color24, color25, 
                color31, color32, color33, color34, color35, color41, color42, color43, color44, color45,
                color51, color52, color53, color54, color55, color61, color62, color63, color64, color65):
    row = row-1
    color_list = [
        color11, color12, color13, color14, color15, color21, color22, color23, color24, color25, 
        color31, color32, color33, color34, color35, color41, color42, color43, color44, color45,
        color51, color52, color53, color54, color55, color61, color62, color63, color64, color65
        ]
    color_string = ''.join(color_list[5*(row-1):5*row]).replace('gray', '0').replace('yellow', '1').replace('green', '2')
    colors = [int(num) for num in color_string]
    poss = []
    for word in words:
        word_colors = wordle.color_word(word.lower(), guess.lower())
        if word_colors == colors:
            poss.append(word)
    if poss:
        words = wordle.sort_words(poss)
    return words

@app.callback(
    [Output(f'{j+1},{i+1}', 'children') for j in range(6) for i in range(5)],
    Input('guesses', 'children')
)
def update_tiles(guesses):
    tiles = ['' for j in range(6) for i in range(5)]
    tile_num = 0
    for guess in guesses:
        while len(guess) < 5:
            guess += ' '
        for letter in guess:
            if letter != ' ':
                tiles[tile_num] = letter  
            tile_num += 1
    return tiles

color_cycle = ['gray', 'yellow', 'green']

@app.callback(
    [Output(f'{j+1},{i+1}', 'n_clicks') for j in range(6) for i in range(5)],
    [Output(f'{j+1},{i+1}', 'color') for j in range(6) for i in range(5)],
    Output('colors', 'children'),
    Input('row', 'children'),
    [Input(f'{j+1},{i+1}', 'n_clicks') for j in range(6) for i in range(5)],
    [Input(f'{j+1},{i+1}', 'color') for j in range(6) for i in range(5)]
)
def color_tiles(row, clicks11, clicks12, clicks13, clicks14, clicks15, clicks21, clicks22, clicks23, clicks24, clicks25,
                clicks31, clicks32, clicks33, clicks34, clicks35, clicks41, clicks42, clicks43, clicks44, clicks45,
                clicks51, clicks52, clicks53, clicks54, clicks55, clicks61, clicks62, clicks63, clicks64, clicks65,
                color11, color12, color13, color14, color15, color21, color22, color23, color24, color25, 
                color31, color32, color33, color34, color35, color41, color42, color43, color44, color45,
                color51, color52, color53, color54, color55, color61, color62, color63, color64, color65):
    click_list = [
        clicks11, clicks12, clicks13, clicks14, clicks15, clicks21, clicks22, clicks23, clicks24, clicks25,
        clicks31, clicks32, clicks33, clicks34, clicks35, clicks41, clicks42, clicks43, clicks44, clicks45,
        clicks51, clicks52, clicks53, clicks54, clicks55, clicks61, clicks62, clicks63, clicks64, clicks65
        ]
    color_list = [
        color11, color12, color13, color14, color15, color21, color22, color23, color24, color25, 
        color31, color32, color33, color34, color35, color41, color42, color43, color44, color45,
        color51, color52, color53, color54, color55, color61, color62, color63, color64, color65
        ]
    for i, click in enumerate(click_list):
        if click == 1:
            if i//5 == row-1:
                if color_cycle.index(color_list[i]) == len(color_cycle)-1:
                    color_list[i] = color_cycle[0]
                else:
                    color_list[i] = color_cycle[color_cycle.index(color_list[i])+1]
    colors = list('00000')
    for i, color in enumerate(color_list[5*(row-1):5*row]):
        if color == 'yellow':
            colors[i] = '1'
        elif color == 'green':
            colors[i] = '2'
    return [0]*30 + color_list + [''.join(colors)]

if __name__ == '__main__':
    app.run(debug=True)
