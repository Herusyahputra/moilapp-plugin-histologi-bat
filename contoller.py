from src.plugin_interface import PluginInterface
from PyQt6.QtWidgets import QWidget
from .ui_main import Ui_Form
from skimage.segmentation import watershed
from scipy import ndimage
import os
import cv2
import numpy as np
import imutils

class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.image = None
        self.set_stylesheet()

    def set_stylesheet(self):
        # This is set up style label on bonding box ui
        self.ui.label_ori_1.setStyleSheet(self.model.style_label())
        self.ui.label_1_1.setStyleSheet(self.model.style_label())
        self.ui.label_1_2.setStyleSheet(self.model.style_label())
        self.ui.label_1_3.setStyleSheet(self.model.style_label())
        self.ui.label_1_4.setStyleSheet(self.model.style_label())
        self.ui.label_ori_2.setStyleSheet(self.model.style_label())
        self.ui.label_3.setStyleSheet(self.model.style_label())

        self.ui.label_2_1.setStyleSheet(self.model.style_label())
        self.ui.label_2_2.setStyleSheet(self.model.style_label())
        self.ui.label_2_3.setStyleSheet(self.model.style_label())
        self.ui.label_2_4.setStyleSheet(self.model.style_label())
        self.ui.label_13.setStyleSheet(self.model.style_label())
        self.ui.label_14.setStyleSheet(self.model.style_label())

        self.ui.label.setStyleSheet(self.model.style_label())
        self.ui.label_2.setStyleSheet(self.model.style_label())
        self.ui.label_4.setStyleSheet(self.model.style_label())
        self.ui.label_5.setStyleSheet(self.model.style_label())
        self.ui.label_6.setStyleSheet(self.model.style_label())
        self.ui.label_7.setStyleSheet(self.model.style_label())
        self.ui.label_9.setStyleSheet(self.model.style_label())
        self.ui.label_10.setStyleSheet(self.model.style_label())
        self.ui.label_11.setStyleSheet(self.model.style_label())
        self.ui.label_12.setStyleSheet(self.model.style_label())
        self.ui.label_15.setStyleSheet(self.model.style_label())

        self.ui.line.setStyleSheet(self.model.style_line())
        self.ui.line_2.setStyleSheet(self.model.style_line())
        self.ui.line_3.setStyleSheet(self.model.style_line())
        self.ui.line_4.setStyleSheet(self.model.style_line())
        self.ui.line_5.setStyleSheet(self.model.style_line())

        # This is set up style button on bonding box ui
        self.ui.load_img1.setStyleSheet(self.model.style_pushbutton())
        self.ui.multi_1.setStyleSheet(self.model.style_pushbutton())
        self.ui.params_1.setStyleSheet(self.model.style_pushbutton())
        self.ui.clear_1.setStyleSheet(self.model.style_pushbutton())

        self.ui.load_img2.setStyleSheet(self.model.style_pushbutton())
        self.ui.multi_2.setStyleSheet(self.model.style_pushbutton())
        self.ui.params_2.setStyleSheet(self.model.style_pushbutton())
        self.ui.clear_2.setStyleSheet(self.model.style_pushbutton())

        # This is set up to connect to other function to make action on ui
        self.ui.load_img1.clicked.connect(self.load_image_1)
        self.ui.multi_1.clicked.connect(self.cam_params)
        self.ui.params_1.clicked.connect(self.cam_params)
        self.ui.clear_1.clicked.connect(self.clearImg)

        # This is set up to connect to other function to make action on ui
        self.ui.load_img2.clicked.connect(self.load_image_2)
        self.ui.multi_2.clicked.connect(self.cam_params)
        self.ui.params_2.clicked.connect(self.cam_params)
        self.ui.clear_2.clicked.connect(self.cam_params)

    def clearImg(self):
        self.ui.label_1_4

    def load_image_1(self):
        file = self.model.select_file()
        if file:
            if file:
                self.moildev = self.model.connect_to_moildev(parameter_name=file)
            self.image_original = cv2.imread(file)
            self.image = self.image_original.copy()
            # self.app(file)
            self.show_to_ui_img_1(file)

    def load_image_2(self):
        file = self.model.select_file()
        if file:
            if file:
                self.moildev = self.model.connect_to_moildev(parameter_name=file)
            self.image_original = cv2.imread(file)
            self.image = self.image_original.copy()
            self.show_to_ui_img_2(file)

    def show_to_ui_img_1(self, img_path):
        self.model.show_image_to_label(self.ui.label_ori_1, self.image, 500)
        img = cv2.imread(img_path)

        gray = self.convert_grayscale(img)
        self.model.show_image_to_label(self.ui.label_1_1, gray, 300)

        thresh = self.thresholding(gray)
        self.model.show_image_to_label(self.ui.label_1_2, thresh, 300)

        morpho = self.morphological_opr(thresh)
        self.model.show_image_to_label(self.ui.label_1_3, morpho, 300)

        dir_img_save_path = "./plugins/moilapp-plugin-histologi-bat/saved_img/HFD"

        cells, cell_count = self.count_cells(img_path, dir_img_save_path)
        self.model.show_image_to_label(self.ui.label_1_4, cells, 300)
        self.ui.label_14.setText(f"{cell_count}")

        self.crop_img(dir_img_save_path)

    def show_to_ui_img_2(self, img_path):
        self.model.show_image_to_label(self.ui.label_ori_2, self.image, 500)
        img = cv2.imread(img_path)

        gray = self.convert_grayscale(img)
        self.model.show_image_to_label(self.ui.label_2_1, gray, 300)

        thresh = self.thresholding(gray)
        self.model.show_image_to_label(self.ui.label_2_2, thresh, 300)

        morpho = self.morphological_opr(thresh)
        self.model.show_image_to_label(self.ui.label_2_3, morpho, 300)

        dir_img_save_path = "./plugins/moilapp-plugin-histologi-bat/saved_img/ND"

        cells, cell_count = self.count_cells(img_path, dir_img_save_path)
        self.model.show_image_to_label(self.ui.label_2_4, cells, 300)
        self.ui.label_15.setText(f"{cell_count}")

        self.crop_img(dir_img_save_path)

    def cam_params(self):
        self.model.form_camera_parameter()

    def convert_grayscale(self, img):
        # konversi warna gambar jadi abu-abu
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def thresholding(self, gray):
        # konversi gambar abu-abu jadi biner
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        return thresh

    def morphological_opr(self, thresh):
        # membersihkan gambar biner atau menghilangkan noise pada objek
        img_mop = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1)))
        img_mop = cv2.morphologyEx(img_mop, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))

        # perhitungan jarak transformasi
        D = ndimage.distance_transform_edt(img_mop)

        # mencari nalai lokal max di jarak tranformasi gambar menggunakan numpy
        local_max_coords = np.argwhere((D == ndimage.maximum_filter(D, size=20)) & (D > 0))

        # konversi kodinat lokal max ke bool
        localMax = np.zeros(D.shape, dtype=bool)
        localMax[tuple(local_max_coords.T)] = True

        markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]

        # untuk labeling gambar https://pyimagesearch.com/2015/11/02/watershed-opencv/
        labels = watershed(-D, markers, mask=img_mop)

        return D


    def count_cells(self, image_path, dir_path):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_mop = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1)))
        img_mop = cv2.morphologyEx(img_mop, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
        D = cv2.distanceTransform(img_mop, cv2.DIST_L2, 5)
        localMax = np.zeros(D.shape, dtype=np.uint8)
        localMax[thresh == 255] = 255
        markers = cv2.connectedComponents(localMax)[1]
        markers = markers + 1
        markers[thresh == 0] = 0
        markers = cv2.watershed(image, markers)

        cell_count = len(np.unique(markers)) - 1
        # self.ui.label_14.setText(f"{cell_count}")

        for label in np.unique(markers):
            if label == -1:
                continue
            mask = np.zeros(gray.shape, dtype="uint8")
            mask[markers == label] = 255
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            c = max(cnts, key=cv2.contourArea)
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (255, 61, 139), 1, 5)
            cv2.putText(image, "{}".format(label), (int(x) - 4, int(y)), cv2.FONT_HERSHEY_COMPLEX, 0.45, (0, 0, 155), 1)

        # dir_path = "./plugins/moilapp-plugin-histologi-bat/saved_img"
        img_save_path = f"{dir_path}/count_cell.png"

        if (os.path.exists(f"{dir_path}")):
            if (os.path.isdir(f"{dir_path}")):
                os.system(f"rm -R {dir_path}")
                os.mkdir(f"{dir_path}")
                cv2.imwrite(img_save_path, image)
        else:
            os.mkdir(f"{dir_path}")

        return image, cell_count

    def crop_img(self, dir_path):
        # jumlah potongan gambar
        jmh_crop = 8

        # gambar yg sudah di labeling
        img = cv2.imread(f"{dir_path}/count_cell.png")
        height, width = img.shape[:2]

        # menghitung ukuran gambar untuk dipotong
        row_start, row_end = self.count_crop_img(jmh_crop, height)
        col_start, col_end = self.count_crop_img(jmh_crop, width)

        for i in range(0, jmh_crop):
            for j in range(0, jmh_crop):
                # memotong gambar
                cropped = img[row_start[i]:row_end[i], col_start[j]:col_end[j]]

                # menyimpan gambar
                cv2.imwrite(f"{dir_path}/img_crop_{i + 1}_{j + 1}.png", cropped)

    def count_crop_img(self, jmh_crop, size_img):
        start_crop = []
        end_crop = []

        # perhitungan ukuran potongan gambar
        size_crop = int(size_img / jmh_crop)
        for i in range(0, jmh_crop + 1):
            # fungsi append untuk menambahkan nilai list
            end_crop.append(i * size_crop)
            start_crop.append(end_crop[i] - size_crop)

        # fungsi pop untuk menhapus list index 0
        start_crop.pop(0)
        end_crop.pop(0)
        return start_crop, end_crop


class HistologiBat(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "This is a plugins application"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()

