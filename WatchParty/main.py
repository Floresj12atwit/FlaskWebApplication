from website import create_app
from flask_socketio import SocketIO, emit, join_room, leave_room



app, socketio = create_app()

# events happen HERE
# solution could be to simply run the app in views? OR have events run here 

if __name__ == '__main__':  #If we run this file the line below will be executed (The web server)
    socketio.run(app, debug=True)     #Starts up a web server, everytime a change is made to python code the web server is going to be re run_

    '''
    This website base taken from this youtube video as we were not completely familiar with 
    web development we wanted to implement it in a website

    https://www.youtube.com/watch?v=dam0GPOAvVI&t=334s
    Github for the youtube video code shown:
    https://github.com/techwithtim/Flask-Web-App-Tutorial
    l
    '''