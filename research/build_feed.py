"""Append the 65 reviewed editorial profiles to the original 35 feed entries.

Re-run with: rtk python research/build_feed.py
Requires cardinfo.json (YGOPRODeck API v7 response) beside this script.
The first 35 records are retained, including on a repeated build.
"""
import collections, datetime, hashlib, json, pathlib, re, sys
sys.stdout.reconfigure(encoding='utf-8')
from editorial import PROFILES
import refinements
R=pathlib.Path(__file__).resolve().parent
ROOT=R.parent
DATE='2026-10-04'
VERSION=4
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path,obj):path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def norm(s):return re.sub(r'[<>]','',s).lower()
cards=read(R/'cardinfo.json')['data']
lookup={norm(c['name']):c for c in cards}
lookup['el shaddoll meshachrer']=next(c for c in cards if c['name']=='El Shaddoll Meshahrail')
def card(name):return lookup[norm(name)]
def ids(names):return list(dict.fromkeys(card(n)['id'] for n in names))
def slug(s):
    overrides={'P.U.N.K.':'punk','@Ignister':'ignister','Live☆Twin':'live-twin','Live☆Twin Spright':'live-twin-spright','Dinos':'dinosaurs'}
    return overrides.get(s,re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-'))
selected=read(R/'selected.json')
assert len(selected)==65 and set(x['name'] for x in selected)==set(PROFILES)
decks=read(ROOT/'decks.json');guides=read(ROOT/'guides.json');ban=read(ROOT/'banlist.json');manifest=read(ROOT/'manifest.json')
if manifest['dataVersion']>VERSION:
    raise SystemExit('Historical version 4 builder: refusing to overwrite a newer release. Use the current banlist migration instead.')
original_decks=decks['decks'][:35];original_ids={d['id'] for d in original_decks}
original_guides=[g for g in guides['guides'] if g['deckId'] in original_ids]
assert len(original_decks)==len(original_guides)==35
limits_by_list=[]
for b in ban['lists']:
    limits_by_list.append({e['cardId']:{'forbidden':0,'limited':1,'semi-limited':2,'unlimited':3}[e['status']] for e in b['entries']})
def limit(i):return min(x.get(i,3) for x in limits_by_list)
tech_notes={
 'Ash Blossom & Joyous Spring':('hand-trap','Chặn thêm bài, gửi từ Deck hoặc Special Summon từ Deck; chọn đúng hiệu ứng đối thủ.'),
 'Infinite Impermanence':('hand-trap','Negate Effect Monster face-up; dùng từ tay khi không điều khiển bài.'),
 'Effect Veiler':('hand-trap','Negate quái face-up trong Main Phase đối thủ.'),
 'Droll & Lock Bird':('hand-trap','Sau lần thêm bài từ Main Deck đầu tiên, chặn các lần thêm tiếp theo trong lượt.'),
 'Maxx "C"':('hand-trap','Rút theo Special Summon đối thủ sau khi hiệu ứng resolve.'),
 'Mulcharmy Fuwalos':('hand-trap','Dùng khi không điều khiển bài để rút theo các triệu hồi từ Deck/Extra Deck.'),
 'Mulcharmy Purulia':('hand-trap','Dùng khi không điều khiển bài để rút theo các triệu hồi từ tay.'),
 'Ghost Belle & Haunted Mansion':('hand-trap','Chặn các hiệu ứng có thao tác GY thuộc điều kiện của Belle.'),
 'Ghost Ogre & Snow Rabbit':('hand-trap','Phá bài khi hiệu ứng hợp lệ được kích hoạt; không tự negate hiệu ứng.'),
 'Nibiru, the Primal Being':('hand-trap','Sau ít nhất năm quái được Normal/Special Summon trong lượt, Tribute quái face-up theo hiệu ứng.'),
 'Crossout Designator':('protection','Cần bản cùng tên trong Main Deck để banish và negate tên đã khai báo.'),
 'Forbidden Droplet':('board-breaker','Gửi bài làm cost để giảm ATK và negate; số quái tương ứng số bài gửi.'),
 'Forbidden Crown':('board-breaker','Đối chiếu điều kiện khóa của Quick-Play này trước khi dùng nhánh triệu hồi tiếp.'),
 'Evenly Matched':('board-breaker','Cuối Battle Phase, ép đối thủ banish úp cho số bài bằng sân bạn; có thể dùng từ tay khi sân trống.'),
 'Harpie\'s Feather Duster':('board-breaker','Phá toàn bộ Spell/Trap đối thủ.'),
 'Heavy Storm':('board-breaker','Phá toàn bộ Spell/Trap cả hai bên; cân nhắc engine trên sân mình.'),
 'Lightning Storm':('board-breaker','Cần không điều khiển bài face-up; chọn phá quái Attack hoặc Spell/Trap đối thủ.'),
 'Dark Ruler No More':('board-breaker','Negate quái face-up đối thủ; đối thủ không nhận damage trong phần còn lại của lượt.'),
 'Raigeki':('board-breaker','Phá toàn bộ quái đối thủ; có thể bị bảo vệ hoặc negate.'),
 'Dark Hole':('board-breaker','Phá toàn bộ quái cả hai bên.'),
 'Triple Tactics Talent':('utility','Chỉ kích hoạt khi đối thủ đã dùng hiệu ứng quái trong Main Phase của bạn.'),
 'Triple Tactics Thrust':('consistency','Tìm/úp Normal Spell hoặc Normal Trap theo điều kiện hiệu ứng quái đối thủ.'),
 'Solemn Judgment':('protection','Trả nửa LP để negate một triệu hồi hoặc kích hoạt Spell/Trap hợp lệ.'),
}
generic_tech={'D.D. Crow','Ghost Mourner & Moonlit Chill','Ghost Sister & Spooky Dogwood','Skull Meister','Dimension Shifter','Pot of Sloth','Pot of Desires','Pot of Duality','Pot of Extravagance','Small World','Ultimate Slayer','Dominus Impulse','Dominus Purge','Dominus Spark','Dominus Spiral','Songs of the Dominators','Book of Eclipse','PSY-Framegear Gamma','PSY-Frame Driver','Called by the Grave','Solemn Warning','Solemn Strike','Solemn Accusation','Iron Thunder'}
def merged(ls):
    out=collections.OrderedDict()
    for c in ls:
        info=card(c['name']);i=info['id']
        if i not in out:out[i]={'cardId':i,'name':info['name'],'qty':0}
        out[i]['qty']+=c['qty']
    return list(out.values())
records=[]
for rank,source in enumerate(selected,36):
    name=source['name'];profile=PROFILES[name];deck_id=slug(name)
    assert deck_id not in original_ids
    main=merged(source['lists'][0]);extra=merged(source['lists'][1]);changes=[]
    target=sum(c['qty'] for c in main)
    for ls,label in [(main,'Main'),(extra,'Extra')]:
        for c in ls:
            cap=limit(c['cardId'])
            if c['qty']>cap:
                changes.append(f"{label}: {c['name']} {c['qty']} → {cap}")
                c['qty']=cap
        ls[:]=[c for c in ls if c['qty']]
    # Keep original Main size, using real generic interaction instead of illegal slots.
    for n in ['Infinite Impermanence','Ash Blossom & Joyous Spring','Droll & Lock Bird','Mulcharmy Fuwalos','Effect Veiler']:
        missing=target-sum(c['qty'] for c in main)
        if not missing:break
        info=card(n);item=next((c for c in main if c['cardId']==info['id']),None)
        old=item['qty'] if item else 0
        add=min(missing,limit(info['id'])-old)
        if add>0:
            if item:item['qty']+=add
            else:main.append({'cardId':info['id'],'name':info['name'],'qty':add})
            changes.append(f'Main: {n} {old} → {old+add}')
    assert sum(c['qty'] for c in main)==target
    used=set(ids(profile['starters']));pool={c['cardId'] for c in main+extra}
    referenced=ids(profile['starters']+profile['end']+[n for _,ns in profile['steps'] for n in ns])
    assert set(referenced)<=pool,(name,'guide references cards outside deck',set(referenced)-pool)
    notes={}
    for text,ns in profile['steps']:
        for n in ns:notes.setdefault(card(n)['id'],text)
    core=[];tech=[]
    for c in main:
        if c['name'] in tech_notes:
            role,note=tech_notes[c['name']];c.update(role=role,note=note);tech.append(c)
        elif c['name'] in generic_tech:
            c['role']='utility';tech.append(c)
        else:
            c['role']='starter' if c['cardId'] in used else 'engine'
            if c['cardId'] in notes:c['note']=notes[c['cardId']]
            core.append(c)
    for c in extra:
        c['role']='boss' if c['cardId'] in ids(profile['end']) else 'utility'
        if c['cardId'] in notes:c['note']=notes[c['cardId']]
    sample_date=re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December) (\d+)(?:st|nd|rd|th), (\d{4})',source['sample'])
    assert sample_date,(name,'no evidence date')
    month=datetime.datetime.strptime(sample_date[1],'%B').month
    evidence_date=f'{sample_date[3]}-{month:02}-{int(sample_date[2]):02}'
    assert '2026-06-01'<=evidence_date<=DATE
    evidence=source['sample'].split(' — '+sample_date[0])[0]
    source_note=f'MDM: {evidence}, {evidence_date}. Có kết quả ladder/giải; không mặc định thuộc Tier List hiện tại.'
    if name=='Mitsurugi Orcust':source_note=f'MDM: {evidence}, {evidence_date}; có trong nhóm power 1.0 lúc đối chiếu Tier List. Không quy đổi thành tier 1.'
    sources=[{'title':f'Master Duel Meta — {name} Deck Breakdown','url':source['url'],'accessed':DATE,'usage':'decklist-and-results'},
             {'title':'YGOPRODeck API v7 — card effects and passcodes','url':'https://db.ygoprodeck.com/api/v7/cardinfo.php','accessed':DATE,'usage':'fact-check'}]
    record={'id':deck_id,'name':name,'contentLanguage':'vi','aliases':list(dict.fromkeys([name,'Bài '+name])),
            'format':'master-duel','archetypes':[name], 'featuredRank':rank,'playstyleTags':profile['tags'],'difficulty':profile['difficulty'],
            'meta':{'tier':'rogue','asOf':DATE,'source':'editorial','note':source_note},'updatedAt':DATE,
            'banlist':{'version':'MD-2026-09-03','effectiveDate':'2026-09-03','verifiedOn':DATE,'pendingVersionReviewed':'MD-2026-10-06'},
            'contentStatus':'in-review','coreCards':core,'techCards':tech,'extraDeck':extra,'sources':sources}
    def action(text):
        for prefix,value in [('Normal Summon','normal-summon'),('Special Summon','special-summon'),('Synchro ','synchro-summon'),('Xyz ','xyz-summon'),('Link ','link-summon'),('Úp ','set')]:
            if text.startswith(prefix):return value
        return 'activate-effect'
    steps=[{'order':i,'text':text,'cardIds':ids(ns),'action':action(text)} for i,(text,ns) in enumerate(profile['steps'],1)]
    main_ids={c['cardId'] for c in main};extra_ids={c['cardId'] for c in extra}
    main_size=sum(c['qty'] for c in main);extra_size=sum(c['qty'] for c in extra)
    adaptation=f'Decklist tham chiếu MDM: {evidence} ngày {evidence_date}; bản biên tập {main_size} Main / {extra_size} Extra.'
    if changes:adaptation+=' Slot đã điều chỉnh theo hai snapshot banlist: '+'; '.join(changes)+'.'
    guide={'deckId':deck_id,'reviewStatus':'ai_draft','summary':profile['overview'],
           'playstyle':{'overview':profile['overview'],'goingFirst':profile['first'],'goingSecond':profile['second'],'tips':[profile['tip'],adaptation]},
           'strengths':[profile['strength']],'weaknesses':[profile['weakness']],
           'counters':[{'cardId':card('Ash Blossom & Joyous Spring')['id'],'note':profile['weakness']+' Ash chỉ áp dụng khi hiệu ứng được kích hoạt có thao tác Deck thuộc điều kiện của nó.'}],
           'combos':[{'id':deck_id+'-opening','title':'Mở engine: '+profile['starters'][0], 'turn':profile['turn'],'difficulty':profile['difficulty'],
                      'illustrative':True,'summary':'Line mở engine; các điều kiện trên sân và cost bổ sung được ghi trong từng bước.',
                      'starterCardIds':ids(profile['starters']),'extraHandCardsNeeded':profile['hand'],
                      'deckCardIds':list(dict.fromkeys(i for step in steps for i in step['cardIds'] if i in main_ids and i not in used)),
                      'extraDeckCardIds':list(dict.fromkeys(i for step in steps for i in step['cardIds'] if i in extra_ids)),
                      'steps':steps,'endBoard':{'cardIds':ids(profile['end']),'graveyardCardIds':[],'text':profile['board'],'interruptions':[]},
                      'chokePoints':[{'atStep':1,'cardIds':[],'text':profile['weakness']}]}],
           'author':{'name':'MD Guide','role':'Biên soạn tiếng Việt; đối chiếu decklist Master Duel Meta'},'reviewers':[]}
    records.append({'deck':record,'guide':guide,'source':source,'date':evidence_date,'result':evidence,'changes':changes,'sizes':[main_size,extra_size]})
assert len({r['deck']['id'] for r in records})==65
decks['decks']=original_decks+[r['deck'] for r in records]
guides['guides']=original_guides+[r['guide'] for r in records]
for data in [decks,guides,ban,manifest]:data['dataVersion']=VERSION
manifest['generatedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')
for s in manifest['sources']:
    if s['name']=='Master Duel Meta':s['note']='65 added decklists and ladder/tournament results checked on 2026-10-04, with per-deck URLs. Vietnamese guidance authored independently; editorial banlist adaptations disclosed.'
for key,data in [('decks',decks),('guides',guides),('banlist',ban)]:
    path=ROOT/manifest['files'][key]['url'];write(path,data);raw=path.read_bytes()
    manifest['files'][key].update(sha256=hashlib.sha256(raw).hexdigest(),size=len(raw))
write(ROOT/'manifest.json',manifest)
report=['# Đối chiếu 65 deck bổ sung — 04/10/2026','',
 'Nguồn lựa chọn: Master Duel Meta, mục Deck Breakdown/Sample Deck. Chỉ nhận deck có kết quả giải hoặc Master rank/Rating Duels/Win Streak/WCS DLv. Max từ tháng 06–10/2026. Loại các mẫu quá cũ và không thêm deck chỉ vì có tên archetype. Có cả lựa chọn rogue đã có kết quả; không tuyên bố cả 100 deck thuộc tier hiện tại.', '',
 '35 deck và 35 guide ban đầu được giữ nguyên nội dung. Thêm 65 decklist có cardId/qty thực và 65 guide tiếng Việt gồm lối chơi, ưu/nhược điểm, cost, điều kiện và line mở engine. Guide mới giữ `ai_draft` / deck `in-review`; thành tích được ghi theo mẫu cụ thể, không phải tỷ lệ thắng hay tier tự suy diễn.', '',
 'Bản biên tập kiểm tra giới hạn số bản theo cả MD-2026-09-03 và MD-2026-10-06 trong banlist của feed. Những slot không hợp lệ được giảm/xóa, Main được bổ sung hand trap; Extra có thể còn 14 lá, vẫn hợp lệ. Mọi khác biệt so với mẫu nguồn được liệt kê bên dưới.', '',
 'Tên Maliss có/không có dấu `<P>/<C>/<Q>` được chuẩn hóa qua passcode. El Shaddoll Meshachrer trên MDM khớp hiệu ứng/Type/Level với El Shaddoll Meshahrail của YGOPRODeck, passcode 32467459.', '',
 '| # | Deck | Thành tích mẫu | Ngày mẫu | Main / Extra | Nguồn MDM |','|---|---|---|---|---|---|']
for i,r in enumerate(records,36):report.append(f"| {i} | {r['deck']['name']} | {r['result']} | {r['date']} | {r['sizes'][0]} / {r['sizes'][1]} | [Đối chiếu]({r['source']['url']}) |")
report+=['','## Điều chỉnh decklist','']
for r in records:
    if r['changes']:report.append('- **'+r['deck']['name']+'**: '+'; '.join(r['changes'])+'.')
(ROOT/'SOURCES-100-DECKS.md').write_text('\n'.join(report)+'\n',encoding='utf-8',newline='\n')
print(f'Built {len(decks["decks"])} decks / {len(guides["guides"])} guides, dataVersion={VERSION}; {len(records)} new records.')
