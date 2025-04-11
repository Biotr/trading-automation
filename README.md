## trading-autiomation
A bot that listens for **Trading View strategy alerts** and **Discord signals** on defined channel, then execute real trades on a Binance exchange

### Getting started
1. First of all you have to clone repository and install requirements.
```
git clone https://github.com/Biotr/trading-automation.git
cd trading-automation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Next edit `config.py` file as its described inside.
3. Start server on 8000 by executing command.
```
fastapi dev main.py
```
- now if you want get data from tradingview you need tunneling such as `ngrok`
```
ngrok http 8000
```
  In Trading View alert setting in messege paste json located in `tradingview/alert.json`.  
  Enable webhook and paste ngrok `https://...` link.

- to get discord signals you need tampermonkey and paste `discord/tampermonkey.js` file.  
  Edit 7 line by pasting discord channel https link.


### Known issues
- for now in `tampermonkey.js` message fetching is limited
- sometimes getting `Margin is insufficient` error

