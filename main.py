
import pygame
import random
import sys
import os

# --------- CẤU HÌNH CHUNG ---------
WIDTH, HEIGHT = 400, 600
FPS = 60
ICON_SIZE = 35 

# Bird config
BIRD_X = 80
BIRD_RADIUS = 16
GRAVITY = 0.45
JUMP_V = -8.5

# Pipe config
PIPE_WIDTH = 70
PIPE_GAP_MIN = 120
PIPE_GAP_MAX = 180
PIPE_SPEED = 2.5
PIPE_DISTANCE_MIN = 200
PIPE_DISTANCE_MAX = 320

# Ground config
GROUND_HEIGHT = 40 
GROUND_Y = HEIGHT - GROUND_HEIGHT

# File names
HIGH_SCORE_FILE = "highscore.txt"

# --- ĐƯỜNG DẪN ÂM THANH ---
BGM_FILE = "assets/sounds/bgm.mp3" 
JUMP_SOUND_FILE = "assets/sounds/jump.wav"
SCORE_SOUND_FILE = "assets/sounds/score.wav"

# --- ĐƯỜNG DẪN HÌNH ẢNH ---
BIRD_IMAGE_FILE = "image1.png" 
BG_IMAGE_FILE = "assets/image/bg.png" 
SPEAKER_ON_FILE = "assets/image/speaker_on.png"
SPEAKER_OFF_FILE = "assets/image/speaker_off.png"
PAUSE_ICON_FILE = "assets/image/pause_icon.png"
PLAY_ICON_FILE = "assets/image/play_icon.png"

# --------- HỖ TRỢ (load/save settings) Giữ nguyên ---------
def load_settings(path=HIGH_SCORE_FILE):
    hs = 0
    bgm_and_effects_on = True
    try:
        with open(path, "r") as f:
            lines = f.readlines()
            if len(lines) > 0:
                hs = int(lines[0].strip())
            if len(lines) > 1:
                bgm_and_effects_on = (int(lines[1].strip()) == 1)
            return hs, bgm_and_effects_on
    except:
        return hs, bgm_and_effects_on 

def save_settings(score, bgm_and_effects_on, path=HIGH_SCORE_FILE):
    bgm_state = 1 if bgm_and_effects_on else 0
    try:
        with open(path, "w") as f:
            f.write(str(score) + "\n")
            f.write(str(bgm_state) + "\n")
    except Exception as e:
        print("Không lưu được cài đặt:", e)

# --------- LỚP VẬT (Bird, Pipe) Giữ nguyên ---------
class Bird:
    def __init__(self, image):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.vel = 0.0
        self.radius = BIRD_RADIUS
        self.alive = True
        self.rotation = 0.0
        
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        self.vel = JUMP_V

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        
        self.rotation = max(-30, min(60, -self.vel * 4))
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))

        if self.y - self.radius < 0:
            self.y = self.radius
            self.vel = 0
        if self.y + self.radius > GROUND_Y:
            self.y = GROUND_Y - self.radius
            self.alive = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

class Pipe:
    def __init__(self, x):
        self.x = x
        gap = random.randint(PIPE_GAP_MIN, PIPE_GAP_MAX)
        top_h = random.randint(60, GROUND_Y - 60 - gap)
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, top_h)
        self.bottom = pygame.Rect(self.x, top_h + gap, PIPE_WIDTH, GROUND_Y - (top_h + gap)) 
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top.x = int(self.x)
        self.bottom.x = int(self.x)

    def draw(self, surf):
        pygame.draw.rect(surf, (34,139,34), self.top)
        pygame.draw.rect(surf, (34,139,34), self.bottom)
        pygame.draw.rect(surf, (20,100,20), (self.top.x, self.top.height - 8, PIPE_WIDTH, 8))
        pygame.draw.rect(surf, (20,100,20), (self.bottom.x, self.bottom.y, PIPE_WIDTH, 8))

    def off_screen(self):
        return self.x + PIPE_WIDTH < -10

# --------- HÀM HỖ TRỢ Giữ nguyên ---------
def check_collision(bird, pipes):
    bird_rect = bird.get_rect()
    for p in pipes:
        if bird_rect.colliderect(p.top) or bird_rect.colliderect(p.bottom):
            return True
    if bird_rect.bottom >= GROUND_Y:
        return True
    return not bird.alive

def make_initial_pipes():
    pipes = []
    x = WIDTH + 50
    while x < WIDTH + 700:
        pipes.append(Pipe(x))
        x += random.randint(PIPE_DISTANCE_MIN, PIPE_DISTANCE_MAX)
    return pipes

# --------- MAIN GAME (Đã sửa lỗi Tắt FX, BGM luôn phát) ---------
def main():
    # Khởi tạo Pygame Mixer
    try:
        pygame.mixer.pre_init(44100, -16, 2, 512)
    except Exception as e:
        print(f"Lỗi cấu hình Pygame Mixer: {e}")
        
    pygame.init()
    
    mixer_ok = pygame.mixer.get_init() is not None
    if not mixer_ok:
        print("Lỗi: Không thể khởi tạo Pygame Mixer. Âm thanh sẽ bị tắt.")
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Brid")
    clock = pygame.time.Clock()

    # font
    font = pygame.font.SysFont("Arial", 28)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)
    medium_font = pygame.font.SysFont("Arial", 36)

    # --- LOAD HÌNH ẢNH --- (Giữ nguyên)
    bird_image = None
    try:
        if os.path.exists(BIRD_IMAGE_FILE):
             bird_image = pygame.image.load(BIRD_IMAGE_FILE).convert_alpha()
             target_size = BIRD_RADIUS * 2
             bird_image = pygame.transform.scale(bird_image, (target_size, target_size))
        else:
             raise pygame.error("Bird image file not found.")
    except pygame.error as e:
        bird_image = pygame.Surface((BIRD_RADIUS * 2, BIRD_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(bird_image, (255, 220, 0), (BIRD_RADIUS, BIRD_RADIUS), BIRD_RADIUS)
    
    bg_image = None
    try:
        if os.path.exists(BG_IMAGE_FILE):
            bg_image = pygame.image.load(BG_IMAGE_FILE).convert()
            bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        else:
            raise pygame.error("Background image file not found.")
    except pygame.error as e:
        pass
    
    icons = {}
    icon_files = {
        'speaker_on': SPEAKER_ON_FILE, 'speaker_off': SPEAKER_OFF_FILE,
        'pause': PAUSE_ICON_FILE, 'play': PLAY_ICON_FILE
    }
    for name, file in icon_files.items():
        try:
            if os.path.exists(file):
                img = pygame.image.load(file).convert_alpha()
                icons[name] = pygame.transform.scale(img, (ICON_SIZE, ICON_SIZE))
            else:
                raise pygame.error(f"Icon file {file} not found.")
        except pygame.error as e:
            icons[name] = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(icons[name], (255, 0, 255), icons[name].get_rect()) 

    # --- LOAD SOUNDS ---
    jump_sound = None; score_sound = None
    bgm_loaded = False
    
    if mixer_ok:
        try:
            if os.path.exists(JUMP_SOUND_FILE): 
                jump_sound = pygame.mixer.Sound(JUMP_SOUND_FILE)
            if os.path.exists(SCORE_SOUND_FILE): 
                score_sound = pygame.mixer.Sound(SCORE_SOUND_FILE)
            if os.path.exists(BGM_FILE): 
                pygame.mixer.music.load(BGM_FILE)
                bgm_loaded = True
        except Exception as e:
            print(f"Lỗi tải file âm thanh: {e}. Âm thanh bị tắt.")
            mixer_ok = False 

    # Load highscore và trạng thái BGM/FX
    highscore, bgm_and_effects_on = load_settings() 
    if bgm_and_effects_on and bgm_loaded and mixer_ok:
        pygame.mixer.music.play(-1)

    # game state
    bird = Bird(bird_image)
    pipes = make_initial_pipes()
    score = 0
    running = True
    game_over = False
    paused = False 

    bg_color = (135, 206, 235)
    
    # === KHU VỰC CẢM ỨNG (BUTTON RECTS) ===
    BUTTON_PADDING = 10
    BGM_BUTTON_RECT = pygame.Rect(WIDTH - ICON_SIZE - BUTTON_PADDING, BUTTON_PADDING, ICON_SIZE, ICON_SIZE)
    PAUSE_BUTTON_RECT = pygame.Rect(BGM_BUTTON_RECT.left - ICON_SIZE - BUTTON_PADDING, BUTTON_PADDING, ICON_SIZE, ICON_SIZE)
    
    
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # === XỬ LÝ CẢM ỨNG/NHẤP CHUỘT (MOUSEBUTTONDOWN) ===
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                
                # 1. Nhấp vào Nút BGM/FX
                if BGM_BUTTON_RECT.collidepoint(click_pos) and not game_over and mixer_ok:
                    bgm_and_effects_on = not bgm_and_effects_on 
                    
                    if bgm_and_effects_on: # BẬT (ON)
                        if bgm_loaded:
                            # Play BGM nếu nó đang bị STOP (do tắt lần trước)
                            if pygame.mixer.music.get_busy() == 0:
                                pygame.mixer.music.play(-1)
                            
                    else: # TẮT (OFF)
                        # Dừng nhạc nền VÀ FX
                        if bgm_loaded:
                             pygame.mixer.music.stop() 
                        
                    save_settings(highscore, bgm_and_effects_on)
                    
                # 2. Nhấp vào Nút Pause/Resume
                elif PAUSE_BUTTON_RECT.collidepoint(click_pos) and not game_over and mixer_ok:
                    paused = not paused
                    
                    # QUAN TRỌNG: Loại bỏ lệnh PAUSE/UNPAUSE nhạc nền. Nhạc nền LUÔN PHÁT.
                    # if bgm_and_effects_on and bgm_loaded:
                    #     if paused:
                    #         pygame.mixer.music.pause()
                    #     else:
                    #         pygame.mixer.music.unpause()
                            
                # 3. Nhấp để Nhảy 
                elif not game_over and not paused:
                    bird.jump()
                    if jump_sound and mixer_ok and bgm_and_effects_on: 
                        jump_sound.play()
                        
                # 4. Nhấp để Restart (Khi Game Over)
                elif game_over:
                    bird = Bird(bird_image)
                    pipes = make_initial_pipes()
                    score = 0 
                    game_over = False
                    paused = False
                    if jump_sound and mixer_ok:
                        jump_sound.stop()
                    
                    # BGM tự động lặp lại nên không cần play lại ở đây trừ khi nó bị stop
                    if bgm_and_effects_on and bgm_loaded and mixer_ok:
                        if pygame.mixer.music.get_busy() == 0:
                            pygame.mixer.music.play(-1)

            # Giữ lại phím tắt dự phòng (nhảy, ESC)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP) and not paused and not game_over:
                    bird.jump()
                    if jump_sound and mixer_ok and bgm_and_effects_on:
                        jump_sound.play()
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over and not paused:
            # update
            bird.update()
            for p in pipes:
                p.update()

            pipes = [p for p in pipes if not p.off_screen()]

            if len(pipes) == 0 or (pipes[-1].x < WIDTH - random.randint(PIPE_DISTANCE_MIN-50, PIPE_DISTANCE_MAX-50)):
                pipes.append(Pipe(WIDTH + random.randint(0, 80)))

            # scoring:
            for p in pipes:
                if (not p.passed) and (p.x + PIPE_WIDTH < bird.x):
                    p.passed = True
                    score += 1
                    if score_sound and mixer_ok and bgm_and_effects_on:
                        score_sound.play()
                    if score > highscore:
                        highscore = score
                        save_settings(highscore, bgm_and_effects_on)

            # collision check
            if check_collision(bird, pipes):
                game_over = True
                # QUAN TRỌNG: Loại bỏ lệnh dừng nhạc nền khi Game Over
                # if bgm_loaded and mixer_ok:
                #     pygame.mixer.music.stop() 
                if score > highscore:
                    highscore = score
                save_settings(highscore, bgm_and_effects_on)

        # ---------- DRAW ----------
        if bg_image:
            screen.blit(bg_image, (0, 0))
        else:
            screen.fill(bg_color)

        # ground: VẼ THANH NGANG BÊN DƯỚI
        ground_rect = pygame.Rect(0, GROUND_Y, WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(screen, (222,184,135), ground_rect)

        # draw pipes
        for p in pipes:
            p.draw(screen)

        # bird
        bird.draw(screen)

        # HUD: score + highscore
        score_surf = font.render(f"Score: {score}", True, (255,255,255))
        hs_surf = font.render(f"High: {highscore}", True, (255,255,255))
        screen.blit(score_surf, (10, 10))
        screen.blit(hs_surf, (10, 40))
        
        # === VẼ NÚT BIỂU TƯỢNG ===
        
        # 1. Nút BGM (Loa)
        bgm_icon = icons['speaker_on'] if bgm_and_effects_on else icons['speaker_off']
        screen.blit(bgm_icon, BGM_BUTTON_RECT.topleft)

        # 2. Nút Pause/Resume (|| hoặc >)
        pause_icon = icons['pause'] if not paused else icons['play']
        screen.blit(pause_icon, PAUSE_BUTTON_RECT.topleft)
        
        # Game over overlay
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,140))
            screen.blit(overlay, (0,0))
            txt = big_font.render("Game Over", True, (255, 100, 100))
            sub = font.render("Click anywhere to Restart", True, (255,255,255))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))
            
        # Pause overlay
        elif paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,100))
            screen.blit(overlay, (0,0))
            txt = big_font.render("PAUSED", True, (255, 255, 0))
            # Sửa lại hướng dẫn người dùng
            sub = medium_font.render("Click PLAY button to resume", True, (255,255,255)) 
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
            screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 20))


        pygame.display.flip()

    save_settings(highscore, bgm_and_effects_on)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
