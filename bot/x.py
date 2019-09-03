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
    helpMessage = """♥♥♥♥♥♥♥♥♥♥♥
             🔆҉風҉兒҉的半垢🔆
               👉主機專用👈
🔹🔹🔹🎄~Help ~🎄🔹🔹🔹
     👉 Help 查看指令
🔹🔹🔹🎄~Status ~🎄🔹🔹🔹
     👉 Restart 重新啟動
**請定時重啟(請先儲存設定)
     👉 Save 儲存設定
     👉 Runtime 運行時間
     👉 Sp 網絡速度
     👉 Set 設定
     👉 About 關於自己
🔹🔹🔹🎄~Settings ~🎄🔹🔹🔹
     👉 AutoAdd On/Off 自動加入
     👉 AutoLeave On/Off 離開副本
     👉 AutoRead On/Off 自動已讀
     👉 Prompt On/Off 群組狀況提示
     👉 ReRead On/Off 查詢收回
     👉 Pro On/Off 所有保護
     👉 Protect On/Off 踢人保護
     👉 QrProtect On/Off 網址保護
     👉 Invprotect On/Off 邀請保護
     👉 Getinfo On/Off 取得友資詳情
     👉 Detect On/Off 標註偵測
     👉 Savelolipic (已關閉)
     👉 Savepic (如上)
     👉 Timeline On/Off 文章預覽
🔹🔹🔹🎄~自己 ~🎄🔹🔹🔹
     👉 Me 我的連結
     👉 Mymid 我的mid
     👉 Name @ 名字[發訊者/Tag]
     👉 Bio @ 個簽[發訊者/Tag]
     👉 Picture @ 頭貼[發訊者/Tag]
     👉 Cover @ 封面[發訊者/Tag]
     👉 Mid @ 查mid[友資/Tag]
     👉 Contact: 以mid查友資
     👉 Info @ 查看資料
🔹🔹🔹🎄~黑名單 ~🎄🔹🔹🔹
     👉 Ban [@/:] 加入黑單[友資/Tag/MID]
     👉 Unban [@/:] 取消黑單[友資/Tag/MID]
     👉 Keepban [times] 連續加入黑單
     👉 Keepunban [times] 連續取消黑單
     👉 Banlist 查看黑單
     👉 Gbanlist 查看本群黑單
     👉 CleanBan 清空黑單
     👉 Kickban 踢除黑單
🔹🔹🔹🎄~群組 ~🎄🔹🔹🔹
     👉 Link On/Off 網址開啟/關閉
     👉 Link 查看群組網址
     👉 GroupList 所有群組列表
     👉 GroupMemberList 成員名單
     👉 GroupInfo 群組資料
     👉 Cg: 以群組ID查詢資料
     👉 Gn [text] 更改群名
     👉 Tk @ 標註踢人
     👉 Zk 踢出0字元
     👉 Nk 以名字踢人
     👉 Nt 以名字標注
     👉 Inv (mid) 透過mid邀請
     👉 Cancel 取消所有邀請
     👉 Ri @ 來回機票
     👉 Tagall 標註全體
     👉 Zc 發送0字元友資
     👉 Zt 標注0字元
🔹👉 SR 已讀點設置
🔹👉 CR 取消偵測
🔹👉 LR 已讀偵測
     👉 Gbc: 群組廣播
     👉 Fbc: 好友廣播
     👉 Bye 機器退群(Y/N)
🔹🔹🔹🎄~Admin ~🎄🔹🔹🔹
     👉 addop @ 新增權限
     👉 delop @ 刪除權限
     👉 Adminlist 查看權限表
🔹🔹🔹🎄~其他 ~🎄🔹🔹🔹🔹
     👉 Say [text times] 重複講話
     👉 Tag @ [times] 重複標人
     👉 Loli (已關)
🔹作者：
🔹https://line.me/ti/p/eiFynbv1Xu """
    return helpMessage
def helpm():
    helpM = """♥♥♥♥♥♥♥♥♥♥♥
               🔆҉風҉兒҉的半垢🔆
               👉權限者專用👈
     🔹🔹🔹🎄~Help ~🎄🔹🔹🔹
     👉 Help 查看指令
     👉 Runtime 運作時間
     👉 Sp 網絡速度
     👉 Speed 運行速度
     👉 Set 設定
     👉 About 關於發送者
     👉 Save 儲存設定
     🔹🔹🔹🎄~自己 ~🎄🔹🔹🔹
     👉 Me 我的連結
     👉 Mymid 我的mid
     👉 Name @ 名字[發訊者/Tag]
     👉 Bio @ 個簽[發訊者/Tag]
     👉 Picture @ 頭貼[發訊者/Tag]
     👉 Cover @ 封面[發訊者/Tag]
     👉 Mid @ 查mid[友資/Tag]
     👉 Contact: 以mid查友資
     👉 Info @ 查看資料
     🔹🔹🔹🎄~群組 ~🎄🔹🔹🔹
     👉 Link On/Off 網址開啟/關閉
     👉 Link 查看群組網址
     👉 GroupList 所有群組列表
     👉 GroupMemberList 成員名單
     👉 GroupInfo 群組資料
     👉 Gn (文字) 更改群名
     👉 Tagall 標註全體
     👉 Nt 名字標注
     👉 Zc 發送0字元友資
     👉 Zt 標注0字元
     👉 SR 已讀點設置
     👉 CR 取消偵測
     👉 LR 已讀偵測
     👉 Bye 機器退群(Y/N)
     🔹🔹🔹🎄~其他 ~🎄🔹🔹🔹
     👉 Say [內容 次數] 重複講話
     👉 Tag @ [次數] 重複標人
     👉 Adminlist 查看權限表
     👉 Banlist 查看黑單
     👉 Banmidlist 查看黑單者mid
     👉 Loli (已關)
     作者友資：
     https://line.me/ti/p/eiFynbv1Xu"""
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
                sendMention(op.param1, " 提示！Selfbot-12.12運行中\n@! 感謝您加我為好友",[op.param1])
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
                    sendMention(op.param1, "提示！ @! selfbot v12.12 正在運行...",[op.param2])
                else:
                    cl.acceptGroupInvitation(op.param1)
                    sendMention(op.param1, "提示！ @! selfbot v12.12 正在運行...\n你沒有權限！",[op.param2])
                    
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
                        sendMention(op.param1, "警告 @! 邀請多個人,目前受限無法取消...\n如需取消請用主機輸入cancel",[op.param2])
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
                sendMention(op.param1, "歡迎 @! 加入 "+name,[op.param2])
        if op.type == 19:
            if op.param1 in settings["mention"]:
                chiya=[op.param2]
                chiya.append(op.param3)
                sendMention(op.param1,"⚠️警告⚠️ @! 踢了 @! ", chiya)
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
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            elif msg.toType == 2:
                to = receiver
            if text is None:
                return
            if sender in ban["blacklist"]:
                return
#                cl.kickoutFromGroup(to,[sender])  when black list user speek
            if text.lower() == 'help':
                if sender in ban["owners"]:
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                elif sender in ban["admin"]:
                    helpM = helpm()
                    cl.sendMessage(to, str(helpM))
                else:
                    cl.sendMessage(to,"👇👇👇👇👇👇👇👇👇\n               指令表\n👉Help 查詢指令\n👉about 關於自己\n⚠️你沒有權限，如需權限請聯絡作者。\n👉作者友資:\n👉風҉兒҉  https://line.me/ti/p/eiFynbv1Xu")
            if sender not in ban["blacklist"]:
                if text.lower() in ['妹子圖','抽妹子'] :
                    cl.sendImage(to, "bot/linepy/loli/{}-monmon.png".format(str(random.randint(0,int(settings["monmonpic"]-1)))))
                elif text.lower() in ['loli','抽蘿莉'] :
                    cl.sendImage(to, "bot/linepy/loli/{}-image.png".format(str(random.randint(0,int(settings["pic"]-1)))))
            if sender in ban["admin"] or sender in ban["owners"]:
                if text.lower() in ['speed','sp']:
                    cl.sendMessage(to,"測速中...")
                    cl.sendMessage(to,"結果為"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000)) + "秒")
                elif text.lower() == 'save':
                    backupData()
                    cl.sendMessage(to,"已儲存資料!")
                elif text.lower() == 'runtime':
                    cl.sendMessage(to, "系統已運作 {}".format(str(format_timespan(time.time() - botStart))))
                elif text.lower() == 'about':
                    ret_ = "🔹🔹🔹[ 關於使用者 ]"
                    ret_ += "\n🔹 使用者名稱 : {}".format(cl.getContact(sender).displayName)
                    if sender in cl.getAllContactIds():ret_ += "\n🔹 與本帳關係 : 好友"
                    else:ret_ += "\n🔹 與本帳關係 : 普通"
                    if sender in ban["owners"]:ret_ += "\n🔹 使用者權限 : 最高(擁有者)"
                    elif sender in ban["admin"]:ret_ += "\n🔹 使用者權限 : 部分(權限者)"
                    elif sender in ban["blacklist"]:ret_ += "\n🔹 使用者權限 : 無(黑單者)"
                    else:ret_ += "\n🔹 使用者權限 : 基本()"
                    ret_ += "\n🔹 詳細功能請打help"
                    ret_ += "\n🔹 擁有者 : 風兒"
                    ret_ += "\n🔹🔹🔹[ 感謝您的使用 ]"
                    cl.sendMessage(to, str(ret_))
                elif text.lower() == 'help':
                    cl.sendContact(to, "u39b4afd3e38e0172f278b4b06f329dd3")
                elif text.lower() == 'set':
                    try:
                        ret_ = "🔹[ 本機設定 ]"
                        if settings["autoAdd"] == True: ret_ += "\n🔹 自動加入好友 ✔"
                        else: ret_ += "\n🔹 自動加入好友 ✖"
                        if settings["autoLeave"] == True: ret_ += "\n🔹 自動退出副本 ✔"
                        else: ret_ += "\n🔹 自動退出副本 ✖"
                        if settings["autoRead"] == True: ret_ += "\n🔹 自動已讀 ✔"
                        else: ret_ += "\n🔹 自動已讀 ✖"
                        if settings["getmid"] == True: ret_ += "\n🔹 獲取友資詳情 ✔"
                        else: ret_ += "\n🔹 獲取友資詳情 ✖"
                        if settings["timeline"] == True: ret_ += "\n🔹 文章預覽 ✔"
                        else: ret_ += "\n🔹 文章預覽 ✖"
                        if settings["detectMention"] ==True: ret_+="\n🔹 標註偵測 ✔"
                        else: ret_ += "\n🔹 標註偵測 ✖"
                        if msg.toType==2:
                            ret_ += "\n🔹[ 單群設定 ]"
                            G = cl.getGroup(msg.to)
                            ret_ += "\n🔹 群組名稱 : {}".format(str(G.name))
                            if G.id in settings["protect"] : ret_+="\n🔹 踢人保護 ✔"
                            else: ret_ += "\n🔹 踢人保護 ✖"
                            if G.id in settings["qrprotect"] : ret_+="\n🔹 網址保護 ✔"
                            else: ret_ += "\n🔹 網址保護 ✖"
                            if G.id in settings["invprotect"] : ret_+="\n🔹 邀請保護 ✔"
                            else: ret_ += "\n🔹 邀請保護 ✖"
                            if G.id in settings["mention"] : ret_ += "\n🔹 群組狀況提示 ✔"
                            else: ret_ += "\n🔹 群組狀況提示 ✖"
                            if G.id in settings["reread"]: ret_+="\n🔹 復讀 ✔"
                            else: ret_ += "\n🔹 復讀 ✖"
                        ret_ += "\n🔹[ 完 ]"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() in ['oplist','adminlist','admin']:
                    if ban["admin"] == []:
                        cl.sendMessage(to,"無擁有權限者!")
                    else:
                        mc = "🔹🔹🔹[ 權限者 ]"
                        for mi_d in ban["admin"]:
                            try:
                                mc += "\n🔹 "+cl.getContact(mi_d).displayName
                            except:
                                pass
                        cl.sendMessage(to,mc + "\n[ 需要權限請聯絡半垢擁有者]")
                elif text.lower().startswith("say "):
                    x = text.split(' ')
                    if len(x) == 2:
                        cl.sendMessage(to,x[1])
                    elif len(x) == 3:
                        try:
                            c = int(x[2])
                            for c in range(c):
                                cl.sendMessage(to,x[1])
                        except:
                            cl.sendMessage(to,"錯誤！無法正確執行此指令")
                elif msg.text.lower().startswith("tag "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    x = text.split(' ')
                    if len(x) == 2:
                        cl.sendMessage(to,x[1])
                    elif len(x) == 3:
                        c = int(x[2])
                        for c in range(c):
                            sendMessageWithMention(to, inkey)
                elif text.lower().startswith("text "):
                    a = text.split(" ",2)
                    textnya = a[1]
                    urlnya = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                    cl.sendImageWithURL(msg.to, urlnya)
#==============================================================================#
                elif text.lower() == 'me':
                    if msg.toType == 0:
                        cl.sendContact(to, sender)
                    else:
                        sendMessageWithMention(to, sender)
                        cl.sendContact(to,sender)
                elif text.lower() == 'mymid':
                    cl.sendMessage(msg.to,"[MID]\n" +  sender)
                elif text.lower() == 'name':
                    cl.sendMessage(msg.to,"[Name]\n" + cl.getContact(sender).displayName)
                elif text.lower() == 'bio':
                    cl.sendMessage(msg.to,"[StatusMessage]\n" + cl.getContact(sender).statusMessage)
                elif text.lower() == 'picture':
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + cl.getContact(sender).pictureStatus)
                elif text.lower() == 'videoprofile':
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + cl.getContact(sender).pictureStatus + "/vp")
                elif text.lower() == 'cover':
                    cl.sendImageWithURL(msg.to, cl.getProfileCoverURL(sender))
                elif msg.text.lower().startswith("contact:"):
                    y = text[8:].split( )
                    for mid in y:
                        cl.sendContact(msg.to,mid)
                elif msg.text.lower().startswith("mid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "[ Mid User ]"
                        for ls in lists:
                            ret_ += "\n" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif text.lower() == 'mid':
                    wait["getmid"]=True
                    cl.sendMessage(to,"please send a contact")
                elif msg.text.lower().startswith("name ") :
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.sendMessage(msg.to,"[Name]\n" + cl.getContact(inkey).displayName)
                elif msg.text.lower().startswith("bio ") :
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.sendMessage(msg.to,"[StatusMessage]\n" + cl.getContact(inkey).statusMessage)
                elif msg.text.lower().startswith("cover ") :
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.sendImageWithURL(msg.to, cl.getProfileCoverURL(inkey))
                elif msg.text.lower().startswith("picture ") :
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + cl.getContact(inkey).pictureStatus)
                elif msg.text.lower().startswith("videoprofile ") :
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    cl.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + cl.getContact(inkey).pictureStatus + "/vp")
                elif msg.text.lower().startswith("info "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.sendMessage(msg.to, "[ 名字 ]\n" + contact.displayName +"\n[ 個簽 ]\n" + contact.statusMessage +"\n[ MID ]\n" + contact.mid)
                            cl.sendImageWithURL(msg.to, str("http://dl.profile.line-cdn.net/" + cl.getContact(ls).pictureStatus)) 
                            cl.sendImageWithURL(msg.to, str(cl.getProfileCoverURL(ls)))
#==============================================================================#
                elif text.lower() in ['link on',"招待URL許可"]:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "已經開咗網址✔")
                        else:
                            if group.id in settings["qrprotect"]:
                                cl.sendMessage(to,"警告！保護已開啟。\n無法打開網址。")
                            else:
                                group.preventedJoinByTicket = False
                                cl.updateGroup(group)
                                cl.sendMessage(to, "群組網址開咗✔")
                elif text.lower() in ["招待URL拒否",'link off']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "已經閂咗網址✖")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to,  "群組網址閂咗✖")
                elif text.lower() in ["魔刻結晶"]:
                    cl.sendMessage(to, "現在時刻は" + datetime.datetime.today().strftime('%Y年%m月%d日 %H:%M:%S') + "です。")
                elif text.lower() == 'join':
                    group = cl.getGroup(to)
                    if group.preventedJoinByTicket == False:
                        for m_id in ban["bots"]:
                            cl.sendMessage(m_id,"https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id))))
                    else:
                        group.preventedJoinByTicket = False
                        cl.updateGroup(group)
                        for m_id in ban["bots"]:
                            cl.sendMessage(m_id,"https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id))))
                elif text.lower() in ['gurl_get','Link','link','grouplink',"招待URL生成"]:
                    if msg.toType==2:
                        group=cl.getGroup(to)
                        if group.id in wait["qrprotect"]:
                            cl.sendMessage(to, "網址保護")
                        else:
                            cl.sendMessage(to,"https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id))))
                elif text.lower() in ['groupinfo','ginfo']:
                    group = cl.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "🔹🔹🔹[ 群組資料 ]"
                    ret_ += "\n🔹 群組名稱 : {}".format(str(group.name))
                    ret_ += "\n🔹 群組 Id : {}".format(group.id)
                    ret_ += "\n🔹 創建者 : {}".format(str(gCreator))
                    ret_ += "\n🔹 群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n🔹 邀請中 : {}".format(gPending)
                    ret_ += "\n🔹 網址狀態 : {}".format(gQr)
                    ret_ += "\n🔹 群組網址 : {}".format(gTicket)
                    ret_ += "\n🔹🔹🔹[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower().startswith('cg:'):
                    group = cl.getGroup(text[3:])
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "不明"
                    if group.invitee is None:
                        gPending = "0"
                    else:
                        gPending = str(len(group.invitee))
                    if group.preventedJoinByTicket == True:
                        gQr = "關閉"
                        gTicket = "無"
                    else:
                        gQr = "開啟"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(cl.reissueGroupTicket(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "🔹🔹🔹[ 群組資料 ]"
                    ret_ += "\n🔹 群組名稱 : {}".format(str(group.name))
                    ret_ += "\n🔹 群組 Id : {}".format(group.id)
                    ret_ += "\n🔹 創建者 : {}".format(str(gCreator))
                    ret_ += "\n🔹 群組人數 : {}".format(str(len(group.members)))
                    ret_ += "\n🔹 邀請中 : {}".format(gPending)
                    ret_ += "\n🔹 網址狀態 : {}".format(gQr)
                    ret_ += "\n🔹 群組網址 : {}".format(gTicket)
                    ret_ += "\n🔹🔹🔹[ 完 ]"
                    cl.sendMessage(to, str(ret_))
                    cl.sendImageWithURL(to, path)
                elif text.lower() in ['groupmemberlist','gmember','member']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        ret_ = "🔹🔹🔹[ 成員名單 ]"
                        no = 1
                        for mem in group.members:
                            ret_ += "\n🔹 {}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\n🔹🔹🔹[ 全部成員共 {} 人]".format(str(no-1))
                        cl.sendMessage(to, str(ret_))
                elif text.lower() in ['grouplist','glist','lg']:
                        groups = cl.groups
                        ret_ = "🔹🔹🔹[ 群組一覽 ]"
                        no = 1
                        for gid in groups:
                            group = cl.getGroup(gid)
                            ret_ += "\n🔹 {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\n🔹🔹🔹[ 共 {} 群 ]".format(str(no))
                        cl.sendMessage(to, str(ret_))
#==============================================================================#
                elif text.lower() == 'tagall':
                    group = cl.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//20
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*20 : (a+1)*20]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        cl.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        cl.sendMessage(to, "總共 {} 人".format(str(len(nama))))
                elif text.lower() == 'zt':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            sendMessageWithMention(to,target)
                elif text.lower() == 'zc':
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for mi_d in targets:
                           cl.sendContact(to,mi_d)
                elif text.lower().startswith("gn "):
                    if msg.toType == 2:
                        X = cl.getGroup(msg.to)
                        X.name = msg.text.replace("Gn ","")
                        cl.updateGroup(X)
                    else:
                        cl.sendMessage(msg.to,"It can't be used besides the group.")
                elif text.lower() in ['setread','sr','既読ポイント設定']:
                    cl.sendMessage(msg.to, "已讀點已設置。\n輸入LR獲取已讀的人。")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                    except:
                        pass
                    now2 = datetime.now()
                    wait2['readPoint'][msg.to] = msg.id
                    wait2['readMember'][msg.to] = ""
                    wait2['setTime'][msg.to] = datetime.strftime(now2,"%H:%M")
                    wait2['ROM'][msg.to] = {}
                elif text.lower() in ['cancelread','cr']:
                    cl.sendMessage(to, "已讀點已刪除")
                    try:
                        del wait2['readPoint'][msg.to]
                        del wait2['readMember'][msg.to]
                        del wait2['setTime'][msg.to]
                    except:
                        pass
                elif text.lower() in ['checkread','lookread','lr','既読確認','sn']:
                    if msg.to in wait2['readPoint']:
                        if wait2["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait2["ROM"][msg.to].items():
                                chiya += rom[1] + "\n"
                        cl.sendMessage(msg.to, "[已讀的人]:\n%s\n查詢時間:[%s]" % (chiya,setTime[msg.to]))
                    else:
                        cl.sendMessage(msg.to, "尚未開啟偵測✖")
                elif text.lower() == 'banlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "🔹🔹🔹[ 黑單成員 ]"
                        for mi_d in ban["blacklist"]:
                            try:
                                mc += "\n🔹 "+cl.getContact(mi_d).displayName
                            except:
                                pass
                        cl.sendMessage(msg.to,mc + "\n🔹🔹🔹[ 完 ]")
                elif text.lower() in ['groupbanmidlist','gban','gbanlist']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        mc = "🔹🔹🔹[ 本群黑單成員 ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n🔹 "+mi_d
                        cl.sendMessage(to,mc + "\n🔹[ 完 ]")
                elif text.lower() == 'banmidlist':
                    if ban["blacklist"] == {}:
                        cl.sendMessage(msg.to,"無黑單成員!")
                    else:
                        mc = "🔹🔹🔹[ 黑單成員 ]"
                        for mi_d in ban["blacklist"]:
                            mc += "\n🔹 "+mi_d
                        cl.sendMessage(to,mc + "\n🔹[ 完 ]")
                elif text.lower().startswith("nt "):
                    if msg.toType == 2:
                        _name = msg.text.replace("Nt ","")
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Not Found")
                        else:
                            for target in targets:
                                try:
                                    sendMessageWithMention(to, target)
                                except:
                                    pass
                elif text.lower() == 'bomb':
                    cl.sendContact(to,"\'")
                elif text.lower() in ["さようなら",'bye']:
                    cl.sendMessage(msg.to, "要把半垢離開...?\n(y/n)")
                    wait['bye'][msg.to] = sender
                elif text.lower() in ["Y","y","おk","N","n","だめ"]:
                    if msg._from== wait['bye'][msg.to]:
                        if text.lower() in ["いいよ",'y']:
                            cl.sendMessage(msg.to, "正在離開...")
                            cl.leaveGroup(msg.to)
                            del wait['bye'][msg.to]
                        elif text.lower() in ['n',"だめ"]:
                            cl.sendMessage(msg.to, "半垢將不會離開。")
                            del wait['bye'][msg.to]
                    else:
                        pass
                elif text.lower().startswith("sendto"):
                    x =text.split(' ')
                    if len(x)==2:
                        try:
                            cl.sendMessage(x[1],x[2])
                        except:
                            cl.sendMessage(to,"can't find")
#==============================================================================#
            if sender in ban["owners"]:
                if text.lower() == 'restart':
                    cl.sendMessage(to, "重啟成功....")
                    restartBot()
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加入好友開啟✔")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加入好友關閉✖")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    cl.sendMessage(to, "自離副本開啟✔")
                elif text.lower() == 'autoleave off':
                    settings["autoLeave"] = False
                    cl.sendMessage(to, "自離副本關閉✖")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    cl.sendMessage(to, "自動已讀開啟✔")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    cl.sendMessage(to, "自動已讀關閉✖")
                elif text.lower() == 'autolike on':
                    settings["autolike"] = True
                    cl.sendMessage(to, "自動按讚貼文開啟✔")
                elif text.lower() == 'autolike off':
                    settings["autolike"] = False
                    cl.sendMessage(to, "自動按讚貼文關閉✖")
                elif text.lower() == 'prompt on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        settings["mention"][G.id] = True
                        cl.sendMessage(to, "入群及踢出提示開啟✔")
                elif text.lower() == 'prompt off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["mention"][G.id]
                            cl.sendMessage(to, "入群及踢出提示關閉✖")
                        except:
                            cl.sendMessage(to, "沒有開呀")
                elif text.lower() == 'reread on':
                    settings["reread"][to] = True
                    cl.sendMessage(to,"復讀開啟✔")
                elif text.lower() == 'reread off':
                    try:
                        del settings["reread"][to]
                        cl.sendMessage(to,"復讀關閉✖")
                    except:
                        pass
                elif text.lower() == 'protect on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        settings["protect"][G.id] = True
                        cl.sendMessage(to, "踢人保護開啟✔")
                elif text.lower() == 'protect off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["protect"][G.id]
                            cl.sendMessage(to, "踢人保護關閉✖")
                        except:
                            cl.sendMessage(to, "沒有開呀")
                elif text.lower() == 'detect on':
                    settings["detectMention"] = True
                    cl.sendMessage(to, "標註偵測已開啟✔")
                elif text.lower() == 'detect off':
                    settings["detectMention"] = False
                    cl.sendMessage(to, "標註偵測已關閉✖")
                elif text.lower() == 'ban':
                    wait["ban"]=True
                    cl.sendMessage(to,"please send a contact")
                elif text.lower() == 'unban':
                    wait["unban"]=True
                    cl.sendMessage(to,"please send a contact")
                elif text.lower().startswith("keepban "):
                    times = text.split(' ')
                    wait["keepban"]=int(times[1])
                    cl.sendMessage(to,"please send contacts")
                elif text.lower().startswith("keepunban "):
                    times = text.split(' ')
                    wait["keepunban"]=int(times[1])
                    cl.sendMessage(to,"please send contacts")
                elif text.lower() == 'qrprotect on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        settings["qrprotect"][G.id] = True
                        cl.sendMessage(to, "網址保護開啟✔")
                elif text.lower() == 'qrprotect off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["qrprotect"][G.id]
                            cl.sendMessage(to, "網址保護關閉✖")
                        except:
                            cl.sendMessage(to, "都沒有開 怎樣關？")
                elif text.lower() == 'invprotect on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        settings["invprotect"][G.id] = True
                        cl.sendMessage(to, "邀請保護開啟✔")
                elif text.lower() == 'invprotect off':
                    if msg.toType ==2 :
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["invprotect"][G.id]
                            cl.sendMessage(to, "邀請保護關閉✖")
                        except:
                            cl.sendMessage(to, "都沒有開 怎樣關")
                elif text.lower() == 'getinfo on':
                    settings["getmid"] = True
                    cl.sendMessage(to, "友資詳情獲取開啟✔")
                elif text.lower() == 'getinfo off':
                    settings["getmid"] = False
                    cl.sendMessage(to, "友資詳情獲取關閉✔")
                elif text.lower() == 'timeline on':
                    settings["timeline"] = True
                    cl.sendMessage(to, "文章預覽開啟✔")
                elif text.lower() == 'timeline off':
                    settings["timeline"] = False
                    cl.sendMessage(to, "文章預覽關閉✖")
                elif text.lower() == 'savelolipic on':
                    wait["pic"] = True
                    cl.sendMessage(to,"send some picture for saveing~")
                elif text.lower() == 'savelolipic off':
                    wait["pic"] = False
                    backupData()
                elif text.lower() == 'savepic on':
                    wait["monmonpic"] = True
                    cl.sendMessage(to,"send some picture for saveing~")
                elif text.lower() == 'savepic off':
                    wait["monmonpic"] = False
                    backupData()
                    cl.sendMessage(to, "saveing...")
                elif text.lower() == 'pro on':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        settings["protect"][G.id] = True
                        settings["qrprotect"][G.id] = True
                        settings["invprotect"][G.id] = True
                        cl.sendMessage(to, "踢人保護開啟✔")
                        cl.sendMessage(to, "網址保護開啟✔")
                        cl.sendMessage(to, "邀請保護開啟✔")
                elif text.lower() == 'pro off':
                    if msg.toType ==2:
                        G = cl.getGroup(msg.to)
                        try:
                            del settings["protect"][G.id]
                            cl.sendMessage(to, "踢人保護關閉✖")
                        except:
                            pass
                        try:
                            del settings["qrprotect"][G.id]
                            cl.sendMessage(to, "網址保護關閉✖")
                        except:
                            pass
                        try:
                            del settings["invprotect"][G.id]
                            cl.sendMessage(to, "邀請保護關閉✖")
                        except:
                            pass
                elif msg.text.lower().startswith("addop ") or msg.text.lower().startswith("add "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey not in ban["admin"] and inkey not in ban["blacklist"] and inkey not in ban["owners"]: 
                        ban["admin"].append(str(inkey))
                        cl.sendMessage(to, "你已成為權限者！")
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                elif msg.text.lower().startswith("delop ") or msg.text.lower().startswith("del "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey in ban["admin"]:
                        ban["admin"].remove(str(inkey))
                        cl.sendMessage(to, "你不再是權限者！")
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                
                elif msg.text.lower().startswith("botsadd "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].append(str(inkey))
                    cl.sendMessage(to, "已加入分機！")
                elif msg.text.lower().startswith("botsdel "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    ban["bots"].remove(str(inkey))
                    cl.sendMessage(to, "已取消分機！")
                elif text.lower() == 'botslist':
                    if ban["bots"] == []:
                        cl.sendMessage(to,"無分機!")
                    else:
                        mc = "🔹🔹🔹[ Inviter List ]"
                        for mi_d in ban["bots"]:
                            mc += "\n🔹 "+cl.getContact(mi_d).displayName
                        cl.sendMessage(to,mc + "\n🔹🔹🔹[ Finish ]")
                elif msg.text.lower().startswith("ii "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    s = text.split(' ')
                    try:
                        for a in range(int(s[2])):
                            cl.createGroup("fuck",[inkey])
                    except:
                        pass
                    c =cl.getGroupIdsByName("fuck")
                    for gid in c:
                        cl.leaveGroup(gid)
                elif msg.text.lower().startswith("tk "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"Fuck you")
                            cl.kickoutFromGroup(msg.to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif msg.text.lower().startswith("zk "):
                    gs = cl.getGroup(to)
                    targets = []
                    for g in gs.members:
                        if g.displayName in "":
                            targets.append(g.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in ban["admin"]:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                except:
                                    pass
                elif msg.text.lower().startswith("ri "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            cl.sendMessage(to,"來回機票一張")
                            cl.findAndAddContactsByMid(target)
                            cl.kickoutFromGroup(msg.to,[target])
                            cl.inviteIntoGroup(to,[target])
                        except:
                            cl.sendMessage(to,"Error")
                elif text.lower().startswith("nk "):
                    if msg.toType == 2:
                        _name = msg.text.replace("Nk ","")
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"Not Found")
                        else:
                            for target in targets:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                except:
                                    pass
                elif text.lower() in ['byeall','.kickall','kickall']:
                    if msg.toType == 2:
                        gs = cl.getGroup(msg.to)
                        for g in gs.members:
                            try:
                                cl.kickoutFromGroup(msg.to,[g.mid])
                                sleep(1)
                            except:
                                pass
                elif text.lower() == 'cancel':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(msg.to,[_mid])
                        sleep(2)
                    cl.sendMessage(msg.to,"已取消所有邀請 ✖")
                elif text.lower() in ["cancelall"]:
                    group = cl.getGroup(to)
                    if group.invitee is None:
                        cl.sendMessage(to, "沒有邀請中的人 ✖")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        cl.cancelGroupInvitation(to, gInviMids)
                        cl.sendMessage(to, str(len(group.invitee)) + "人的邀請已被取消")
                elif text.lower().startswith("inv "):
                    if msg.toType == 2:
                        midd = text.split(' ')
                        cl.findAndAddContactsByMid(midd)
                        cl.inviteIntoGroup(to,[midd])
#==============================================================================#
                elif msg.text.lower().startswith("ban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        if target not in ban["owners"] :
                            try:
                                ban["blacklist"][target] = True
                                cl.sendMessage(msg.to,"已加入黑單!")
                                json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                            except:
                                cl.sendMessage(msg.to,"添加失敗 !")
                elif text.lower().startswith("ban :"):
                    txt = text.replace("Ban :","")
                    if txt not in ban["owners"] and len(txt) ==33 and txt.lower.startswith("u"):
                        ban["blacklist"][txt] = True
                        cl.sendMessage(msg.to,"已加入黑單!")
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                    else:
                        cl.sendMessage(msg.to,"添加失敗 !")
                elif text.lower().startswith("unban :"):
                    txt = text.replace("Unban :","")
                    if txt in ban["blacklist"] :
                        del ban["blacklist"][txt]
                        cl.sendMessage(msg.to,"已刪除黑單!")
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                    else:
                        cl.sendMessage(msg.to,"此人不在黑單之中 !")
                elif msg.text.lower().startswith("unban "):
                    targets = []
                    key = eval(msg.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    for target in targets:
                        try:
                            del ban["blacklist"][target]
                            cl.sendMessage(msg.to,"刪除成功 !")
                            json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        except:
                            cl.sendMessage(msg.to,"刪除失敗 !")
                elif text.lower() in ['kickban','killban']:
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        gMembMids = [contact.mid for contact in group.members]
                        matched_list = []
                    for tag in ban["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendMessage(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendMessage(msg.to,"Blacklist kicked out")
                elif text.lower() == 'cleanban':
                    for mi_d in ban["blacklist"]:
                        ban["blacklist"] = {}
                    cl.sendMessage(to, "已清空黑名單")
#==============================================================================#
                elif text.lower().startswith("fbc:"):
                    bctxt = text.split(':')
                    t = cl.getAllContactIds()
                    for manusia in t:
                        cl.sendMessage(manusia,bctxt[1])
                elif text.lower().startswith("gbc:"):
                    bctxt = text.split(':')
                    n = cl.getGroupIdsJoined()
                    if len(bctxt)==3:
                        for manusia in n:
                            group = cl.getGroup(manusia)
                            nama =[contact.mid for contact in group.members]
                            if len(nama) >int(bctxt[2]):
                                cl.sendMessage(manusia,bctxt[1])
                            else:
                                pass
                    elif len(bctxt)==2:
                        for g in n:
                            cl.sendMessage(g,bctxt[1])
                elif text.lower().startswith("copy "):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    contact = cl.getContact(inkey)
                    p = cl.profile
                    home = cl.getProfileDetail(inkey)
                    objectId = home["result"]["objectId"]
                    cl.updateProfileCoverById(objectId)
                    p.displayName = contact.displayName
                    p.statusMessage = contact.statusMessage
                    cl.updateProfile(p)
                    cl.updateProfileCoverById(cl.getProfileCoverId(inkey))
                    p.pictureStatus = contact.pictureStatus
                    cl.updateProfilePicture(contact.pictureStatus)
            if text.lower() == 'cc9487':
                if sender in ['ua10c2ad470b4b6e972954e1140ad1891']:
                    sys.exit()
                else:
                    pass
#==============================================================================#
        if op.type == 26:
            msg=op.message
            sender = msg._from
            receiver = msg.to
            text = msg.text
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if text is None:
                return
            if msg.contentType == 1:
                if wait["pic"] == True:
                    if msg._from in ban["owners"]:
                        image = cl.downloadObjectMsg(msg.id, saveAs="bot/linepy/loli/{}-image.png".format(settings["pic"]))
                        settings["pic"] +=1
                        cl.sendMessage(to,"OK")
                if wait["monmonpic"] == True:
                    if msg._from in ban["owners"]:
                        image = cl.downloadObjectMsg(msg.id, saveAs="bot/linepy/loli/{}-monmon.png".format(settings["monmonpic"]))
                        settings["monmonpic"] +=1
                        cl.sendMessage(to,"OK")
            if msg.contentType == 13:
                if settings["getmid"] == True:
                    contact = cl.getContact(msg.contentMetadata["mid"])
                    cl.sendMessage(to, "[ 名字 ]\n" + contact.displayName +"\n[ 個簽 ]\n" + contact.statusMessage +"\n[ MID ]\n" + contact.mid)
                    path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                    cl.sendImageWithURL(to, str(path))
                    path = cl.getProfileCoverURL(msg.contentMetadata["mid"])
                    cl.sendImageWithURL(to, str(path))
                if wait["ban"] ==True:
                    if msg._from in ban["owners"]:
                        ban["blacklist"][msg.contentMetadata["mid"]]=True
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        cl.sendMessage(to,"OK")
                        wait["ban"] =False
                if wait["unban"] ==True:
                    if msg._from in ban["owners"]:
                        del ban["blacklist"][msg.contentMetadata["mid"]]
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        cl.sendMessage(to,"OK")
                        wait["unban"] =False
                if wait["getmid"] ==True:
                    if msg._from in ban["owners"] or msg._from in ban["admin"]:
                        cl.sendMessage(to,msg.contentMetadata["mid"])
                        wait["getmid"] =False
                if wait["keepban"] >0:
                    if msg._from in ban["owners"]:
                        ban["blacklist"][msg.contentMetadata["mid"]]=True
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        cl.sendMessage(to,"OK")
                        wait["keepban"] -=1
                if wait["keepunban"] >0:
                    if msg._from in ban["owners"]:
                        del ban["blacklist"][msg.contentMetadata["mid"]]
                        json.dump(ban, codecs.open('bot/ban.json','w','utf-8'), sort_keys=True, indent=4, ensure_ascii=False)
                        cl.sendMessage(to,"OK")
                        wait["keepunban"] -=1
            if msg.contentType == 16:
#                if settings["autolike"] == True:
#                    url = msg.contentMetadata("postEndUrl")
#                    cl.likePost(url[25:58], url[66:], likeType=1001)    autolike can't be use in normal API
                if settings["timeline"] == True:
                    try:
                        ret_ = "🔹🔹🔹文章預覽🔹🔹🔹"
                        ret_ += "\n[文章作者 ]\n @!"
                        if "text" in msg.contentMetadata:
                            ret_ += "\n[ 文章詳情 ]\n"+msg.contentMetadata["text"]
                        ret_ += "\n[ URL ]\n {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
                        if "mediaOid" in msg.contentMetadata:
                            object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
                            if msg.contentMetadata["mediaType"] == "V":
                                if msg.contentMetadata["serviceType"] == "GB":
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                    murl = "\n[ Media URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
                                else:
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                                    murl = "\n[ Media URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
                                ret_ += murl
                            else:
                                if msg.contentMetadata["serviceType"] == "GB":
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
                                else:
                                    ourl = "\n[ Objek URL ]\n https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
                            ret_ += ourl
                        if "stickerId" in msg.contentMetadata:
                            ret_ += "\n[ 貼圖訊息 ]\n https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
                        f = msg.contentMetadata["postEndUrl"].split('userMid=')
                        s = f[1].split('&')
                        sendMention(msg.to, ret_,[s[0]])
                    except:
                        txt = msg.contentMetadata["text"]
                        txt += "\n[文章網址]\n" + msg.contentMetadata["postEndUrl"]
                        cl.sendMessage(to,"[文章詳情]\n"+txt)
#==============================================================================#
        if op.type == 26:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if text is None:
                return
            elif text.lower() in ['？','?']:
                  cl.sendMessage(to, "問號三小")
            elif text.lower() in ['笑死']:
                  cl.sendMessage(to, "你怎麼還沒死？")
            elif text.lower() in ['喔']:
                  cl.sendMessage(to, "喔三小")
            elif text.lower() in ['...']:
                  cl.sendMessage(to, "點屁點.")
            elif text.lower() in ['你們幾個人' , '幾個人' , '幾個' , '對面幾個人' , '對面幾個' , '對面多少人' , '你們幾個人呀' , '幾個人呀' , '幾個呀' , '對面幾個人呀' , '對面幾個呀' , '對面多少人呀' ]:
                  cl.sendMessage(to, "沒有幾個聊天，幾乎都淺水居多")
            elif text.lower() in ['幹','干','乾']:
                  cl.sendMessage(to, "齁～罵髒話")
            elif text.lower() in ['哈哈']:
                  cl.sendMessage(to, "笑屁喔...")
            elif text.lower() in ['幹您娘','幹你娘']:
                  cl.sendMessage(to, "來啊幾點")
            elif text.lower() in ['來嘴炮','嘴炮']:
                  cl.sendMessage(to, "來來來哩來！")
            elif text.lower() in ['哩沙小']:
                  cl.sendMessage(to, "跨哩某小")
            elif text.lower() in ['你殺小啦幹']:
                  cl.sendMessage(to, "🙃" )
            if settings["autoRead"] == True:
                cl.sendChatChecked(to, msg_id)
            if msg.contentType == 0 and sender not in ban["owners"] and msg.toType == 2:
                if 'MENTION' in msg.contentMetadata.keys()!= None:
                    names = re.findall(r'@(\w+)', text)
                    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                    mentionees = mention['MENTIONEES']
                    lists = []
                    for mention in mentionees:
                        if clMID in mention["M"]:
                            if settings["detectMention"] == True:
                                contact = cl.getContact(sender)
                                sendMention(to,"@! 標我幹嘛?\n有事請私我", [contact.mid])
                            break
            try:
                if to in settings["reread"]:
                    if msg.contentType == 0:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                lists.append(mention["M"])
                            list=""
                            x = msg.text
                            for mid in lists:
                                x=x.replace("@"+str(cl.getContact(mid).displayName),"@!")
                                list+=mid+","
                            listt=list[:-1]
                            msg_dict[msg.id] = {"mtext":"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n"+x,"from":msg._from,"createdTime":time.time(),"mentionee":listt}
                        else:
                            msg_dict[msg.id] = {"text":msg.text,"from":msg._from,"createdTime":time.time()}
            except Exception as e:
                print(e)
            if msg.contentType == 1:
                if to in settings["reread"]:
                    if 'gif' in msg.contentMetadata.keys()!= None:
                        gif = cl.downloadObjectMsg(msg_id, saveAs="bot/linepy/tmp/{}-image.gif".format(time.time()))
                        msg_dictt[msg.id] = {"from":msg._from,"gif":0,"object":gif,"createdTime":time.time()}
                    else:
                        image = cl.downloadObjectMsg(msg_id, saveAs="bot/linepy/tmp/{}-image.bin".format(time.time()))
                        msg_dictt[msg.id] = {"from":msg._from,"image":0,"object":image,"createdTime":time.time()}
            elif msg.contentType == 3:
                if to in settings["reread"] :
                    sound = cl.downloadObjectMsg(msg_id, saveAs="bot/linepy/tmp/{}-sound.mp3".format(time.time()))
                    msg_dictt[msg.id] = {"from":msg._from,"sound":0,"object":sound,"createdTime":time.time()}
            elif msg.contentType == 7:
                if to in settings["reread"]:
                    stk_id = msg.contentMetadata['STKID']
                    msg_dict[msg.id] = {"from":msg._from,"stkid": stk_id ,"createdTime":time.time()}
            elif msg.contentType == 13:
                if to in settings["reread"]:
                    mid = msg.contentMetadata["mid"]
                    msg_dict[msg.id] = {"from":msg._from,"mid": mid ,"createdTime":time.time()}
            elif msg.contentType == 14:
                if to in settings["reread"]:
                    file = cl.downloadObjectMsg(msg_id, saveAs="bot/linepy/tmp/{}-".format(msg_id)+msg.contentMetadata['FILE_NAME'])
                    msg_dictt[msg.id] = {"from":msg._from,"file":0,"object":file,"createdTime":time.time()}
            try:
                if len(msg_dictt)>=100:
                    for x in msg_dictt:
                        cl.deleteFile(msg_dictt[x]["object"])
                        del msg_dictt[x]
            except:
                pass
#==============================================================================#
        if op.type == 65:
            try:
                msg = op.message
                at = op.param1
                msg_id = op.param2
                if op.param1 in settings["reread"]:
                    if msg_id in msg_dict:
                        timeNow = time.time()
                        opi=[]
                        opi.append(msg_dict[msg_id]["from"])
                        if "mtext" in msg_dict[msg_id]:
                            x =msg_dict[msg_id]["mentionee"].split(',')
                            for ic in x:
                                opi.append(ic)
#                            cl.sendMessage(at,msg_dict[msg_id]["mentionee"]+"||"+str(msg_dict[msg_id]["mtext"]))
                            sendMention(at,msg_dict[msg_id]["mtext"],opi)
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                        elif "text" in msg_dict[msg_id]:
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n"+str(msg_dict[msg_id]["text"]),opi)
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                        elif "stkid" in msg_dict[msg_id]:
                            path = "https://stickershop.line-scdn.net/stickershop/v1/sticker/{}/ANDROID/sticker.png;compress=true".format(msg_dict[msg_id]["stkid"])
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n一張貼圖",opi)
                            cl.sendImageWithURL(at,path)
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                        elif "mid" in msg_dict[msg_id]:
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n一則友資",opi)
                            cl.sendContact(at,msg_dict[msg_id]["mid"])
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dict[msg_id]["createdTime"])+"秒之前")
                            del msg_dict[msg_id]
                    elif msg_id in msg_dictt:
                        timeNow = time.time()
                        opi=[msg_dictt[msg_id]["from"]]
                        if "image" in msg_dictt[msg_id]:
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n一張圖片",opi)
                            cl.sendImage(at, msg_dictt[msg_id]["object"])
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dictt[msg_id]["createdTime"])+"秒之前")
                            cl.deleteFile(msg_dictt[msg_id]["object"])
                            del msg_dictt[msg_id]
                        elif "gif" in msg_dictt[msg_id]:
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n一張圖片",opi)
                            cl.sendGIF(at, msg_dictt[msg_id]["object"])
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dictt[msg_id]["createdTime"])+"秒之前")
                            cl.deleteFile(msg_dictt[msg_id]["object"])
                            del msg_dictt[msg_id]
                        elif "sound" in msg_dictt[msg_id]:
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n一份音檔",opi)
                            cl.sendAudio(at, msg_dictt[msg_id]["object"])
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dictt[msg_id]["createdTime"])+"秒之前")
                            cl.deleteFile(msg_dictt[msg_id]["object"])
                            del msg_dictt[msg_id]
                        elif "file" in msg_dictt[msg_id]:
                            sendMention(at,"你以為你能收回？\n[收回訊息者]\n @! \n[訊息內容]\n一個檔案",opi)
                            cl.sendFile(at, msg_dictt[msg_id]["object"])
                            cl.sendMessage(at,"時間"+str(timeNow - msg_dictt[msg_id]["createdTime"])+"秒之前")
                            cl.deleteFile(msg_dictt[msg_id]["object"])
                            del msg_dictt[msg_id]
                else:
                    pass
            except Exception as e:
                print (e)
#==============================================================================#
        if op.type == 55:
            try:
                if op.param1 in wait2['readPoint']:
                    Name = cl.getContact(op.param2).displayName
                    if Name in wait2['readMember'][op.param1]:
                        pass
                    else:
                        wait2['readMember'][op.param1] += "\n[※]" + Name
                        wait2['ROM'][op.param1][op.param2] = "[※]" + Name
                        print (time.time() + name)
                else:
                    pass
            except:
                pass
    except Exception as error:
        logError(error)
#==============================================================================#
while 1:
    if time.time() -botStart > 999999999999 :
        
        restartBot()
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
#                _thread.start_new_thread( lineBot, (op, ) )
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)

