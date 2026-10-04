"""Validate feed integrity, card identities, banlist limits and original records."""
import hashlib,json,pathlib,subprocess,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path(__file__).resolve().parent;ROOT=R.parent
def read(n):return json.loads((ROOT/n).read_text(encoding='utf-8-sig'))
decks=read('decks.json');guides=read('guides.json');ban=read('banlist.json');m=read('manifest.json')
assert len(decks['decks'])==len(guides['guides'])==100
assert {x['dataVersion'] for x in [decks,guides,ban,m]}=={4}
deck_ids=[d['id'] for d in decks['decks']];guide_ids=[g['deckId'] for g in guides['guides']]
assert len(set(deck_ids))==100 and set(deck_ids)==set(guide_ids) and len(set(guide_ids))==100
assert [d['featuredRank'] for d in decks['decks']]==list(range(1,101))
for key,entry in m['files'].items():
    b=(ROOT/entry['url']).read_bytes()
    assert len(b)==entry['size'] and hashlib.sha256(b).hexdigest()==entry['sha256'],key
carddb=json.loads((R/'cardinfo.json').read_text(encoding='utf-8'))['data'];lookup={c['id']:c for c in carddb}
limits=[{e['cardId']:{'forbidden':0,'limited':1,'semi-limited':2,'unlimited':3}[e['status']] for e in l['entries']} for l in ban['lists']]
new=decks['decks'][35:];by_id={d['id']:d for d in new}
for d in new:
    assert d['contentStatus']=='in-review' and d['format']=='master-duel' and d['contentLanguage']=='vi'
    assert d['sources'][0]['url'].startswith('https://www.masterduelmeta.com/tier-list/deck-types/')
    main=d['coreCards']+d['techCards'];extra=d['extraDeck'];allcards=main+extra
    assert 40<=sum(c['qty'] for c in main)<=60 and 0<sum(c['qty'] for c in extra)<=15,d['id']
    count=collections.Counter()
    for c in allcards:
        assert isinstance(c['qty'],int) and 1<=c['qty']<=3
        assert c['cardId'] in lookup and lookup[c['cardId']]['name']==c['name'],(d['id'],c['name'])
        is_extra=any(t in lookup[c['cardId']]['type'] for t in ['Fusion','Synchro','XYZ','Link'])
        assert is_extra==(c in extra),(d['id'],c['name'],'wrong zone')
        count[c['cardId']]+=c['qty']
    assert len(allcards)==len(count),(d['id'],'duplicate entry')
    for l in limits:
        assert all(q<=l.get(i,3) for i,q in count.items()),(d['id'],'banlist')
for g in guides['guides'][35:]:
    d=by_id[g['deckId']];pool={c['cardId'] for c in d['coreCards']+d['techCards']+d['extraDeck']}
    assert g['reviewStatus']=='ai_draft' and g['summary'] and g['strengths'] and g['weaknesses']
    assert all(g['playstyle'][k] for k in ['overview','goingFirst','goingSecond','tips'])
    for combo in g['combos']:
        assert combo['starterCardIds'] and len(combo['steps'])>=3
        assert [s['order'] for s in combo['steps']]==list(range(1,len(combo['steps'])+1))
        assert all(s['action'] in {'activate-card','activate-effect','fusion-summon','link-summon','normal-summon','other','ritual-summon','search','set','special-summon','synchro-summon','xyz-summon'} for s in combo['steps'])
        refs=combo['starterCardIds']+combo['deckCardIds']+combo['extraDeckCardIds']+combo['endBoard']['cardIds']
        refs += [i for s in combo['steps'] for i in s['cardIds']]
        assert set(refs)<=pool,(g['deckId'],'missing combo card')
# Compare JSON contents rather than bytes because the new dataVersion rewrites roots.
for fn,key in [('decks.json','decks'),('guides.json','guides')]:
    proc=subprocess.run(['rtk','git','show','HEAD:'+fn],cwd=ROOT,capture_output=True)
    assert proc.returncode==0,proc.stderr
    previous=json.loads(proc.stdout.decode('utf-8-sig'))
    current=read(fn)
    assert current[key][:35]==previous[key][:35],(fn,'original contents changed')
assert ban['lists']==json.loads(subprocess.check_output(['rtk','git','show','HEAD:banlist.json'],cwd=ROOT).decode('utf-8-sig'))['lists']
print('PASS: 100 unique decks / 100 unique guides; 65 additions; original 35+35 unchanged.')
print('PASS: card IDs/names/zones, Main 40–60, Extra ≤15, combined copy limits under both banlists, combo references.')
print('PASS: dataVersion=4 in all four JSON files, manifest SHA-256/size match exact bytes; banlist entries unchanged.')
