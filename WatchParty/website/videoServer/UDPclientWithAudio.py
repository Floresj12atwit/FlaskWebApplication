import cv2, imutils, socket
import numpy as np
import time, os
import base64
import threading, wave, pyaudio, pickle, struct
BUFF_SIZE= 65536

     
def runClient():  #IP will most likely need to be passed in
    BREAK = False
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '127.0.0.1' # This will need to be dynamically updated somehow use the IP made in the server
    print(host_ip)
    port = 4444
    message = b'TAKE THIS! :D'
    
    client_socket.sendto(message, (host_ip, port))
    
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as executor:
        #executor.submit(video_stream, client_socket)
        executor.submit(audio_stream, host_ip, port, BREAK)
        executor.submit(video_stream, client_socket)
      

def video_stream():
    
        cv2.namedWindow('Received Video')
        cv2.moveWindow('Receiving Video', 10,360)
        fps,st,frames_to_count,cnt = (0,0,20,0)
        while True:
                packet,_ = client_socket.recvfrom(BUFF_SIZE)
                data = base64.b64decode(packet,' /')
                npdata = np.fromstring(data, dtype = np.uint8)

                frame = cv2.imdecode(npdata,1)
                frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                cv2.imshow("RECEIVING VIDEO",frame)	        
                key = cv2.waitKey(1) & 0xFF
              
                if key == ord('q'):
                        client_socket.close()
                        os._exit(1)
                        break
                if cnt == frames_to_count:
                        try:
                                fps = round(frames_to_count/(time.time()-st))
                                st=time.time()
                                cnt=0
                        except:
                                pass
                cnt+=1
        

        client_socket.close()
        cv2.destroyAllWindows()

def audio_stream(host_ip, port, BREAK):
       
        p = pyaudio.PyAudio()
        CHUNK = 1024
        stream = p.open(format=p.get_format_from_width(2),
					channels=2,
					rate=44100,
					output=True,
					frames_per_buffer=CHUNK)
        #create socket for audio stream (TCP)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_address = (host_ip, port-1)      #chooses the next port over for the audio stream 
        print('server listening at',socket_address)
        client_socket.connect(socket_address) 
        print("CLIENT CONNECTED TO",socket_address)
        data = b""
        payload_size = struct.calcsize("Q")
        while True:
               try:
                        while len(data) < payload_size:
                               packet = client_socket.recv(4*1024)
                               if not packet: break
                               data += packet
                        packed_msg_size = data[:payload_size]
                        data = data[payload_size:]
                        msg_size = struct.unpack("Q", packed_msg_size)[0]
                        while len(data) < msg_size:
                               data += client_socket.recv(4*1024)
                        frame_data = data[:msg_size]
                        data = data[msg_size:]
                        frame = pickle.loads(frame_data)
                        stream.write(frame)
               except:
                      
                      break
        client_socket.close()
        print('Audio closed', BREAK)
        os._exit(1)

runClient()