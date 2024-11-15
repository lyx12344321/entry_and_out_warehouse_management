# from module.Record import Record
from enumeration.RecordType import RecordType
from exception.RecordTypeUndefined import RecordTypeUndefined

from matplotlib import pyplot as plt
import io
from PIL import Image, ImageDraw, ImageFont
import matplotlib as mpl
import xlwings as xw
import configparser

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 指定默认字体：解决plot不能显示中文问题
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def getSheetLength(workBook: xw.Book, sheetName: str):
    sheet = workBook.sheets[sheetName]
    no = 0
    while True:
        if sheet[no, 0].value is None:
            break
        no += 1
    return no + 1

def recordToImage(record, workBook: xw.Book) -> Image.Image:

    config = configparser.ConfigParser()
    config.read("./config.ini")
    startId = config.get('other', 'startId', fallback=None)
    try:
        startId = int(startId)
    except:
        raise ValueError("配置文件中起始磅单值格式错误")
    
    if record.sheetName == None:
        raise RecordTypeUndefined('出入库类型未设置')

    currentLine = getSheetLength(workBook, record.sheetName)
    if workBook.sheets[record.sheetName][currentLine - 1, 1].value is None:
        record.id = 2024000001
    else:
        record.id = int(workBook.sheets[record.sheetName][currentLine - 1, 1].value) + 1
    record.calculateNetWeight()
    record.calculateProfitLoss()

    if record.isGenerateImage == True:
        return

    # 填写表格内容
    data = [
        ["日期：", record.creatTime.strftime("%Y年%m月%d日")],
        ["磅单编号：", f"{record.id}"],
        ["车排号：", f"{record.plateNumber}"],
        ["煤种：", f"{record.varietyCoal}"],
        ["发货单位：", f"{record.shippingUnit}"],
        ["收货单位：", f"{record.receivingUnit}"],
        ["毛重（吨）：", f"{record.grossWeight}"],
        ["皮重（吨）：", f"{record.tare}"],
        ["净重（吨）：", f"{record.netWeight}"],
        ["过重时间：", f"{record.excessiveTime}"],
        ["过空时间：", f"{record.emptyTime}"],
        ["司磅员：", f"{record.weigher}"]
    ]

    fig, ax = plt.subplots(figsize=(7.08, 12.21))
    fig.set_dpi(2000)
    ax.axis('off')
    ax.axis('tight')

    table = ax.table(cellText=data, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width([0, 1])
    table.scale(1, 1.97)

    for i in range(len(data)):
        for j in range(len(data[0])):
            cell = table.get_celld()[(i, j)]
            cell.set_text_props(ha='center', va='center') 

    # 将绘图保存到字节流
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # 使用PIL读取字节流
    image = Image.open(buf)
    image = image.crop((220, 363, 506, 817))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", size=20)

    w = font.getlength('国康煤场过磅单')

    draw.text(xy=((image.width - w) / 2 - 15, 14), text='国康煤场出库过磅单', font=font, fill=(0, 0, 0))
    image = image.resize((473, 816))
    record.image = image
    return image


# input 拦截器

from enumeration.CheckType import CheckType
from exception.QuitException import QuitException


def check(optional: CheckType, optionalArgs: any, value: any):

    if value.lower() == 'q':
        raise QuitException()
    
    if optional is None:
        raise Exception("optional不能为空")
    
    if optional == CheckType.OPTIONTYPE and isinstance(optionalArgs, list): # 选项类型检查optionalArgs必须为列表
        if value in optionalArgs:
            return True
        else:
            return False

    if optional == CheckType.RANGETYPE and isinstance(optionalArgs, tuple): # 范围类型检查optionalArgs必须为元组
        if value.isdigit() and int(value) in optionalArgs:
            return True
        else:
            return False
        
    if optional == CheckType.DATATYPE and isinstance(optionalArgs, type): # 类型检查optionalArgs必须为type类型
        try:
            typed_value = optionalArgs(value)
            return True
        except ValueError as e:
            print(f"输入无效，请输入 {optionalArgs.__name__} 类型的值。")
            return False
        
    print("未实现的类型检查: " + optionalArgs.__name__)

def isIterable(obj):
    try:
        iter(obj)
        return True
    except Exception:
        return False

def inputChecker(optional: CheckType, optionalArgs: any, instructions: str = ""):

    value = input(instructions).strip()
    while True:
        if check(optional, optionalArgs, value):
            return value
        else:
            print("无效值，请重新输入")
            value = input(instructions)
                
def strIsEmpty(str: str):
    return not str.strip()

def strToFloat(str: str):
    try:
        result = float(str)
        return result
    except Exception as e:
        return None
    
def rangeIntToString(array):
    if type(array) != type(range(1)):
        return []
    
    ret = []
    for i in array:
        ret.append(str(i))
    return ret
