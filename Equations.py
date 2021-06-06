from math import pow


class EquationSolver:
    """
    Collection of Methods to solve different Equations
    """

    @staticmethod
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
        return p1, p2, t1, t2, g