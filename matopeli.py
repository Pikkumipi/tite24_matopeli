# pip install PySide6

import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)

        self.game_started = False
        self.init_screen()

    def keyPressEvent(self, event):
        key = event.key()

        # Aloitetaan peli jos ei vielä käynnissä
        if not self.game_started:
            self.game_started = True
            self.scene().clear()
            self.start_game()
            return

        # Suunnan vaihto
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # Tarkistetaan rajat ja osuma itseensä
        if new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
            self.timer.stop()
            self.scene().clear()

            #Game over text
            game_over_text = self.scene().addText("Game Over", QFont("Arial", 24))
            text_width = game_over_text.boundingRect().width()
            text_x = (self.width() - text_width) / 2
            game_over_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else:
            self.snake.pop()

        # Nopeuden kasvatus
        if self.score == self.level_limit:
            self.level_limit += 5
            self.timer_delay = max(50, int(self.timer_delay * 0.9))
            self.timer.setInterval(self.timer_delay)

        self.print_game()

    def print_game(self):
        self.scene().clear()
        self.scene().addText(f"Score: {self.score}", QFont("Arial", 12)).setPos(5, 0)

        # Käärmeen segmentit
        for i, (x, y) in enumerate(self.snake):
            color = Qt.darkGreen if i == 0 else Qt.green
            self.scene().addRect(
                x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE,
                QPen(Qt.black), QBrush(color)
            )

        # Ruoka "omena"
        fx, fy = self.food
        self.scene().addEllipse(
            fx * CELL_SIZE + 4, fy * CELL_SIZE + 4,
            CELL_SIZE - 8, CELL_SIZE - 8,
            QPen(Qt.red), QBrush(Qt.red)
        )
        self.scene().addRect(
            fx * CELL_SIZE + (CELL_SIZE//2 - 2), fy * CELL_SIZE,
            4, CELL_SIZE//4,
            QPen(Qt.green), QBrush(Qt.green)
        )

    def init_screen(self):
        start_text = self.scene().addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        start_text.setPos((CELL_SIZE * GRID_WIDTH - text_width) / 2, GRID_HEIGHT * CELL_SIZE / 2)

    def start_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.food = self.spawn_food()
        self.score = 0
        self.level_limit = 5
        self.timer_delay = 300
        self.timer.start(self.timer_delay)

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
