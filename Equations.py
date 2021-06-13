from math import pow


def ideal_compression_p_vs_t(p1, p2, t1, t2, g):
    """
    Solve Ideal Compression Law for Pressure
    """
    if p1 == 0 and (p2 * t1 * t2) != 0:
        p1 = p2 * pow((t1 / t2), (g / (g - 1)))
    if p2 == 0 and (p1 * t1 * t2) != 0:
        p2 = p1 * pow((t2 / t1), (g - 1) / g)
    if t1 == 0 and (p1 * p2 * t2) != 0:
        t1 = t2 * pow((p1 / p2), ((g - 1) / g))
    if t2 == 0 and (p1 * t1 * t2) != 0:
        t2 = t1 * pow((p2 / p1), ((g - 1) / g))
    return p1, p2, t1, t2


def static_temperature(tt, ts, m, g):
    """
    Solve Static Temperature Equation
    """
    if (tt == 0) and (ts * m) != 0:
        tt = ts * (1 + ((pow(m, 2) * (g - 1) / 2)))
    if (ts == 0) and (tt * m) != 0:
        ts = tt / (1 + ((pow(m, 2) * (g - 1) / 2)))
    if (m == 0) and (ts * tt) != 0:
        m = pow((tt / ts - 1) / ((g - 1) / 2), 0.5)
    return ts, tt, m


def static_pressure(pt, ps, m, g):
    """
    Solve Static Pressure Equation
    """
    if (pt == 0) and (ps * m) != 0:
        pt = ps * pow((1 + ((pow(m, 2) * (g - 1) / 2))), (g / (g - 1)))
    if (ps == 0) and (pt * m) != 0:
        ps = pt / pow((1 + ((pow(m, 2) * (g - 1) / 2))), (g / (g - 1)))
    if (m == 0) and (ps * pt) != 0:
        m = pow((pow(pt / ps, (g - 1) / g) - 1) / ((g - 1) / 2), 0.5)
    return ps, pt, m


# Shaft Work mCP DT
# Compressor Effeciency
# Flat Plate Correlation
# Duct Correlation
