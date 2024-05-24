# Project Title

tradingview-binance-bot converts alerts from tradingview strategies to real orders in Binance.

## Description

Bot uses alerts and webhook to send json with order properties. ngrok https link is forwarding to localhost on the same port as flask works. Python script remove last opened order and then opening position with half of your account balance.


https://github.com/Biotr/tradingview-binance-bot/assets/51881112/61e284b2-2342-4668-8cf2-1ba7cfdda9c8


## Getting Started

### Dependencies

* Flask
* python-binance
* ngrok
* Trading view Essential (free 30 days trial)

### Installing

* Get a cross-platform application that allows you to expose local web servers to the internet such as ngrok (recommended).
* Get Binance API_KEY, API_SECRET and run app.py on the same port as ngrok.
* Paste json file to alert message.
* Paste ngronk http link to webhook property.

### Executing program

* Run ngrok
  ```
  ngrok.exe http 5000
  ```
* Run flask
  ```
  flask run --port=5000  
  ```
* Turn on alert
## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details
