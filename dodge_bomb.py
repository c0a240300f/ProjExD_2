import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5), pg.K_DOWN:(0, +5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(+5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数はこうかとんRectまたは爆弾Rect
    戻り値は判定結果タプル(横, 縦)
    画面内ならTrue画面外ならFalse
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    爆弾に当たったら半透明の黒が背景
    泣いているこうかとん及び文字列GameOverが出力するようにする
    """
    bl_img = pg.Surface((WIDTH*2, HEIGHT*2))  # 半透明黒背景
    bl_img.set_alpha(120)
    pg.draw.rect(bl_img,(0, 0, 0),pg.Rect(0, 0, WIDTH, HEIGHT))
    bl_rct = bl_img.get_rect()
    bl_rct.center = (WIDTH, HEIGHT)
    screen.blit(bl_img, bl_rct)
    fonto = pg.font.Font(None, 50)  # 文字列
    txt = fonto.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(txt, [450, 310])
    kk_img1 = pg.image.load("fig/8.png")  # こうかとんの画像左
    kk_img1 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct1 = kk_img1.get_rect()
    kk_rct1.center = 390, 320
    screen.blit(kk_img1, kk_rct1)
    kk_img2 = pg.image.load("fig/8.png")  # こうかとんの画像右
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_rct2 = kk_img2.get_rect()
    kk_rct1.center = 710, 320
    screen.blit(kk_img1, kk_rct1)
    pg.display.update()
    time.sleep(5)

    
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")  
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとん抽出
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾制作
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5
    clock = pg.time.Clock()  # 時間観測
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])

        # こうかとんと爆弾の座標の重なりを計測
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return
        
        key_lst = pg.key.get_pressed()  # DELTAから座標の値を取得
        sum_mv = [0, 0]
        for key, mv in DELTA.items():  # キーボードの入力による出力の変更
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 左右
                sum_mv[1] += mv[1]  # 上下
        kk_rct.move_ip(sum_mv)
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5

        # こうかとん画面外検知及び挙動
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)

        # 爆弾の画面外検知及び挙動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
