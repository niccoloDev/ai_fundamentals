from webapp import app, socketio

# Checks if the run.py file has executed directly and not imported
if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="0.0.0.0")
    # app.run(debug=True)
    