from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

model = load_model('./model/best.h5')

class GameUI(tk.Frame):
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self,master)
        self.master.title('オセロ')
        self.state = State()
        self.next_action = pv_mcts_action(model, 0.0)
        self.c = tk.Canvas(self,width=320,height=320,highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()
        self.on_draw()
    def turn_of_human(self,event):
        if self.state.is_end():
            self.state = State()
            self.on_draw()
            return
        if not self.state.is_first_player():
            return
        x = event.x//40
        y = event.y//40
        if x<0 or x>7 or y<0 or y>7:
            return
        action = x+y*8
        legal_actions = self.state.legal_actions()
        if legal_actions == [64]:
            action = 64
        if action != 64 and not action in legal_actions:
            return
        self.state = self.state.next(action)
        self.on_draw()
        self.master.after(1,self.turn_of_ai)
    def turn_of_ai(self):
        if self.state.is_end():
            return
        action = self.next_action(self.state)
        self.state = self.state.next(action)
        self.on_draw()
    def draw_pieces(self, index, first_player):
        x = (index%8)*40+5
        y = (index//8)*40+5
        if first_player:
            self.c.create_oval(x, y, x+30, y+30, width=1.0, outline='#000000', fill='#C2272D')
        else:
            self.c.create_oval(x, y, x+30, y+30, width=1.0, outline='#000000', fill='#FFFFFF')
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0,0,320,320,width=0.0,fill='#C69C6C')
        for i in range(1,10):
            self.c.create_line(0,i*40,320,i*40,width=1.0,fill='#000000')
            self.c.create_line(i*40,0,i*40,320,width=1.0,fill='#000000')
        for i in range(64):
            if self.state.pieces[i]:
                self.draw_piece(i,self.state.is_first_player())
            if self.state.enemy_pieces[i]:
                self.draw_piece(i,not self.state.is_first_player())
f = GameUI(model=model)
f.pack()
f.mainloop()