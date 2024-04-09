import kivy
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.label import Label
from kivy.core.window import Window
from PIL import Image
from io import BytesIO
import base64
from kivy.clock import Clock
import pytesseract
import os, cv2, imutils
import numpy as np

os.environ['TESSDATA_PREFIX'] = r"OCR/tessdata"
pytesseract.pytesseract.tesseract_cmd = r"OCR/tesseract.exe"

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical")
        self.camera = Camera(play=True, resolution=(340, 220))
        self.camera.bind(on_tex=self.capture_frame)
        layout.add_widget(self.camera)

        self.text_label = Label(text='',size_hint_y=None, height = 50, font_size = 20, color = "white")
        layout.add_widget(self.text_label)

        self.frame_number = 0       
        Clock.schedule_interval(self.capture_frame, 1)

        return layout

    def capture_frame(self, dt):
        self.frame_number += 1

        texture = self.camera.texture
        if texture:
            image = Image.frombytes('RGBA', texture.size, texture.pixels)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            data_uri = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')
            self.process_image(data_uri)

    def process_image(self, data_uri):
        image_data = base64.b64decode(data_uri.split(',')[1])

        image_array = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        ratio = image.shape[0] / 500.0
        orig = image.copy()
        image = imutils.resize(image, height=500)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 75, 200)

        contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            zoom_crop = image[y:y + h, x:x + w]
            contour_array = np.squeeze(c.astype(np.float32))
            x, y, w, h = cv2.boundingRect(contour_array)
            zoom_img = cv2.resize(zoom_crop, (image.shape[1], image.shape[0]))

            extracted_text = pytesseract.image_to_string(zoom_img)
            image = cv2.rotate(zoom_img, cv2.ROTATE_90_COUNTERCLOCKWISE)

            self.show_result(image, extracted_text)
        else:
            print("No contours found")

    def show_result(self, zoom_img, text):
        zoom_img_array = cv2.cvtColor(zoom_img, cv2.COLOR_BGR2RGB)

        texture = Texture.create(size=(zoom_img_array.shape[1], zoom_img_array.shape[0]), colorfmt='rgb')
        texture.blit_buffer(zoom_img_array.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        if not hasattr(self, 'image_widget'):
            self.image_widget = KivyImage()
            self.root.add_widget(self.image_widget)

        self.image_widget.texture = texture
        if not hasattr(self, 'label'):
            self.label = Label()
            self.root.add_widget(self.label)
        self.label.text = text


if __name__ == '__main__':
    MainApp().run()
