def INCHES(x):
    return x * 25.4


def _faces_match(obj, face, n):
    nf = len(obj.faces(face).vals())
    return nf == n


def _edges_match(obj, face, n):
    nf = len(obj.faces(face).edges().vals())
    return abs(nf - n) < 3


def _almost_same(x, y, tol=1e-3):
    if isinstance(x, (list, tuple)):
        return all((abs(xe - ye) < tol for xe, ye in zip(x, y)))
    return abs(x - y) < tol
