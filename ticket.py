# coding: utf-8

"""命令行火车票查看器

Usage:
    ticket [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""

from docopt import docopt
import requests
import prettytable
from colorama import init, Fore
from stations import stations


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    # stated_url=u'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date=2018-3-28&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=CQW&purpose_codes=ADULT'
    URL = (
    'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(
        date, from_station, to_station
    )
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        , 'Connection': 'keep-alive'}

    r = requests.get(URL, verify=False, headers=headers)
    available_trains = r.json()['data']['result']
    available_place = r.json()['data']['map']
    options = ''.join([
        key for key, value in arguments.items() if value is True
    ])
    TrainsCollection(available_trains, available_place, options).pretty_print()


class TrainsCollection:
    header = '车次 车站 时间 历时 一等 二等 高级卧铺 软卧 硬卧 硬座 无座'.split()

    def __init__(self, available_trains, available_place, options):
        """查询的火车班次集合
        :param available_trains:一个列表，包含可获得的火车班次，每个火车班次是一个字典
        :param options:查询的选项，如高铁，动车，等等"""

        self.available_trains = available_trains
        self.available_place = available_place
        self.options = options

    @property
    def trains(self):
        for raw_train in self.available_trains:
            raw_train_list = raw_train.split('|')
            train_no = raw_train_list[3]
            initial = train_no[0].lower()
            duration = raw_train_list[10]
            init()
            if not self.options or initial in self.options:
                train = [
                    train_no,#train number
                    '\n'.join([Fore.LIGHTGREEN_EX + self.available_place[raw_train_list[6]] + Fore.RESET,#始发站
                               Fore.LIGHTRED_EX + self.available_place[raw_train_list[7]] + Fore.RESET]),#终点站
                    '\n'.join([Fore.LIGHTGREEN_EX + raw_train_list[8] + Fore.RESET,
                               Fore.LIGHTRED_EX + raw_train_list[9] + Fore.RESET]),
                    duration,#时长
                    raw_train_list[-6] if raw_train_list[-6] else '--',#一等
                    raw_train_list[-7] if raw_train_list[-7] else '--',  # 二等
                    raw_train_list[-15] if raw_train_list[-15] else '--',  # 高级软卧
                    raw_train_list[-8] if raw_train_list[-8] else '--',  # 软卧
                    raw_train_list[-14] if raw_train_list[-14] else '--',  # 硬卧
                    raw_train_list[-11] if raw_train_list[-11] else '--',  # 硬座
                    raw_train_list[-9] if raw_train_list[-9] else '--',  # 无座
                ]
                yield  train

    def pretty_print(self):
        pt = prettytable.PrettyTable()
        pt._set_field_names(self.header)
        for train in self.trains:
            pt.add_row(train)
        print(pt)


if __name__ == '__main__':
    cli()
