

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import pafy
import humanize
import urllib.request
from urllib.request import Request, urlopen




FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"Download_Manager.ui"))


class Mainapp(QMainWindow , FORM_CLASS):



    def __init__(self , parent=None):

        try :
            super(Mainapp,self).__init__(parent)
            QMainWindow.__init__(self)
            self.setupUi(self)
            self.Hanle_UI()
            self.Handle_Buttons()


        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)


    def Hanle_UI(self):


        try:
            self.setWindowTitle('Abouseif Downloader')
            self.setFixedSize(714,350)

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)

    def Handle_Buttons(self):

        try :
            self.pushButton.clicked.connect(self.Download)
            self.pushButton_2.clicked.connect(self.Handle_Browse)
            self.pushButton_10.clicked.connect(self.Get_youtube_video)
            self.pushButton_8.clicked.connect(self.Save_browse)
            self.pushButton_9.clicked.connect(self.Save_browse)
            self.pushButton_3.clicked.connect(self.Download_youtube_video)
            self.pushButton_7.clicked.connect(self.Playlist_download)


        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)


    def Handle_Browse(self):

        try :

            save_place  =QFileDialog.getSaveFileName(self,caption="Save As",directory=".",filter="All Files(*.*)")
            text = str(save_place)
            name = (text[2:].split(',')[0].replace("'",''))
            self.lineEdit_2.setText(name)

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)

    def Handle_Progress_files(self,blocknum,blocksize,totalsize):

        try:

            read = blocknum * blocksize
            if totalsize > 0 :
                percent = read * 100 / totalsize
                self.progressBar.setValue(percent)
                QApplication.processEvents()

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)

    def Download(self):
        url =self.lineEdit1.text()
        Save_location = self.lineEdit_2.text()


        try:
            urllib.request.urlretrieve(url,Save_location,self.Handle_Progress_files)
        except Exception as e:
            msg = str(e)
            QMessageBox.warning(self,"Error",msg)
            return
        QMessageBox.information(self,"100% Complete","Download Completed !")
        self.progressBar.setValue(0)
        self.lineEdit1.setText('')
        self.lineEdit_2.setText('')


    def Save_browse(self):


        try:
            save = QFileDialog.getExistingDirectory(self,"Select download directory")
            self.lineEdit_7.setText(save)
            self.lineEdit_6.setText(save)

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)



    def Get_youtube_video(self):

        try:

            video_link = self.lineEdit1_9.text()
            v = pafy.new(video_link)
            st = v.allstreams
            print(st)
            for s in st :
                size = humanize.naturalsize(s.get_filesize())
                data = '{} {} {} {}'.format(s.mediatype , s.extension , s.quality , size)
                self.comboBox_2.addItem(data)

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)

    def Download_youtube_video(self):
        try:

            video_link = self.lineEdit1_9.text()
            save_location=self.lineEdit_7.text()
            v = pafy.new(video_link)
            st = v.allstreams
            quality =self.comboBox_2.currentIndex()
            down =st[quality].download(filepath=save_location)
            QMessageBox.information(self,"Success","Download Completed")
            self.lineEdit1_9.setText('')
            self.lineEdit_7.setText('')
            self.comboBox_2.clear()

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)

    def Playlist_download(self):

        try:
            playlist_URL = self.lineEdit1_5.text()
            save_location=self.lineEdit_6.text()
            playlist =pafy.get_playlist(playlist_URL)
            videos = playlist['items']
            os.chdir(save_location)
            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))
            else:
                os.mkdir(str(playlist['title']))
                os.chdir(str(playlist['title']))

            for video in videos :
                p = video['pafy']
                best =p.getbest(preftype='mp4')
                best.download()
                QMessageBox.information(self,"Success" , "Download Completed !")
                self.lineEdit1_5.setText('')
                self.lineEdit_6.setText('')

        except Exception as e :
            msg = str(e)
            QMessageBox.warning(self,"ERROR", msg)



def main():

    app = QApplication(sys.argv)
    window = Mainapp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()
