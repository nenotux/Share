#by nenotux 29-10-2023
#launch the program with python3 and have fun!

import curses
import random

def main(stdscr):
    # Impostazioni iniziali
    curses.curs_set(0)
    stdscr.nodelay(1)
    sh, sw = stdscr.getmaxyx()
    w = stdscr.subwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    # Posizione iniziale del serpente
    snake_x = sw // 4
    snake_y = sh // 2
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]

    # Posizione del cibo
    food = [sh // 2, sw // 2]
    w.addch(food[0], food[1], curses.ACS_PI)

    # Direzione iniziale del serpente
    key = curses.KEY_RIGHT

    # Inizializza il punteggio
    score = 0

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        # Controlla se il serpente ha mangiato il cibo
        if snake[0] == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, sh - 1),
                    random.randint(1, sw - 1)
                ]
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], curses.ACS_PI)
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        # Muovi il serpente
        new_head = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)
        w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

        # Termina il gioco se il serpente colpisce il bordo
        if (
            snake[0][0] in [0, sh] or
            snake[0][1] in [0, sw] or
            snake[0] in snake[1:]
        ):
            msg = "Game Over!"
            w.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            w.refresh()
            w.getch()
            break

if __name__ == "__main__":
    curses.wrapper(main)
