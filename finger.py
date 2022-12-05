# _*_ coding:utf-8 _*_

# description: the fingercode base on the Gabor filter

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import sqlite3
import os


'''def initlize_db(db_name):

    # if have existed
    if os.path.isfile(db_name):
        print ("this database has existed......")
        return

    # initlizing the database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    # create tables
    tables_sql = 'create table fingercode (id int, image_name text, angle0 text, angle1 text, angle2 text, angle3 text,' \
                 'angle4 text, angle5 text, angle6 text, angle7 text)'

    print ("initlizing the database now ......")
    c.execute(tables_sql)
    conn.commit()
    conn.close()
    print ("initlizing the database is ok.....")


# save the fingercode
def save_fingercode(db_name, result):

    print ("start saving the result....")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "INSERT INTO fingercode VALUES (?,?,?,?,?,?,?,?,?,?)"
    c.execute(sql, result)
    print ("execute.....")
    conn.commit()
    print ("commit....")
    conn.close()
    print ("close...")


# get the fingercode
def get_fingercode(db_name):

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    sql = "select * from fingercode where id=?"
    c.execute(sql, '1')
    result = c.fetchone()
    conn.close()
    return result


# get all data
def get_all(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    print ("start getting all...")
    c.execute('select * from fingercode')
    result = c.fetchall()
    conn.close()
    print ("close....")
    return result'''

def cal_standar(points, mean):
    total = 0
    for i in range(len(points)):
        point = points[i]
        total += math.pow(point.Gray - mean, 2)
    if len(points) != 0:
        return total / len(points)
    else:
        return 0

# calculate the fingercode
def fingercode(img):

    # divide the sectors
    sectors = Divide_sector(img)
    result = []
    Mean = []
    for i in range(len(sectors)):
        Mean.append(cal_mean(sectors[i]))

    Variance = []
    for i in range(len(sectors)):
        Variance.append(cal_standar(sectors[i], Mean[i]))

    for i in range(len(sectors)):
        temp = round(math.sqrt(Variance[i]), 0)
        #print temp
        result.append(int(temp))
    #return result
    #print ("------")
    #print (result)
    #print ("------")
    # show the fingercode
    for i in range(len(sectors)):
        sector = sectors[i]
        for point in sector:
            img[point.X, point.Y] = result[i]
    return img, result
    #return result


# get the result from database and convert to list
# return list type
def convert_list(result):
    target = []
    for i in range(2, len(result)):
        temp = list(eval(result[i]))
        #print type(temp)
    target.append(temp)
    return target


# calculate the fingercode Euler ventor
def cal_euler_distance(result1, result2):
    distance = 0
    for i in range(len(result1)):
        temp1 = result1[i]
        temp2 = result2[i]
        for j in range(len(temp1)):
            distance += math.pow(temp1[j] - temp2[j], 2)

    return distance


# get the images name from the database
def get_image_name(result):

    image_name = []
    for i in result:
        image_name.append(i[1])
    return image_name
def build_filters():
    filters = []
    sigma = 4
    gamma = 1.0
    ksize = 33
    lamba = 10
    ps = (90-180)*np.pi/180.0
    for theta in np.arange(0, np.pi, np.pi / 8):
        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamba, gamma, ps)
        #kern = kern/2 + 0.5
        filters.append(kernel)
    return filters


# processing the img
def process(img, kernel):
    #img = np.array(img, dtype=np.float32)
    #img /= 255.
    dest = cv2.filter2D(img, -1, kernel)
    return dest


# get the image's result after the Gabor filtering
def getGabor(img):
    filters = build_filters()
    res = []
    for i in filters:
        res1 = process(img, i)
        res.append(res1)
    """
    plt.figure(2)
    for temp in xrange(len(res)):
        plt.subplot(4, 6, temp+1)
        plt.imshow(res[temp], cmap='gray')

    plt.show()
    """
    return res

class Point:

    # param: X: the pixel x, Y: the pixel y, Gray: the pixel gray value
    def __init__(self, x, y, gray):
        self.X = x
        self.Y = y
        self.Gray = gray
        self.Normal_value = None


# calculate the number of sector's point
def cal_num(points):
    return len(points)


# calculate the mean of sector's points gray value
def cal_mean(points):
    total = 0
    num = cal_num(points)
    for i in range(len(points)):
        point = points[i]
        total += point.Gray
    return total / num



# calculate the variance of the sector's points
def cal_variance(points, mean):
    total = 0
    for i in range(len(points)):
        point = points[i]
        total += math.pow(point.Gray - mean, 2)
    return total / (len(points)-1)

# divide the core image into 80 sectors
def Divide_sector(img):
    k = 16
    b = 10
    T = []
    angle = []
    rows, cols = img.shape[:2]
    core_x = cols / 2
    core_y = rows / 2
    for i in range(81):
        T.append(int(i / k))
        angle.append((i % k) * (2 * 180.0 / k))

    sectors = []

    for i in range(80):
        x = 1
        y = 1
        sector = []
        for x in range(cols):
            #print x
            for y in range(rows):
                x0 = x - core_x
                y0 = y - core_y
                r = math.sqrt(pow(x0, 2) + pow(y0, 2))
                #print r
                if x0 == 0.0:
                    if y0 > 0:
                        point_angle = 270.0
                    else:
                        point_angle = 90.0

                if y0 == 0.0:
                    if x0 > 0:
                        point_angle = 0.0
                    else:
                        point_angle = 180.0
                # in 1 district
                if(y0 < 0.0)&(x0 > 0.0):
                    point_angle = abs(math.degrees(math.atan(y0 / x0)))
                # in 2 district
                if(y0 < 0.0)&(x0 < 0.0):
                    point_angle = abs(math.degrees(math.atan(x0 / y0))) + 90.0
                # in 3 district
                if(y0 > 0.0)&(x0 < 0.0):
                    point_angle = abs(math.degrees(math.atan(y0 / x0))) + 180.0
                # in 4 district
                if (y0 > 0.0)&(x0 > 0.0):
                    point_angle = abs(math.degrees(math.atan(x0 / y0))) + 270.0
                #point_angle = math.degrees(math.atan((y - core_y) / (x - core_x)))
                #print point_angle, r
                if (point_angle <= 337.5)&(b * (T[i] + 1) <= r)&(b * (T[i] + 2) > r)&(angle[i] <= point_angle)&(angle[i+1] > point_angle):
                    point = Point(y, x, img[y][x])
                    sector.append(point)
                if (point_angle > 337.5)&(b * (T[i] + 1) <= r)&(b * (T[i] + 2) > r)&(angle[i] <= point_angle)&(360.0 > point_angle):
                    point = Point(y, x, img[y][x])
                    sector.append(point)
        #print len(sector)
        sectors.append(sector)

    return sectors


# normalize the image after divide into sectors
def Normalize_img(img, sectors):
    M0 = 100
    V0 = 100
    Mean = []
    Variance = []
    # calculate the mean of the image gray
    for i in range(len(sectors)):
        Mean.append(cal_mean(sectors[i]))
    # calculate the variance of the image gray
    for i in range(len(sectors)):
        Variance.append(cal_variance(sectors[i], Mean[i]))
    for i in range(len(sectors)):
        sector = sectors[i]
        for j in range(len(sector)):
            point = sector[j]
            if Variance[i] == 0:
                Variance[i] = 1
            temp = math.sqrt(V0 * math.pow((point.Gray - Mean[i]), 2) / Variance[i])
            temp = int(temp)
            if point.Gray > Mean[i]:
                img[point.X, point.Y] = M0 + temp
            else:
                img[point.X, point.Y] = M0 - temp
    return img
# get all images path from a folder
def get_all_image(folder):
    files = os.listdir(folder)
    files_path = []
    for i in files:
        temp = folder + '/' + i
        files_path.append(temp)
    return files_path


# get the reference frame
def Get_central_point(img):
    img1 = img.copy()
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.blur(img, (5, 5))
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)

    sobelx1 = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    #abssobelx = cv2.convertScaleAbs(sobelx)
    #abssobelx1 = cv2.convertScaleAbs(sobelx1)

    A = sobelx.copy()
    B = sobelx1 + A
    gh = cv2.Sobel(B, cv2.CV_16S, 1, 1, ksize=3)
    gh_blur = cv2.GaussianBlur(gh, (15, 15), 0)
    gh_blur = cv2.convertScaleAbs(gh_blur,gh_blur)
    gh_media = cv2.medianBlur(gh_blur, 5)
    gh_media = cv2.medianBlur(gh_media, 5)
    gh_media = cv2.medianBlur(gh_media, 3)
    rows, cols = img.shape[:2]
    """
    for i in range(rows):
        for j in range(cols):
            print gh_media[i][j]
    """
    gh_media = cv2.convertScaleAbs(gh_media)
    gh_media = cv2.cvtColor(gh_media, cv2.COLOR_BGR2GRAY)
    ret1, binary1 = cv2.threshold(gh_media, 35, 255, cv2.THRESH_BINARY)
    #binary1 = cv2.adaptiveThreshold(gh_media, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    #print binary1[152][130]
    #image, contours, hierarchy = cv2.findContours(gh_media, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #img1 = cv2.drawContours(img, contours, 3, (0, 255, 0), 1)
    kernel = np.ones((5, 5), np.uint8)
    gh_blur = cv2.erode(binary1, kernel, iterations=1)
    rows, cols = gh_blur.shape[:2]
    max = 0.0
    row = 0
    col = 0
    for i in range(rows):
        for j in range(cols):
            if binary1[i][j] > 0:
                max = gh_blur[i][j]
                row = i
                col = j
                 #print row, col

    #print gh_media[373][387]
    #gh_blur = cv2.convertScaleAbs(gh_blur,gh_blur)
    #print rows, cols
    #print "------"
    #print row, col
    #print "------"
    rows, cols = img.shape[:2]
    if row != 0:
        if (col + 75 < cols) & (row + 75 < rows):
            print ("success")
            #continue
        else:
            row = 0
            col = 0
            #print ("failed")
    else:
        print ("failed")

    plt.figure()
    plt.subplot(1, 3, 1)
    plt.imshow(binary1, cmap='gray')
    plt.subplot(1, 3, 2)
    plt.imshow(img, cmap='gray')
    plt.subplot(1, 3, 3)
    plt.imshow(gh_media, cmap='gray')
    #plt.show()

    return col, row

# copy the reference frame
def Get_core_img(img, core_x, core_y):
    radius = 75
    # crop the image 80*80
    #core_img = np.zeros((radius, radius, 3), np.uint8)
    core_img = img[core_y-radius:core_y+radius, core_x-radius:core_x+radius]

    return core_img


if __name__ == '__main__':
	final()
    	
def final():
        img = cv2.imread('2/107_1.tif')
        rows, cols = img.shape[:2]
        # get the reference point
        core_x, core_y = Get_central_point(img)

        print (core_x, core_y)

        if core_x != 0:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            core_img = Get_core_img(img, core_x, core_y)

            plt.figure()
            plt.subplot(1, 2, 1)
            plt.imshow(img, cmap='gray')
            plt.subplot(1, 2, 2)
            plt.imshow(core_img, cmap='gray')
            #plt.show()

            # divide the img sector
            sectors = Divide_sector(core_img)

            core_img = Normalize_img(core_img, sectors)

            #cv2.imwrite('kkk.tif', core_img)
            # show normalize image
            print("displaying normalized image..")
            plt.figure()
            plt.subplot(1, 1, 1)
            plt.imshow(core_img, cmap='gray')
            #plt.show()

            result = getGabor(core_img)
            # show Gabor filters process images
            print("displaying gabor filters process images")

            plt.figure()
            for i in range(len(result)):
                plt.subplot(1, 8, i+1)
                plt.imshow(result[i], cmap='gray')
            #plt.show()

            gh = []
            ADD = []
            for i in result:

                imgtemp, fingercodetemp = fingercode(i)
                gh.append(imgtemp)
                ADD.append(fingercodetemp)
            # convert tht array to string
            temp = []
            for i in ADD:
                temp.append(i)
                #print(i)

            plt.figure()
            print("showing all the final filters")
            for i in range(len(gh)):
                plt.subplot(1, 8, i+1)
                plt.imshow(gh[i], cmap='gray')
        return temp
            #plt.show()
