import pygame #type: ignore

pygame.init()
screen = pygame.display.set_mode((1280, 720))
FONT = pygame.font.SysFont("Ariel", 30)
VFONT = pygame.font.SysFont("Ariel", 50)
clock = pygame.time.Clock()
running = True
COLUMNS = 7
ROWS = 6
game_ended = 0
slots = [[0]*COLUMNS]*ROWS
slots = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
text = FONT.render('Press On a Column', False, (0, 0, 0))
slot_size = 100
slot_margin = 5
board_offset_left = screen.get_width()//2-slot_size*COLUMNS//2
board_offset_top = screen.get_height()//2-slot_size*ROWS//2
board_color = "blue"
background_color = "grey90"
scores = [0,0] # player1,player2
player1 = "green"
player2 = "orange"
turn = player1

# Functions 
def left_mouse_click():
    global game_ended,slots,turn
    if game_ended == 0:
        pos = pygame.mouse.get_pos()
        if is_on_board(pos):
            add_coin(pos)
        game_ended = check_victory()
    else:
        if game_ended == 1:
            scores[0] +=1
        else:
            scores[1] += 1
        slots = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        game_ended = 0
        turn = player1

def is_on_board(pos = None):
    if not pos: 
        print("ERROR: No Pos given.")
        return False
    
    col = (pos[0]-board_offset_left)//slot_size
    row = (pos[1]-board_offset_top)//slot_size
    if col > COLUMNS-1 or col<0 or row > ROWS-1 or row < 0:
        print("ERROR: Pressed outside of board. Col",col,"Row",row)
        return False
    
    return True

def add_coin(pos = None):
    global turn
    if not pos: 
        print("ERROR: No Pos given.")
        return
    col = (pos[0]-board_offset_left)//slot_size
    
    for slot in range(ROWS):
        if slot == 0 and slots[slot][col] != 0:
            print("ERROR: No more space in selected column")
            return
        if slot<ROWS-1 and slots[slot+1][col] == 0:
            continue           
         
        if turn == player1:
            slots[slot][col] = 1
            turn = player2
        else:
            slots[slot][col] = 2
            turn = player1
        return
    
def check_victory():
    piece = 1 if turn == player2 else 2
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if slots[r][c] == piece and slots[r][c+1] == piece and slots[r][c+2] == piece and slots[r][c+3] == piece:
                return piece
 
    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if slots[r][c] == piece and slots[r+1][c] == piece and slots[r+2][c] == piece and slots[r+3][c] == piece:
                return piece
 
    # Check positively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if slots[r][c] == piece and slots[r+1][c+1] == piece and slots[r+2][c+2] == piece and slots[r+3][c+3] == piece:
                return piece
 
    # Check negatively sloped diaganols
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if slots[r][c] == piece and slots[r-1][c+1] == piece and slots[r-2][c+2] == piece and slots[r-3][c+3] == piece:
                return piece
            
    return 0

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points
    
def render(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

# Game Loop
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            left_mouse_click()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background_color)
    color = background_color
    
    pygame.draw.circle(screen,player1,(board_offset_left/2,screen.get_height()/2),slot_size//2)
    pygame.draw.circle(screen,player2,(board_offset_left*1.5+(COLUMNS)*slot_size,screen.get_height()/2),slot_size//2)
    p1 = (FONT.render((str)(scores[0]), False, (0, 0, 0)))
    screen.blit(p1, (board_offset_left/2-p1.get_rect().width/2,screen.get_height()/2-p1.get_rect().height/2))
    p2 = (FONT.render((str)(scores[1]), False, (0, 0, 0)))
    screen.blit(p2, (-p2.get_rect().width/2+board_offset_left*1.5+(COLUMNS)*slot_size,screen.get_height()/2-p2.get_rect().height/2))

    
    # draws the board
    for col in range(COLUMNS):
        for row in range(ROWS): 
            pygame.draw.rect(screen,"blue",pygame.Rect((slot_size*col)+board_offset_left,(slot_size*row)+board_offset_top,slot_size,slot_size))
            if slots[row][col] == 1:
                color = player1
            elif slots[row][col] == 2:
                color = player2
            else:
                color = background_color
            pygame.draw.circle(screen,color,(slot_size*col+slot_size//2+board_offset_left,slot_size*row+slot_size//2+board_offset_top),slot_size//2-slot_margin)
    
    
    # Text
    screen.blit(text, (-text.get_rect().width/2+slot_size*COLUMNS/2+board_offset_left,text.get_rect().height/2+slot_size*ROWS+board_offset_top))
    if game_ended > 0:
        victory_text = (f'{f"Player1-{player1}" if game_ended == 1 else f"Player2-{player2}"} Won!')
        screen.blit(render(victory_text,VFONT,gfcolor=pygame.Color(background_color),ocolor=pygame.Color("black")),(-text.get_rect().width/2+screen.get_width()/2,-text.get_rect().height/2+screen.get_height()/2))
        
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    

pygame.quit()

