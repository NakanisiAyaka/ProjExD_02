import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1250, 680

delta = {#3移動量辞書
    pg.K_UP: (0, -5),#キー：横/縦
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}
def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面買いを判定し、真理値タプルを返す関数
    引数 rct:こうかとんor爆弾Surfaceのrct
    戻り値:横方向、縦方向はみ出し判定結果（画面内:True/画面外:False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()

    kk_rct.center = 900,400
    bom_img = pg.Surface((20, 20))
    bom_img.set_colorkey((0, 0, 0))#1
    pg.draw.circle(bom_img, (255, 0, 0), (10, 10), 10)#1

    bom_rct = bom_img.get_rect()#1
    bom_rct.centerx = random.randint(0,WIDTH)#1
    bom_rct.centery = random.randint(0,HEIGHT)#1
    vx, vy = +5, +5 #2

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bom_rct):
            print("Game Over")
            return   

        screen.blit(bg_img, [0, 0])
        key_lst =pg.key.get_pressed()
        sum_mv =[0,0]
        for k,tpl in delta.items():
            if key_lst[k]:#キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)

        screen.blit(kk_img,kk_rct)
        kk_rct.move_ip(sum_mv[0], sum_mv[1])#こうかとん移動
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bom_rct.move_ip(vx, vy) #2　爆弾移動
        yoko, tate = check_bound(bom_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        bom_rct.move_ip(vx, vy)
        screen.blit(bom_img,bom_rct)#1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()