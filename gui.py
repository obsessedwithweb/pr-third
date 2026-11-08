import pygame

def draw_vertical_gradient(surface, top_color, bottom_color):
    width, height = surface.get_size()
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))


def draw_shadow_rect(surface, rect, radius=8, alpha=70, offset=(4, 6)):
    shadow_surf = pygame.Surface((rect.width + 12, rect.height + 12), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, alpha), (offset[0], offset[1], rect.width, rect.height), border_radius=radius)
    surface.blit(shadow_surf, (rect.x - 6, rect.y - 6))


def render_gui(initial_puzzle, solution_node, explored_count, algo_name="A*"):
    pygame.init()
    states = solution_node.getPath() if solution_node else [initial_puzzle]
    actions = solution_node.getSolution() if solution_node else []

    rows = initial_puzzle.rows
    cols = initial_puzzle.cols
    TILE_SIZE = min(64, max(44, 480 // max(rows, cols)))
    BOARD_PADDING = 24
    HEADER_HEIGHT = 70
    CONTROL_PANEL_HEIGHT = 130

    board_width = cols * TILE_SIZE
    board_height = rows * TILE_SIZE

    screen_width = max(board_width + (BOARD_PADDING * 2), 640)
    screen_height = HEADER_HEIGHT + board_height + CONTROL_PANEL_HEIGHT + (BOARD_PADDING * 2)

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(f"Sokoban AI Studio (Part 3) - {algo_name}")

    font_title = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 20, bold=True)
    font_bold = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 15, bold=True)
    font_main = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 14)
    font_small = pygame.font.SysFont("Segoe UI, Helvetica, Arial", 12)

    bg_surface = pygame.Surface((screen_width, screen_height))
    draw_vertical_gradient(bg_surface, (15, 23, 42), (30, 41, 59))

    step_idx = 0
    auto_play = False
    delay_ms = 1000
    last_tick = pygame.time.get_ticks()

    btn_play_rect = pygame.Rect(screen_width // 2 - 60, screen_height - 95, 120, 38)
    btn_prev_rect = pygame.Rect(screen_width // 2 - 160, screen_height - 95, 80, 38)
    btn_next_rect = pygame.Rect(screen_width // 2 + 80, screen_height - 95, 80, 38)
    btn_reset_rect = pygame.Rect(screen_width // 2 - 250, screen_height - 95, 70, 38)
    btn_faster_rect = pygame.Rect(screen_width // 2 + 180, screen_height - 95, 45, 38)
    btn_slower_rect = pygame.Rect(screen_width // 2 + 235, screen_height - 95, 45, 38)

    running = True
    clock = pygame.time.Clock()

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_play_rect.collidepoint(mouse_pos):
                    auto_play = not auto_play
                elif btn_prev_rect.collidepoint(mouse_pos) and step_idx > 0:
                    step_idx -= 1
                elif btn_next_rect.collidepoint(mouse_pos) and step_idx < len(states) - 1:
                    step_idx += 1
                elif btn_reset_rect.collidepoint(mouse_pos):
                    step_idx = 0
                    auto_play = False
                elif btn_faster_rect.collidepoint(mouse_pos):
                    delay_ms = max(200, delay_ms - 200)
                elif btn_slower_rect.collidepoint(mouse_pos):
                    delay_ms = min(2000, delay_ms + 200)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    auto_play = not auto_play
                elif event.key == pygame.K_RIGHT and step_idx < len(states) - 1:
                    step_idx += 1
                elif event.key == pygame.K_LEFT and step_idx > 0:
                    step_idx -= 1
                elif event.key == pygame.K_r:
                    step_idx = 0
                    auto_play = False
                elif event.key == pygame.K_UP or event.key == pygame.K_EQUALS:
                    delay_ms = max(200, delay_ms - 200)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_MINUS:
                    delay_ms = min(2000, delay_ms + 200)

        now = pygame.time.get_ticks()
        if auto_play and (now - last_tick >= delay_ms):
            if step_idx < len(states) - 1:
                step_idx += 1
            else:
                auto_play = False
            last_tick = now

        screen.blit(bg_surface, (0, 0))

        header_rect = pygame.Rect(20, 15, screen_width - 40, 48)
        draw_shadow_rect(screen, header_rect, radius=10, alpha=80, offset=(0, 4))
        pygame.draw.rect(screen, (30, 41, 59), header_rect, border_radius=10)
        pygame.draw.rect(screen, (71, 85, 105), header_rect, 1, border_radius=10)

        title_surf = font_title.render("SOKOBAN AI STUDIO (PART 3)", True, (248, 250, 252))
        screen.blit(title_surf, (36, 26))

        algo_badge = font_bold.render(f"Algorithm: {algo_name}", True, (56, 189, 248))
        screen.blit(algo_badge, (screen_width - algo_badge.get_width() - 40, 29))

        board_x = (screen_width - board_width) // 2
        board_y = HEADER_HEIGHT + BOARD_PADDING // 2

        board_bg_rect = pygame.Rect(board_x - 6, board_y - 6, board_width + 12, board_height + 12)
        draw_shadow_rect(screen, board_bg_rect, radius=12, alpha=100, offset=(0, 6))
        pygame.draw.rect(screen, (15, 23, 42), board_bg_rect, border_radius=12)

        current_board = states[step_idx].board

        for r in range(rows):
            for c in range(cols):
                tx = board_x + c * TILE_SIZE
                ty = board_y + r * TILE_SIZE
                tile_rect = pygame.Rect(tx, ty, TILE_SIZE, TILE_SIZE)
                cell = current_board[r][c]

                if cell == 'O':
                    draw_shadow_rect(screen, tile_rect, radius=6, alpha=40, offset=(2, 3))
                    pygame.draw.rect(screen, (51, 65, 85), tile_rect, border_radius=6)
                    pygame.draw.rect(screen, (71, 85, 105), tile_rect, 2, border_radius=6)
                    pygame.draw.line(screen, (100, 116, 139), (tx + 4, ty + TILE_SIZE // 2), (tx + TILE_SIZE - 4, ty + TILE_SIZE // 2), 1)
                else:
                    pygame.draw.rect(screen, (241, 234, 224), tile_rect, border_radius=4)
                    pygame.draw.rect(screen, (226, 214, 198), tile_rect, 1, border_radius=4)

                if cell in ('S', '.', '*'):
                    pad = max(4, TILE_SIZE // 4)
                    tgt_rect = pygame.Rect(tx + pad, ty + pad, TILE_SIZE - pad * 2, TILE_SIZE - pad * 2)
                    pygame.draw.rect(screen, (239, 68, 68), tgt_rect, border_radius=6)
                    pygame.draw.circle(screen, (254, 202, 202), (tx + TILE_SIZE // 2, ty + TILE_SIZE // 2), max(2, TILE_SIZE // 10))

                if cell in ('B', '*'):
                    pad = max(4, TILE_SIZE // 8)
                    b_rect = pygame.Rect(tx + pad, ty + pad, TILE_SIZE - pad * 2, TILE_SIZE - pad * 2)
                    draw_shadow_rect(screen, b_rect, radius=8, alpha=90, offset=(2, 4))
                    if cell == '*':
                        pygame.draw.rect(screen, (34, 197, 94), b_rect, border_radius=8)
                        pygame.draw.rect(screen, (74, 222, 128), b_rect, 2, border_radius=8)
                        pygame.draw.circle(screen, (220, 252, 231), (tx + TILE_SIZE // 2, ty + TILE_SIZE // 2), max(3, TILE_SIZE // 8))
                    else:
                        pygame.draw.rect(screen, (180, 105, 50), b_rect, border_radius=8)
                        pygame.draw.rect(screen, (217, 135, 78), b_rect, 2, border_radius=8)
                        pygame.draw.line(screen, (138, 77, 33), (tx + pad + 4, ty + pad + 4), (tx + TILE_SIZE - pad - 4, ty + TILE_SIZE - pad - 4), 2)
                        pygame.draw.line(screen, (138, 77, 33), (tx + pad + 4, ty + TILE_SIZE - pad - 4), (tx + TILE_SIZE - pad - 4, ty + pad + 4), 2)

                if cell in ('R', '.'):
                    center_pos = (tx + TILE_SIZE // 2, ty + TILE_SIZE // 2)
                    radius = max(8, TILE_SIZE // 3)
                    shadow_circle = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(shadow_circle, (0, 0, 0, 80), (TILE_SIZE // 2 + 2, TILE_SIZE // 2 + 3), radius)
                    screen.blit(shadow_circle, (tx, ty))

                    pygame.draw.circle(screen, (37, 99, 235), center_pos, radius)
                    pygame.draw.circle(screen, (96, 165, 250), center_pos, radius, 2)
                    eye_offset = max(2, radius // 4)
                    eye_r = max(1, radius // 5)
                    pygame.draw.circle(screen, (248, 250, 252), (center_pos[0] - eye_offset, center_pos[1] - eye_offset), eye_r * 2)
                    pygame.draw.circle(screen, (248, 250, 252), (center_pos[0] + eye_offset, center_pos[1] - eye_offset), eye_r * 2)
                    pygame.draw.circle(screen, (15, 23, 42), (center_pos[0] - eye_offset + 1, center_pos[1] - eye_offset), eye_r)
                    pygame.draw.circle(screen, (15, 23, 42), (center_pos[0] + eye_offset + 1, center_pos[1] - eye_offset), eye_r)

        ctrl_rect = pygame.Rect(20, screen_height - 125, screen_width - 40, 110)
        draw_shadow_rect(screen, ctrl_rect, radius=12, alpha=90, offset=(0, 4))
        pygame.draw.rect(screen, (30, 41, 59), ctrl_rect, border_radius=12)
        pygame.draw.rect(screen, (71, 85, 105), ctrl_rect, 1, border_radius=12)

        total_actions = len(actions)
        last_move = actions[step_idx - 1] if step_idx > 0 else "START"
        stat_line = f"Step: {step_idx}/{total_actions}  |  Last Action: {last_move}  |  Cost: {solution_node.g if solution_node else 0}  |  Explored: {explored_count}"
        screen.blit(font_main.render(stat_line, True, (226, 232, 240)), (36, screen_height - 118))

        status_text = "PLAYING" if auto_play else "PAUSED"
        status_color = (34, 197, 94) if auto_play else (245, 158, 11)
        status_surf = font_bold.render(status_text, True, status_color)
        screen.blit(status_surf, (screen_width - status_surf.get_width() - 40, screen_height - 118))

        play_color = (16, 185, 129) if auto_play else (59, 130, 246)
        if btn_play_rect.collidepoint(mouse_pos):
            play_color = tuple(min(255, c + 25) for c in play_color)
        pygame.draw.rect(screen, play_color, btn_play_rect, border_radius=8)
        play_label = "Pause" if auto_play else "Start"
        play_txt = font_bold.render(play_label, True, (255, 255, 255))
        screen.blit(play_txt, (btn_play_rect.centerx - play_txt.get_width() // 2, btn_play_rect.centery - play_txt.get_height() // 2))

        def draw_button(rect, text, bg=(71, 85, 105), fg=(241, 245, 249)):
            color = tuple(min(255, c + 20) for c in bg) if rect.collidepoint(mouse_pos) else bg
            pygame.draw.rect(screen, color, rect, border_radius=8)
            txt_surf = font_bold.render(text, True, fg)
            screen.blit(txt_surf, (rect.centerx - txt_surf.get_width() // 2, rect.centery - txt_surf.get_height() // 2))

        draw_button(btn_prev_rect, "◀ Step")
        draw_button(btn_next_rect, "Step ▶")
        draw_button(btn_reset_rect, "Reset", bg=(100, 116, 139))
        draw_button(btn_faster_rect, "+", bg=(51, 65, 85))
        draw_button(btn_slower_rect, "-", bg=(51, 65, 85))

        spd_txt = font_small.render(f"Delay: {delay_ms/1000:.1f}s", True, (148, 163, 184))
        screen.blit(spd_txt, (btn_slower_rect.right + 10, screen_height - 85))

        pygame.display.flip()
        clock.tick(30)

        total_actions = len(actions)

    pygame.quit()
