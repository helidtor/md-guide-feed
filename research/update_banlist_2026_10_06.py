"""Apply the seven changes in the user-provided 06/10/2026 banlist image.

Preserves the previous snapshot and increments all dataVersion roots together.
Idempotent after the release has been applied; does not push to GitHub.
"""
import collections, datetime, hashlib, json, pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parent.parent
DATE='2026-10-06';BAN_VERSION='MD-2026-10-06'
SOURCE='https://www.masterduelmeta.com/forbidden-limited-list'
CHANGES={
 74586817:('PSY-Framelord Omega','forbidden'),
 91800273:('Dimension Shifter','forbidden'),
 99243014:('Synchro Overtake','forbidden'),
 16387555:('Kewl Tune Cue','limited'),
 20508881:('Radiant Typhoon Vision','limited'),
 54143349:('Radiant Typhoon Eldam','semi-limited'),
 30271097:('The Fallen & The Virtuous','semi-limited'),
}
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8-sig'))
def write(name,data):(ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
d=read('decks.json');g=read('guides.json');b=read('banlist.json');m=read('manifest.json')
versions={x['dataVersion'] for x in [d,g,b,m]}
assert len(versions)==1,'Root dataVersions differ; resolve before applying migration.'
if all(x['banlist']['version']==BAN_VERSION for x in d['decks']) and m['dataVersion']>=5:
    print('Release already applied; no files changed.')
    sys.exit(0)
assert m['dataVersion']==4,'This migration expects the dataVersion 4 release.'
version=m['dataVersion']+1
previous=next(x for x in b['lists'] if x['version']=='MD-2026-09-03')
active=next((x for x in b['lists'] if x['version']==BAN_VERSION),None)
if active is None:
    active=json.loads(json.dumps(previous));active.update(version=BAN_VERSION,effectiveDate=DATE+'T11:00:00+07:00',effectiveTimeConfirmed=False)
    b['lists'].append(active)
by_id={e['cardId']:e for e in active['entries']}
for i,(name,status) in CHANGES.items():by_id[i]={'cardId':i,'name':name,'status':status}
active['entries']=sorted(by_id.values(),key=lambda e:e['cardId'])
active['sourceUrls']=list(dict.fromkeys(active.get('sourceUrls',[])+[SOURCE]))
active['note']='Đối chiếu 7 thay đổi theo ảnh người dùng cung cấp ngày 06/10/2026 và trang Forbidden/Limited List của Master Duel Meta. Giữ các giới hạn khác từ snapshot trước. Ngày hiệu lực 06/10/2026; mốc 11:00 +07:00 được kế thừa, chưa xác nhận giờ chính thức.'
now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
active['fetchedAt']=now
limits={e['cardId']:{'forbidden':0,'limited':1,'semi-limited':2,'unlimited':3}[e['status']] for e in active['entries']}
decks={x['id']:x for x in d['decks']};guides={x['deckId']:x for x in g['guides']}
edits=[]
def remove(deck,key,i):
    item=next(c for c in deck[key] if c['cardId']==i);deck[key].remove(item)
    return item
elf=decks['elfnote'];remove(elf,'extraDeck',74586817)
edits.append('Elfnote: bỏ 1 PSY-Framelord Omega; Extra Deck còn 14 lá, line Elfnote hiện tại không dùng Omega.')
mix=decks['elfnote-kewl-tune']
next(c for c in mix['coreCards'] if c['cardId']==16387555)['qty']=1
next(c for c in mix['techCards'] if c['cardId']==97268402)['qty']=3
edits.append('Elfnote Kewl Tune: Kewl Tune Cue 2 → 1; Effect Veiler 2 → 3, giữ Main Deck 40 lá; Mix giữ 2 bản.')
sync=decks['synchrons'];remove(sync,'coreCards',99243014)
converter=next(c for c in sync['coreCards'] if c['cardId']==11069680);converter['qty']=3
converter['note']='Gửi chính nó và một Tuner từ tay vào GY để tìm Synchron; chuẩn bị non-Tuner Level 2 trong GY cho Junk Synchron. Khi dùng làm Synchro Material, có thể hồi Tuner theo điều kiện.'
edits.append('Synchrons: bỏ 1 Synchro Overtake; Junk Converter 2 → 3, giữ Main Deck 40 lá và sửa hướng dẫn đi sau.')
for deck in d['decks']:
    deck['banlist']={'version':BAN_VERSION,'effectiveDate':DATE,'verifiedOn':DATE}
    deck['updatedAt']=DATE
    if any(c['cardId'] in CHANGES for k in ['coreCards','techCards','extraDeck'] for c in deck[k]) or deck['id'] in ['elfnote','synchrons']:
        deck['sources'].append({'title':'Master Duel Meta — Forbidden/Limited List: October 6th, 2026','url':SOURCE,'accessed':DATE,'usage':'fact-check'})
    for k in ['coreCards','techCards','extraDeck']:
        for c in deck[k]:
            if c['cardId'] in CHANGES:
                cap=limits[c['cardId']]
                assert c['qty']<=cap,(deck['id'],c['name'],'still over limit')
                if c['name'] in ['Kewl Tune Cue','Radiant Typhoon Vision','Radiant Typhoon Eldam','The Fallen & The Virtuous']:
                    c['note']=c.get('note','')+f' Giới hạn từ 06/10/2026: tối đa {cap} bản.'
eg=guides['elfnote'];eg['playstyle']['tips']=[t.replace('40 Main / 15 Extra','40 Main / 14 Extra') for t in eg['playstyle']['tips']]
eg['playstyle']['tips'].append('Banlist 06/10/2026: Omega bị cấm và đã bỏ khỏi Extra Deck; line ô giữa Elfnote vẫn dùng được.')
guides['elfnote-kewl-tune']['playstyle']['tips'].append('Banlist 06/10/2026: Cue chỉ còn 1 bản; tăng Effect Veiler lên 3 để bù slot, giữ Mix ở 2 bản theo giới hạn hiện hành. Line minh họa mở Elfnote giữ nguyên.')
sg=guides['synchrons']
sg['playstyle']['goingSecond']='Dùng Junk Converter cùng một Tuner trên tay để chuẩn bị quái Level 2 trong GY và tìm Synchron; giữ extender cho trường hợp Junk Synchron hoặc Speeder bị negate. Synchro Overtake đã bị cấm từ 06/10/2026 nên không dùng nó để mở hay vượt negate.'
sg['playstyle']['tips'].append('Banlist 06/10/2026: bỏ Synchro Overtake, tăng Junk Converter lên 3; Converter cần chính nó và một Tuner khác trên tay để search.')
for combo in sg['combos']:
    combo['deckCardIds']=list(dict.fromkeys(11069680 if i==99243014 else i for i in combo['deckCardIds']))
# A forbidden counter must not remain a recommendation in today's guides.
ig=guides['infernoid']
ig['weaknesses']=[t.replace('bị Dimension Shifter','bị khóa hoặc banish GY') for t in ig['weaknesses']]
for co in ig['combos']:
    for point in co['chokePoints']:point['text']=point['text'].replace('bị Dimension Shifter','bị khóa hoặc banish GY')
for counter in ig['counters']:counter['note']=counter['note'].replace('bị Dimension Shifter','bị khóa hoặc banish GY')
source_note={'name':'Master Duel Meta — banlist 2026-10-06','url':SOURCE,'note':'Seven changes cross-checked against the user-provided image dated 2026-10-06. All 100 decklists checked against the active snapshot; Vietnamese guidance revised where affected.'}
m['sources'].append(source_note)
for data in [d,g,b,m]:data['dataVersion']=version
m['generatedAt']=now
for name,data in [('decks',d),('guides',g),('banlist',b)]:
    filename=m['files'][name]['url'];write(filename,data);raw=(ROOT/filename).read_bytes()
    m['files'][name].update(size=len(raw),sha256=hashlib.sha256(raw).hexdigest())
write('manifest.json',m)
print(f'Applied {BAN_VERSION}; dataVersion {version}; {len(d["decks"])} decks / {len(g["guides"])} guides.')
for edit in edits:print(edit)
