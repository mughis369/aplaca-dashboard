#!/usr/bin/env python3

from flask import Flask, render_template, request, url_for, redirect
from app import utils, record, stream
import config
import logging


import threading
class StreamThread(threading.Thread):

     def run(self):
          logging.info("Stream system thread")

          try:
               while 1:
                   stream.start()
                   time.sleep(1)
          except KeyboardInterrupt:
               GPIO.cleanup()



def create_app():

    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
    
    app = Flask(__name__)
    app.config.from_object(config.PRODUCTION_CONFIG)
    StreamThread().start()

    # region routes

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/account')
    def account():
        details = utils.get_account()
        return render_template('account.html', details=details)

    @app.route('/orders', methods=["GET", "POST", "PUT"])
    def orders():
        msg, orders = utils.handle_order_query(
            method=request.method, 
            order_id=request.json, 
            form=request.form
        )
        return render_template('orders.html', tables=orders, msg=msg)

    @app.route('/market_watch', methods=['POST', 'GET'])
    def market_watch():

        header, records = utils.get_records(request.form)
        last_update = utils.get_last_update()

        if request.method == 'GET':
            print("GET")
            return render_template('watch.html', headers=header, table=records, last_update=last_update)
        elif request.method == 'POST':
            print("POST")
            return render_template('table.html', headers=header, table=records, last_update=last_update)
        else:
            return "Undefined header recieved"
    # endregion


    return app




# if __name__=="__main__":
#     app.config.from_object(config.DEBUG_CONFIG)

#     scheduler = APScheduler()
#     scheduler.init_app(app)
#     scheduler.start()

#     app.run(use_reloader=False)