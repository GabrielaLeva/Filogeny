import os

import pygame.mixer_music

from main import *

from PySide6.QtWidgets import (QGroupBox,QRadioButton,QButtonGroup,QTextEdit,QComboBox)

class MainWindow(QMainWindow):

#Whats the worst that can happen? <- Clueless

    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,1000,700)

        self.current_tree = None
        self.visualizer = None
        self.selected_file_path = None

        central_widget=QWidget()
        self.setCentralWidget(central_widget)
        main_layout=QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        header=QLabel("This Program is a test program for Phylogenetic Tree Creation")
        header.setStyleSheet("background-color: blue; color:white; padding:15px; font-size: 20px; font-weight: bold;")
        main_layout.addWidget(header)

        content_layout=QHBoxLayout()
        content_layout.setContentsMargins(0,0,0,0)
        content_layout.setSpacing(0)

        sidebar = QWidget()
        sidebar.setStyleSheet("Background-color:blue;")
        sidebar.setFixedWidth(200)
        sidebar_layout=QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10,10,10,10)
        sidebar_layout.setSpacing(10)

        self.btn_TreeCreate=QPushButton("Tree Creation")
        self.btn_Vis=QPushButton("Tree Visualization")
        self.btn_settings=QPushButton("Settings")

        button_style= """QPushButton{background-color:blue; color:white; border:none; padding:12px; text-align:left; font-size: 14px; border-radius: 5px;} QPushButton:hover {background-color: orange;} QPushButton:pressed {background-color:white;}"""

        self.btn_TreeCreate.setStyleSheet(button_style)
        self.btn_Vis.setStyleSheet(button_style)
        self.btn_settings.setStyleSheet(button_style)

        sidebar_layout.addWidget(self.btn_TreeCreate)
        sidebar_layout.addWidget(self.btn_Vis)
        sidebar_layout.addWidget(self.btn_settings)

        if os.path.exists("DNA_orbit_animated.gif"):

            sidebar_layout.addSpacing(20)
            dna_label=QLabel()
            self.dna_move = QMovie("DNA_orbit_animated.gif")
            dna_label.setMovie(self.dna_move)
            dna_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            dna_label.setScaledContents(True)
            dna_label.setMaximumHeight(300)
            self.dna_move.start()
            sidebar_layout.addWidget(dna_label)
            self.DestructionRatLabel=dna_label

        else:

            placeholder=QLabel("Shit aint worky")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("color:white; font-size:48px;")
            sidebar_layout.addWidget(placeholder)


        sidebar_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background-color: white;")

        self.page_Tree = self.TreeAlgorithmOptions("Tree Selection Algorithm Options","This section is designated to create, choose and generate a phylogenetic Tree, that is displayed in visualization tab.")

        self.page_Visualize = self.CreatePlaceHolder("Tree Visualization")

        self.page_Setting = self.SpinningRatEasterEgg()

        self.content_stack.addWidget(self.page_Tree)
        self.content_stack.addWidget(self.page_Visualize)
        self.content_stack.addWidget(self.page_Setting)

        self.btn_TreeCreate.clicked.connect(lambda: self.content_stack.setCurrentIndex(0))
        self.btn_Vis.clicked.connect(lambda: self.content_stack.setCurrentIndex(1))
        self.btn_settings.clicked.connect(lambda: self.content_stack.setCurrentIndex(2))

        content_layout.addWidget(sidebar)
        content_layout.addWidget(self.content_stack)
        main_layout.addLayout(content_layout)

        self.content_stack.setCurrentIndex(0)

    def CreatePlaceHolder(self,title):

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20,20,20,20)

        title_label=QLabel(title)
        title_label.setStyleSheet("font-size:24px;font-weight:bold;color:green;")

        layout.addWidget(title_label)
        layout.addStretch()

        return page

    #Christ help me here

    def TreeAlgorithmOptions(self,title,desc):

        page=QWidget()
        layout=QVBoxLayout(page)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        title_layout=QLabel(title)
        title_layout.setStyleSheet("font-size: 30px; font-weight:bold; color:orange; text-align:center;")
        title_layout.setContentsMargins(20,20,20,20)
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc_label=QLabel(desc)
        desc_label.setStyleSheet("font-size:15px; font-weight:bold;color:blue;")

        alg_group = QGroupBox("Algorithm Selection")
        alg_group.setStyleSheet("""QGroupBox{font-size:12px; color: black;font-weight:bold;border:2px solid black; border-radius: 3px;} QGroupBox::title{subcontrol-origin:margin; left:15px; padding: -11px 0 0 0;}""")
        alg_layout = QVBoxLayout()

        self.algorithm_group = QButtonGroup()
        self.radio_upgma = QRadioButton("UPGMA ( Unweighted Pair Group Method with Arithetic Mean )")
        self.radio_nj = QRadioButton("Neighbor Joining ( NJ )")
        self.radio_upgma.setChecked(True)
        self.radio_nj.setStyleSheet("color:black;")
        self.radio_upgma.setStyleSheet("color:black;")

        self.algorithm_group.addButton(self.radio_upgma,0)
        self.algorithm_group.addButton(self.radio_nj,1)

        alg_layout.addWidget(self.radio_upgma)
        alg_layout.addWidget(self.radio_nj)
        alg_group.setLayout(alg_layout)
        layout.addWidget(alg_group)

        data_group = QGroupBox("Data Input")
        data_group.setStyleSheet("""QGroupBox{font-size:12px; color: black;font-weight:bold;border:2px solid black; border-radius:5px;} QGroupBox::title{subcontrol-origin:margin; left:15px;padding: -11px 0 0 0;}""")
        data_layout = QVBoxLayout()
        input_label=QLabel("Input Method:")
        input_label.setStyleSheet("color:black;")
        self.input_method=QComboBox()
        self.input_method.addItems(["Random Test Data","Load From File","Database Import"])
        self.input_method.setStyleSheet("color:black;")
        self.input_method.currentTextChanged.connect(self.FastaOpt)

        data_layout.addWidget(input_label)
        data_layout.addWidget(self.input_method)

        self.file_select_btn=QPushButton("Select FASTA File")
        self.file_select_btn.setStyleSheet("""QPushButton{background-color: white; color:black;}""")
        self.file_select_btn.clicked.connect(self.select_fasta_file)
        self.file_select_btn.setVisible(False)
        data_layout.addWidget(self.file_select_btn)

        self.file_label=QLabel("No File Selected")
        self.file_label.setStyleSheet("color:black;")
        self.file_label.setVisible(False)
        data_layout.addWidget(self.file_label)

        self.status_text=QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(100)
        self.status_text.setPlaceholderText("Status message.")
        self.status_text.setStyleSheet("color:black;")
        data_layout.addWidget(self.status_text)

        data_group.setLayout(data_layout)
        layout.addWidget(data_group)

        settings_group=QGroupBox("Alignment Settings")
        settings_group.setStyleSheet("""QGroupBox{font-size: 12px; color: black; font-weight:bold;border:2px solid black; border-radius:3px;} QGroupBox::title{subcontrol-origin:margin; left:15px; padding: -11px 0 0 0;}""")

        settings_layout=QVBoxLayout()

        mode_label=QLabel("Alignment Mode:")
        mode_label.setStyleSheet("color:black;")
        self.alignment_mode = QComboBox()
        self.alignment_mode.addItems(["Global","Local"])
        self.alignment_mode.setStyleSheet("color:black;")

        settings_layout.addWidget(mode_label)
        settings_layout.addWidget(self.alignment_mode)
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)

        self.Generate_Btn=QPushButton("Generate Tree")
        self.Generate_Btn.setStyleSheet("""QPushButton{background-color:#618e9e; color:black; border:none; padding:12px; text-align:left; font-size: 14px; border-radius: 5px;} QPushButton:hover {background-color: #677798;} QPushButton:pressed {background-color: #26b1d9;}""")
        self.Generate_Btn.clicked.connect(self.generate_tree)
        layout.addWidget(self.Generate_Btn)

        layout.addStretch()
        return page

    def FastaOpt(self,method):
        if method == "Load From File":
            self.file_select_btn.setVisible(True)
            self.file_label.setVisible(True)
        else:
            self.file_select_btn.setVisible(False)
            self.file_label.setVisible(False)
            self.file_label.setText("No Fasta File Selected")

    def select_fasta_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,"Select Fasta File",os.getcwd(),"All Files(*)")

        if file_path:
            filename=os.path.basename(file_path)
            self.file_label.setText(f"Selected: {filename}")
            self.selected_file_path = file_path
        else:
            self.file_label.setText("No File Selected")

    def load_fasta_sequence(self,file_path):

            if not file_path or not os.path.exists(file_path):
                raise FileNotFoundError("Invalid or Missing FASTA file path.")
            sequences=[]
            labels=[]

            for record in SeqIO.parse(file_path,"fasta"):
                sequences.append(record.seq)
                labels.append(record.id)

            if len(sequences) < 2:
                raise ValueError("FASTA file must contain at least 2 Sequences")

            return sequences,labels

    def score_to_distance(self,score,max_score):
        return max_score - score

    def align_dataset(self,settings):

        aligner = PairwiseAligner()
        aligner.mode = settings.algorithm_mode
        distance_matrix=[]

        max_score=float("-inf")
        for i, seqi in enumerate(settings.dataset):
            distance_matrix.append([aligner.score(seqi,seqj) for seqj in settings.dataset[i+1:]])

        distance_matrix.pop()

        for i in distance_matrix:
            n = max(i)
            if max_score <= n:
                max_score = n

        distance_matrix = [[self.score_to_distance(j,max_score) for j in i] for i in distance_matrix]
        return distance_matrix

    def generate_tree(self):
        self.status_text.clear()
        self.status_text.append("Generating Tree...")
        try:
            algorithm="UPGMA" if self.radio_upgma.isChecked() else "NJ"
            input_method=self.input_method.currentText()
            alignment_mode=self.alignment_mode.currentText().lower()

            self.status_text.append(f"Algorithm: {algorithm}")
            self.status_text.append(f"Input: {input_method}")
            self.status_text.append(f"Alignment: {alignment_mode}")

            settings = AlgorithmSettings()
            settings.algorithm_mode = alignment_mode

            if input_method == "Random Test Data":
                num_seq = 20
                taxa_labels = [f"seq{i}" for i in range(num_seq)]
                text_seq = [Seq(''.join([choice(["A","C","T","G"]) for _ in range(1000)])) for _ in range(num_seq)]
                settings.dataset = text_seq

                self.status_text.append(f"Generated {num_seq} random sequences")

            elif input_method == "Load From File":

                self.status_text.append("Loading sequences from FASTA File")
                text_seq,taxa_labels = self.load_fasta_sequence(self.selected_file_path)
                settings.dataset = text_seq

                self.status_text.append(f"Loaded {len(text_seq)} sequences")
                self.status_text.append(f"Taxa: {', '.join(taxa_labels[:5])}{'...' if len(taxa_labels) > 5 else ''}")

            elif input_method == "Database Import":
                self.status_text.append("Error: Database import not yet Implemented.")
                return

            align = self.align_dataset(settings)
            taxa = [[0 for _ in range(len(align)+1)] for _ in range(len(align)+1)]

            for i, seqi in enumerate(align):
                for j, seqj in enumerate(seqi):
                    taxa[i][i+j+1]=seqj
                    taxa[i+j+1][i]=seqj

            if algorithm=="UPGMA":
                self.current_tree=UPMGA(taxa,taxa_labels)
            else:
                self.current_tree=NJ(taxa,taxa_labels)

            self.status_text.append("Tree Generated Successfully.")
            self.display_tree()
            self.content_stack.setCurrentIndex(1)

        except Exception as e:
            self.status_text.append(f"Error: {str(e)}")

    def display_tree(self):

        old_widget=self.content_stack.widget(1)
        if old_widget:
            self.content_stack.removeWidget(old_widget)
            old_widget.deleteLater()

        self.visualizer = Visualizer()
        self.visualizer.DisplayTree(self.current_tree)

        self.content_stack.insertWidget(1,self.visualizer)
        self.content_stack.setCurrentIndex(1)

    def SpinningRatEasterEgg(self):

        page=QWidget()
        layout=QVBoxLayout(page)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(10)

        title_label=QLabel("Settings")
        title_label.setStyleSheet("font-size:22px; font-weight:bold; color:green;")
        layout.addWidget(title_label)


        SpeedRat = QGroupBox("Spin that boi!")

        SpeedRat.setStyleSheet("""QGroupBox{font-size:15px;font-weight:bold;color:black;border:2px solid black; border-radius:5px; padding-top:20px;} QGroupBox::title {subcontrol-origin:margin; left: 12px;}""")

        Speed = QVBoxLayout()

        self.SpinBtn=QPushButton("THE RAT REQUIRES THE SPIN")
        self.SpinBtn.setStyleSheet("""QPushButton{font-size:18px;font-weight:bold;background-color:grey;color:black;border:none;border-radius:8px;} QPushButton:hover{background-color: pink;} QPushButton:pressed{background-color:red;} QPushButton:disabled{background-color:black; color: white;}""")
        self.SpinBtn.clicked.connect(self.SpinBegin)

        Speed.addWidget(self.SpinBtn)

        self.speed_label=QLabel("Current Speed: 10")
        self.speed_label.setStyleSheet("font-size:14px; font-weight:bold; color:black;")
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Speed.addWidget(self.speed_label)

        SpeedRat.setLayout(Speed)
        layout.addWidget(SpeedRat)
        layout.addStretch()

        self.Current_spin_speed=10
        self.rat_destroyed=False
        self.rat_visible = False

        self.click_count=0
        self.click_sound=None
        self.backgroundMusic=False

        if hasattr(self,'dna_move'):
            self.OrignialRat=self.dna_move

        return page

    def SpinBegin(self):

        if self.rat_destroyed:
            return

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        if not self.backgroundMusic:
            try:
                if os.path.exists("backgroundMusic.mp3"):
                    pygame.mixer.music.load("backgroundMusic.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)
                    self.backgroundMusic=True
            except Exception as e:
                print(f"Background Music Error: {e}")


            try:
                if os.path.exists("click.wav"):
                    if not self.click_sound:
                        self.click_sound=pygame.mixer.Sound("click.wav")

                        pitch = 1.0 + (self.click_count * 0.1)
                        pitch = min(pitch, 3.0)

                        sound_array = pygame.sndarray.array(self.click_sound)
                        adjusted_sound = pygame.mixer.Sound(sound_array)

                        adjusted_sound.set_volume(0.3 + (self.click_count * 0.02))
                        adjusted_sound.play()

                        self.click_count+=1
            except Exception as e:
                print(f"Click Sound Problem: {e}")

        if not self.rat_visible and os.path.exists("Rat.gif"):
            self.dna_move=QMovie("Rat.gif")
            self.DestructionRatLabel.setMovie(self.dna_move)
            self.dna_move.start()
            self.rat_visible=True

        self.Current_spin_speed += 5

        self.speed_label.setText(f"Current Speed: {self.Current_spin_speed}")
        self.speed_label.setStyleSheet("font-size:14px; font-weight:bold; color:black;")
        speed = 200 - self.Current_spin_speed + 10
        self.dna_move.setSpeed(100*(100/speed))

        if self.Current_spin_speed >= 300:
            self.Kabum()


    def Kabum(self):
        self.SpinBtn.setEnabled(False)
        self.rat_destroyed=True

        self.dna_move.stop()

        if os.path.exists("SkeletonRat.png"):
            skeleton_map=QPixmap("SkeletonRat.png")
            self.DestructionRatLabel.setPixmap(skeleton_map.scaled(self.DestructionRatLabel.width(),self.DestructionRatLabel.height(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation))
            self.DestructionRatLabel.setScaledContents(False)

        try:
            if os.path.exists("bad_to_the_bone.mp3"):
                pygame.mixer.music.load("bad_to_the_bone.mp3")
                pygame.mixer.music.set_volume(0.7)
                pygame.mixer.music.play()
        except ImportError as e:
            print(f"Error: {e}")
            print("DAMN IT GOD DAMN IT!")

        QTimer.singleShot(2500,self.Explosion)

    def Explosion(self):
        if os.path.exists("Explosion.gif"):
            explosion = QMovie("Explosion.gif")
            self.DestructionRatLabel.setMovie(explosion)
            explosion.start()
            explosion.frameChanged.connect(lambda:self.CheckExplosionEnd(explosion))
            self.dna_move = explosion

        try:
            if os.path.exists("Explosion.mp3"):
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Explosion.mp3")
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play()

        except Exception as e:
            print(f"Explosion Sound Error: {e}")

        QTimer.singleShot(3000,self.Ending)

    def CheckExplosionEnd(self,movie):
        if movie.currentFrameNumber() == movie.frameCount() - 1:
            movie.stop()
            movie.jumpToFrame(movie.frameCount()-1)

    def Ending(self):

        self.DestructionRatLabel.clear()
        self.speed_label.setText("The deed has been done. Good job my child. Farewell.")
        self.speed_label.setStyleSheet("color:black;")
        self.SpinBtn.setText("There's nothing left for you here.")

