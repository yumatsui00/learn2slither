import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTabWidget, QLabel, 
                            QSpinBox, QDoubleSpinBox, QGroupBox)
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from modules.environment import Stage
from modules.agent import Agent

class ConfigTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # 学習パラメータグループ
        param_group = QGroupBox("Learning Parameters")
        param_layout = QVBoxLayout()
        
        # 各パラメータの設定
        self.params = {}
        params_config = {
            'epsilon_start': ('Epsilon Start', 0.3, 0, 1.0, 0.01),
            'epsilon_end': ('Epsilon End', 0.01, 0.001, 0.1, 0.001),
            'epsilon_decay': ('Epsilon Decay', 0.995, 0.9, 0.999, 0.001),
            'grid_size': ('Grid Size', 10, 5, 30, 1)
        }
        
        for param_name, (label, default, min_val, max_val, step) in params_config.items():
            param_layout.addLayout(self._create_param_layout(
                param_name, label, default, min_val, max_val, step))
            
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        layout.addStretch()
        self.setLayout(layout)
        
    def _create_param_layout(self, param_name, label, default, min_val, max_val, step):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        
        if isinstance(default, int):
            spinbox = QSpinBox()
        else:
            spinbox = QDoubleSpinBox()
        
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setValue(default)
        spinbox.setSingleStep(step)
        
        self.params[param_name] = spinbox
        layout.addWidget(spinbox)
        return layout

class StatsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # グラフの設定
        self.score_plot = pg.PlotWidget(title="Score per Episode")
        self.reward_plot = pg.PlotWidget(title="Average Reward per Episode")
        
        self.score_plot.setLabel('left', 'Score')
        self.score_plot.setLabel('bottom', 'Episode')
        self.reward_plot.setLabel('left', 'Average Reward')
        self.reward_plot.setLabel('bottom', 'Episode')
        
        self.score_line = self.score_plot.plot(pen='b')
        self.reward_line = self.reward_plot.plot(pen='r')
        
        layout.addWidget(self.score_plot)
        layout.addWidget(self.reward_plot)
        
        self.scores = []
        self.rewards = []
        self.episodes = []
        
        self.setLayout(layout)
    
    def update_stats(self, episode, score, avg_reward):
        self.episodes.append(episode)
        self.scores.append(score)
        self.rewards.append(avg_reward)
        
        self.score_line.setData(self.episodes, self.scores)
        self.reward_line.setData(self.episodes, self.rewards)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snake Game AI")
        self.setGeometry(100, 100, 800, 600)
        
        # メインウィジェットとレイアウトの設定
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        
        # コントロールボタン
        control_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Training")
        self.start_button.clicked.connect(self.start_training)
        self.play_button = QPushButton("Play Trained Model")
        self.play_button.clicked.connect(self.play_trained_model)
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.play_button)
        layout.addLayout(control_layout)
        
        # タブウィジェット
        tabs = QTabWidget()
        self.config_tab = ConfigTab()
        self.stats_tab = StatsTab()
        
        tabs.addTab(self.config_tab, "Configuration")
        tabs.addTab(self.stats_tab, "Statistics")
        
        layout.addWidget(tabs)
        main_widget.setLayout(layout)
        
        # 学習関連の変数
        self.env = None
        self.agent = None
        self.training = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.training_step)
    
    def start_training(self):
        if not self.training:
            # パラメータの取得
            params = {name: widget.value() 
                     for name, widget in self.config_tab.params.items()}
            
            # 環境とエージェントの初期化
            self.env = Stage(params['grid_size'])
            self.agent = Agent(
                params['learning_rate'],
                params['epsilon_start'],
                params['epsilon_end'],
                params['epsilon_decay']
            )
            
            self.training = True
            self.start_button.setText("Stop Training")
            self.timer.start(100)  # 100ms間隔でtraining_stepを呼び出し
        else:
            self.training = False
            self.start_button.setText("Start Training")
            self.timer.stop()
    
    def training_step(self):
        if self.training:
            # ここに1ステップの学習処理を実装
            # 例: episode_score, avg_reward = self.train_one_episode()
            # self.stats_tab.update_stats(episode, episode_score, avg_reward)
            pass
    
    def play_trained_model(self):
        # 学習済みモデルでのプレイ実装
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())