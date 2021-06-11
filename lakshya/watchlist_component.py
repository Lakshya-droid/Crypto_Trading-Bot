import tkinter as tk
import typing

from encdec import decr
from models import *

from autocomplete_widget import Autocomplete
from scrollable_frame import ScrollableFrame

from database import WorkspaceData
import hashlib

import dateutil.parser
import time
from urllib.parse import urlencode
import hmac
import datetime
import pandas as pd
try:
    df1=pd.read_csv("inp.csv")
    mod=df1.dark[0]
    if mod=="on":
        from styling2 import *
    else :
        from styling1 import *
except:
    from styling2 import *


class Watchlist(tk.Frame):
    def __init__(self, binance_contracts: typing.Dict[str, Contract], bitmex_contracts: typing.Dict[str, Contract],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = WorkspaceData()

        self.binance_symbols = list(binance_contracts.keys())
        self.bitmex_symbols = list(bitmex_contracts.keys())

        self._commands_frame = tk.Frame(self, bg=BG_COLOR)
        self._commands_frame.pack(side=tk.TOP)

        self._table_frame = tk.Frame(self, bg=BG_COLOR)
        self._table_frame.pack(side=tk.TOP)

        self._binance_label = tk.Label(self._commands_frame, text="Binance", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self._binance_label.grid(row=0, column=0)

        self._binance_entry = Autocomplete(self.binance_symbols, self._commands_frame, fg=FG_COLOR, justify=tk.CENTER,
                                       insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self._binance_entry.bind("<Return>", self._add_binance_symbol)
        self._binance_entry.grid(row=1, column=0, padx=5)

        self._bitmex_label = tk.Label(self._commands_frame, text="Bitmex", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self._bitmex_label.grid(row=0, column=1)

        self._bitmex_entry = Autocomplete(self.bitmex_symbols, self._commands_frame, fg=FG_COLOR, justify=tk.CENTER,
                                      insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self._bitmex_entry.bind("<Return>", self._add_bitmex_symbol)
        self._bitmex_entry.grid(row=1, column=1)

        self.body_widgets = dict()

        self._headers = ["symbol", "exchange", "bid", "ask", "Interval","Graph","remove"]

        self._headers_frame = tk.Frame(self._table_frame, bg=BG_COLOR)

        self._col_width = 9

        # Creates the headers dynamically

        for idx, h in enumerate(self._headers):
            header = tk.Label(self._headers_frame, text=h.capitalize() if (h != "remove" or h!="Graph" or h!="Interval") else "", bg=BG_COLOR,
                              fg=FG_COLOR, font=GLOBAL_FONT, width=self._col_width)
            header.grid(row=0, column=idx)

        header = tk.Label(self._headers_frame, text="", bg=BG_COLOR,
                          fg=FG_COLOR, font=GLOBAL_FONT, width=2)
        header.grid(row=0, column=len(self._headers))

        self._headers_frame.pack(side=tk.TOP, anchor="nw")

        # Creates the table body

        self._body_frame = ScrollableFrame(self._table_frame, bg=BG_COLOR, height=250)
        self._body_frame.pack(side=tk.TOP, fill=tk.X, anchor="nw")

        # Add keys to the body_widgets dictionary, the keys represents columns or data related to a column
        # You could also have another logic: instead of body_widgets[column][row] have body_widgets[row][column]
        for h in self._headers:
            self.body_widgets[h] = dict()
            if h in ["bid", "ask"]:
                self.body_widgets[h + "_var"] = dict()

        self._body_index = 0

        # Loads the Watchlist symbols saved to the database during a previous session
        saved_symbols = self.db.get("watchlist")

        for s in saved_symbols:
            self._add_symbol(s['symbol'], s['exchange'])

    def _remove_symbol(self, b_index: int):

        for h in self._headers:
            self.body_widgets[h][b_index].grid_forget()
            del self.body_widgets[h][b_index]

    def _candle_graph(self,symbol: str, exchange: str,b_index):
        import requests
        import pandas as pd
        import plotly.graph_objects as go
        tick_interval =self.tick_var.get()

        market = symbol

        if exchange == "Binance":
            url = 'https://api.binance.com/api/v3/klines?symbol=' + market + '&interval=' + tick_interval
            data = requests.get(url).json()
            df = pd.DataFrame()
            for i in data:
                df = df.append([[datetime.datetime.fromtimestamp(int(i[0]) / 1000), float(i[1]), float(i[2]),
                                 float(i[3]), float(i[4]), float(i[5])]],
                               ignore_index=True)
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

        elif exchange == "Bitmex":
            data = dict()
            data['symbol'] = symbol
            data['partial'] = True
            data['binSize'] = tick_interval
            data['count'] = 500
            data['reverse'] = True
            headers = dict()
            expires = str(int(time.time()) + 5)
            headers['api-expires'] = expires
            df=pd.read_csv("inp.csv")
            headers['api-key'] = df.btpk[0]
            message = "GET" + "/api/v1/trade/bucketed" + "?" + urlencode(data) + expires if len(
                data) > 0 else "GET" + "/api/v1/trade/bucketed" + expires
            headers['api-signature'] = hmac.new(df.btsk[0].encode(),
                                                message.encode(), hashlib.sha256).hexdigest()
            data = requests.get("https://testnet.bitmex.com/api/v1/trade/bucketed", params=data, headers=headers).json()
            df= pd.DataFrame()
            for i in data:
                openp = i['open']
                high = i['high']
                low = i['low']
                close = i['close']
                volume = i['volume']
                df = df.append([[i['timestamp'], openp, high, low, close, volume]],ignore_index=True)
            df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']

        fig = go.Figure(
            data=[go.Candlestick(x=df['timestamp'], open=df["open"], high=df["high"], low=df["low"], close=df["close"],
                                 increasing_line_color= '#00CC00', decreasing_line_color= 'rgb(255,0,0)')], )
        fig.update_layout(
            title=f"{market}'s adjusted stock price",
            yaxis_title="Price ($)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgb(32,32,32)'

        )

        fig.show()


    def _add_binance_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.binance_symbols:
            self._add_symbol(symbol, "Binance")
            event.widget.delete(0, tk.END)

    def _add_bitmex_symbol(self, event):
        symbol = event.widget.get()

        if symbol in self.bitmex_symbols:
            self._add_symbol(symbol, "Bitmex")
            event.widget.delete(0, tk.END)

    def _add_symbol(self, symbol: str, exchange: str):

        b_index = self._body_index

        self.body_widgets['symbol'][b_index] = tk.Label(self._body_frame.sub_frame, text=symbol, bg=BG_COLOR,
                                                        fg=FG_COLOR_2, font=GLOBAL_FONT, width=self._col_width)
        self.body_widgets['symbol'][b_index].grid(row=b_index, column=0)

        self.body_widgets['exchange'][b_index] = tk.Label(self._body_frame.sub_frame, text=exchange, bg=BG_COLOR,
                                                          fg=FG_COLOR_2, font=GLOBAL_FONT, width=self._col_width)
        self.body_widgets['exchange'][b_index].grid(row=b_index, column=1)

        self.body_widgets['bid_var'][b_index] = tk.StringVar()
        self.body_widgets['bid'][b_index] = tk.Label(self._body_frame.sub_frame,
                                                     textvariable=self.body_widgets['bid_var'][b_index],
                                                     bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT, width=self._col_width)
        self.body_widgets['bid'][b_index].grid(row=b_index, column=2)

        self.body_widgets['ask_var'][b_index] = tk.StringVar()
        self.body_widgets['ask'][b_index] = tk.Label(self._body_frame.sub_frame,
                                                     textvariable=self.body_widgets['ask_var'][b_index],
                                                     bg=BG_COLOR, fg=FG_COLOR_2, font=GLOBAL_FONT, width=self._col_width)
        self.body_widgets['ask'][b_index].grid(row=b_index, column=3)
        if exchange=="Bitmex":
            self._all_timeframes = ["1m", "5m", "1h", "1d" ]
        else:
            self._all_timeframes = ["1m", "5m", "1h", "1d","1w","1M"]
        self.tick_var = tk.StringVar()
        self.tick_var.set(self._all_timeframes[0])
        self.body_widgets['Interval'][b_index] = tk.OptionMenu(self._body_frame.sub_frame,
                                                              self.tick_var,
                                                              *self._all_timeframes)
        self.body_widgets['Interval'][b_index].grid(row=b_index, column=4)
        self.body_widgets['Graph'][b_index] = tk.Button(self._body_frame.sub_frame, text="Y",
                                                       bg="darkblue", fg=FG_COLOR, font=GLOBAL_FONT,
                                                       command=lambda: self._candle_graph(symbol, exchange,b_index)
                                                       , width=11)
        self.body_widgets['Graph'][b_index].grid(row=b_index, column=5)


        self.body_widgets['remove'][b_index] = tk.Button(self._body_frame.sub_frame, text=" X",
                                                         bg="darkred", fg=FG_COLOR, font=GLOBAL_FONT,
                                                         command=lambda: self._remove_symbol(b_index), width=12)
        self.body_widgets['remove'][b_index].grid(row=b_index, column=6)


        self._body_index += 1

