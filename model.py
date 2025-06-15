import numpy as np


def shuangti(u0, course0, r0, f1, f2, dt):
    """
    修正后的双体船运动状态更新
    参数:
        u0: 当前速度 (m/s)
        course0: 当前航向角 (rad)
        r0: 当前角速度 (rad/s)
        f1, f2: 左右推进器推力 (N)
        dt: 时间步长 (s)
    返回:
        u: 更新后的速度
        course: 更新后的航向角
        r: 更新后的角速度
    """
    M = 5000  # 船的质量 (kg)
    L = 2.0  # 船体长度 (m)

    # 固定转动惯量 (基于船体几何形状计算)
    I_x = (1.0 / 12.0) * M * L ** 2  # 绕x轴转动惯量

    # 改进的阻力系数
    k1_linear = 50.0  # 线性阻力系数 (N/(m/s))
    k1_quad = 0.1  # 二次阻力系数 (N/(m/s)^2)
    k2_linear = 100.0  # 线性旋转阻力系数 (N·m/(rad/s))
    k2_quad = 500.0  # 二次旋转阻力系数 (N·m/(rad/s)^2)

    # 改进的阻力模型 (包含线性和二次项)
    f_touph = k1_linear * u0 + k1_quad * u0 ** 2 * np.sign(u0)
    r_touph = k2_linear * r0 + k2_quad * r0 ** 2 * np.sign(r0)

    # 运动方程修正
    # 线加速度 (推力总和减去阻力)
    du = (f1 + f2 - f_touph) / M

    # 角加速度 (力矩=力×力臂, 力臂应为L/2)
    torque = (f1 - f2) * (L / 2.0)  # 有效力矩
    dr = (torque - r_touph) / I_x  # 使用转动惯量

    # 状态更新
    u = u0 + du * dt
    r = r0 + dr * dt
    course = (course0 + r * dt) % (2.0 * np.pi)  # 角度归一化

    return u, course, r


def get_xy(x, y, f1, f2, u0, course0, r0, dt):
    """
    更新船的位置坐标
    参数:
        x, y: 当前位置坐标
        f1, f2: 左右推进器推力
        u0: 当前速度
        course0: 当前航向角
        r0: 当前角速度
        dt: 时间步长
    返回:
        更新后的位置坐标和状态
    """
    u, course, r = shuangti(u0, course0, r0, f1, f2, dt)

    # 位置更新
    dx = u * np.sin(course) * dt
    dy = u * np.cos(course) * dt

    x += dx
    y += dy

    return x, y, u, course, r
