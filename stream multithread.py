from imutils.video import VideoStream
from flask import Flask
from flask import render_template
from flask import Response
import threading
import cv2

app = Flask(__name__)
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
camera = VideoStream(src=0).start()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def capture_image():
    # grab global references to the video stream, output frame, and
	# lock variables
	global camera,outputFrame, lock
    # loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = camera.read()
		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame

def gen():
    while True:
        #ret, img = camera.read()
        ret= True
        if ret:
            test = cv2.imencode('.jpg', outputFrame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + test + b'\r\n')
        else:
            break

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # start a thread that will perform video capture
	t = threading.Thread(target=capture_image)
	t.daemon = True
	t.start()
    # start the flask app
	app.run(host='0.0.0.0', port=7070, debug=True,
		threaded=True, use_reloader=False)
# release the video stream pointer
camera.stop()