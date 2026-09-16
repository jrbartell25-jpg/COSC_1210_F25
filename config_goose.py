# config_goose.py
# Display
WIDTH, HEIGHT = 600, 600
FPS = 60
BG_COLOR = (95, 133, 117)    # green
WALL_COLOR = (200, 200, 200)

# Player
PLAYER_SPEED = 180.0  # px/sec
PLAYER_IMAGE_L  = "./assets/goose_left.png"
PLAYER_IMAGE_LS = "./assets/goose_LS.png"
PLAYER_IMAGE_R  = "./assets/goose_right.png"
PLAYER_IMAGE_RS = "./assets/goose_RS.png"
PLAYER_IMAGE_SIZE = (48, 48)   # w, h

# bread
BREAD_IMAGE = "./assets/cute-bread-cartoon-png.png"  # <- put your bread png here
BREAD_IMAGE_SIZE = (20, 20)

# balls
BALL_RADIUS = 14
BALL_SPEEDS = [(-150, 140), (160, -130), (170, 160)]   # three balls (vx, vy)
BALL_COLOR = (111, 27, 79)
N_BALLS = 3
N_BREAD = 5
