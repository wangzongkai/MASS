import math

import numpy as np
import pygame
def  position2screen( x0 , y0 ,o_s,rho):
    # 屏幕转化器，有平时的坐标转化成特殊坐标
    x_s0 , y_s0 =o_s[0],o_s[1]
    x_screen = (x0-x_s0)*rho
    y_screen = (-y0-y_s0)*rho
    return x_screen , y_screen


import math
import pygame

def draw_point(screen,points, o_s, rho):
    for p in points:
        xs0, ys0 = position2screen(p[0], p[1], o_s, rho)
        pygame.draw.circle(screen,'red',[xs0, ys0],1)
def draw_catamaran1(screen, x0, y0, course0, rudder, shipname, o_s, rho):
    """
    绘制双体船图形（数学坐标系）
    :param screen: Pygame屏幕对象
    :param x0: 船中心x坐标（数学坐标系）
    :param y0: 船中心y坐标（数学坐标系）
    :param course0: 航向角度（正Y轴顺时针，0°指向+Y，90°指向+X）
    :param rudder: 舵角
    :param shipname: 船名
    :param o_s: 屏幕偏移量
    :param rho: 缩放比例
    :return: None
    """
    # 绘制双体船的两个船体和甲板
    hull1, hull2, deck = draw_catamaran_shape1(x0, y0, course0, rudder)

    # 转换第一个船体坐标并绘制
    hull1_screen = [position2screen(x, y, o_s, rho) for x, y in zip(hull1[0], hull1[1])]
    pygame.draw.polygon(screen, 'blue', hull1_screen, width=1)

    # 转换第二个船体坐标并绘制
    hull2_screen = [position2screen(x, y, o_s, rho) for x, y in zip(hull2[0], hull2[1])]
    pygame.draw.polygon(screen, 'blue', hull2_screen, width=1)

    # 计算两个船体的中心点（在数学坐标系）
    x_a = np.mean(hull1[0])  # 第一个船体X中心
    y_a = np.mean(hull1[1])  # 第一个船体Y中心
    x_b = np.mean(hull2[0])  # 第二个船体X中心
    y_b = np.mean(hull2[1])  # 第二个船体Y中心

    # 转换中心点到屏幕坐标
    x_a_screen, y_a_screen = position2screen(x_a, y_a, o_s, rho)
    x_b_screen, y_b_screen = position2screen(x_b, y_b, o_s, rho)

    # 绘制连接线
    pygame.draw.line(screen, 'blue', (x_a_screen, y_a_screen), (x_b_screen, y_b_screen), 2)

    # 绘制船名
    x0_screen, y0_screen = position2screen(x0, y0, o_s, rho)
    font = pygame.font.SysFont('Arial Narrow', 18)
    text = font.render(shipname, True, 'black')
    # 将文字放在船中心稍上方位置
    screen.blit(text, (x0_screen - text.get_width() / 2, y0_screen - 20))


def draw_catamaran_shape1(x0, y0, course, rudder):
    """
    生成双体船的形状坐标（数学坐标系）
    :param x0: 中心x坐标
    :param y0: 中心y坐标
    :param course: 航向（正Y轴顺时针，0°指向+Y，90°指向+X）
    :param rudder: 舵角
    :return: (hull1, hull2, deck) 两个船体和甲板的坐标
    """
    # 船体尺寸参数（数学坐标系）
    hull_length = 20  # 船体长度
    hull_width = 4  # 船体宽度
    separation = 12  # 两个船体之间的间距
    deck_length = 15  # 甲板长度

    # 计算旋转角度（弧度），转换为从正X轴逆时针方向的角度（标准数学角度）
    # 因为course是正Y轴顺时针方向，所以转换为标准角度是 (90 - course) % 360
    angle = (np.pi / 2) - course  # 90度 = π/2 弧度，然后减去 course（弧度）
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    # 左船体（从船尾到船头，顺时针定义多边形）
    left_hull = [
        [-hull_length / 2, -hull_length / 2, hull_length / 2, hull_length / 2],  # X坐标
        [-separation / 2 - hull_width, -separation / 2, -separation / 2, -separation / 2 - hull_width]  # Y坐标
    ]

    # 右船体
    right_hull = [
        [-hull_length / 2, -hull_length / 2, hull_length / 2, hull_length / 2],
        [separation / 2, separation / 2 + hull_width, separation / 2 + hull_width, separation / 2]
    ]

    # 甲板（连接两个船体）
    deck = [
        [-deck_length / 2, deck_length / 2, deck_length / 2, -deck_length / 2],
        [-separation / 2, -separation / 2, separation / 2, separation / 2]
    ]

    # 旋转和平移所有点
    def rotate_translate(points):
        rotated = []
        for i in range(len(points[0])):
            x = points[0][i]
            y = points[1][i]
            # 旋转（标准数学旋转公式）
            x_rot = x * cos_angle - y * sin_angle
            y_rot = x * sin_angle + y * cos_angle
            # 平移
            rotated.append([x_rot + x0, y_rot + y0])

        # 分离x和y坐标
        x_coords = [p[0] for p in rotated]
        y_coords = [p[1] for p in rotated]
        return [x_coords, y_coords]

    left_hull_rot = rotate_translate(left_hull)
    right_hull_rot = rotate_translate(right_hull)
    deck_rot = rotate_translate(deck)

    return left_hull_rot, right_hull_rot, deck_rot

def draw_catamaran(screen, x0, y0, course0,shipname, o_s, rho):
    """
    绘制双体船图形（数学坐标系）
    """
    # 获取船体、甲板和船头标记的坐标
    hull1, hull2, deck, bow1, bow2 = draw_catamaran_shape(x0, y0, course0)

    # 转换并绘制第一个船体
    hull1_screen = [position2screen(x, y, o_s, rho) for x, y in zip(hull1[0], hull1[1])]
    pygame.draw.polygon(screen, 'blue', hull1_screen, width=1)

    # 转换并绘制第二个船体
    hull2_screen = [position2screen(x, y, o_s, rho) for x, y in zip(hull2[0], hull2[1])]
    pygame.draw.polygon(screen, 'blue', hull2_screen, width=1)

    # 转换并绘制左船头三角形
    bow1_screen = [position2screen(x, y, o_s, rho) for x, y in zip(bow1[0], bow1[1])]
    pygame.draw.polygon(screen, 'blue', bow1_screen, width=1)  # 实心填充

    # 转换并绘制右船头三角形
    bow2_screen = [position2screen(x, y, o_s, rho) for x, y in zip(bow2[0], bow2[1])]
    pygame.draw.polygon(screen, 'blue', bow2_screen, width=1)  # 实心填充

    # 计算两个船体的中心点（在数学坐标系）
    x_a = np.mean(hull1[0])  # 第一个船体X中心
    y_a = np.mean(hull1[1])  # 第一个船体Y中心
    x_b = np.mean(hull2[0])  # 第二个船体X中心
    y_b = np.mean(hull2[1])  # 第二个船体Y中心

    # 转换中心点到屏幕坐标
    x_a_screen, y_a_screen = position2screen(x_a, y_a, o_s, rho)
    x_b_screen, y_b_screen = position2screen(x_b, y_b, o_s, rho)

    # 绘制连接线
    pygame.draw.line(screen, 'blue', (x_a_screen, y_a_screen), (x_b_screen, y_b_screen), 2)

    # 绘制船名
    x0_screen, y0_screen = position2screen(x0, y0, o_s, rho)
    font = pygame.font.SysFont('Arial Narrow', 18)
    text = font.render(shipname, True, 'black')
    screen.blit(text, (x0_screen - text.get_width() / 2, y0_screen - 20))
def draw_catamaran_shape(x0, y0, course):
    """
    生成双体船的形状坐标（数学坐标系）
    :param x0: 中心x坐标
    :param y0: 中心y坐标
    :param course: 航向（正Y轴顺时针，0°指向+Y，90°指向+X）
    :param rudder: 舵角
    :return: (hull1, hull2, deck, bow1, bow2) 两个船体、甲板和两个船头标记的坐标
    """
    # 船体尺寸参数（数学坐标系）
    hull_length = 20  # 船体长度
    hull_width = 4  # 船体宽度
    separation = 12  # 两个船体之间的间距
    deck_length = 15  # 甲板长度
    bow_size = 7 # 船头三角形大小

    # 计算旋转角度（弧度），转换为从正X轴逆时针方向的角度（标准数学角度）
    angle = (np.pi / 2) - course  # 90度 = π/2 弧度，然后减去 course（弧度）
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    # 左船体（从船尾到船头，顺时针定义多边形）
    left_hull = [
        [-hull_length / 2, -hull_length / 2, hull_length / 2, hull_length / 2],  # X坐标
        [-separation / 2 - hull_width, -separation / 2, -separation / 2, -separation / 2 - hull_width]  # Y坐标
    ]

    # 右船体
    right_hull = [
        [-hull_length / 2, -hull_length / 2, hull_length / 2, hull_length / 2],
        [separation / 2, separation / 2 + hull_width, separation / 2 + hull_width, separation / 2]
    ]

    # 甲板（连接两个船体）
    deck = [
        [-deck_length / 2, deck_length / 2, deck_length / 2, -deck_length / 2],
        [-separation / 2, -separation / 2, separation / 2, separation / 2]
    ]

    # 左船头三角形
    left_bow = [
        [hull_length / 2, hull_length / 2 + bow_size, hull_length / 2],  # X坐标
        [-separation  + hull_width/2 , -separation / 2 -hull_width/2, -separation / 2]  # Y坐标
    ]

    # 右船头三角形
    right_bow = [
        [hull_length / 2, hull_length / 2 + bow_size, hull_length / 2],  # X坐标
        [separation / 2 + hull_width , separation / 2+ hull_width/2 , separation / 2]  # Y坐标
    ]

    # 旋转和平移所有点
    def rotate_translate(points):
        rotated = []
        for i in range(len(points[0])):
            x = points[0][i]
            y = points[1][i]
            # 旋转（标准数学旋转公式）
            x_rot = x * cos_angle - y * sin_angle
            y_rot = x * sin_angle + y * cos_angle
            # 平移
            rotated.append([x_rot + x0, y_rot + y0])

        # 分离x和y坐标
        x_coords = [p[0] for p in rotated]
        y_coords = [p[1] for p in rotated]
        return [x_coords, y_coords]

    left_hull_rot = rotate_translate(left_hull)
    right_hull_rot = rotate_translate(right_hull)
    deck_rot = rotate_translate(deck)
    left_bow_rot = rotate_translate(left_bow)
    right_bow_rot = rotate_translate(right_bow)

    return left_hull_rot, right_hull_rot, deck_rot, left_bow_rot, right_bow_rot