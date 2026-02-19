import curses
import time
import random
from curses import wrapper

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    def main_menu(lang="en"):
        max_y, max_x = stdscr.getmaxyx()

        stdscr.nodelay(False)
        stdscr.timeout(-1)
        stdscr.clear()
        if lang == "en":
            stdscr.addstr(int(max_y / 2) - 3, int(max_x / 2) - len("Welcome to Minesweeper made by Kuraidoryo!") // 2, "Welcome to Minesweeper made by Kuraidoryo!")
            stdscr.addstr(int(max_y / 2) - 1, int(max_x / 2) - len("Press 'l' to change the language") // 2, "Press 'l' to change the language")
            stdscr.addstr(int(max_y / 2),     int(max_x / 2) - len("Press 's' to Start Game") // 2, "Press 's' to Start Game")
            stdscr.addstr(int(max_y / 2) + 1, int(max_x / 2) - len("Press 'i' for Instructions") // 2, "Press 'i' for Instructions")
            stdscr.addstr(int(max_y / 2) + 2, int(max_x / 2) - len("Press 'q' to Quit") // 2, "Press 'q' to Quit")
        else:
            stdscr.addstr(int(max_y / 2) - 3, int(max_x / 2) - len("Witaj w grze Saper autorstwa Kuraidoryo!") // 2, "Witaj w grze Saper autorstwa Kuraidoryo!")
            stdscr.addstr(int(max_y / 2) - 1, int(max_x / 2) - len("Kliknij 'l' aby zmienić język") // 2, "Kliknij 'l' aby zmienić język")
            stdscr.addstr(int(max_y / 2),     int(max_x / 2) - len("Kliknij 's' aby rozpocząć grę") // 2, "Kliknij 's' aby rozpocząć grę")
            stdscr.addstr(int(max_y / 2) + 1, int(max_x / 2) - len("Kliknij 'i' aby zobaczyć instrukcje") // 2, "Kliknij 'i' aby zobaczyć instrukcje")
            stdscr.addstr(int(max_y / 2) + 2, int(max_x / 2) - len("Kliknij 'q' aby zakończyć") // 2, "Kliknij 'q' aby zakończyć")
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('s'):
                main_game(lang)
                break
            elif key == ord('i'):
                instructions(lang)
                break
            elif key == ord('l'):
                lang = "pl" if lang == "en" else "en"
                return main_menu(lang)
            elif key == ord('q'):
                return

    def instructions(lang):
        max_y, max_x = stdscr.getmaxyx()

        stdscr.clear()
        if lang == "en":
            lines = [
                "Instructions:",
                "Use 'WASD' keys to move the cursor.",
                "Press 'e' to reveal a cell.",
                "Press 'f' to place/remove a flag.",
                "Press 'p' to pause during the game.",
                "Avoid revealing mines!",
                "First reveal is always safe.",
                "Press any key to return to the main menu.",
            ]
        else:
            lines = [
                "Instrukcje:",
                "Użyj klawiszy 'WASD' aby poruszać kursorem.",
                "Naciśnij 'e' aby odkryć pole.",
                "Naciśnij 'f' aby postawić/usunąć flagę.",
                "Naciśnij 'p' aby wstrzymać grę.",
                "Unikaj odkrywania min!",
                "Pierwsze odkrycie jest zawsze bezpieczne.",
                "Naciśnij dowolny klawisz aby wrócić do menu głównego.",
            ]

        start_y = int(max_y / 2) - len(lines) // 2
        for i, line in enumerate(lines):
            stdscr.addstr(start_y + i, int(max_x / 2) - len(line) // 2, line)

        stdscr.refresh()
        stdscr.getch()
        main_menu(lang)

    def pause_menu(lang):
        max_y, max_x = stdscr.getmaxyx()

        stdscr.clear()
        if lang == "en":
            stdscr.addstr(int(max_y / 2) - 1, int(max_x / 2) - len("Game Paused") // 2, "Game Paused")
            stdscr.addstr(int(max_y / 2), int(max_x / 2) - len("Press 'r' to Resume") // 2, "Press 'r' to Resume")
            stdscr.addstr(int(max_y / 2) + 1, int(max_x / 2) - len("Press 'q' to Quit to Main Menu") // 2, "Press 'q' to Quit to Main Menu")
        else:
            stdscr.addstr(int(max_y / 2) - 1, int(max_x / 2) - len("Gra wstrzymana") // 2, "Gra wstrzymana")
            stdscr.addstr(int(max_y / 2), int(max_x / 2) - len("Naciśnij 'r' aby wznowić") // 2, "Naciśnij 'r' aby wznowić")
            stdscr.addstr(int(max_y / 2) + 1, int(max_x / 2) - len("Naciśnij 'q' aby wrócić do menu głównego") // 2, "Naciśnij 'q' aby wrócić do menu głównego")

        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key == ord('r'):
                return
            elif key == ord('q'):
                main_menu(lang)
                return

    def main_game(lang):
        stdscr.nodelay(True)
        stdscr.timeout(100) 
        max_y, max_x = stdscr.getmaxyx()

        header_rows = 2
        rows = max(8, min(20, max_y - header_rows - 2))
        cols = max(8, min(40, max_x - 1))
        mines_count = max(10, int(rows * cols * 0.15))

        revealed = [[False for _ in range(cols)] for _ in range(rows)]
        flagged = [[False for _ in range(cols)] for _ in range(rows)]
        mines = [[False for _ in range(cols)] for _ in range(rows)]
        numbers = [[0 for _ in range(cols)] for _ in range(rows)]
        first_reveal_done = False
        start_time = None
        paused_total = 0.0
        game_over = False
        win = False

        cur_r, cur_c = rows // 2, cols // 2
        flags_left = mines_count

        best_time = None
        best_file = "minesweeper_best.txt"
        try:
            with open(best_file, "r") as f:
                content = f.read().strip()
                if content:
                    best_time = float(content)
        except:
            best_time = None

        def neighbors(r, c):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        yield nr, nc

        def place_mines(exclude_r, exclude_c):
            forbidden = {(exclude_r, exclude_c)}
            for nr, nc in neighbors(exclude_r, exclude_c):
                forbidden.add((nr, nc))
            positions = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in forbidden]
            random.shuffle(positions)
            for i in range(mines_count):
                r, c = positions[i]
                mines[r][c] = True

            for r in range(rows):
                for c in range(cols):
                    if mines[r][c]:
                        numbers[r][c] = -1
                    else:
                        numbers[r][c] = sum(1 for nr, nc in neighbors(r, c) if mines[nr][nc])

        def flood_reveal(sr, sc):
            stack = [(sr, sc)]
            while stack:
                r, c = stack.pop()
                if revealed[r][c]:
                    continue
                revealed[r][c] = True
                if flagged[r][c]:
                    flagged[r][c] = False
                if numbers[r][c] == 0:
                    for nr, nc in neighbors(r, c):
                        if not revealed[nr][nc] and not mines[nr][nc]:
                            stack.append((nr, nc))

        def check_win():
            for r in range(rows):
                for c in range(cols):
                    if not mines[r][c] and not revealed[r][c]:
                        return False
            return True

        def current_elapsed():
            if start_time is None:
                return 0.0
            return time.time() - start_time - paused_total

        def draw():
            stdscr.clear()
            elapsed = current_elapsed()
            if lang == "en":
                hud = f"Mines: {mines_count}  Flags left: {flags_left}  Time: {elapsed:.1f}s"
                if best_time is not None:
                    hud += f"  Best: {best_time:.1f}s"
            else:
                hud = f"Miny: {mines_count}  Flagi: {flags_left}  Czas: {elapsed:.1f}s"
                if best_time is not None:
                    hud += f"  Rekord: {best_time:.1f}s"

            stdscr.addstr(0, 0, hud[:max_x - 1])

            if lang == "en":
                stdscr.addstr(1, 0, "WASD: move  e: reveal  f: flag  p: pause  q: quit")
            else:
                stdscr.addstr(1, 0, "WASD: ruch  e: odkryj  f: flaga  p: pauza  q: wyjdź")

            start_y = 2
            for r in range(rows):
                for c in range(cols):
                    ch = '.'
                    attr = curses.A_NORMAL
                    if revealed[r][c]:
                        if mines[r][c]:
                            ch = '*'
                            attr = curses.A_BOLD
                        else:
                            n = numbers[r][c]
                            ch = ' ' if n == 0 else str(n)
                    else:
                        if flagged[r][c]:
                            ch = 'F'
                            attr = curses.A_BOLD

                    if r == cur_r and c == cur_c:
                        attr |= curses.A_REVERSE

                    try:
                        stdscr.addstr(start_y + r, c, ch, attr)
                    except curses.error:
                        pass

            if game_over or win:
                msg = "You hit a mine! Game Over." if not win else "You win!"
                if lang == "pl":
                    msg = "Trafiłeś na minę! Koniec gry." if not win else "Wygrana!"
                stdscr.addstr(start_y + rows + 1, 0, msg[:max_x - 1])
                final_time = current_elapsed()
                if lang == "en":
                    stdscr.addstr(start_y + rows + 2, 0, f"Final time: {final_time:.1f}s")
                    stdscr.addstr(start_y + rows + 3, 0, "Press any key to return to menu.")
                else:
                    stdscr.addstr(start_y + rows + 2, 0, f"Czas końcowy: {final_time:.1f}s")
                    stdscr.addstr(start_y + rows + 3, 0, "Naciśnij dowolny klawisz aby wrócić do menu.")

            stdscr.refresh()

        while True:
            draw()

            if game_over or win:
                final_time = current_elapsed()
                if win and start_time is not None and (best_time is None or final_time < best_time):
                    try:
                        with open(best_file, "w") as f:
                            f.write(str(final_time))
                        best_time = final_time
                    except:
                        pass
                stdscr.nodelay(False)
                stdscr.timeout(-1)
                stdscr.getch()
                main_menu(lang)
                return

            key = stdscr.getch()

            if key in (ord('w'), curses.KEY_UP):
                cur_r = max(0, cur_r - 1)
            elif key in (ord('s'), curses.KEY_DOWN):
                cur_r = min(rows - 1, cur_r + 1)
            elif key in (ord('a'), curses.KEY_LEFT):
                cur_c = max(0, cur_c - 1)
            elif key in (ord('d'), curses.KEY_RIGHT):
                cur_c = min(cols - 1, cur_c + 1)
            elif key == ord('p'):
                pause_start = time.time()
                stdscr.nodelay(False)
                stdscr.timeout(-1)
                pause_menu(lang)
                paused_total += time.time() - pause_start
                stdscr.nodelay(True)
                stdscr.timeout(100)
            elif key == ord('q'):
                main_menu(lang)
                return
            elif key == ord('f'):
                if not revealed[cur_r][cur_c]:
                    if flagged[cur_r][cur_c]:
                        flagged[cur_r][cur_c] = False
                        flags_left += 1
                    else:
                        if flags_left > 0:
                            flagged[cur_r][cur_c] = True
                            flags_left -= 1
            elif key == ord('e'):
                if not revealed[cur_r][cur_c] and not flagged[cur_r][cur_c]:
                    if not first_reveal_done:
                        place_mines(cur_r, cur_c)
                        first_reveal_done = True
                        start_time = time.time()

                    if mines[cur_r][cur_c]:
                        revealed[cur_r][cur_c] = True
                        game_over = True
                        for r in range(rows):
                            for c in range(cols):
                                if mines[r][c]:
                                    revealed[r][c] = True
                    else:
                        if numbers[cur_r][cur_c] == 0:
                            flood_reveal(cur_r, cur_c)
                        else:
                            revealed[cur_r][cur_c] = True

                    if not game_over and check_win():
                        win = True

    main_menu()

if __name__ == "__main__":
    wrapper(main)