#!/usr/bin/env python

#==========================================================#
import pandas as pd
import tkinter as tk
import requests as rq
from tkinter import filedialog  as fd
import tkinter.messagebox as msgb
import finplot as fplt
#import logging as log    <- Only for debugging
import multiprocessing as mp
import os
from datetime import datetime as dt
#==========================================================#

# defining globals...
APIKEY = 'FQKOBP9I7N44ZTJK'  # The API key
CPU_CORES = mp.cpu_count()   # No of CPU cores in the CPU

#==========================================================#
class GUI:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        self.root.title('Stock Data')
        self.root.configure(bg='#000')
        self.txflag = False
        
        tk.Label(self.root, text='Stock Data - Time Series', bg='#000', fg='#ff0',
                 font=('roboto', 25)).pack(side=tk.TOP, pady=15)
        
        fr = tk.Frame(self.root, bg='#000')
        fr.pack(side=tk.TOP, pady=25, fill='both', padx=50)
        
        tk.Label(fr, text='Enter API key. Leave blank to use existing...', bg='#000', fg='#fff',
                 font=('roboto', 15)).grid(row=0, column=0, pady=20)
        
        self.keyentry = tk.Entry(fr, width=30, bg='#fff',  fg='#000', font=('roboto', 12))
        self.keyentry.grid(row=1, column=0, pady=10, ipady=11)
        
        tk.Label(fr, text='Select the text file having symbol names...', bg='#000', fg='#fff',
                 font=('robot', 15)).grid(row=0, column=1, pady=20, padx=35)
        
        self.fbtn = tk.Button(fr, text='Select Input File', font=('roboto', 15),
                              bg='#fff', fg='#000', width=20,
                              command=self.getInputFile)
        self.fbtn.grid(row=1, column=1, pady=10, padx=35, ipady=7)
        self.fbtn.bind('<Enter>', lambda args: self.btnconf(2))
        self.fbtn.bind('<Leave>', lambda args: self.btnconf(3))
        
        tk.Label(fr, text='Interval', bg='#000', fg='#fff',
                 font=('roboto', 15)).grid(row=0, column=2, padx=30)
        
        self.intervar = tk.StringVar(self.root)
        self.intervar.set('30min')
        self.opt = tk.OptionMenu(fr, self.intervar,
                                 '1min', '5min', '15min', '30min', '60min')
        self.opt.config(width=8, font=('roboto', 15), bg='#fff', fg='#000')
        self.opt.grid(row=1, column=2, ipady=4, padx=30)
        
        tk.Label(fr, text='Output Size', bg='#000', fg='#fff',
                 font=('roboto', 15)).grid(row=0, column=3, padx=42)

        self.opsize = tk.StringVar(self.root)
        self.opsize.set('compact')
        self.optsize = tk.OptionMenu(fr, self.opsize,
                                 'compact', 'full')
        self.optsize.config(width=8, font=('roboto', 15), bg='#fff', fg='#000')
        self.optsize.grid(row=1, column=3, ipady=4, padx=42)

        self.btn = tk.Button(self.root, text='Fire Up!', width=30, font=('roboto', 20),
                             command=self.fireUp, bg='#000', fg='#ff0')
        self.btn.pack(padx=0, pady=60, ipady=26)
        self.btn.bind('<Enter>', lambda args: self.btnconf(1))
        self.btn.bind('<Leave>', lambda args: self.btnconf(0))
        
        self.root.update_idletasks()
        msgb.showinfo('Important', 'Please read this short guide before using the program.'+
                      '\nHit ENTER if you\'ve already read this guide.\n'
                      '\n    1. If you have an API key with you, enter it in input box given. You'+
                      '\n       can leave it blank and default key '+APIKEY+ ' will be used.\n'+
                      '\n    2. You must select an input text file using \'select input\' button.'+
                      '\n       The file should have symbol names, one symbol name per line. '+
                      '\n       Unless you have a premium API key, make sure there aren\'t too'+
                      '\n       many symbol names in the file as access to the API is limited.\n'+
                      '\n    3. The interval selection should not be confused with the update'+
                      '\n       frequency. The update frequency will always be 60min no matter'+
                      '\n       what the interval is. The interval represents the difference'+
                      '\n       between two consecutive data values.Selecting a lower value '+
                      '\n       for interval will result in a more dense graph and more data'+
                      '\n       points.\n'+
                      '\n    4. Output size is recommended to be kept at compact level. '+
                      '\n       Compact size will return most recent 100 entries. Selecting'+
                      '\n       full will return data for last significant days which can get'+
                      '\n       up to 14 days to a few months depending on API response.'+
                      '\n\nWhen you decide to terminate the app, you MUST close all the opened'+
                      '\ngraphs before closing the main GUI. It is to ensure that the data is'+
                      '\nnot corrupted because the background processes must be stopped'+
                      '\nbefore exiting the main app.')
        
        self.keyentry.focus_set()

    def btnconf(self, signal):
        if signal == 1:
            self.btn.config(bg='#ff0', fg='#000', text='Light up the candles!')
        if signal == 0:
            self.btn.config(bg='#000', fg='#ff0', text='Fire Up!')
            
        if signal == 2:
            self.fbtn.config(bg='#000', fg='#ff0', text='Browse')
            
        if signal == 3:
            self.fbtn.config(bg='#fff', fg='#000', text='Select Input File')

    def getInputFile(self):
        self.txtaddr = fd.askopenfilename(title='Select text file containing symbols',
                                     defaultextension='*.txt',
                                     filetypes=[('Text files', '*.txt'), ('All Files', '*.*')])
        if not self.txflag:
            if self.txtaddr is None or not self.txtaddr.endswith('.txt'):
                msgb.showinfo('Incorrect input', 'The graphs will not be loaded as you either did not select a valid'+
                              ' Text file or you cancelled the file selection. Click on the button again to select a '+
                              'valid symbol text file.')
                return
        
        self.txflag = True
        
        self.fbtn.config(text=os.path.basename(self.txtaddr))
        self.fbtn.bind('<Enter>', donothing)
        self.fbtn.bind('<Leave>', donothing)
        
        
        with open(self.txtaddr) as f:
            self.symbols = f.read().split('\n')
            
    def fireUp(self):
        global APIKEY
        self.inter = self.intervar.get()
        self.ops = self.opsize.get()
        api = self.keyentry.get()
        
        if api=='':
            pass
        elif api != '' and api.isupper():
            APIKEY = api
        
        else:
            msgb.showerror('Invalid API key', 'Please check the API key again. If you\'re'+
                           ' not sure what\'s wrong with your API key, try leaving the API input'+
                           ' blank to use default API key, and check with the API provider to know why the API'+
                           ' does not work.')
            return
        
        if not self.txflag:
            
            msgb.showerror('No Text file selected', 'You did not select the input text file '+
                           'containing symbol names.')
            return
        
        self.fbtn.config(state=tk.DISABLED)
        self.keyentry.config(state=tk.DISABLED)
        self.opt.config(state=tk.DISABLED)
        self.optsize.config(state=tk.DISABLED)
        self.btn.bind('<Enter>', donothing)
        self.btn.bind('<Leave>', donothing)
        self.btn.configure(state=tk.DISABLED, bg='#000', fg='#ff0', text='Fire Up!')
        
        tk.Label(self.root, font=('roboto', 13), bg='#000', fg='#fff',
                 text='Your graphs will appear soon!\nThe graphs will update automatically '+
                 'every 60 minutes. Be sure to check Network Connectivity if they don\'t.\n'+
                 'Do NOT close this window without closing all the opened graphs.\n'+
                 'doing so might corrupt the data files. If you want to change any values now,'+
                 '\nsimply close all graphs, then close this window and re-run the script.'+
                 '\n\nScript started at '+str(dt.today().hour)+':'+str(dt.today().minute)).pack()
        
        
        self.setProcess()
        
            
    def setProcess(self):
        self.processes = []
        
        for symbol in self.symbols:
            
            p = mp.Process(target=worker, args=(symbol, self.inter, self.ops, csvlock, [],), daemon=True)
            p.start()
            self.processes.append(p)
            

#==========================================================#
            
def worker(sym, inter, ops, csvlock, plots):
    def drawplot():
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=%s&apikey=%s&datatype=csv&outputsize=%s'%(sym, inter, APIKEY, ops)
        res = rq.get(url)
        
        with open(sym+'temp.csv', 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)
        
        try:
            data = pd.read_csv(sym+'temp.csv', parse_dates=['timestamp'], index_col='timestamp').sort_index()
            
        except:
            return # if API does not respond with valid data.
        
        update_csv(sym, data)
        
        candles = data[['open','close','high','low']]

        volumes = data[['open','close','volume']]
            
        if len(plots) == 0:
            plots.append(fplt.volume_ocv(volumes, ax=ax2))
            plots.append(fplt.candlestick_ochl(candles, ax=ax))
            
        else:
            plots[0].update_data(volumes)
            plots[1].update_data(candles)
            
    #==============================================#
    
    ax, ax2 = fplt.create_plot(sym+' Stock Time Series - '+inter+' - '+ops, rows=2)    
    drawplot()
    fplt.timer_callback(drawplot, 3600.0)   # draw the graphs every 60 mins (3600 secs)
    fplt.show()

#=========================================================#
def update_csv(sym, df):
    df = df.reset_index()
    
    if os.path.exists(os.path.join(os.getcwd(), sym+'stockData.csv')):
        cmb = pd.concat([pd.read_csv(sym+'stockData.csv'), df])
        cmb['timestamp'] = cmb['timestamp'].astype(str)
        cmb = cmb.drop_duplicates(subset=['timestamp'])
        cmb.to_csv(sym+'stockData.csv', index=False)
        
    elif not os.path.exists(os.path.join(os.getcwd(), sym+'stockData.csv')):
        df.to_csv(sym+'stockData.csv', index=False)
        
    try:
        os.remove(sym+'temp.csv')
    except:
        pass
    
def donothing(*args):
    pass

#=========================================================#
if __name__ == '__main__':
    csvlock = mp.Lock()
    win = tk.Tk()
    g = GUI(win)
    win.mainloop()
#=========================================================#