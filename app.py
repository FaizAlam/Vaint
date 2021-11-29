from flask import Flask, render_template, Response
import os
import cv2
import cam

app = Flask(__name__,template_folder='templates')

folderPath = 'header'
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    cam1 = cam.VideoCamera(overlay_image=overlayList)

    while True:
        frame = cam1.get_frame(overlay_image=overlayList)
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

    
@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)

