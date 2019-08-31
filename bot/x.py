# -*-coding: utf-8 -*-
from linepy import *
#from numba import jit
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse, timeit, _thread
#==============================================================================#
f = open('bot/run.txt','r')
ttoken = f.read()
f.close()
cl = LINE(ttoken) 
print("Auth Token : " + str(cl.authToken))
f = open('bot/token.txt','w')
f.write(str(cl.authToken))
f.close()
clMID = cl.profile.mid
botStart = time.time()
oepoll = OEPoll(cl)
ban = json.load(codecs.open("bot/ban.json","r","utf-8"))
pic = json.load(codecs.open("bot/picture.json","r","utf-8"))
settings = json.load(codecs.open("bot/temp.json","r","utf-8"))
msg_dict = {}
msg_dictt = {}
restart = False
def restartBot():
    print ("[ INFO ] BOT RESETTED")
    backupData()
    t = open('bot/run.txt','w')
    t.write(str(cl.authToken))
    t.close()
    for x in msg_dictt:
        cl.deleteFile(msg_dictt[x]["object"])
        del msg_dict[x]
    python = sys.executable
    os.execl(python, python, *sys.argv)
def backupData():
    try:
        json.dump(settings,codecs.open('bot/temp.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(pic,codecs.open('bot/picture.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ ERROR ] " + str(text))
    with open("bot/errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invaliod mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
            textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    cl.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
def helpmessage():
    helpMessage = """╔═══════════
╠        🔆҉風҉兒҉的半垢🔆
╠═✪〘 owners專用 〙✪═
╠✪〘 Help 〙✪═════
╠➥ Help 查看指令
╠✪〘 Status 〙✪════
╠➥ Restart 重新啟動
╠➥ Save 儲存設定
╠➥ Runtime 運作時間
╠➥ Speed 速度
╠➥ Set 設定
╠➥ About 關於發送者
╠✪〘 Settings 〙✪═══
╠➥ AutoAdd On/Off 自動加入
╠➥ AutoLeave On/Off 離開副本
╠➥ AutoRead On/Off 自動已讀
╠➥ Prompt On/Off 群組狀況提示
╠➥ ReRead On/Off 查詢收回
╠➥ Pro On/Off 所有保護
╠➥ Protect On/Off 踢人保護
╠➥ QrProtect On/Off 網址保護
╠➥ Invprotect On/Off 邀請保護
╠➥ Getinfo On/Off 取得友資詳情
╠➥ Detect On/Off 標註偵測
╠➥ Savelolipic On/Off (沒有用
╠➥ Savepic On/Off  (沒有用
╠➥ Timeline On/Off 文章預覽
╠✪〘 Self 〙✪═════
╠➥ Me 我的連結
╠➥ Mymid 我的mid
╠➥ Name @ 名字[發訊者/Tag]
╠➥ Bio @ 個簽[發訊者/Tag]
╠➥ Picture @ 頭貼[發訊者/Tag]
╠➥ Cover @ 封面[發訊者/Tag]
╠➥ Mid @ 查mid[友資/Tag]
╠➥ Contact: 以mid查友資
╠➥ Info @ 查看資料
╠✪〘 Blacklist 〙✪═══
╠➥ Ban [@/:] 加入黑單[友資/Tag/MID]
╠➥ Unban [@/:] 取消黑單[友資/Tag/MID]
╠➥ Keepban [times] 連續加入黑單
╠➥ Keepunban [times] 連續取消黑單
╠➥ Banlist 查看黑單
╠➥ Banlist 查看黑單
╠➥ Gbanlist 查看本群黑單
╠➥ CleanBan 清空黑單
╠➥ Kickban 踢除黑單
╠✪〘 Group 〙✪════
╠➥ Link On/Off 網址開啟/關閉
╠➥ Link 查看群組網址
╠➥ GroupList 所有群組列表
╠➥ GroupMemberList 成員名單
╠➥ GroupInfo 群組資料
╠➥ Cg: 以群組ID查詢資料
╠➥ Gn [text] 更改群名
╠➥ Tk @ 標註踢人
╠➥ Zk 踢出0字元
╠➥ Nk 以名字踢人
╠➥ Nt 以名字標注
╠➥ Inv (mid) 透過mid邀請
╠➥ Cancel 取消所有邀請
╠➥ Ri @ 來回機票
╠➥ Tagall 標註全體
╠➥ Zc 發送0字元友資
╠➥ Zt 標注0字元
╠➥ Setread 已讀點設置
╠➥ Cancelread 取消偵測
╠➥ Checkread 已讀偵測
╠➥ Gbc: 群組廣播(可限制人數)
╠➥ Fbc: 好友廣播
╠➥ Bye 機器退群(確認請打Y)
╠✪〘 Admin 〙✪════
╠➥ Adminadd @ 新增權限
╠➥ Admindel @ 刪除權限
╠➥ Adminlist 查看權限表
╠✪〘 Other 〙✪════
╠➥ Say [text times] 重複講話
╠➥ Tag @ [times] 重複標人
╠➥ Loli 
╠作者：
╚https://line.me/ti/p/eiFynbv1Xu """
    return helpMessage
def helpm():
    helpM = """╔═══════════
╠       🔆҉風҉兒҉的半垢🔆
╠═✪〘 admin專用 〙✪═
╠✪〘 Help 〙✪═════
╠➥ Help 查看指令
╠➥ Runtime 運作時間
╠➥ Speed 速度
╠➥ Set 設定
╠➥ About 關於發送者
╠➥ Save 儲存設定
╠✪〘 Self 〙✪═════
╠➥ Me 我的連結
╠➥ Mymid 我的mid
╠➥ Name @ 名字[發訊者/Tag]
╠➥ Bio @ 個簽[發訊者/Tag]
╠➥ Picture @ 頭貼[發訊者/Tag]
╠➥ Cover @ 封面[發訊者/Tag]
╠➥ Mid @ 查mid[友資/Tag]
╠➥ Contact: 以mid查友資
╠➥ Info @ 查看資料
╠✪〘 Group 〙✪════
╠➥ Link On/Off 網址開啟/關閉
╠➥ Link 查看群組網址
╠➥ GroupList 所有群組列表
╠➥ GroupMemberList 成員名單
╠➥ GroupInfo 群組資料
╠➥ Gn (文字) 更改群名
╠➥ Tagall 標註全體
╠➥ Nt 名字標注
╠➥ Zc 發送0字元友資
╠➥ Zt 標注0字元
╠➥ Setread 已讀點設置
╠➥ Cancelread 取消偵測
╠➥ Checkread 已讀偵測
╠➥ Bye 機器退群(確認請打Y)
╠✪〘 Other 〙✪════
╠➥ Say [內容 次數] 重複講話
╠➥ Tag @ [次數] 重複標人
╠➥ Adminlist 查看權限表
╠➥ Banlist 查看黑單
╠➥ Banmidlist 查看黑單者mid
╠➥ Loli 
╠作者：
╚https://line.me/ti/p/eiFynbv1Xu"""
    return helpM
wait = {
    "ban":False,
    "unban":False,
    "getmid":False,
    "pic":False,
    "monmonpic":False,
    "keepban":0,
    "keepunban":0,
    'rapidFire':{},
    'bye':{}
}
wait2 = {
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
}
setTime = {}
setTime = wait2['setTime']

if clMID not in ban["owners"]:
    ban["owners"].append(clMID)
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                sendMention(op.param1, " @! 感謝您加我為好友",[op.param1])
        if op.type == 11:
            G = cl.getGroup(op.param1)
            if op.param1 in settings["mention"]:
                sendMention(op.param1, " @! 更改群組設定",[op.param2])
            if op.param1 in settings["qrprotect"]:
                if op.param2 in ban["admin"] or op.param2 in ban["owners"]:
                    pass
                else:
                    gs = cl.getGroup(op.param1)
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    ban["blacklist"][op.param2] = True
                    gs.preventJoinByTicket = True
                    cl.updateGroup(gs)
        if op.type == 13:
            if clMID in op.param3:
                group = cl.getGroup(op.param1)
                if op.param2 in ban["admin"] or op.param2 in ban["owners"]:
                    cl.acceptGroupInvitation(op.param1)
                    sendMention(op.param1, "權限者 @! 邀請入群",[op.param2])
                else:
                    cl.acceptGroupInvitation(op.param1)
                    sendMention(op.param1, "@! 你不是權限者",[op.param2])
                    
            elif op.param1 in settings["invprotect"]:
                if op.param2 in ban["admin"] or op.param2 in ban["bots"] or op.param2 in ban["owners"]:
                    pass
                else:
                    ban["blacklist"][op.param2] = True
                    if len(op.param3) < 6:
                        for x in op.param3:
                            try:
                                cl.cancelGroupInvitation(op.param1,[x.mid])
                            except:
                                sleep(0.2)
                                cl.kickoutFromGroup(op.param1,[op.param3])
                    else:
                        sendMention(op.param1, "警告 @! 試圖邀請多個人,但是基於限制無法取消QQ",[op.param2])
            else:
                gInviMids = []
                for z in op.param3:
                    if z in ban["blacklist"]:
                        gInviMids.append(z.mid)
                if gInviMids == []:
                    pass
                else:
                    for mid in gInviMids:
                        cl.cancelGroupInvitation(op.param1, [mid])
                    cl.sendMessage(op.param1,"Do not invite blacklist user...")
        if op.type == 17:
            if op.param1 in ban["blacklist"]:
                cl.kickoutFromGroup(op.param1,[op.param1])
                cl.sendMessage(op.param1,"Blacklist user joined...")
            if op.param1 in settings["mention"]:
                name = str(cl.getGroup(op.param1).name)
                sendMention(op.param1, "你好 @! 歡迎加入"+name,[op.param2])
        if op.type == 19:
            if op.param1 in settings["mention"]:
                chiya=[op.param2]
                chiya.append(op.param3)
                sendMention(op.param1,"警告!! @! 踢了 @! ", chiya)
            if op.param2 in ban["admin"] or op.param2 in ban["bots"] or op.param2 in ban["owners"]:
                pass
            elif op.param3 in ban["owners"]:
                ban["blacklist"][op.param2] = True
                json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                cl.kickoutFromGroup(op.param1,[op.param2])
                cl.inviteIntoGroup(op.param1,[op.param3])
            elif op.param1 in settings["protect"]:
                ban["blacklist"][op.param2] = True
                cl.kickoutFromGroup(op.param1,[op.param2])
                json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
        if op.type == 24 or op.type == 21 or op.type ==22:
            if settings["autoLeave"] == True:
                cl.leaveRoom(op.param1)
        if (op.type == 25 or op.type == 26) and op.message.contentType == 0:
            msg = op.message
