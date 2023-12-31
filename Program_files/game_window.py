from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from .question_window import QuestionWindow, Question
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Team():
    '''
    Team Class
    '''

    def __init__(self, name: str, points=0):
        self.name = name  # team name
        self.points = points  # points

    def get_name(self) -> str:
        '''
        Function to get team name.
        '''
        return self.name

    def get_points(self) -> float:
        '''
        Function to get points.
        '''
        return self.points

    def set_points(self, points: float) -> None:
        '''
        Function to set points.

            Parameter:
                points: how many points to set
        '''
        self.points = points

    def add_points(self, points: float) -> None:
        '''
        Function to add points.

            Parameter:
                points: how many points to add.
        '''
        self.points = self.points + points

    def remove_points(self, points: float) -> None:
        '''
        Function to remove points.

            Parameter:
                points: how many points to remove.
        '''
        self.points = self.points - points


class GameWindow(QMainWindow):
    '''
    Class to handle the game window
    '''

    def __init__(self, team_names: list, category_names: list, questions: list, parent=None):
        super(GameWindow, self).__init__(parent=parent)
        uic.loadUi('UI_Files/game_window.ui', self)
        self.showMaximized()

        self.team_names = team_names
        self.team_objects = self.make_teams()

        # variables to store and keep track of things
        self.team_names = team_names
        self.category_names = category_names
        self.all_questions = questions
        self.question_window = None
        self.music_muted = False

        # Main Frame
        self.main_frame = self.findChild(QtWidgets.QFrame, 'main_frame')

        # toolbar
        self.action_toggle_mute = self.findChild(
            QtWidgets.QAction, "actionMute"
        )
        self.action_toggle_mute.triggered.connect(self.toggle_mute)

        # Column (Category) Headers
        self.category_header_1 = self.findChild(
            QtWidgets.QPushButton, 'category_header_1'
        )
        self.category_header_2 = self.findChild(
            QtWidgets.QPushButton, 'category_header_2'
        )
        self.category_header_3 = self.findChild(
            QtWidgets.QPushButton, 'category_header_3'
        )
        self.category_header_4 = self.findChild(
            QtWidgets.QPushButton, 'category_header_4'
        )
        self.category_header_5 = self.findChild(
            QtWidgets.QPushButton, 'category_header_5'
        )
        self.category_header_6 = self.findChild(
            QtWidgets.QPushButton, 'category_header_6'
        )
        self.category_headers = [
            self.category_header_1, self.category_header_2, self.category_header_3, self.category_header_4, self.category_header_5, self.category_header_6
        ]

        # setting buttons and headers
        self.set_up_buttons()
        self.set_category_names(category_names)
        self.show()

        # showing team window
        self.team_window = TeamWindow(
            team_names=team_names, team_objects=self.team_objects, parent=self)
        self.team_window.show()

        # object to play song
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(
            QMediaContent(
                QUrl.fromLocalFile('Program_files/Jeopardy-theme-song.mp3')
            )
        )

    def closeEvent(self, event) -> None:
        '''
        Function to handle close event.
        '''
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Exiting Jeopardy!")
        msg.setText("Are you sure you want to quit?")
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.Cancel
        )
        msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
        user = msg.exec_()
        if user == QtWidgets.QMessageBox.Yes:
            if self.parent().isVisible():
                self.parent().close()
            event.accept()
            if self.team_window.isVisible():
                self.team_window.close()
            event.accept()
        else:
            event.ignore()

    def toggle_mute(self):
        '''
        Function to toggle the music volume.
        '''
        self.music_muted = not self.music_muted  # switches bool state.
        self.media_player.setMuted(self.music_muted)

        if self.music_muted:
            self.action_toggle_mute.setText('Unmute Music')
        else:
            self.action_toggle_mute.setText('Mute Music')

    def make_teams(self) -> None:
        '''
        Function to make the teams
        '''
        teams = {}
        for name in self.team_names:
            teams[name] = Team(name)
        return teams

    def toggle_header_btns(self, enabled=False) -> None:
        '''
        Function to toggle the header buttons, used in editting mode.

            Parameters:
                enabled: True -  button is activated.
        '''
        for cat in self.category_headers:
            cat.setEnabled(enabled)

    def set_category_names(self, names: list) -> None:
        '''
        Function set the  column (category) label text

            Parameters:
                names: list of names for each column (category).
        '''
        self.toggle_header_btns()
        for index, name in enumerate(names):
            self.category_headers[index].setText(name)

        for cat in self.category_headers:
            cat.setStyleSheet(
                '''
                QPushButton {
                    color: white;
                    font-size: 45px;
                    background-color: rgb(50, 50, 255);
                    padding: 5px;
                }
                '''
            )

    def set_up_buttons(self) -> None:
        '''
        Function to set up buttons and add styles.
        '''

        for btn in self.findChildren(QtWidgets.QPushButton):
            if btn not in self.category_headers:
                btn.setStyleSheet(
                    '''
                QPushButton {
                    background-color: rgb(50, 50, 255);
                    color: rgb(255, 170, 0);
                    font: Arial Bold;
                    font-size: 40px;
                }

                QPushButton:hover {
                    background-color: rgb(100, 100, 255);
                }

                '''
                )

        self.findChild(QtWidgets.QPushButton, 'question_1').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_2').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_3').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_4').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_5').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_6').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[0][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_7').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_8').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_9').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_10').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_11').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_12').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[1][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_13').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_14').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_15').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_16').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_17').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_18').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[2][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_19').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_20').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_21').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_22').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_23').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_24').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[3][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_25').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_26').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_27').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_28').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_29').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_30').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[4][5])
        )

        self.findChild(QtWidgets.QPushButton, 'question_31').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][0])
        )
        self.findChild(QtWidgets.QPushButton, 'question_32').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][1])
        )
        self.findChild(QtWidgets.QPushButton, 'question_33').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][2])
        )
        self.findChild(QtWidgets.QPushButton, 'question_34').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][3])
        )
        self.findChild(QtWidgets.QPushButton, 'question_35').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][4])
        )
        self.findChild(QtWidgets.QPushButton, 'question_36').clicked.connect(
            lambda: self.open_question_window(
                self.all_questions[5][5])
        )

    def make_teams(self) -> None:
        '''
        Function to make the teams
        '''
        teams = {}
        for name in self.team_names:
            teams[name] = Team(name)
        return teams

    def open_question_window(self, questionObj: Question) -> None:
        '''
        Function to open the question window
        '''
        btn = self.sender()
        btn_name = btn.objectName()
        clicked_btn = self.findChild(QtWidgets.QPushButton, btn_name)

        self.question_window = QuestionWindow(
            parent=self,
            questionObj=questionObj,
            clicked_btn=clicked_btn
        )
        self.question_window.show()
        self.media_player.play()


class TeamWindow(QMainWindow):
    '''
    Class to run the team window for add points
    '''

    def __init__(self, team_names: list, team_objects: dict, parent=None):
        super(TeamWindow, self).__init__(parent=parent)
        uic.loadUi('UI_Files/team_window.ui', self)

        self.team_names = team_names
        self.team_objects = team_objects

        ''' Finding Widgets '''

        self.team_frame_1 = self.findChild(
            QtWidgets.QFrame, "team_frame_1"
        )
        self.team_frame_2 = self.findChild(
            QtWidgets.QFrame, "team_frame_2"
        )
        self.team_frame_3 = self.findChild(
            QtWidgets.QFrame, "team_frame_3"
        )
        self.team_frame_4 = self.findChild(
            QtWidgets.QFrame, "team_frame_4"
        )
        self.team_frame_5 = self.findChild(
            QtWidgets.QFrame, "team_frame_5"
        )
        self.team_frame_6 = self.findChild(
            QtWidgets.QFrame, "team_frame_6"
        )
        self.team_frame_7 = self.findChild(
            QtWidgets.QFrame, "team_frame_7"
        )
        self.team_frame_8 = self.findChild(
            QtWidgets.QFrame, "team_frame_8"
        )
        self.team_frame_9 = self.findChild(
            QtWidgets.QFrame, "team_frame_9"
        )
        self.team_frame_10 = self.findChild(
            QtWidgets.QFrame, "team_frame_10"
        )
        self.team_frames = [self.team_frame_1, self.team_frame_2, self.team_frame_3,
                            self.team_frame_4, self.team_frame_5, self.team_frame_6, self.team_frame_7, self.team_frame_8, self.team_frame_9, self.team_frame_10]
        self.hide_frames(self.team_frames)

        self.lineEdit1 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_1"
        )
        self.lineEdit2 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_2"
        )
        self.lineEdit3 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_3"
        )
        self.lineEdit4 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_4"
        )
        self.lineEdit5 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_5"
        )
        self.lineEdit6 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_6"
        )
        self.lineEdit7 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_7"
        )
        self.lineEdit8 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_8"
        )
        self.lineEdit9 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_9"
        )
        self.lineEdit10 = self.findChild(
            QtWidgets.QLineEdit, "lineEdit_10"
        )

        # setting lineEdit to allow only numbers.
        for lineEdit in self.findChildren(QtWidgets.QLineEdit):
            lineEdit.setValidator(QIntValidator())

        ''' Attaching Functions to spinBox '''
        self.lineEdit1.returnPressed.connect(self.user_change)
        self.lineEdit2.returnPressed.connect(self.user_change)
        self.lineEdit3.returnPressed.connect(self.user_change)
        self.lineEdit4.returnPressed.connect(self.user_change)
        self.lineEdit5.returnPressed.connect(self.user_change)
        self.lineEdit6.returnPressed.connect(self.user_change)
        self.lineEdit7.returnPressed.connect(self.user_change)
        self.lineEdit8.returnPressed.connect(self.user_change)
        self.lineEdit9.returnPressed.connect(self.user_change)
        self.lineEdit10.returnPressed.connect(self.user_change)

        # Showing N Teams frames
        self.frames_to_show = []
        for index, team_name in enumerate(self.team_names):
            self.frames_to_show.append(self.team_frames[index])
        self.show_frames(self.frames_to_show)
        self.set_team_names()

        # styling
        for frame in self.team_frames:
            frame.setStyleSheet(
                '''
                QFrame {
                    border: 1px solid;
                    background-color: rgb(50, 50, 255);
                }

                QLabel {
                    border: none;
                    padding: 5px;
                    font-size: 40px;
                    font-style: Times;
                    color: rgb(250, 170, 0);
                }

                QLineEdit {
                    background-color: white;
                    font-size: 30px;
                }
                '''
            )
        self.setStyleSheet(
            '''
            background-color: black;
            '''
        )

        # showing window
        self.adjustSize()
        self.show()

    def closeEvent(self, event) -> None:
        '''
        Function to handle close event.
        '''
        user = self.parent().close()
        if user:
            event.accept()
        else:
            event.ignore()

    def hide_frames(self, frames: list) -> None:
        '''
        Function to hide team sub frames.

            Parameters:
                frames: list of frames to hide.
        '''
        for frame in frames:
            frame.hide()

    def show_frames(self, frames: list) -> None:
        '''
        Function to show team sub frames.

            Parameters:
                frames: list of frames to show.
        '''
        for frame in frames:
            frame.show()

    def set_team_names(self) -> None:
        '''
        Function to set labels with set names
        '''
        for frame, name, in zip(self.frames_to_show, self.team_names):
            frame.findChildren(QtWidgets.QLabel)[0].setText(name)
            points = self.team_objects[name].get_points()
            frame.findChildren(QtWidgets.QLineEdit)[0].setText(str(points))

    def user_change(self) -> None:
        '''
        Function to handle LineEdit values changing
        '''

        # Popup warning user that manualling edit points will overwrite the team points.
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        pixmapi = getattr(QtWidgets.QStyle, "SP_MessageBoxWarning")
        icon = self.style().standardIcon(pixmapi)
        msg.setWindowIcon(icon)
        msg.setWindowTitle("Jeopardy! - Changing Points")
        text = 'Warning!\n\n This will overwrite Team points.'
        msg.setText(text)
        msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok |
            QtWidgets.QMessageBox.Cancel
        )
        msg.setDefaultButton(QtWidgets.QMessageBox.Ok)
        user = msg.exec_()

        # checking user's response
        sender = self.sender()
        sender_name = sender.objectName()
        lineEdit = self.findChild(QtWidgets.QLineEdit, sender_name)
        team_objects = self.parent().team_objects
        match user:
            case QtWidgets.QMessageBox.Ok:
                # getting what lineEdit has been editted.

                points = lineEdit.text()  # user typed points.
                lineEdit.setText(points)

                # updating Team Object's points:
                for index, frame in enumerate(self.frames_to_show):
                    if lineEdit in frame.findChildren(QtWidgets.QLineEdit):
                        team_name = list(team_objects)[index]
                        team_objects[team_name].set_points(float(points))
            case _:  # user cancels
                for index, frame in enumerate(self.frames_to_show):
                    if lineEdit in frame.findChildren(QtWidgets.QLineEdit):
                        team_name = list(team_objects)[index]
                        points = team_objects[team_name].get_points()
                        lineEdit.setText("{:.0f}".format(points))

    def points_changed(self, points=0) -> None:
        '''
        Function to update team points
        '''

        sender = self.sender()
        sender_name = sender.objectName()

        name_dict = {
            1: 'lineEdit_1',
            2: 'lineEdit_2',
            3: 'lineEdit_3',
            4: 'lineEdit_4',
            5: 'lineEdit_5',
            6: 'lineEdit_6',
            7: 'lineEdit_7',
            8: 'lineEdit_8',
            9: 'lineEdit_9',
            10: 'lineEdit_10',
        }

        key = int(sender_name.split('_')[-1])
        self.team_to_update = self.team_objects[list(self.team_objects)[key-1]]

        self.team_to_update.add_points(points)

        lineEdit = self.findChild(
            QtWidgets.QLineEdit, name_dict[float(sender_name.split('_')[-1])]
        )
        lineEdit.setText(str(round(self.team_to_update.get_points())))
