# coding:utf-8

import mysql.connector

student = mysql.connector.connect(user = 'root',
                                  password = '123456',
                                  host = '127.0.0.1',
                                  database = 'student')
cursor = student.cursor()


def convert_data():
    global cursor
    sql = "SELECT * FROM QUESRECORD;"
    cursor.execute(sql)
    data = cursor.fetchall()
    num = len(data)
    for i in range(0, num):
        # time_length = 'A' + str(int(data[i][0] / 20))
        # count = 'B' + str(int(data[i][1] / 20))
        # re_time_length = 'C' + str(int(data[i][2] / 20))
        # re_final = 'D' + str(int(data[i][3] / 20))
        # final = 'G' + str(int(data[i][4] / 20))
        stu_id = data[i][0]
        name = data[i][1]
        t1 = '201' + data[i][2]
        t2 = '202' + data[i][3]
        t3 = '203' + data[i][4]
        t4 = '204' + data[i][5]
        t12 = '212' + data[i][6]
        t14 = '114' + data[i][7]
        t15 = '515' + data[i][8]
        t16 = '516' + data[i][9]
        t18 = '518' + data[i][10]
        t19 = '519' + data[i][11]
        t20 = '520' + data[i][12]
        t21 = '121' + data[i][13]
        t24 = '324' + data[i][14]
        t25 = '325' + data[i][15]
        t26 = '326' + data[i][16]
        t27 = '327' + data[i][17]
        t28 = '328' + data[i][18]
        t56 = '456' + data[i][19]
        t57 = '457' + data[i][20]
        t59 = '459' + data[i][21]
        t60 = '460' + data[i][22]
        test = data[i][23]

        # sql_insert = "INSERT INTO PERFORMANCE2(TIME_LENGTH, COUNT, RE_TIME_LENGTH, RE_FINAL, FINAL) " \
        #              "VALUES ('%s', '%s', '%s', '%s', '%s')" % (time_length, count,  re_time_length, re_final, final)
        sql_insert = "INSERT INTO QUESDATA(STU_ID, NAME, T1, T2, T3, T4, T12, T14, T15, T16, T18, T19, T20, T21, T24, T25, T26, T27, T28, T56, T57, T59, T60, TEST ) " \
                     "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                     % (stu_id, name, t1, t2, t3, t4, t12, t14, t15, t16, t18, t19, t20, t21, t24, t25, t26, t27, t28, t56, t57, t59, t60, test)
        cursor = student.cursor()
        cursor.execute(sql_insert)

    sql = "SELECT * FROM QUESDATA;"
    cursor.execute(sql)
    data2 = cursor.fetchall()
    # datalist = []
    # for i in range(0, num):
    #     list = []
    #     for j in range(3):
    #         list.append(data2[i][j])
    #     datalist.append(list)

    student.commit()
    student.close()
    # print(data2)
    return


def convert_testdata():
    student = mysql.connector.connect(user = 'root',
                                  password = '123456',
                                  host = '127.0.0.1',
                                  database = 'student')
    cursor = student.cursor()
    # global cursor
    sql = "SELECT * FROM TESTDATA;"
    cursor.execute(sql)
    data = cursor.fetchall()
    num = len(data)
    for i in range(0, num):
        time_length = 'A' + str(int(data[i][0] / 20))
        count = 'B' + str(int(data[i][1] / 20))
        re_time_length = 'C' + str(int(data[i][2] / 20))
        re_final = 'D' + str(int(data[i][3] / 20))
        final = 'G' + str(int(data[i][4] / 20))
        # print(stu_id, time_length, count,final)

        sql_insert = "INSERT INTO TESTDATA2(TIME_LENGTH, COUNT, RE_TIME_LENGTH, RE_FINAL, FINAL) " \
                     "VALUES ('%s', '%s', '%s', '%s', '%s')" % (time_length, count,  re_time_length, re_final, final)
        cursor = student.cursor()
        cursor.execute(sql_insert)

    student.commit()
    student.close()
    return


def load_data(table_name, colnum):
    student = mysql.connector.connect(user='root',
                                      password='123456',
                                      host='127.0.0.1',
                                      database='student')
    cursor = student.cursor()
    # global student,cursor
    sql = "SELECT * FROM %s;" % table_name
    cursor.execute(sql)
    data = cursor.fetchall()
    num = len(data)
    datalist = []
    for i in range(0, num):
        list = []
        for j in range(2, colnum):
            list.append(data[i][j])
        datalist.append(list)
    # print(datalist)
    return datalist


# convert_data()
# load_data('TASKNEW2', 24)
# convert_testdata()
