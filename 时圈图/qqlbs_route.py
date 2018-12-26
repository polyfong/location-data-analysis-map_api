# -*- coding: utf-8 -*-
"""
@author: IvanChan
"""

import requests
import pandas as pd


def get_least_time(key, from_coord, to_coord):
    # 使用direction api

    lbs_https = 'https://apis.map.qq.com/ws/direction/v1/transit/?'
    # 腾讯地图修改了api服务, 把http协议改为https协议/公交服务

    route_api = lbs_https+'from='+from_coord+'&to='+to_coord+'&police=LEAST_TIME'+'&key='+key
    route = requests.get(route_api)
    route_dict = route.json()

    if route_dict["status"] == 0:
        # 如果成功调用

        time = route_dict["result"]["routes"][0]["duration"]
        # 根据api返回的json格式直接编写

    else:
        time = None  # 如果调用失败，直接返回空值
        print('Query Error')

    return time


def cal_time_grid(coordination_file_path, lbs_api_key, dest_latlng):

    # 计算格网点到目的地的时间距离

    with open(coordination_file_path) as coord_file:
        coord_df = pd.read_csv(coord_file)

    coord_df['time'] = None

    for row in coord_df.index:

        from_lat = str(coord_df.at[row, 'lat'])
        from_lng = str(coord_df.at[row, 'lng'])
        from_latlng = from_lat+','+from_lng

        least_time = get_least_time(lbs_api_key, from_latlng, dest_latlng)
        coord_df.at[row, 'time'] = least_time
        print(coord_df.loc[row])

    with open('time_matrix.csv', 'w') as time_file:
        coord_df.to_csv(time_file)


if __name__ == '__main__':

    qq_lbs_api_key = '                 '  # 填入你的api key
    # city_centre = '30.253949,120.163938' # 杭州龙翔桥gcj_02坐标
    dest_point = '30.291923,120.073292'  # 杭州西溪银泰商场gcj_02坐标
    file_path = " .csv"  # 先准备一个用csv文件储存的坐标文件，以lat、lng字段保存经纬度
    cal_time_grid(file_path, qq_lbs_api_key, dest_point)



