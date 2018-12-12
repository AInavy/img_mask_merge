# -*- coding=utf-8 -*-
import os, sys
import numpy as np
import cv2

def image_merge(img, mask, pole_mask, detect):
    cv2.namedWindow('img', 0)
    cv2.imshow('img', img)
    cv2.namedWindow('mask', 0)
    cv2.imshow('mask', mask)
    cv2.namedWindow('pole_mask', 0)
    cv2.imshow('pole_mask', pole_mask)

    color_mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
    color_pole = cv2.cvtColor(pole_mask, cv2.COLOR_RGB2GRAY)


    mask[color_mask > 100] = (0, 255, 255)
    mask[color_pole > 100] = (255, 0, 0)

    img_mix = cv2.addWeighted(img, 0.6, mask, 0.4, 0)

    cv2.namedWindow('merge', 0)
    for i in range(0, len(detect)):
        x, y, w, h = detect[i].split(',')
        if int(x) + int(w) > 30 and int(y) + int(h) > 30:
            cv2.rectangle(img_mix,(int(x),int(y)), (int(x) + int(w) ,int(y) + int(h)), (0, 0, 255), 2)


    cv2.imshow('merge', img_mix)
    cv2.imwrite('/cvg_home/home/mahj/data/断头路/images0_pole_mask/merge/' + imgname,img_mix)

    if cv2.waitKey(1) & 0xFF == ord('p'):
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)




def unicom_area(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)


    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(img, contours, -1, (0, 0, 255), 1)

    # cv2.namedWindow("img",0)
    # cv2.imshow("img", img)
    # cv2.waitKey(0)



    length = len(contours)
    print length
    for i in range(length):
        cnt = contours[i]

        epsilon = 0.00001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        area = cv2.contourArea(cnt)
        # print area
        if area > 100.0:
            cv2.polylines(img, [approx], True, (0, 255, 255), 1) #approx N个轮廓点集合
            # print len(approx)
            # for xx in approx:
            #     for xxx in xx:
            #         cv2.circle(img, (int(xxx[0]), int(xxx[1])), 1, (0, 255, 255), 1)


    cv2.namedWindow("approx", 0)
    cv2.imshow("approx", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    # for i in range(1, 4667):
    with open('/cvg_home/home/mahj/data/断头路/images0_pole_mask/caffe2_detection_sign.txt') as f:
        for line in f:
            line = line.strip()
            sub = line.split(' ')
            imgname = sub[0]

            img = cv2.imread('/cvg_home/home/mahj/data/断头路/images0_undistort/' + imgname)
            mask = cv2.imread('/cvg_home/home/mahj/data/断头路/images0_dash_lane_mask/' + imgname)

            xx = imgname.split('.')[0]
            xx= '%04d' % int(xx)
            pole_mask = cv2.imread('/cvg_home/home/mahj/data/断头路/images0_undistort_pole_seg/' + str(xx) + '.png')

            detect = sub[1:(len(sub))]
            image_merge(img, mask, pole_mask, detect)

            # cv2.namedWindow('img', 0)
            # cv2.imshow('img', img)
            # unicom_area(pole_mask)


