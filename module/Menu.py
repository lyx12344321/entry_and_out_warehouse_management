from enumeration.MenuName import MenuName

class Menu:

    menus = {
        MenuName.MAIN: {
            '1': '创建记录',
            '2': '查看记录',
            '3': '修改记录',
            '4': '删除记录',
            '5': '生成图片',
            '6': '退出系统'
        },
        MenuName.RECORDTYPE: {
            '0': '记录类型：',
            '1': '入库记录',
            '2': '出库记录',
        },
        MenuName.UPDATE: {
            '0' :'修改记录仅能通过uid修改，uid见2. 查看记录时展示的数据'
        },
        MenuName.RECORDINFO: {
            '1' : '修改日期',
            '2' : '修改煤种',
            '3' : '修改车牌号',
            '4' : '修改毛重',
            '5' : '修改皮重',
            '6' : '修改原发',
            '7' : '修改过空时间',
            '8' : '修改过重时间',
            '9' : '修改发货单位',
            '10': '修改收货单位',
            '11': '修改司磅员',
        },
        MenuName.REMOVE: {
            '0': '删除记录仅能通过uid删除，uid见主菜单2. 查看记录时展示的数据'
        }
    }

    @staticmethod
    def show(menu_name):
        print()
        for item in Menu.menus[menu_name].items():
            if (item[0] == '0'):
                print(item[1])
            else:
                print(f'{item[0]}. {item[1]}')
        print()
