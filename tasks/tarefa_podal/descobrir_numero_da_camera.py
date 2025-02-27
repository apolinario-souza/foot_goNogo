#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 08:33:58 2025

@author: tercio
"""

import cv2

def find_cameras():
    cameras = []
    for i in range(10):  # Testa de 0 a 9 (ajuste conforme necessário)
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append(i)
            cap.release()
    return cameras

cameras_found = find_cameras()
print(f"Câmeras disponíveis: {cameras_found}")