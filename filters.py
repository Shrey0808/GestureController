# filters.py
import math
import time
import config

class OneEuroFilter:
    """
    Implements the 1€ Filter, a first-order low-pass filter with an adaptive 
    cutoff frequency. Reduces jitter while keeping latency low.
    """
    def __init__(self, min_cutoff=config.MIN_CUTOFF, beta=config.BETA):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.x_prev = 0
        self.t_prev = time.time()

    def filter(self, x, t):
        dt = t - self.t_prev
        if dt <= 0: return self.x_prev
        
        dx = (x - self.x_prev) / dt
        cutoff = self.min_cutoff + self.beta * abs(dx)
        r = 2 * math.pi * cutoff * dt
        alpha = r / (r + 1)
        
        x_hat = alpha * x + (1 - alpha) * self.x_prev
        self.x_prev = x_hat
        self.t_prev = t
        return x_hat