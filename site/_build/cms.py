# Sanity'den içerik çeker, görselleri img/cms/ altına indirir ve build.py'nin kullandığı yapıları döndürür.
import os, json, re, ssl, urllib.request, urllib.parse, concurrent.futures as cf
try:
    import certifi; _CTX=ssl.create_default_context(cafile=certifi.where())
except Exception: _CTX=ssl.create_default_context()
def _get(u):
    with urllib.request.urlopen(u,timeout=90,context=_CTX) as r: return r.read()
CONF=os.path.join(os.path.dirname(os.path.abspath(__file__)),"sanity.json")
Q='''{
 "series":*[_type=="series" && !(_id in path("drafts.**")) && hidden!=true]|order(order asc){..., "productImages":productImages[]{color,side,set,"u":asset->url,"id":asset->_id},
   "lifestyle":lifestyle[]{color,size,tex,"u":asset->url,"id":asset->_id}, "drawings":drawings[]{"u":asset->url,"id":asset->_id}, "extraLifestyle":extraLifestyle[]{"u":asset->url,"id":asset->_id}},
 "posts":*[_type=="post" && !(_id in path("drafts.**"))]|order(date desc){..., "img":{"u":image.asset->url,"id":image.asset->_id}},
 "settings":*[_id=="settings"][0]{..., "catalogUrl":catalog.asset->url},
 "home":*[_id=="home"][0]{..., "hero":heroSeries->slug.current, "img":{"u":heroImage.asset->url,"id":heroImage.asset->_id}, "imgm":{"u":heroImageMobile.asset->url,"id":heroImageMobile.asset->_id},
   "video":heroVideo.asset->url, "featured":featured[]->slug.current, "spaces":spaces[]{label_tr,label_en,"s":series->slug.current,"u":image.asset->url,"id":image.asset->_id}},
 "about":*[_id=="about"][0]{..., "img":{"u":image.asset->url,"id":image.asset->_id}},
 "faq":*[_id=="faq"][0].items
}'''
def slugify(x): 
    tr=str.maketrans("çğıöşüÇĞİÖŞÜ ","cgiosuCGIOSU-"); return re.sub(r"[^a-z0-9-]","",x.translate(tr).lower())
def load(OUT):
    if not os.path.exists(CONF): return None
    c=json.load(open(CONF)); pid,ds=c["projectId"],c.get("dataset","production")
    url=f"https://{pid}.apicdn.sanity.io/v2024-01-01/data/query/{ds}?query="+urllib.parse.quote(Q)
    data=json.loads(_get(url))["result"]
    os.makedirs(OUT+"/img/cms",exist_ok=True); os.makedirs(OUT+"/video",exist_ok=True); jobs={}
    def local(o,name,folder="img/cms"):
        if not o or not o.get("u"): return None
        ext=os.path.splitext(urllib.parse.urlparse(o["u"]).path)[1] or ".jpg"
        p=f"{folder}/{slugify(name)}-{(o.get('id') or o['u']).split('-')[1][:8] if '-' in (o.get('id') or '') else abs(hash(o['u']))%10**8}{ext}"
        jobs[p]=o["u"]; return p
    SER=[]; LIFE={}
    for s in data["series"]:
        slug=s["slug"]["current"]; N=s["name"]
        sizes=[]
        for z in s.get("sizes") or []:
            sizes.append(("b",z.get("d"),z.get("w"),z.get("h")) if z.get("kind")=="b" else ("r",z.get("d"),z.get("h")))
        prod=[dict(src=local(p,f"mogra-{N}-{p.get('color','')}"+("-yan" if p.get("side") else "")+("-set" if p.get("set") else "")),color=p.get("color",""),side=bool(p.get("side")),set=bool(p.get("set"))) for p in s.get("productImages") or []]
        LIFE[slug]=[dict(color=x.get("color",""),size=x.get("size") or 0,tex=x.get("tex") or "",src=local(x,f"mogra-{N}-{x.get('color','')}-{x.get('size','')}-mekan")) for x in s.get("lifestyle") or []]
        SER.append(dict(slug=slug,name=N,grp=s["group"],tr=dict(form=s.get("form_tr",""),doku=s.get("doku_tr",""),kisa=s.get("kisa_tr","")),
            en=dict(form=s.get("form_en",""),doku=s.get("doku_en",""),kisa=s.get("kisa_en","")),colors=s.get("colors") or [""],prod=prod,
            life=[local(o,f"mogra-{N}-mekan") for o in s.get("extraLifestyle") or []],olcu=[local(o,f"mogra-{N}-olcu") for o in s.get("drawings") or []],
            sizes=sizes,guide=[z.get("guide","") for z in s.get("sizes") or []],t=dict(ozet=s.get("lead_tr",""),desc=s.get("desc_tr") or [],tek=s.get("tek_tr") or [],use=s.get("use_tr") or []),
            xs=[],en_name=s.get("en_name") or N))
    def blocks(bs):
        out=[]
        for b in bs or []:
            t="".join(c.get("text","") for c in b.get("children",[]))
            if b.get("listItem"):
                if out and out[-1][0]=="ul": out[-1][1].append(t)
                else: out.append(("ul",[t]))
            else: out.append(("h" if b.get("style","").startswith("h") else "p",t))
        return out
    POSTS=[dict(slug=p["slug_tr"]["current"],en_slug=(p.get("slug_en") or p["slug_tr"])["current"],date=p.get("date","2026-01-01"),img=local(p["img"],"blog-"+p["slug_tr"]["current"]),
        tr=dict(title=p["title_tr"],desc=p.get("desc_tr",""),lead=p.get("lead_tr",""),body=blocks(p.get("body_tr"))),
        en=dict(title=p.get("title_en") or p["title_tr"],desc=p.get("desc_en") or "",lead=p.get("lead_en") or "",body=blocks(p.get("body_en") or p.get("body_tr")))) for p in data["posts"]]
    st=data.get("settings") or {}; hm=data.get("home") or {}; ab=data.get("about") or {}
    if st.get("catalogUrl"): jobs["katalog/MOGRA_Katalog_2026.pdf"]=st["catalogUrl"]
    vid=None
    if hm.get("video"): vid="video/mogra-hero"+os.path.splitext(hm["video"])[1]; jobs[vid]=hm["video"]
    CFG=dict(settings=st,home=dict(hm,img=local(hm.get("img"),"mogra-hero"),imgm=local(hm.get("imgm"),"mogra-hero-mobil"),video=vid,
             spaces=[dict(sp,img=local(sp,"mogra-mekan-"+(sp.get("label_tr") or ""))) for sp in hm.get("spaces") or []]),
             about=dict(ab,img=local(ab.get("img"),"mogra-hakkimizda")),faq=data.get("faq") or [])
    def dl(item):
        p,u=item; f=os.path.join(OUT,p)
        if p.startswith("img/cms/") and os.path.exists(f) and os.path.getsize(f)>0: return
        os.makedirs(os.path.dirname(f),exist_ok=True); open(f+".part","wb").write(_get(u)); os.replace(f+".part",f)
    with cf.ThreadPoolExecutor(12) as ex: list(ex.map(dl,jobs.items()))
    print("cms:",len(SER),"seri,",len(POSTS),"yazı,",len(jobs),"dosya")
    return SER,LIFE,POSTS,CFG
