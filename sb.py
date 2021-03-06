# -*- coding: utf-8 -*-
from linepy import *
import json, time

client = LineClient()
#client = LineClient(authToken='AuthToken')
client.log("Auth Token : " + str(client.authToken))
channel = LineChannel(client)
client.log("Channel Access Token : " + str(channel.channelAccessToken))

poll = LinePoll(client)
cctv={
    "cyduk":{},
    "point":{},
    "sidermem":{}
}

def mention(to, nama):
    aa = ""
    bb = ""
    strt = int(42)
    akh = int(42)
    nm = nama
    myid = client.getProfile().mid
    if myid in nm:    
      nm.remove(myid)
    #print nm
    for mm in nm:
      akh = akh + 2
      aa += """{"S":"""+json.dumps(str(strt))+""","E":"""+json.dumps(str(akh))+""","M":"""+json.dumps(mm)+"},"""
      strt = strt + 6
      akh = akh + 4
      bb += "╠ @x \n"
    aa = (aa[:int(len(aa)-1)])
    text = "╔═══════════\n║ MENTION ALL\n╠═══════════\n"+bb+"╚═══════════\n"
    try:
       client.sendMessage(to, text, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
       print(error)

while True:
    try:
        ops=poll.singleTrace(count=50)
        
        for op in ops:
            if op.type == OpType.SEND_MESSAGE:
                msg = op.message
                text = msg.text
                msg_id = msg.id
                receiver = msg.to
                sender = msg._from
                try:
                    if msg.contentType == 0:
                        if msg.toType == 2:
                            client.sendChatChecked(receiver, msg_id)
                            contact = client.getContact(sender)
                            if text.lower() == 'me':
                                client.sendMessage(receiver, None, contentMetadata={'mid': sender}, contentType=13)
                            elif text.lower() == 'speed':
                                start = time.time()
                                client.sendText(receiver, "TestSpeed")
                                elapsed_time = time.time() - start
                                client.sendText(receiver, "%sdetik" % (elapsed_time))
                            elif 'spic' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = client.getContact(u).pictureStatus
                                    print(client.getContact(u))
                                    client.sendImageWithURL(receiver, 'http://dl.profile.line.naver.jp/'+a)
                                except Exception as e:
                                    print(e)
                            elif 'scover' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = client.getProfileCoverURL(mid=u)
                                    print(a)
                                    client.sendImageWithURL(receiver, a)
                                except Exception as e:
                                    print(e)
                            elif text.lower() == 'tagall':
                                group = client.getGroup(msg.to)
                                nama = [contact.mid for contact in group.members]
                                nm1, nm2, nm3, jml = [], [], [], len(nama)
                                if jml <= 100:
                                    mention(msg.to, nama)
                                if jml > 100 and jml < 200:
                                    for i in range(0, 100):
                                        nm1 += [nama[i]]
                                    mention(msg.to, nm1)
                                    for j in range(101, len(nama)):
                                        nm2 += [nama[j]]
                                    mention(msg.to, nm2)
                                if jml > 200 and jml < 300:
                                    for i in range(0, 100):
                                        nm1 += [nama[i]]
                                    mention(msg.to, nm1)
                                    for j in range(101, 200):
                                        nm2 += [nama[j]]
                                    mention(msg.to, nm2)
                                    for k in range(201, len(nama)):
                                        nm3 += [nama[k]]
                                    mention(msg.to, nm3)
                                if jml > 300:
                                    print("Waow,,300+ member")
                                client.sendText(receiver, "Members :"+str(jml))
                            elif text.lower() == 'ceksider':
                                try:
                                    del cctv['point'][msg.to]
                                    del cctv['sidermem'][msg.to]
                                    del cctv['cyduk'][msg.to]
                                except:
                                    pass
                                cctv['point'][msg.to] = msg.id
                                cctv['sidermem'][msg.to] = ""
                                cctv['cyduk'][msg.to]=True
                            elif text.lower() == 'offread':
                                if msg.to in cctv['point']:
                                    cctv['cyduk'][msg.to]=False
                                    client.sendText(msg.to, cctv['sidermem'][msg.to])
                                else:
                                    client.sendText(msg.to, "Heh belom di Set")
                except Exception as e:
                    client.log("[SEND_MESSAGE] ERROR : " + str(e))

            if op.type == OpType.NOTIFIED_READ_MESSAGE:
                try:
                    if cctv['cyduk'][op.param1]==True:
                        if op.param1 in cctv['point']:
                            Name = client.getContact(op.param2).displayName
                            if Name in cctv['sidermem'][op.param1]:
                                pass
                            else:
                                cctv['sidermem'][op.param1] += "\n・" + Name
                                #cl.mention(op.param1, op.param2)
                                if " " in Name:
                                    nick = Name.split(' ')
                                    if len(nick) == 2:
                                        client.sendText(op.param1, 'haii... '+nick[0])
                                    else:
                                        client.sendText(op.param1, 'paagi '+nick[1])
                                else:
                                    client.sendText(op.param1, 'hai '+Name)
                        else:
                            pass
                    else:
                        pass
                except:
                    pass

            else:
                pass

            # Don't remove this line, if you wan't get error soon!
            poll.setRevision(op.revision)
            
    except Exception as e:
        client.log("[SINGLE_TRACE] ERROR : " + str(e))
