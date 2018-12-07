import pyglet
import GameEngine

'''source code: https://bitbucket.org/pyglet/pyglet/src/
738617edac87a5e313414b790db412763983524e/examples/text_input.py?at=default&fileviewer=file-view-default'''

#function to load dictionary
def dictionary(x):
    data_file = pyglet.resource.file(x,'rt')
    listofwords = []
    for line in data_file:
        if line != '':
            words = line.rstrip()
            words = words.lower()
            listofwords.append(words)

    return listofwords

#assigning dictionary file to variables
Phi = dictionary('province.txt')
Ele = dictionary('element.txt')
Ani = dictionary('animal.txt')
Cou = dictionary('country.txt')
Col = dictionary('color.txt')

#creating textbox strep no.1
class rectangle(object):
    '''Draws a rectangle into a batch.'''
    def __init__(self, x1, y1, x2, y2, batch):
        self.vertex_list = batch.add(4, pyglet.gl.GL_QUADS, None,
            ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
            ('c4B', [250, 250, 250, 0] * 4)
        )

#textbox for user input
class TextWidget(object):
    def __init__(self, text, x, y, width, batch):
        self.document = pyglet.text.document.UnformattedDocument(text)
        self.document.set_style(0, len(self.document.text), 
            dict(color=(0, 0, 0, 255))
        )
        font = self.document.get_font()
        height = 20

        self.layout = pyglet.text.layout.IncrementalTextLayout(
            self.document, width, height, multiline=False, batch=batch)
        self.caret = pyglet.text.caret.Caret(self.layout)

        self.layout.x = x
        self.layout.y = y

        # Rectangular outline
        pad = 7
        self.rectangle = rectangle(x - pad, y - pad, 
                                   x + width + pad, y + height + pad, batch)

    def hit_test(self, x, y):
        return (0 < x - self.layout.x < self.layout.width and
                0 < y - self.layout.y < self.layout.height)



#main window
class Window(pyglet.window.Window):
   
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(600, 500,  style = Window.WINDOW_STYLE_TOOL, caption='Cherry D\' Apple')
        #highscore from game engine
        self.highscore = GameEngine.highscore()
        #compilation of all elements in the window
        self.batch = pyglet.graphics.Batch()
        #labels/texts
        self.labels = [
            pyglet.text.Label('CHERRY D\' APPLE', font_size =35, x=30, y=420, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),   
            pyglet.text.Label('Score = 0',font_size =20,  x=50, y=300, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Category:', font_size =20, x=50, y=250, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Letter : ',font_size =20, x=50, y=200, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('Press right key to start game',font_size =20, x = 50, y=70, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('High Score: ' + str(self.highscore),font_size =20, x=50, y=350, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch),
            pyglet.text.Label('' ,font_size =20, x=100, y=50, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch
                              )
        ]
        #textbox
        self.widgets = [
            TextWidget('', 50, 130, 350, self.batch),
        ]

        self.category = GameEngine.category()
        self.letter = GameEngine.letter(self.category)
        self.score = int(0)
        self.mistake = 0
        
        self.text_cursor = self.get_system_mouse_cursor('text')

        self.focus = None
        self.set_focus(self.widgets[0])

    '''def on_resize(self, width, height):
        super(Window, self).on_resize(width, height)
        for widget in self.widgets:
            widget.width = width - 110'''

    def on_draw(self):
        pyglet.gl.glClearColor(.75,.75,.75,1)
        self.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_mouse_cursor(self.text_cursor)
                break
        else:
            self.set_mouse_cursor(None)

    def on_mouse_press(self, x, y, button, modifiers):
        for widget in self.widgets:
            if widget.hit_test(x, y):
                self.set_focus(widget)
                break
        else:
            self.set_focus(None)

        if self.focus:
            self.focus.caret.on_mouse_press(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.focus:
            self.focus.caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_text(self, text):
        if self.focus:
            self.focus.caret.on_text(text)
    
    #modifies keyboard key roles
    def on_key_press(self, symbol, modifiers):
        #right key to load and start the game proper
        if symbol == pyglet.window.key.RIGHT:
            #if no. of mistakes reaches 5, game over, new game
            if self.mistake == 5:
                    GameEngine.save(self.score)
                    self.labels[5].delete()
                    self.highscore = GameEngine.highscore()
                    self.labels[5] = pyglet.text.Label('High Score: ' + str(self.highscore),font_size =20, x=50, y=350, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
                    self.mistake = 0
                    self.labels[6].delete()
                    self.labels[6] = pyglet.text.Label('' ,font_size =15, x=50, y=30, anchor_y='bottom',
                          color=(0, 0, 0, 255), batch=self.batch)
                    self.labels[4].delete()
                    self.labels[4] = pyglet.text.Label('Game Over : Press right key for new game',font_size =20, x=30, y=70, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)                   
                    self.score = 0
                    self.labels[1].delete()
                    self.labels[1] = pyglet.text.Label('Score = ' + str(self.score),font_size =20,  x=50, y=300, anchor_y='bottom',
                          color=(0, 0, 0, 255), batch=self.batch)

            else:
                category = self.category
                letter = self.letter
    
                self.widgets[0].document.text = ''
                self.labels[4].delete()
                self.labels[4] = pyglet.text.Label('Type your answer and press Enter',font_size =20, x=30, y=70, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)


                self.labels[2].delete()
                self.labels[2] = pyglet.text.Label('Category : ' + category, font_size =20, x=50, y=250, anchor_y='bottom',
                          color=(0, 0, 0, 255), batch=self.batch)

                self.labels[3].delete()
                self.labels[3] = pyglet.text.Label('Letter : ' + letter, font_size =20, x=50, y=200, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
                
                self.labels[6].delete()
                self.labels[6] = pyglet.text.Label('' ,font_size =15, x=100, y=30, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
        #for submission of answer
        if symbol == pyglet.window.key.ENTER:
            print(self.category,self.letter)
            category = self.category
            letter = self.letter
            player_input = self.widgets[0].document.text
            player_input = player_input.rstrip()

            #checks if the player input is correct
            if GameEngine.checker(player_input,category) == True:
                score = int(GameEngine.scoring(player_input))
                self.score += score
                self.labels[1].delete()
                self.labels[1] = pyglet.text.Label('Score = ' + str(self.score),font_size =20,  x=50, y=300, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
                self.labels[6].delete()
                self.labels[6] = pyglet.text.Label('Nice! Congrats!' ,font_size =15, x=120, y=30, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
            #if wrong...
            else:
                print('Oops!')
                self.mistake += 1
                print(self.mistake)
                self.labels[6].delete()
                self.labels[6] = pyglet.text.Label('Oh no! You have ' + str(self.mistake) + '/5 mistake/s' ,font_size =15, x=60, y=30, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)                    
                
            self.labels[4].delete()
            self.labels[4] = pyglet.text.Label('Press right key',font_size =20, x=100, y=70, anchor_y='bottom',
                              color=(0, 0, 0, 255), batch=self.batch)
            
            self.category = GameEngine.category()
            self.letter = GameEngine.letter(self.category)

    def on_text_motion(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion(motion)
      
    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    def set_focus(self, focus):
        if self.focus:
            self.focus.caret.visible = False
            self.focus.caret.mark = self.focus.caret.position = 0
        self.focus = focus
        if self.focus:
            self.focus.caret.visible = True
            self.focus.caret.mark = 0
            self.focus.caret.position = len(self.focus.document.text)

window = Window(resizable=False)
pyglet.app.run()