import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox, END
import json

# JSON后端部分的代码
# 读取Json文件
def load_data_from_json():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []

# 保存写入Json文件
def save_data_to_json(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

# 楼层信息关系图
def populate_tree(tree, parent, floors):
    for floor in floors:
        tree.insert(parent, "end",text=floor["floornum"],values=[floor["floornum"]])

# 创建treeview
def create_treeview(root, data):
    style = ttk.Style()
    style.configure("Treeview", font=("微软雅黑", 12))

    tree = ttk.Treeview(root, style="Treeview", columns=("floornum"), show='tree')  # 设置 show 参数为 'tree' 来隐藏 values 列
    tree.column('floornum', width=0, stretch=False)  # 设置 'floornum' 列的宽度为 0 来隐藏该列

    # 根节点
    root_node = tree.insert("", "end", text="楼层信息")

    # 子节点
    floor_types = set(item["floortype"] for item in data)
    for floor_type in floor_types:
        type_node = tree.insert(root_node, "end", text=floor_type)
        floors = [item for item in data if item["floortype"] == floor_type]
        populate_tree(tree, type_node, floors)

    # 在创建 Treeview 时绑定双击事件
    tree.bind('<Double-1>', lambda event: (populate_listbox1(event, tree, VEULL), populate_listbox2(event, tree, VEURL), on_double_click_level(event, tree)))

    tree.place(width=256,height=400,x=0,y=64)

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

def populate_listbox1(event, tree, listbox):
    listbox.delete(0, END)  # 清空 listbox 中的所有条目
    # 获取选中的 floornum
    item = tree.selection()[0]
    values = tree.item(item, 'values')  # 获取 Treeview 项目的值
    if values:  # 检查值是否为空
        selected_floornum = values[0]  # 获取楼层编号

        # 首先将当前选择的 floornum 条目下的 floorentrance 的每一个由逗号隔开的字符串插入到 listbox 中，字体颜色为绿色
        for item in data:
            if item['floornum'] == selected_floornum:
                entrances = item['floorentrance'].split(',')
                for entrance in entrances:
                    listbox.insert(END, entrance)
                    listbox.itemconfig(END, {'fg': 'green'})

        # 接着遍历所有的条目，当有一个条目的 floorexit 中有一条由逗号隔开的字符串与当前选择的 floornum 值相同，且 floorexit 所在的条目中的 floornum 未被插入到 listbox 中，则将 floorexit 的值所在的 floornum 插入到 listbox 中，字体颜色为橙色，如果已经插入则跳过
        for item in data:
            exits = item['floorexit'].split(',')
            if selected_floornum in exits and item['floornum'] not in listbox.get(0, END):
                listbox.insert(END, item['floornum'])
                listbox.itemconfig(END, {'fg': 'orange'})

def populate_listbox2(event, tree, listbox):
    listbox.delete(0, END)  # 清空 listbox 中的所有条目
    # 获取选中的 floornum
    item = tree.selection()[0]
    values = tree.item(item, 'values')  # 获取 Treeview 项目的值
    if values:  # 检查值是否为空
        selected_floornum = values[0]  # 获取楼层编号

        # 首先将当前选择的 floornum 条目下的 floorexit 的每一个由逗号隔开的字符串插入到 listbox 中，字体颜色为绿色
        for item in data:
            if item['floornum'] == selected_floornum:
                exits = item['floorexit'].split(',')
                for exit in exits:
                    listbox.insert(END, exit)
                    listbox.itemconfig(END, {'fg': 'green'})

        # 接着遍历所有的条目，当有一个条目的 floorentrance 中有一条由逗号隔开的字符串与当前选择的 floornum 值相同，且 floorentrance 所在的条目中的 floornum 未被插入到 listbox 中，则将 floorentrance 的值所在的 floornum 插入到 listbox 中，字体颜色为橙色，如果已经插入则跳过
        for item in data:
            entrances = item['floorentrance'].split(',')
            if selected_floornum in entrances and item['floornum'] not in listbox.get(0, END):
                listbox.insert(END, item['floornum'])
                listbox.itemconfig(END, {'fg': 'orange'})

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

# 这部分代码还未经过测试

# 判断输入框的内容是否有变动
def if_entry_changed():
    load_data_from_json()
    floornum = floornum_var.get()
    floorname = floorname_var.get()
    difficulties = difficulties_var.get()
    floortype = floortype_var.get()
    floorlink = floorlink_var.get()
    floorentrance = floorentrance_var.get()
    floorexit = floorexit_var.get()
   
    # 比较输入的值和 JSON 数据
    if (floornum == data['floornum'] and
        floorname == data['floorname'] and
        difficulties == data['difficulties'] and
        floortype == data['floortype'] and
        floorlink == data['floorlink'] and
        floorentrance == data['floorentrance'] and
        floorexit == data['floorexit']):
        print('无需更改')
        return False
    elif(floornum == data['floornum']):
        if_save() 
        if if_save():
            print('保存成功')
            return False
    else:
        if_save_as()
        if if_save_as():
            print('另存为成功')
            return False

# 是否保存的选项
def if_save():
    result = messagebox.askyesno("保存", "是否保存更改？")
    if result:
        add_level()
        return True

# 是否另存为的选项
def if_save_as():
    result = messagebox.askyesno("保存", "是否创建新的楼层？")
    if result:
        add_level()
        return True

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

# 将选中楼层显示在输入框中
def on_double_click_level(event, tree):
    item = tree.selection()[0]
    values = tree.item(item, 'values')  # 获取 Treeview 项目的值
    if values:  # 检查值是否为空
        floornum = values[0]  # 获取楼层编号
        for item in data:
            if item['floornum'] == floornum:
                floornum_var.set(item['floornum'])
                floorname_var.set(item['floorname'])
                difficulties_var.set(item['difficulties'])
                floortype_var.set(item['floortype'])
                floorlink_var.set(item['floorlink'])
                floorentrance_var.set(item['floorentrance'])
                floorexit_var.set(item['floorexit'])
                break

# 添加楼层
def add_level():
    floornum = floornum_var.get()
    floorname = floorname_var.get()
    difficulties = difficulties_var.get()
    floortype = floortype_var.get()
    floorlink = floorlink_var.get()
    floorentrance = floorentrance_var.get()
    floorexit = floorexit_var.get()
    if floornum and floorname and difficulties and floortype and floorlink and floorentrance and floorexit:
        # 检查floornum是否已经存在
        for item in data:
            if item['floornum'] == floornum:
                # 如果floornum已经存在，更新对应的JSON条目
                item.update({"floornum": floornum, "floorname": floorname, "difficulties": difficulties, "floortype": floortype, "floorlink": floorlink, "floorentrance": floorentrance, "floorexit": floorexit})
                break
        else:
            # 如果floornum不存在，添加新的JSON条目
            data.append({"floornum": floornum, "floorname": floorname, "difficulties": difficulties, "floortype": floortype, "floorlink": floorlink, "floorentrance": floorentrance, "floorexit": floorexit})
        save_data_to_json(data)
        create_treeview(VLevels, data)

# 清空输入框
def clear_entry():
    floornum_var.set('')
    floorname_var.set('')
    difficulties_var.set('')
    floortype_var.set('')
    floorlink_var.set('')
    floorentrance_var.set('')
    floorexit_var.set('')
    VEULL.delete(0, END)
    VEURL.delete(0, END)

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

MainWindow = tk.Tk()
MainWindow.title('Backrooms')
MainWindow.geometry('960x450')
MainWindow.resizable(False, False)

#定义的参数
floornum_var = tk.StringVar()
floorname_var = tk.StringVar()
difficulties_var = tk.StringVar()
floortype_var = tk.StringVar()
floorlink_var = tk.StringVar()
floorentrance_var = tk.StringVar()
floorexit_var = tk.StringVar()

data = load_data_from_json()


#主菜单的内容
Menubar = tk.Menu(MainWindow) #主菜单名字Menubar
FileMenu = tk.Menu(Menubar, tearoff=0) #FileMenu
# FileMenu添加到菜单栏
Menubar.add_cascade(label="文件", menu=FileMenu)
FileMenu.add_command(label='新建') #子菜单添加命令
FileMenu.add_command(label='打开') #子菜单添加命令
FileMenu.add_command(label='保存/另存为') #子菜单添加命令
FileMenu.add_separator() #子菜单添加分割线
FileMenu.add_command(label='退出', command=MainWindow.quit) #子菜单添加命令
MainWindow.config(menu=Menubar)

#A左侧文件显示的内容
VFiles = tk.Frame(MainWindow, width=64, height=450, bg='#1E1F22')
VFiles.pack(side='left')

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

#B中侧关卡显示的内容
VLevels = tk.Frame(MainWindow, width=256, height=450, bg='#2B2D31')
VLevels.pack(side='left')
LevelName = tk.Label(VLevels, height=2, bg='#2B2D31', fg='white', text='文件名称', font=('微软雅黑', 12, 'bold'))
LevelName.place(width=256, x=0, y=0)
create_treeview(VLevels, data)

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

#C右侧编辑器显示的内容
VEditor = tk.Frame(MainWindow, width=640, height=450, bg='#313338')
VEditor.pack(side='right')


#CA右侧标题部分
VETitle = tk.Frame(VEditor, width=640, height=64, bg='#313338')
VETitle.pack(side='top')
VEHead = tk.Label(VETitle, height=1, bg='#313338', fg='white', text='后室编辑工具', font=('微软雅黑', 18, 'bold'))
VEHead.place(width=640, x=0, y=16)


#CB右侧编辑器左侧部分
VEleft = tk.Frame(VEditor, width=280, height=400, bg='#313338')
VEleft.pack(side='left')

#CB1右侧编辑器左部分-Label
VELL = tk.Frame(VEleft, width=80, height=400, bg='#313338')
VELL.pack(side='left')
VELL1 = tk.Label(VELL, height=1, bg='#313338', fg='white', text='楼层号', font=('微软雅黑', 12, 'bold')).place(x=8, y=32)
VELL2 = tk.Label(VELL, height=1, bg='#313338', fg='white', text='楼层名称', font=('微软雅黑', 12, 'bold')).place(x=8, y=80)
VELL3 = tk.Label(VELL, height=1, bg='#313338', fg='white', text='生存难度', font=('微软雅黑', 12, 'bold')).place(x=8, y=128)
VELL4 = tk.Label(VELL, height=1, bg='#313338', fg='white', text='楼层类型', font=('微软雅黑', 12, 'bold')).place(x=8, y=176)
VELL5 = tk.Label(VELL, height=1, bg='#313338', fg='white', text='楼层链接', font=('微软雅黑', 12, 'bold')).place(x=8, y=224)
VELL6 = tk.Label(VELL, height=1, bg='#313338', fg='white', text='楼层入口', font=('微软雅黑', 12, 'bold')).place(x=8, y=272)
VELL7= tk.Label(VELL, height=1, bg='#313338', fg='white', text='楼层出口', font=('微软雅黑', 12, 'bold')).place(x=8, y=320)

#CB2右侧编辑器有部分-Entry
VELR = tk.Frame(VEleft, width=200, height=400, bg='#313338')
VELR.pack(side='right')
VELR1 = tk.Entry(VELR, width=16, textvariable=floornum_var,font=('微软雅黑', 12, 'bold')).place(x=16, y=32)
VELR2 = tk.Entry(VELR, width=16, textvariable=floorname_var, font=('微软雅黑', 12, 'bold')).place(x=16, y=80)
VELR3 = tk.Entry(VELR, width=16, textvariable=difficulties_var, font=('微软雅黑', 12, 'bold')).place(x=16, y=128)
VELR4 = tk.Entry(VELR, width=16, textvariable=floortype_var, font=('微软雅黑', 12, 'bold')).place(x=16, y=176)
VELR5 = tk.Entry(VELR, width=16, textvariable=floorlink_var, font=('微软雅黑', 12, 'bold')).place(x=16, y=224)
VELR6 = tk.Entry(VELR, width=16, textvariable=floorentrance_var,font=('微软雅黑', 12, 'bold')).place(x=16, y=272)
VELR7 = tk.Entry(VELR, width=16, textvariable=floorexit_var, font=('微软雅黑', 12, 'bold')).place(x=16, y=320)

#CC右侧编辑器出入口编辑部分
VEright = tk.Frame(VEditor, width=360, height=400, bg='#313338')
VEright.pack(side='right')

VEUL = tk.Frame(VEright, width=180, height=240, bg='#313338')
VEUL.place(x=0, y=0)
VEUR = tk.Frame(VEright, width=180, height=240, bg='#313338')
VEUR.place(x=180, y=0)

VEULT = tk.Label(VEUL, height=1, bg='#313338', fg='white', text='楼层入口', font=('微软雅黑', 12, 'bold')).place(width=180, x=0, y=8)
VEURT = tk.Label(VEUR, height=1, bg='#313338', fg='white', text='楼层出口', font=('微软雅黑', 12, 'bold')).place(width=180, x=0, y=8)

VEULL = tk.Listbox(VEUL, width=20, height=8, font=('微软雅黑', 12, 'bold'))
VEULL.place(x=0, y=48)
VEURL = tk.Listbox(VEUR, width=20, height=8, font=('微软雅黑', 12, 'bold'))
VEURL.place(x=0, y=48)


VEM = tk.Frame(VEright, width=360, height=64, bg='#313338')
VEM.place(x=0, y=256)

VLM = tk.Frame(VEright, width=360, height=64, bg='#313338')
VLM.place(x=0, y=320)

VSave = tk.Button(VLM, text='保存', font=('微软雅黑', 12, 'bold'), command=add_level)
VSave.place(x=224, y=16)
VClose = tk.Button(VLM, text='关闭', font=('微软雅黑', 12, 'bold'), command=clear_entry)
VClose.place(x=288, y=16)

MainWindow.mainloop()