import cv2
import numpy as np
from pathlib import Path
import dlib
from imutils import face_utils
from imutils.face_utils import FaceAligner


print("hello")

def main(): 
	print("hello2")

	detector = dlib.get_frontal_face_detector()
	shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
	face_aligner = FaceAligner(shape_predictor, desiredFaceWidth=200)

	#face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

	video_capture = cv2.VideoCapture(0)


	name = input("Enter name of person: ")
	dir = get_dir(name)
	capture(dir, detector, video_capture, face_aligner, name)


	video_capture.release()
	cv2.destroyAllWindows()



def get_dir(name): 
	path = Path('images')
	print(path)
	directory = Path(path / f"{name}")
	directory.mkdir(exist_ok=True, parents=True)

	return directory


def capture(directory, detector, video_capture, face_aligner, name): 
	number_of_images = 0
	MAX_NUMBER_OF_IMAGES = 50
	count = 0

	while number_of_images < MAX_NUMBER_OF_IMAGES:
		ret, frame = video_capture.read()

		frame = cv2.flip(frame, 1)

		frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		#faces = face_cascade.detectMultiScale(frame, 1.3, 5)
		faces = detector(frame_gray)
		if len(faces) == 1:
			face = faces[0]
			(x, y, w, h) = face_utils.rect_to_bb(face)
			face_img = frame_gray[y-50:y + h+100, x-50:x + w+100]
			face_aligned = face_aligner.align(frame, frame_gray, face)

			if count == 5:
				new_image = Path(directory)
				new_image.mkdir(exist_ok=True, parents=True)

				cv2.imwrite((str(new_image)+"/"+str(name+str(number_of_images)+'.jpg')), face_aligned)
				number_of_images += 1
				count = 0
			print(count)
			count+=1
			

		cv2.imshow('Video', frame)

		if(cv2.waitKey(1) & 0xFF == ord('q')):
			break


if __name__ == '__main__': 
	main()