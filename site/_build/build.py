import os, json, re, html, glob
from urllib.parse import quote
from series import S, FORMS, SWATCH, COLOR_EN
from blog import POSTS
HOME=os.path.expanduser("~"); OUT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=HOME+"/Downloads/WEB SİTE ÜRÜNLER/Mogra"
import cms as CMSMOD
CMS=CMSMOD.load(OUT)
if not CMS: IM=json.load(open(OUT+"/_work/images.json")); XL=json.load(open(OUT+"/_work/excel.json"))
E=html.escape
WA="905444720903"; PHONE="0544 472 09 03"; PHONE_INT="+90 544 472 09 03"; MAIL="ekrem@serinova.com.tr"
SITE="https://mogra.com.tr"
ADDR_TR="İSTOÇ 15. Ada No:152, Mahmutbey Mah. 2433. Sk.<br>Bağcılar / İstanbul"
ADDR_EN="İSTOÇ Block 15 No:152, Mahmutbey Mah. 2433. Sk.<br>Bağcılar / Istanbul, Türkiye"
TELS=[("0212 659 15 10","+902126591510"),("0212 659 34 14","+902126593414")]
MAP_Q="Serinova Plastik İSTOÇ 15. Ada No:152 Bağcılar İstanbul"
if CMS:
    _st=CMS[3]["settings"]
    WA=_st.get("whatsapp") or WA; PHONE=_st.get("phone") or PHONE; MAIL=_st.get("email") or MAIL
    PHONE_INT="+90 "+PHONE.lstrip("0") if PHONE.startswith("0") else PHONE
    if _st.get("address_tr"): ADDR_TR=_st["address_tr"].strip().replace("\n","<br>")
    if _st.get("address_en"): ADDR_EN=_st["address_en"].strip().replace("\n","<br>")
    if _st.get("landlines"): TELS=[(l,"+90"+"".join(ch for ch in l if ch.isdigit()).lstrip("0")) for l in _st["landlines"]]
    MAP_Q=_st.get("mapQuery") or MAP_Q
import hashlib
ASSET_V=hashlib.md5(open(OUT+"/assets/style.css","rb").read()+open(OUT+"/assets/site.js","rb").read()).hexdigest()[:8]
GA_ID=os.environ.get("GA_ID","G-KYD3L5GE75")
PG={"index":("index.html","index.html"),"kol":("koleksiyon.html","collection.html"),"fib":("fiberclay.html","fiberclay.html"),
    "hak":("hakkimizda.html","about.html"),"mim":("mimari-destek.html","architectural-support.html"),"ilet":("iletisim.html","contact.html"),"sss":("sss.html","faq.html"),
    "mag":("magaza.html","store.html"),"blog":("blog.html","blog.html")}
def path(lang,key=None,slug=None):
    base="" if lang=="tr" else "en/"
    if slug: return base+("seri/" if lang=="tr" else "series/")+slug+".html"
    p=PG[key][0 if lang=="tr" else 1]
    return base+("" if p=="index.html" else p)
def bpath(lang,post): return ("" if lang=="tr" else "en/")+"blog/"+(post["slug"] if lang=="tr" else post["en_slug"])+".html"
def url(lang,key=None,slug=None): return SITE+"/"+path(lang,key,slug)
WA_SVG='<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15l-1.4 5 5.2-1.4A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3.1.8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>'
def lo(x): return x.replace("I","ı").replace("İ","i").lower()
# cümle içi: yalnız ilk harfi küçült; U form, Utah, Texa gibi özel adlar korunur
def lf(x):
    w=x.split(" ",1); keep={"U","Utah","Texa"}
    return x if w[0] in keep else lo(w[0])+(" "+w[1] if len(w)>1 else "")
def en_surf(d):
    s=lf(d); return s if s.endswith(("texture","textures","finish")) else s+" finish"
def an(s): return s if s.endswith("s") else ("an " if s[0].lower() in "aeiou" and not s.startswith("U ") else "a ")+s
def num(x):
    v=float(x); return (f"{v:.1f}".rstrip("0").rstrip(".")).replace(".",",")
def num_en(x):
    v=float(x); return f"{v:.1f}".rstrip("0").rstrip(".")
def txt(slug):
    name={"cigar":"Aura/Cıgar.txt","cana":"Çana/Çana.txt"}.get(slug)
    if not name:
        c=[x for x in glob.glob(f"{SRC}/*/*.txt") if os.path.basename(os.path.dirname(x)).lower().replace("ü","u")==slug]
        name=c[0][len(SRC)+1:] if c else None
    if not name or not os.path.exists(SRC+"/"+name): return {}
    t=open(SRC+"/"+name,encoding="utf-8").read()
    def sec(a,b):
        m=re.search(re.escape(a)+r"\s*\n(.*?)(?=\n"+re.escape(b)+r"|\Z)",t,re.S)
        return [l.strip() for l in m.group(1).split("\n") if l.strip()] if m else []
    return {"ozet":" ".join(sec("Kısa Özet (TR)","Ürün Açıklaması")),"desc":sec("Ürün Açıklaması (TR)","Teknik Özellikler"),
            "tek":sec("Teknik Özellikler (TR)","Kullanım Alanları"),"use":sec("Kullanım Alanları","@@@")}
def sentences(t): return [x.strip() for x in re.split(r"(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ0-9])",t) if x.strip()]
def parse_size(raw,grp):
    s=raw.strip().upper().replace("\n","")
    ns=re.findall(r"\d+(?:[.,]\d+)?",s); ns=[n.replace(",",".") for n in ns]
    rnd = grp!="kare"
    if s.startswith("D") or (rnd and (len(ns)==2 or (len(ns)==3 and ns[0]==ns[1]))):
        d,h=(ns[0],ns[-1]); return ("r",d,h)
    if len(ns)==3: return ("b",ns[0],ns[1],ns[2])
    return ("r",ns[0],ns[-1])
def fmt_size(t,lang):
    f=num if lang=="tr" else num_en
    return f"Ø {f(t[1])} × {f(t[2])}" if t[0]=="r" else f"{f(t[1])} × {f(t[2])} × {f(t[3])}"

ORD=["Bej","Kum","Vizon","Gri","Granit Gri","Kurşun Gri","Grafit","Antrasit","Siyah"]
if not CMS:
    SER=[]
    for slug,name,grp,tr,en,xk in S:
        d=IM[slug]; x=XL.get(xk,{"desc":[],"sizes":[],"en":[]})
        colors=[]
        for p in d["product"]:
            if p["color"] not in colors: colors.append(p["color"])
        colors.sort(key=lambda c:ORD.index(c) if c in ORD else 99)
        prod=sorted(d["product"],key=lambda p:(p["set"],p["side"],colors.index(p["color"])))
        # Excel'den ölçüler + boy cümleleri (ilk görüldüğü sırayla, tekil)
        sizes=[];guide=[];seen=set()
        for raw,ds in zip(x["sizes"],x["desc"]+[""]*len(x["sizes"])):
            t=parse_size(raw,grp); k=t[1:]
            if k in seen: continue
            seen.add(k); sizes.append(t)
            g=[s for s in sentences(ds) if "ölçüsündeki" in s]
            guide.append(g[0] if g else "")
        order=sorted(range(len(sizes)),key=lambda i:(float(sizes[i][-1]),float(sizes[i][1])))
        sizes=[sizes[i] for i in order]; guide=[guide[i] for i in order]
        if not sizes: sizes=[("r",str(a),str(b)) for a,b in d["sizes"]]; guide=[""]*len(sizes)
        xs=sentences(x["desc"][0]) if x["desc"] else []
        en_name=re.sub(r"\b(Beige|Graphite|Desert|Black|Grey|Gray|Sand|Mink|S\d)\b","",(x["en"] or [""])[0],flags=re.I)
        en_name=re.sub(r"\s+"," ",en_name.replace("ClayFibre","Clayfibre").replace("Clay Fiber","Clayfibre")).strip(" /")
        SER.append(dict(slug=slug,name=name,grp=grp,tr=dict(zip(("form","doku","kisa"),tr)),en=dict(zip(("form","doku","kisa"),en)),
            colors=colors,prod=prod,life=d["life"],olcu=d["olcu"],sizes=sizes,guide=guide,t=txt(slug),xs=xs,en_name=en_name))
    BY={s["slug"]:s for s in SER}
    LIFE={}
    _jobs={j["index"]:j for j in json.load(open(OUT+"/_work/jobs.json"))}
    _done=json.load(open(OUT+"/_work/life_done.json")) if os.path.exists(OUT+"/_work/life_done.json") else {}
    for _k,_o in sorted(_done.items(),key=lambda kv:int(kv[0])):
        _j=_jobs[int(_k)]
        if os.path.exists(OUT+"/"+_o): LIFE.setdefault(_j["slug"],[]).append(dict(color=_j["color"],size=_j["size"],src=_o,tex=("Texa" if "texa" in _j["key"] else "Utah" if "utah" in _j["key"] else "")))
else:
    SER,LIFE,POSTS=CMS[0],CMS[1],CMS[2]
    BY={x["slug"]:x for x in SER}
for _s in SER:
    L=LIFE.get(_s["slug"],[])
    if L: _s["hero"]=([x for x in L if x["color"]==_s["colors"][0]] or L)[min(len(L)-1,len([x for x in L if x["color"]==_s["colors"][0]])//2)]["src"]
def hrange(s,lang):
    h=[float(t[-1]) for t in s["sizes"]]; f=num if lang=="tr" else num_en
    n=len(h); w="boy" if lang=="tr" else ("sizes" if n>1 else "size")
    return f"{n} {w} · {f(min(h))}–{f(max(h))} cm" if n>1 else f"{f(h[0])} cm"
def cname(c,lang): return c if lang=="tr" else COLOR_EN.get(c,c)
def swatches(s,lang): return '<span class="swatches">'+"".join(f'<i class="sw" style="background:{SWATCH.get(c,"#ccc")}" title="{E(cname(c,lang))}"></i>' for c in s["colors"])+'</span>'
for s in SER: s["en_name"]=re.sub(r"\s*/\s*"," / ",s["en_name"]).replace("Tropic / Utah","Tropic Utah")
T={"tr":dict(top="Mimari projeler ve toptan siparişler için özel fiyatlandırma",top_a="Teklif alın",kol="Koleksiyonlar",mek="Mekânlar",fib="Fiberclay",hak="Hakkımızda",
      mim="Mimari Destek",kat="Katalog",ilet="İletişim",all="Tüm seriler →",mega_p="{n} seri, fiberclay. İç ve dış mekân için.",
      foot="MOGRA, Serinova'nın fiberclay saksı markasıdır. 1986'dan bu yana İstanbul'da üretim yapan Serinova'nın deneyimiyle mimari projeler, oteller ve yaşam alanları için tasarlanır.",
      f_kur="Kurumsal",f_pop="Popüler Seriler",f_all="Tüm Seriler",f_mat="Fiberclay Malzeme",f_kat="Katalog 2026",wa="WhatsApp ile yazın",open="Menüyü aç",close="Menüyü kapat",
      seri_w="seri",mag="Mağaza",blog="Blog",shop="Online Mağaza",lang_other="EN",lang_other_name="English"),
   "en":dict(top="Project pricing for architects, hospitality and trade orders",top_a="Request a quote",kol="Collections",mek="Spaces",fib="Fiberclay",hak="About",
      mim="Architectural Support",kat="Catalogue",ilet="Contact",all="All series →",mega_p="{n} fiberclay series for indoor and outdoor use.",
      foot="MOGRA is the fiberclay planter brand of Serinova, a manufacturer producing in Istanbul since 1986. Designed for architectural projects, hotels and living spaces.",
      f_kur="Company",f_pop="Popular Series",f_all="All Series",f_mat="Fiberclay Material",f_kat="Catalogue 2026",wa="Message us on WhatsApp",open="Open menu",close="Close menu",
      seri_w="series",mag="Store",blog="Blog",shop="Online Shop",lang_other="TR",lang_other_name="Türkçe")}
if CMS:
    for _l in ("tr","en"):
        if _st.get("topbar_"+_l): T[_l]["top"]=_st["topbar_"+_l]
        if _st.get("footer_"+_l): T[_l]["foot"]=_st["footer_"+_l]
ORG={"@context":"https://schema.org","@type":"Organization","name":"MOGRA","alternateName":"MOGRA Home & Garden","url":SITE+"/","logo":SITE+"/img/brand/mogra-mark.png",
     "telephone":PHONE_INT,"email":MAIL,"address":{"@type":"PostalAddress","streetAddress":"İSTOÇ 15. Ada No:152, Mahmutbey Mah. 2433. Sk.","addressLocality":"Bağcılar","addressRegion":"İstanbul","addressCountry":"TR"},
     "parentOrganization":{"@type":"Organization","name":"Serinova Plastik","foundingDate":"1986","url":"https://www.serinovashop.com"},"sameAs":["https://www.serinovashop.com"]}
def ld(o): return '<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False)+'</script>'
def crumbs(lang,items): return ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(items)]})
def stock_msg(s,lang): return f"Merhaba, {s['name']} serisinin stok durumunu öğrenebilir miyim?" if lang=="tr" else f"Hello, could you tell me the stock status of the {s['name']} series?"
def card(s,lang,pre):
    im=s["prod"][0]["src"] if s["prod"] else s["life"][0]
    al=s.get("hero") or (s["life"][0] if s["life"] else None)
    alt=f'<img class="alt" src="{pre}{al}" alt="" loading="lazy">' if al else ""
    L=s[lang]; nm=lo(s["name"])
    return (f'<a class="p-card" href="{pre}{path(lang,slug=s["slug"])}" data-form="{s["grp"]}" data-colors="{"|".join(s["colors"])}" data-name="{E(nm)} {E(lo(L["form"]))} {E(lo(L["doku"]))}">'
            f'<div class="p-img"><img src="{pre}{im}" alt="MOGRA {E(s["name"])} {"fiberclay saksı" if lang=="tr" else "fiberclay planter"}" loading="lazy">{alt}</div>'
            f'<div class="p-meta"><h3>{E(s["name"])}</h3>{swatches(s,lang)}</div><p class="p-sub">{E(L["form"])} · {E(hrange(s,lang))}</p><span class="stock-btn" role="button" tabindex="0" data-wa="{E(stock_msg(s,lang))}">{"Stok için sorun" if lang=="tr" else "Ask about stock"}</span></a>')

def layout(lang,me,other,title,desc,body,hero=False,cur="",og="img/hero/mogra-ana-ekran-lifestyle-gorseli.jpg",head=""):
    t=T[lang]; pre="../"*me.count("/")
    P=lambda k=None,slug=None: (pre+path(lang,k,slug)) or "./"
    tr_url=SITE+"/"+(me if lang=="tr" else other); en_url=SITE+"/"+(other if lang=="tr" else me)
    clean=lambda u:u.replace("/index.html","/")
    tr_url,en_url=clean(tr_url),clean(en_url)
    groups="".join(f'<div><h5>{E(FORMS[g][lang][0])}</h5><ul>'+"".join(f'<li><a href="{P(slug=s["slug"])}"><img src="{pre}{s["prod"][0]["src"]}" alt="" loading="lazy">{E(s["name"])}</a></li>' for s in SER if s["grp"]==g)+'</ul></div>' for g in FORMS)
    dser="".join(f'<a href="{P(slug=s["slug"])}">{E(s["name"])}</a>' for s in SER)
    ac=lambda k:' aria-current="page"' if cur==k else ""
    kat=pre+"katalog/MOGRA_Katalog_2026.pdf"
    other_href=(pre+other) or "./"
    ga=(f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("consent","default",{{ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied",analytics_storage:(function(){{try{{return localStorage.getItem("mogra-consent")==="yes"?"granted":"denied"}}catch(e){{return "denied"}}}})()}});gtag("js",new Date());gtag("config","{GA_ID}");</script>') if GA_ID else ""
    canon=tr_url if lang=="tr" else en_url
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}"><link rel="alternate" hreflang="tr" href="{tr_url}"><link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="x-default" href="{tr_url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="MOGRA"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/{og}"><meta property="og:locale" content="{"tr_TR" if lang=="tr" else "en_US"}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#C97C5F"><link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="192x192" href="{pre}img/brand/favicon-192.png"><link rel="apple-touch-icon" href="{pre}img/brand/favicon-192.png">
<link rel="preload" href="{pre}fonts/Nexa-XBold.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{pre}assets/style.css?v={ASSET_V}">{head}{ga}
</head><body class="{"has-hero" if hero else ""}">
<div class="topbar">{t["top"]} · <a href="{P("mim")}">{t["top_a"]}</a></div>
<header class="hdr"><div class="hdr-in">
<nav class="nav nav-l" aria-label="Menü"><button type="button" data-mega aria-expanded="false"{ac("kol")}>{t["kol"]}</button><a href="{P("index")}#mekanlar">{t["mek"]}</a><a href="{P("fib")}"{ac("fib")}>{t["fib"]}</a><a href="{P("hak")}"{ac("hak")}>{t["hak"]}</a></nav>
<button class="burger" type="button" data-drawer aria-label="{t["open"]}"><span></span></button>
<a class="logo-wrap" href="{P("index") or "./"}" aria-label="MOGRA"><img class="mark" src="{pre}img/brand/mogra-mark.png" alt="mogra." width="54" height="51"></a>
<nav class="nav nav-r" aria-label="{t["ilet"]}"><a class="hide-m" href="{P("mim")}"{ac("mim")}>{t["mim"]}</a><a class="hide-m" href="{kat}" target="_blank" rel="noopener">{t["kat"]}</a><a class="hide-m" href="{P("ilet")}"{ac("ilet")}>{t["ilet"]}</a><a href="{other_href}" hreflang="{"en" if lang=="tr" else "tr"}" lang="{"en" if lang=="tr" else "tr"}" title="{t["lang_other_name"]}">{t["lang_other"]}</a><a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}</a><a class="hide-m nav-shop" href="https://www.serinovashop.com" target="_blank" rel="noopener">{t["shop"]}</a></nav>
</div>
<div class="mega" hidden><div class="mega-in"><div class="mega-side"><h4>{t["kol"]}</h4><p>{t["mega_p"].format(n=len(SER))}</p><a class="link-arrow" href="{P("kol")}">{t["all"]}</a></div><div class="mega-groups">{groups}</div></div></div>
</header>
<div class="drawer" hidden><div class="drawer-top"><img class="mark" src="{pre}img/brand/mogra-mark.png" alt="mogra."><button class="close-x" type="button" data-drawer aria-label="{t["close"]}">×</button></div>
<nav><a href="{P("kol")}">{t["kol"]}</a><div class="series">{dser}</div><a href="{P("index")}#mekanlar" data-drawer>{t["mek"]}</a><a href="{P("fib")}">{t["fib"]}</a><a href="{P("hak")}">{t["hak"]}</a><a href="{P("mim")}">{t["mim"]}</a><a href="{P("mag")}">{t["mag"]}</a><a href="{P("blog")}">{t["blog"]}</a><a href="{kat}">{t["kat"]}</a><a href="{P("ilet")}">{t["ilet"]}</a><a href="https://www.serinovashop.com" target="_blank" rel="noopener">{t["shop"]}</a><a href="{other_href}">{t["lang_other_name"]}</a></nav></div>
<main>{body}</main>
<footer class="ftr"><div class="wrap"><div class="ftr-top">
<div class="ftr-brand"><img src="{pre}img/brand/mogra-mark.png" alt="mogra." loading="lazy"><p>{t["foot"]}</p></div>
<div><h5>{t["kol"]}</h5><ul>{"".join(f'<li><a href="{P("kol")}#{g}">{E(FORMS[g][lang][0])}</a></li>' for g in FORMS)}<li><a href="{P("kol")}">{t["f_all"]}</a></li></ul></div>
<div><h5>{t["f_kur"]}</h5><ul><li><a href="{P("hak")}">{t["hak"]}</a></li><li><a href="{P("fib")}">{t["f_mat"]}</a></li><li><a href="{P("mim")}">{t["mim"]}</a></li><li><a href="{P("mag")}">{t["mag"]}</a></li><li><a href="{P("blog")}">{t["blog"]}</a></li><li><a href="{P("sss")}">{"SSS" if lang=="tr" else "FAQ"}</a></li><li><a href="{kat}">{t["f_kat"]}</a></li><li><a href="https://www.serinovashop.com" target="_blank" rel="noopener">{t["shop"]} · serinovashop.com</a></li></ul></div>
<div><h5>{t["f_pop"]}</h5><ul>{"".join(f'<li><a href="{P(slug=k)}">{BY[k]["name"]}</a></li>' for k in ["titan","oval","orion","kale","uranium"])}</ul></div>
<div><h5>{t["ilet"]}</h5><ul><li><a href="tel:+905444720903">{PHONE if lang=="tr" else PHONE_INT}</a></li><li><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="{P("mag")}">{ADDR_TR if lang=="tr" else ADDR_EN}</a></li></ul></div>
</div><div class="ftr-bot"><span>© <span id="yil">2026</span> MOGRA Home &amp; Garden · Serinova</span><span><a href="{other_href}">{t["lang_other_name"]}</a> · <a href="https://www.serinovashop.com" target="_blank" rel="noopener">serinovashop.com</a></span></div></div></footer>
<a class="wa-float" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="{t["wa"]}">{WA_SVG}</a>
<div class="consent" id="consent" hidden><p>{"Sitemizi geliştirmek için analiz çerezleri kullanıyoruz." if lang=="tr" else "We use analytics cookies to improve this site."}</p><div><button type="button" class="btn btn-fill" data-consent="yes">{"Kabul et" if lang=="tr" else "Accept"}</button><button type="button" class="btn btn-line" data-consent="no">{"Reddet" if lang=="tr" else "Decline"}</button></div></div>
<script src="{pre}assets/site.js?v={ASSET_V}" defer></script></body></html>'''

def ic(p): return f'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">{p}</svg>'
ICONS=[ic('<path d="M6 22h20M9 22l2-10h10l2 10M13 12V8h6v4"/>'),ic('<path d="M16 4v24M6 10l20 12M26 10L6 22"/>'),
       ic('<circle cx="16" cy="16" r="5"/><path d="M16 3v4M16 25v4M3 16h4M25 16h4M6.8 6.8l2.8 2.8M22.4 22.4l2.8 2.8M6.8 25.2l2.8-2.8M22.4 9.6l2.8-2.8"/>'),
       ic('<path d="M5 26h22M8 26V12l8-6 8 6v14M13 26v-7h6v7"/>')]
FEATS={"tr":[("Hafif","Kil ve cam elyafı karışımı, aynı ölçüdeki beton ve taş saksılardan çok daha hafiftir. Taşıması ve yerleştirmesi kolaydır."),
             ("Dona dayanıklı","Dış mekânda kış koşullarına göre üretilir; ısı değişimlerinde formunu korur."),
             ("UV dayanımı","Güneş altında rengini ve doku derinliğini uzun süre korur."),
             ("İç ve dış mekân","Salondan otel terasına aynı seriyle tutarlı bir mekân dili kurulur.")],
       "en":[("Lightweight","A blend of clay and glass fibre, far lighter than concrete or stone planters of the same size. Easy to move and place."),
             ("Frost resistant","Made for outdoor winters; it keeps its form through temperature changes."),
             ("UV resistant","Holds its colour and texture depth under the sun for years."),
             ("Indoor and outdoor","One series can carry a consistent look from living room to hotel terrace.")]}
VID={"titan":"video/mogra-titan-film.mp4"} if os.path.exists(OUT+"/video/mogra-titan-film.mp4") else {}
HM=CMS[3]["home"] if CMS else None
if HM: VID={HM.get("hero") or "titan":HM["video"]} if HM.get("video") else {}
def index(lang):
    me=path(lang,"index"); other=path("en" if lang=="tr" else "tr","index"); pre="../"*me.count("/")
    tr=lang=="tr"; P=lambda k=None,slug=None:(pre+path(lang,k,slug)) or "./"
    slides=[("img/hero/titan-film-poster.jpg" if VID else "img/titan/life/titan-bej-8.jpg","img/hero/mogra-ana-ekran-lifestyle-gorseli.jpg","titan",
             ("Mekâna ölçek veren form.","Titan: 30 cm'den 112 cm'ye dokuz boy. Zeytin ağacından fikus'a, büyük bitkiler için fiberclay gövde.") if tr else ("Form that gives a space its scale.","Titan: nine sizes from 30 to 112 cm. A fiberclay body for olive trees, ficus and other large plants."))]
    if HM: slides=[(HM.get("img") or slides[0][0],HM.get("imgm") or slides[0][1],HM.get("hero") if HM.get("hero") in BY else "titan",(HM.get("heroTitle_"+lang) or slides[0][3][0],HM.get("heroText_"+lang) or slides[0][3][1]))]
    sl=""
    for i,(d,m,k,(h,p)) in enumerate(slides):
        src=f'<source media="(max-width:700px)" srcset="{pre}{m}">' if m else ""
        tag="h1" if i==0 else "h2"
        cap=f'<div class="hero-cap"><div class="wrap"><span class="eyebrow" style="color:#fff">MOGRA · {BY[k]["name"]} {"Serisi" if tr else "Series"}</span><{tag}>{h}</{tag}><p>{p}</p><div class="row"><a class="btn btn-fill" href="{P(slug=k)}">{"Seriyi incele" if tr else "View the series"}</a><a class="btn btn-light" href="{P("kol")}">{"Tüm koleksiyon" if tr else "Full collection"}</a></div></div></div>'
        vid=VID.get(k); vtag=f'<video class="hero-vid" muted playsinline loop preload="none" aria-hidden="true" data-src="{pre}{vid}"></video>' if vid else ""
        sl+=f'<div class="slide{" on" if i==0 else ""}"><picture>{src}<img src="{pre}{d}" alt="MOGRA {BY[k]["name"]}" {"fetchpriority=\"high\"" if i==0 else "loading=\"lazy\""}></picture>{vtag}{cap}</div>'
    forms="".join(f'<a class="form-card" href="{P("kol")}#{g}"><span class="n">{sum(1 for s in SER if s["grp"]==g)} {T[lang]["seri_w"]}</span><img src="{pre}{BY[k]["prod"][0]["src"]}" alt="" loading="lazy"><div class="c"><h3>{E(FORMS[g][lang][0])}</h3><span>→</span></div></a>' for g,k in [("yuvarlak","oval"),("kare","atlas"),("yuksek","orion"),("canak","cana")])
    def story(k,eb,title,text,thumbs,img,rev=False):
        th="".join(f'<a href="{P(slug=t)}" aria-label="{BY[t]["name"]}"><img src="{pre}{BY[t]["prod"][0]["src"]}" alt="MOGRA {BY[t]["name"]}" loading="lazy"></a>' for t in thumbs)
        return f'<section class="story{" rev" if rev else ""}"><div class="story-img"><img src="{pre}{img}" alt="MOGRA {BY[k]["name"]}" loading="lazy"></div><div class="story-txt"><span class="eyebrow">{eb}</span><h2>{title}</h2><p>{text}</p><div class="story-thumbs">{th}</div><a class="link-arrow" href="{P(slug=k)}">{"Seriyi keşfet →" if tr else "Explore the series →"}</a></div></section>'
    feat=[k for k in (HM.get("featured") or []) if k in BY] if HM else []
    rail="".join(card(BY[k],lang,pre) for k in (feat or [k for k in ["titan","oval","terra","kale","orion","lina","uranium","pera","sade","cana","astra","zenit"] if k in BY]))
    sp=[("oval","img/oval/life/oval-bej-4.jpg","Otel Lobisi","Hotel Lobby"),("titan","img/titan/life/titan-kursun-gri-6.jpg","Teras","Terrace"),("cigar","img/cigar/life/cigar-bej-2.jpg","Spa","Spa"),("lina","img/lina/life/lina-bej-2.jpg","Villa Terası","Villa Terrace"),("blok","img/blok/life/blok-bej-2.jpg","Havuz Başı","Poolside"),("zenit","img/zenit/life/zenit-bej-1.jpg","Restoran","Restaurant")]
    if HM and HM.get("spaces"): sp=[(x.get("s"),x["img"],x.get("label_tr",""),x.get("label_en") or x.get("label_tr","")) for x in HM["spaces"] if x.get("img") and x.get("s") in BY]
    spaces="".join(f'<a href="{P(slug=k)}"><img src="{pre}{i}" alt="MOGRA {BY[k]["name"]} — {a if tr else b}" loading="lazy"><span>{a if tr else b} · {BY[k]["name"]}</span></a>' for k,i,a,b in sp)
    nsize=sum(len(s["sizes"])*max(1,len(s["colors"])) for s in SER)
    fe="".join(f'<div>{ICONS[i]}<h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate(FEATS[lang]))
    X=(lambda a,b:a) if tr else (lambda a,b:b)
    dots=('<div class="hero-dots">'+"".join(f'<button type="button" aria-label="{i+1}"{" class=on" if i==0 else ""}></button>' for i in range(len(slides)))+'</div>') if len(slides)>1 else ""
    kat_band=f'<section class="sec stone kat-band"><div class="wrap kat-in"><div><span class="eyebrow">{X("Katalog 2026","Catalogue 2026")}</span><h2>{X("Tüm seriler, ölçüler ve renkler tek dosyada.","Every series, size and colour in one file.")}</h2><p>{X("Teknik çizimler ve ölçü tablolarıyla MOGRA 2026 kataloğunu PDF olarak indirin.","Download the MOGRA 2026 catalogue as a PDF, with drawings and size tables.")}</p></div><a class="btn btn-fill" href="{pre}katalog/MOGRA_Katalog_2026.pdf" download>{X("Katalog indir (PDF)","Download catalogue (PDF)")}</a></div></section>'
    body=f'''<section class="hero" aria-label="MOGRA">{sl}
{dots}</section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Formlar","Forms")}</span><h2>{X("Mekânınıza göre bir form seçin.","Choose a form for your space.")}</h2></div><p>{X(f"{len(SER)} seri dört form ailesinde toplanır. Her seri birden fazla boy ve renkle gelir.",f"{len(SER)} series in four form families, each in several sizes and colours.")}</p></div><div class="forms">{forms}</div></div></section>
{story("titan",X("Koleksiyon · Titan","Collection · Titan"),X("Büyük bitkiler için mimari ölçek.","Architectural scale for large plants."),E(BY["titan"][lang]["kisa"])+X(" Bej ve kurşun gri iki renk."," In beige and lead grey."),["sade","pera","nadir"],"img/titan/titan-lifestyle.jpg")}
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Öne çıkanlar","Featured")}</span><h2>{X("Seriler","Series")}</h2></div><div class="rail-nav" data-rail="rail1"><button type="button" data-dir="-1" aria-label="←">←</button><button type="button" data-dir="1" aria-label="→">→</button></div></div><div class="rail" id="rail1">{rail}</div><p style="margin-top:28px"><a class="link-arrow" href="{P("kol")}">{X(f"Tüm {len(SER)} seriyi gör →",f"See all {len(SER)} series →")}</a></p></div></section>
{kat_band}
{story("kale",X("Doku","Texture"),X("Taş, tuğla, volkan. Yüzeyde karakter.","Stone, brick, volcano. Character in the surface."),X("Kale'nin tuğla dokusu, Terra'nın Utah yüzeyi, Çana'nın volkan dokusu. Fiberclay, doğal taşın görünümünü hafif ve dayanıklı bir gövdede verir.","Kale's brick texture, Terra's Utah surface, Çana's volcano finish. Fiberclay gives the look of natural stone in a light, durable body."),["terra","cana","merkur"],"img/kale/kale-lifestyle2.jpg",True)}
<section class="sec" id="mekanlar"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Mekânlar","Spaces")}</span><h2>{X("MOGRA mekânda.","MOGRA in place.")}</h2></div><p>{X("Otel lobisinden ev salonuna, restoran terasından ofis girişine.","From hotel lobbies to living rooms, restaurant terraces to office entrances.")}</p></div><div class="spaces">{spaces}</div></div></section>
<section class="sec stone"><div class="wrap material"><div><span class="eyebrow">{X("Malzeme","Material")}</span><h2>{X("Neden fiberclay?","Why fiberclay?")}</h2><p>{X("Fiberclay, kil ile cam elyafının birleşiminden oluşan kompozit bir malzemedir. Toprak ve taş saksıların görünümünü taşır, onlardan çok daha hafiftir ve dış mekân koşullarına dayanır.","Fiberclay is a composite of clay and glass fibre. It has the look of terracotta and stone planters, weighs far less and stands up to outdoor conditions.")}</p><p style="margin-top:24px"><a class="link-arrow" href="{P("fib")}">{X("Malzemeyi tanıyın →","About the material →")}</a></p></div><div class="feats">{fe}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Sayılarla","In numbers")}</span><h2>{X("MOGRA ve Serinova","MOGRA and Serinova")}</h2></div></div><div class="numbers"><div><b>1986</b><span>{X("Serinova'nın İstanbul'da üretime başladığı yıl","The year Serinova began manufacturing in Istanbul")}</span></div><div><b>90<i>+</i></b><span>{X("Serinova ürünlerinin ulaştığı ülke","Countries Serinova products reach")}</span></div><div><b>{len(SER)}</b><span>{X("MOGRA fiberclay seri","MOGRA fiberclay series")}</span></div><div><b>{nsize}</b><span>{X("boy ve renk seçeneği","size and colour options")}</span></div></div></div></section>
<section class="cta"><img src="{pre}img/uranium/uranium-lifestyle.jpg" alt="" loading="lazy"><div class="wrap"><span class="eyebrow" style="color:#fff">{T[lang]["mim"]}</span><h2>{X("Projeniz için ölçü, renk ve adet planı.","Sizes, colours and quantities planned for your project.")}</h2><p>{X("Mimarlar, peyzaj tasarımcıları, oteller ve kurumsal alanlar için proje bazlı fiyatlandırma, numune ve sevkiyat planı hazırlıyoruz.","For architects, landscape designers, hotels and commercial spaces we prepare project pricing, samples and delivery plans.")}</p><div class="row" style="display:flex;gap:12px;flex-wrap:wrap"><a class="btn btn-fill" href="{P("mim")}">{X("Teklif isteyin","Request a quote")}</a><a class="btn btn-light" href="{pre}katalog/MOGRA_Katalog_2026.pdf" target="_blank" rel="noopener">{X("Kataloğu indirin","Download the catalogue")}</a></div></div></section>'''
    head=ld(ORG)+ld({"@context":"https://schema.org","@type":"WebSite","name":"MOGRA","url":SITE+"/","inLanguage":lang})
    return me,layout(lang,me,other,X("MOGRA | Fiberclay Saksı Koleksiyonu","MOGRA | Fiberclay Planters"),
        X("MOGRA fiberclay saksılar: Titan, Oval, Orion, Kale ve 24 seri. Hafif, dona ve UV'ye dayanıklı, iç ve dış mekân için. Mimari projelere özel teklif.","MOGRA fiberclay planters from Türkiye: Titan, Oval, Orion, Kale and 24 series. Lightweight, frost and UV resistant, for indoor and outdoor projects."),
        body,hero=True,head=head)

GEN={"tr":dict(tek=["Hafif ve dayanıklı fiberclay malzeme","UV ışınlarına ve dış hava koşullarına dayanıklı","İç ve dış mekân kullanımına uygun"],
               use=["Salon ve iç mekân","Balkon ve teras","Bahçe peyzajı","Otel ve restoran projeleri","Ofis ve plaza girişleri","Villa projeleri"]),
     "en":dict(tek=["Lightweight, durable fiberclay","Resistant to UV and outdoor weather","Suitable for indoor and outdoor use"],
               use=["Living rooms and interiors","Balconies and terraces","Garden landscaping","Hotel and restaurant projects","Office and lobby entrances","Villa projects"])}
def seri(s,lang):
    tr=lang=="tr"; X=(lambda a,b:a) if tr else (lambda a,b:b)
    me=path(lang,slug=s["slug"]); other=path("en" if tr else "tr",slug=s["slug"]); pre="../"*me.count("/")
    P=lambda k=None,slug=None:(pre+path(lang,k,slug)) or "./"
    N=s["name"]; L=s[lang]; t=s["t"] if tr else {}
    thumbs=[(p["src"],p["color"],False,f'{N} {cname(p["color"],lang)}'+(X(" ikili set"," set of two") if p["set"] else "")+(X(" yan açı"," side view") if p["side"] else "")) for p in s["prod"]]
    newl=LIFE.get(s["slug"],[])
    thumbs=[t+("",) for t in thumbs]
    thumbs+=[(x["src"],x["color"],True,f'{N} {x["size"]} · {cname(x["color"],lang)}'+(f' {x["tex"]}' if x["tex"] else "")+X(" mekânda"," in a space"),str(x["size"])) for x in newl]
    if not newl: thumbs+=[(l,"",True,X(f"{N} mekânda",f"{N} in a space"),"") for l in s["life"]]
    th="".join(f'<button type="button" data-src="{pre}{a}" data-color="{E(c)}" data-size="{sz}" data-alt="MOGRA {E(lab)}"{" data-life=1" if lf else ""} aria-current="{"true" if i==0 else "false"}" aria-label="{E(lab)}" title="{E(lab)}"><img class="{"" if lf else "c"}" src="{pre}{a}" alt="MOGRA {E(lab)}" loading="lazy"></button>' for i,(a,c,lf,lab,sz) in enumerate(thumbs))
    first=thumbs[0]
    cols="".join(f'<button type="button" data-color="{E(c)}" aria-pressed="{"true" if i==0 else "false"}"><i class="sw" style="background:{SWATCH.get(c,"#ccc")}"></i>{E(cname(c,lang))}</button>' for i,c in enumerate(s["colors"]))
    box=s["sizes"][0][0]=="b"
    hd=X("Ölçü (cm) · "+("U × G × Y" if box else "Ø × Y"),"Size (cm) · "+("L × W × H" if box else "Ø × H"))
    rows="".join(f'<tr data-size="{i+1}" data-label="{E(N)} {i+1} · {fmt_size(z,lang)} cm"{" class=on" if i==0 else ""} tabindex="0" role="button" aria-pressed="{"true" if i==0 else "false"}" title="{X("Bu boyu seç","Select this size")}"><td>{N} {i+1}</td><td>{fmt_size(z,lang)}</td><td class="see">{X("Seç","Select")}</td></tr>' for i,z in enumerate(s["sizes"]))
    if tr:
        lead=t.get("ozet") or (" ".join(s["xs"][:2]) if s["xs"] else L["kisa"])
        desc=t.get("desc") or ([" ".join(s["xs"][:2]), s["xs"][2] if len(s["xs"])>2 else "", L["kisa"]+f" {N} serisi {len(s['sizes'])} boy ve {len(s['colors'])} renk seçeneğiyle tek başına ya da farklı boylarla gruplanarak kullanılabilir. Mimari projeler, oteller ve kurumsal alanlar için toplu siparişlerde proje fiyatı veriyoruz."])
        tek=t.get("tek") or [L["form"],L["doku"]+" yüzey"]+GEN[lang]["tek"]
        use=t.get("use") or GEN[lang]["use"]
        guide=[(fmt_size(z,lang),g) for z,g in zip(s["sizes"],s["guide"]) if g]
    else:
        lead=f'{L["kisa"]} MOGRA {N} is {an(lf(L["form"]))} planter with {an(en_surf(L["doku"]))}, made from fiberclay.'
        desc=[f'MOGRA {N} ({s["en_name"]}) combines {an(lf(L["form"]))} with {an(en_surf(L["doku"]))}. {L["kisa"]}',
              "Fiberclay is a composite of clay and glass fibre. It has the look of terracotta and natural stone, weighs far less than concrete planters, and resists frost, UV and rain, so it can be used indoors and outdoors for years.",
              f'The {N} series comes in {len(s["sizes"])} size{"s" if len(s["sizes"])>1 else ""} and {len(s["colors"])} colour{"s" if len(s["colors"])>1 else ""} ({", ".join(cname(c,lang) for c in s["colors"])}), to be used on its own or grouped in different sizes. We offer project pricing for architects, hotels, landscape designers and trade buyers.']
        tek=[L["form"],L["doku"]]+GEN[lang]["tek"]; use=GEN[lang]["use"]; guide=[]
    desc=[d for d in desc if d]
    olcu="".join(f'<img src="{pre}{o}" alt="MOGRA {E(N)} {X("ölçü çizimi","dimension drawing")}" loading="lazy">' for o in s["olcu"])
    rel=[x for x in SER if x["grp"]==s["grp"] and x is not s][:4]
    msg=X(f"Merhaba, MOGRA {N} serisi için fiyat ve stok bilgisi almak istiyorum.",f"Hello, I would like price and availability for the MOGRA {N} series.")
    gsec=(f'<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Boy rehberi","Size guide")}</span><h2>{X("Hangi boy, hangi bitki?","Which size for which plant?")}</h2></div></div><div class="guide">'+"".join(f'<div><b>{N} {i+1} · {z} cm</b><p>{E(g)}</p></div>' for i,(z,g) in enumerate(guide))+'</div></div></section>') if guide else ""
    FG=FORMS[s["grp"]][lang][0]
    body=f'''<div class="wrap"><div class="pd">
<div><div class="gal-main"><img id="gmain" src="{pre}{first[0]}" alt="MOGRA {E(first[3])}" fetchpriority="high"></div><div class="gal-thumbs">{th}</div></div>
<div class="pd-info"><nav class="crumb"><a href="{P("index")}">MOGRA</a> / <a href="{P("kol")}">{X("Koleksiyon","Collection")}</a> / <a href="{P("kol")}#{s["grp"]}">{E(FG)}</a></nav>
<div><span class="eyebrow">Fiberclay · {E(FG)}</span><h1>{E(N)}</h1>{"" if tr else f'<p style="color:var(--muted);margin-top:8px">{E(s["en_name"])}</p>'}</div><p class="lead">{E(lead)}</p>
<div class="facts"><div><small>Form</small><b>{E(L["form"])}</b></div><div><small>{X("Doku","Texture")}</small><b>{E(L["doku"])}</b></div><div><small>{X("Boy","Sizes")}</small><b>{len(s["sizes"])} {X("seçenek","options")}</b></div></div>
<div><span class="lbl">{X("Renk","Colour")}: <span id="selcolor">{E(cname(s["colors"][0],lang))}</span></span><div class="colors">{cols}</div></div>
<div><span class="lbl">{X("Boy","Size")}: <span id="selsize">{E(N)} 1 · {fmt_size(s["sizes"][0],lang)} cm</span></span><p class="hint">{X("Bir boy seçin; galeride o boyun mekân görseli gösterilir.","Pick a size; the gallery shows that size in a space.")}</p><table class="sizes"><thead><tr><th>Model</th><th>{hd}</th><th></th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="pd-cta"><a class="btn btn-fill" id="stockbtn" data-msg="{E(stock_msg(s,lang))}" data-l-color="{X("Renk","Colour")}" data-l-size="{X("Boy","Size")}" href="https://wa.me/{WA}?text={quote(stock_msg(s,lang))}" target="_blank" rel="noopener">{X("Stok için sorun","Ask about stock")}</a><a class="btn btn-line" href="{P("mim")}?seri={quote(N)}#teklif">{X("Teklif formu","Quote form")}</a></div>
</div></div></div>
<section class="stone"><div class="wrap desc"><div><span class="eyebrow">{X("Ürün hakkında","About the product")}</span><h2 style="font-size:clamp(28px,3.4vw,46px);margin:12px 0 24px">MOGRA {E(N)} {X("fiberclay saksı","fiberclay planter")}</h2><div class="txt">{"".join(f"<p>{E(p)}</p>" for p in desc)}</div></div>
<div><span class="lbl">{X("Teknik özellikler","Specifications")}</span><ul>{"".join(f"<li>{E(x)}</li>" for x in tek)}</ul><span class="lbl" style="margin-top:36px">{X("Kullanım alanları","Where to use")}</span><div class="tags">{"".join(f"<span>{E(x)}</span>" for x in use)}</div></div></div></section>
{gsec}
{f'<section class="sec{" stone" if gsec else ""}"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Teknik çizim","Drawings")}</span><h2>{X("Ölçü görselleri","Dimension drawings")}</h2></div></div><div class="olcu-grid">{olcu}</div></div></section>' if olcu else ""}
<section class="sec"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">{X("Aynı form ailesi","Same form family")}</span><h2>{X("Benzer seriler","Related series")}</h2></div><a class="link-arrow" href="{P("kol")}#{s["grp"]}">{X("Tümü →","All →")}</a></div><div class="grid">{"".join(card(x,lang,pre) for x in rel)}</div></div></section>'''
    imgs=[SITE+"/"+p["src"] for p in s["prod"][:4]]+[SITE+"/"+x["src"] for x in LIFE.get(s["slug"],[])[:4]]
    prod={"@context":"https://schema.org","@type":"Product","name":f"MOGRA {N}","description":lead,"brand":{"@type":"Brand","name":"MOGRA"},
          "manufacturer":{"@type":"Organization","name":"Serinova Plastik"},"material":"Fiberclay","category":X("Fiberclay saksı","Fiberclay planter"),
          "image":imgs,"url":SITE+"/"+me,"color":[cname(c,lang) for c in s["colors"]],"countryOfOrigin":"TR",
          "additionalProperty":[{"@type":"PropertyValue","name":X("Ölçü","Size"),"value":fmt_size(z,lang)+" cm"} for z in s["sizes"]]}
    head=ld(prod)+crumbs(lang,[("MOGRA",SITE+"/"+path(lang,"index")),(X("Koleksiyon","Collection"),SITE+"/"+path(lang,"kol")),(N,SITE+"/"+me)])
    base_t=X(f'MOGRA {N} Fiberclay Saksı',f'MOGRA {N} Fiberclay Planter')
    title=next(t for t in [f'{base_t} | {L["form"]}, {L["doku"]}',f'{base_t} | {L["form"]}',base_t] if len(t)<=60 or t==base_t)
    d=X(f'MOGRA {N}: {lf(L["form"])}, {lf(L["doku"])} fiberclay saksı. {hrange(s,lang)}, {", ".join(s["colors"])}. Hafif, dona ve UV\'ye dayanıklı; iç ve dış mekân. Proje teklifi.',
        f'MOGRA {N}: {lf(L["form"])} fiberclay planter, {en_surf(L["doku"])}. {hrange(s,lang)}, {", ".join(cname(c,lang) for c in s["colors"])}. Lightweight, frost and UV resistant. Project pricing.')
    og=s.get("hero") or (s["life"] or [s["prod"][0]["src"]])[0]
    return me,layout(lang,me,other,title,d,body,cur="kol",og=og,head=head)

def ph(lang,pre,crumb,h,p): return f'<section class="page-hero"><div class="wrap"><nav class="crumb"><a href="{(pre+path(lang,"index")) or "./"}">MOGRA</a> / {crumb}</nav><h1>{h}</h1><p>{p}</p></div></section>'
def ctx(lang,key):
    tr=lang=="tr"; me=path(lang,key); other=path("en" if tr else "tr",key); pre="../"*me.count("/")
    return tr,(lambda a,b:a) if tr else (lambda a,b:b),me,other,pre,(lambda k=None,slug=None:(pre+path(lang,k,slug)) or "./")
def koleksiyon(lang):
    tr,X,me,other,pre,P=ctx(lang,"kol")
    chips=f'<button class="chip" type="button" data-f="form" data-v="all" aria-pressed="true">{X("Tümü","All")}</button>'+"".join(f'<button class="chip" type="button" data-f="form" data-v="{g}" aria-pressed="false">{E(v[lang][0])}</button>' for g,v in FORMS.items())
    allc=[]
    for s in SER:
        for c in s["colors"]:
            if c not in allc: allc.append(c)
    allc.sort(key=lambda c:ORD.index(c) if c in ORD else 99)
    cchips=f'<button class="chip" type="button" data-f="color" data-v="all" aria-pressed="true">{X("Tüm renkler","All colours")}</button>'+"".join(f'<button class="chip" type="button" data-f="color" data-v="{E(c)}" aria-pressed="false"><i class="sw" style="background:{SWATCH.get(c)};display:inline-block;vertical-align:-2px;margin-right:6px"></i>{E(cname(c,lang))}</button>' for c in allc)
    body=ph(lang,pre,X("Koleksiyon","Collection"),X("Koleksiyon","Collection"),X(f"{len(SER)} fiberclay seri. Form ailesine, renge ya da isme göre filtreleyin.",f"{len(SER)} fiberclay series. Filter by form, colour or name."))+f'''
<div class="wrap"><p class="kat-inline"><a class="btn btn-line" href="{pre}katalog/MOGRA_Katalog_2026.pdf" download>{X("Katalog indir (PDF)","Download catalogue (PDF)")}</a></p><div class="filters"><div class="chips">{chips}</div><input class="search" id="q" type="search" placeholder="{X("Seri ara: Titan, Oval…","Search: Titan, Oval…")}" aria-label="{X("Seri ara","Search series")}"></div>
<div class="chips" style="margin:-16px 0 28px">{cchips}</div><p id="count" data-w="{T[lang]["seri_w"]}" style="color:var(--muted);font-size:14px;margin-bottom:20px">{len(SER)} {T[lang]["seri_w"]}</p>
<div class="grid" id="grid">{"".join(card(s,lang,pre) for s in SER)}</div><p class="empty" id="empty" hidden>{X("Bu filtreye uyan seri yok. Filtreleri değiştirin.","No series match these filters. Try another filter.")}</p></div><div style="height:96px"></div>'''
    il={"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":SITE+"/"+path(lang,slug=s["slug"]),"name":"MOGRA "+s["name"]} for i,s in enumerate(SER)]}
    return me,layout(lang,me,other,X("Koleksiyon | MOGRA Fiberclay Saksılar","Collection | MOGRA Fiberclay Planters"),
        X("MOGRA fiberclay saksı koleksiyonu: yuvarlak, kare, dikdörtgen, yüksek ve çanak formlarda 24 seri. Renk ve form filtresiyle inceleyin.","The MOGRA fiberclay planter collection: 24 series in round, square, trough, tall and bowl forms. Filter by form and colour."),
        body,cur="kol",og="img/oval/oval-lifestyle.jpg",head=ld(il)+crumbs(lang,[("MOGRA",SITE+"/"+path(lang,"index")),(X("Koleksiyon","Collection"),SITE+"/"+me)]))
def ABOUT_P(lang,X):
    if CMS and CMS[3]["about"].get("body_"+lang): return "".join(f"<p>{E(x)}</p>" for x in CMS[3]["about"]["body_"+lang])
    return f'''<p>{X("Serinova, 1986'da İstanbul Bayrampaşa'da kuruldu. Bugün Selimpaşa ve Malkara'daki tesislerinde saksı, vazo ve bahçe ürünleri üretiyor; ürünleri 90'dan fazla ülkeye ulaşıyor.","Serinova was founded in 1986 in Bayrampaşa, Istanbul. Today it manufactures planters, vases and garden products at its facilities in Selimpaşa and Malkara, and its products reach more than 90 countries.")}</p>
<p>{X("MOGRA, bu üretim birikiminden doğdu. Serinova'nın fiberclay saksı markası olarak 2025'te yola çıktı ve mimari projeler, oteller, restoranlar, ofisler ve evler için geniş bir form, doku ve ölçü yelpazesi sunuyor.","MOGRA grew out of that manufacturing experience. Launched in 2025 as Serinova's fiberclay brand, it offers a wide range of forms, textures and sizes for architectural projects, hotels, restaurants, offices and homes.")}</p>
<p>{X("Her seriyi birden fazla boy ve renkle tasarlıyoruz. Böylece bir lobide, bir terasta ya da bir salonda aynı dilde, farklı ölçeklerde kompozisyon kurmak mümkün oluyor.","Every series comes in several sizes and colours, so a lobby, a terrace or a living room can be composed in one language at different scales.")}</p>'''
def hakkimizda(lang):
    tr,X,me,other,pre,P=ctx(lang,"hak")
    body=ph(lang,pre,T[lang]["hak"],T[lang]["hak"],X("MOGRA, Serinova'nın fiberclay saksı markasıdır.","MOGRA is the fiberclay planter brand of Serinova."))+f'''<div class="banner"><img src="{pre}{(CMS and CMS[3]["about"].get("img")) or "img/oval/oval-lifestyle2.jpg"}" alt="MOGRA"></div>
<section class="sec"><div class="wrap two"><div class="prose"><h2 style="margin-top:0">{X("Serinova'nın deneyimi, MOGRA'nın formu","Serinova's experience, MOGRA's form")}</h2>
{ABOUT_P(lang,X)}</div>
<div class="numbers" style="grid-template-columns:1fr 1fr"><div><b>1986</b><span>{X("Serinova'nın kuruluş yılı","Serinova founded")}</span></div><div><b>90<i>+</i></b><span>{X("ihracat yapılan ülke","export countries")}</span></div><div style="padding-left:0"><b>{len(SER)}</b><span>{X("MOGRA serisi","MOGRA series")}</span></div><div><b>2025</b><span>{X("MOGRA'nın kuruluşu","MOGRA launched")}</span></div></div></div></section>
<section class="story rev"><div class="story-img"><img src="{pre}img/titan/titan-lifestyle-kursun-gri.jpg" alt="MOGRA Titan" loading="lazy"></div><div class="story-txt"><span class="eyebrow">{X("Yaklaşım","Approach")}</span><h2>{X("Bitkiyi öne çıkaran sade formlar.","Quiet forms that put the plant first.")}</h2><p>{X("MOGRA saksıları, bitkiyle ve mimariyle yarışmak için değil, onları tamamlamak için tasarlanır. Doğal tonlar, taş ve kil dokuları, yalın siluetler.","MOGRA planters are designed to complete the plant and the architecture, not compete with them. Natural tones, stone and clay textures, simple silhouettes.")}</p><a class="link-arrow" href="{P("kol")}">{X("Koleksiyonu inceleyin →","View the collection →")}</a></div></section>'''
    return me,layout(lang,me,other,X("Hakkımızda | MOGRA","About | MOGRA"),X("MOGRA, 1986'dan beri üretim yapan Serinova'nın fiberclay saksı markasıdır. Mimari projeler, oteller ve yaşam alanları için tasarlanır.","MOGRA is the fiberclay planter brand of Serinova, a manufacturer since 1986. Designed for architectural projects, hotels and living spaces."),body,cur="hak",og="img/oval/oval-lifestyle2.jpg",head=ld(ORG))
def fiberclay(lang):
    tr,X,me,other,pre,P=ctx(lang,"fib")
    f=[(X("Hafif","Lightweight"),X("Aynı ölçüdeki beton ve taş saksılardan çok daha hafiftir. Teras ve balkonlarda taşıma yükünü azaltır.","Far lighter than concrete and stone planters of the same size, reducing load on terraces and balconies.")),
       (X("Dona dayanıklı","Frost resistant"),X("Isı değişimlerinde çatlamaya karşı dirençlidir; dış mekânda yıl boyu kullanılır.","Resists cracking through temperature changes; used outdoors all year.")),
       (X("UV dayanımı","UV resistant"),X("Güneş altında rengini ve dokusunu uzun süre korur.","Keeps its colour and texture under the sun for years.")),
       (X("Doğal doku","Natural textures"),X("Utah, Texa, volkan, tuğla ve granit gibi dokularla taşın görünümünü verir.","Utah, Texa, volcano, brick and granite finishes give the look of stone."))]
    body=ph(lang,pre,"Fiberclay",X("Fiberclay malzeme","Fiberclay material"),X("Toprağın ve taşın görünümü, çok daha hafif ve dayanıklı bir gövdede.","The look of terracotta and stone in a much lighter, more durable body."))+f'''<div class="banner"><img src="{pre}img/kale/kale-lifestyle.jpg" alt="MOGRA Kale"></div>
<section class="sec"><div class="wrap two"><div class="prose"><h2 style="margin-top:0">{X("Fiberclay nedir?","What is fiberclay?")}</h2><p>{X("Fiberclay, kil ile cam elyafının birleşiminden oluşan kompozit bir malzemedir. Kilin doğal görünümünü ve dokusunu korurken cam elyafı gövdeye dayanım kazandırır.","Fiberclay is a composite of clay and glass fibre. The clay keeps its natural look and texture while the glass fibre gives the body strength.")}</p>
<p>{X("Sonuç, geleneksel toprak ve beton saksılara göre çok daha hafif, darbelere karşı daha dirençli ve dış mekân koşullarına dayanıklı bir saksıdır. Büyük boylarda bile taşımak, yerleştirmek ve yer değiştirmek kolaydır.","The result is a planter far lighter than terracotta or concrete, more resistant to knocks, and made for outdoor conditions. Even large sizes are easy to move and place.")}</p>
<h2>{X("Bakım","Care")}</h2><p>{X("Yüzeyi nemli bir bezle silmek yeterlidir. Dış mekânda kullanılan saksılarda drenaj deliğinin açık olduğundan emin olun; kış aylarında saksı içinde su birikmesini önleyin. Büyük boyları taşırken saksıyı gövdesinden, dolu değilken kaldırın.","Wipe the surface with a damp cloth. Outdoors, keep the drainage hole clear and avoid standing water in winter. Lift large sizes by the body, and only when empty.")}</p></div>
<div class="feats" style="grid-template-columns:1fr">{"".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a,b in f)}</div></div></section>'''
    faq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":X("Fiberclay nedir?","What is fiberclay?"),"acceptedAnswer":{"@type":"Answer","text":X("Kil ile cam elyafının birleşiminden oluşan, hafif ve dış mekâna dayanıklı kompozit bir saksı malzemesidir.","A lightweight composite of clay and glass fibre used for durable indoor and outdoor planters.")}},
        {"@type":"Question","name":X("Fiberclay saksı dış mekânda kullanılır mı?","Can fiberclay planters be used outdoors?"),"acceptedAnswer":{"@type":"Answer","text":X("Evet. Dona ve UV ışınlarına dayanıklıdır; drenaj deliği açık tutulmalı ve kışın içinde su birikmesi önlenmelidir.","Yes. It resists frost and UV; keep the drainage hole clear and avoid standing water in winter.")}}]}
    return me,layout(lang,me,other,X("Fiberclay Saksı Nedir? | MOGRA","What Is Fiberclay? | MOGRA"),X("Fiberclay, kil ve cam elyafından oluşan hafif, dona ve UV'ye dayanıklı bir malzemedir. MOGRA saksılarının malzemesini ve bakımını tanıyın.","Fiberclay is a lightweight, frost and UV resistant composite of clay and glass fibre. Learn about the material and care of MOGRA planters."),body,cur="fib",og="img/kale/kale-lifestyle.jpg",head=ld(faq))

def form_html(lang,btn,ctxmsg,extra=""):
    X=(lambda a,b:a) if lang=="tr" else (lambda a,b:b)
    return f'''<form class="form" data-wa="{E(ctxmsg)}"><div class="r2"><label for="f-ad">{X("Ad soyad","Full name")}<input id="f-ad" data-l="{X("Ad soyad","Name")}" autocomplete="name" required></label><label for="f-firma">{X("Firma","Company")}<input id="f-firma" data-l="{X("Firma","Company")}" autocomplete="organization"></label></div>
<div class="r2"><label for="f-tel">{X("Telefon","Phone")}<input id="f-tel" type="tel" data-l="{X("Telefon","Phone")}" autocomplete="tel" required></label><label for="f-mail">{X("E-posta","Email")}<input id="f-mail" type="email" data-l="{X("E-posta","Email")}" autocomplete="email"></label></div>{extra}
<label for="f-not">{X("Mesajınız","Message")}<textarea id="f-not" data-l="{X("Mesaj","Message")}" placeholder="{X("Seri, boy, renk ve adet bilgisi","Series, size, colour and quantity")}"></textarea></label>
<button class="btn btn-fill" type="submit" style="justify-self:start">{btn}</button><p style="font-size:13px;color:var(--muted)">{X("Gönder'e bastığınızda mesajınız WhatsApp'ta hazır açılır.","Your message opens ready to send in WhatsApp.")}</p></form>'''
def mimari(lang):
    tr,X,me,other,pre,P=ctx(lang,"mim")
    opts="".join(f'<option>{E(s["name"])}</option>' for s in SER)
    types=X(["Otel","Restoran / Kafe","Ofis / Plaza","AVM","Villa / Konut","Peyzaj","Bayi / Toptan"],["Hotel","Restaurant / Café","Office","Shopping centre","Villa / Residential","Landscape","Dealer / Trade"])
    extra=f'<div class="r2"><label for="f-tip">{X("Proje tipi","Project type")}<select id="f-tip" data-l="{X("Proje tipi","Project type")}"><option value="">{X("Seçin","Select")}</option>{"".join(f"<option>{x}</option>" for x in types)}</select></label><label for="f-seri">{X("İlgilendiğiniz seri","Series")}<select id="f-seri" data-l="{X("Seri","Series")}"><option value="">{X("Seçin","Select")}</option>{opts}</select></label></div><div class="r2"><label for="f-adet">{X("Adet","Quantity")}<input id="f-adet" type="number" min="1" inputmode="numeric" data-l="{X("Adet","Quantity")}" required></label><label for="f-tarih">{X("İstenen teslim tarihi","Required delivery date")}<input id="f-tarih" type="date" data-l="{X("Teslim tarihi","Delivery date")}"></label></div>'
    st=X([("Brief","Mekân, bitki ve adet bilgilerini bize iletin."),("Seçki","Ölçü, renk ve doku önerisiyle seri seçkisi hazırlayalım."),("Teklif","Proje adedine göre özel fiyat ve termin verelim."),("Sevkiyat","Ürünleri planlanan tarihte sahaya ulaştıralım.")],
         [("Brief","Send us the space, plants and quantities."),("Selection","We propose series, sizes, colours and textures."),("Quote","Project pricing and lead time based on quantity."),("Delivery","Products delivered to site on the planned date.")])
    body=ph(lang,pre,T[lang]["mim"],T[lang]["mim"],X("Mimarlar, peyzaj tasarımcıları, oteller ve kurumsal alanlar için proje bazlı fiyat, numune ve sevkiyat planı.","Project pricing, samples and delivery planning for architects, landscape designers, hotels and commercial spaces."))+f'''<section class="sec"><div class="wrap"><div class="steps">{"".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a,b in st)}</div></div></section>
<section class="sec stone" id="teklif"><div class="wrap two"><div class="prose"><span class="eyebrow">{X("Teklif formu","Quote form")}</span><h2 style="margin-top:8px">{X("Projenizi anlatın","Tell us about your project")}</h2><p>{X("Formu doldurun, aynı gün dönüş yapalım. Teknik çizimler ve tüm seriler için","Fill in the form and we will reply the same day. For drawings and all series, download the")} <a class="link-arrow" href="{pre}katalog/MOGRA_Katalog_2026.pdf" target="_blank" rel="noopener">{X("2026 kataloğunu","2026 catalogue")}</a>{X(" indirebilirsiniz.",".")}</p><div class="banner" style="height:320px;margin-top:12px"><img src="{pre}img/orion/orion-lifestyle2.jpg" alt="MOGRA Orion" loading="lazy"></div></div>
{form_html(lang,X("Teklif iste","Request a quote"),X("MOGRA proje teklif talebi","MOGRA project quote request"),extra)}</div></section>'''
    return me,layout(lang,me,other,X("Mimari Destek ve Proje Teklifi | MOGRA","Architectural Support & Project Quotes | MOGRA"),X("Otel, restoran, ofis ve peyzaj projeleri için MOGRA fiberclay saksılarda proje fiyatı, numune ve sevkiyat planı.","Project pricing, samples and delivery for MOGRA fiberclay planters in hotel, restaurant, office and landscape projects."),body,cur="mim",og="img/orion/orion-lifestyle2.jpg")
def iletisim(lang):
    tr,X,me,other,pre,P=ctx(lang,"ilet")
    body=ph(lang,pre,T[lang]["ilet"],T[lang]["ilet"],X("Sorularınız, numune ve teklif talepleriniz için bize ulaşın.","Get in touch for questions, samples and quotes."))+f'''<section class="sec"><div class="wrap two"><div class="contact-list">
<div><small>{X("Telefon","Phone")}</small><b><a href="tel:+905444720903">{PHONE if tr else PHONE_INT}</a></b></div><div><small>WhatsApp</small><b><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{X("Mesaj gönderin →","Send a message →")}</a></b></div>
<div><small>{X("E-posta","Email")}</small><b><a href="mailto:{MAIL}">{MAIL}</a></b></div><div><small>{X("Sabit hat","Landline")}</small><b>{" · ".join(f'<a href="tel:{b}">{a}</a>' for a,b in TELS)}</b></div><div><small>{X("Mağaza","Store")}</small><b><a href="{P("mag")}">{ADDR_TR if tr else ADDR_EN}</a></b></div>
<div><small>{X("Online satış","Online shop")}</small><b><a href="https://www.serinovashop.com" target="_blank" rel="noopener">serinovashop.com</a></b></div></div>
{form_html(lang,X("Gönder","Send"),X("MOGRA web sitesi iletişim formu","MOGRA website contact form"))}</div></section>'''
    return me,layout(lang,me,other,X("İletişim | MOGRA","Contact | MOGRA"),X("MOGRA fiberclay saksılar için iletişim: telefon, WhatsApp, e-posta ve adres.","Contact MOGRA fiberclay planters: phone, WhatsApp, email and address."),body,cur="ilet",head=ld(ORG))

FAQ={"tr":[("Fiberclay nedir?","Kil ile cam elyafının birleşiminden oluşan kompozit bir malzemedir. Toprak ve taş saksıların görünümünü taşır, onlardan çok daha hafiftir."),
 ("MOGRA saksılar dış mekânda kullanılabilir mi?","Evet. Fiberclay dona, UV ışınlarına ve yağmura dayanıklıdır. Kış aylarında saksı içinde su birikmemesi için drenajın açık olduğundan emin olun."),
 ("Fiberclay saksılar ağır mı?","Hayır. Aynı ölçüdeki beton veya taş saksılardan çok daha hafiftir; teras ve balkonlarda taşıma yükünü azaltır."),
 ("Hangi boyu seçmeliyim?","Her seri sayfasında 'Hangi boy, hangi bitki?' rehberi var. Bitkinizin kök hacmine ve mekânın ölçeğine göre boy seçebilir, emin olamazsanız WhatsApp'tan bize sorabilirsiniz."),
 ("Proje ve toptan siparişlerde özel fiyat var mı?","Evet. Mimari projeler, oteller, peyzaj uygulamaları ve bayiler için adede göre proje fiyatı veriyoruz. Mimari Destek sayfasındaki formdan teklif isteyebilirsiniz."),
 ("Teslim süresi ne kadar?","Stok durumuna ve sipariş adedine göre değişir. Teklifimizde termin tarihini ayrıca belirtiyoruz."),
 ("Renk seçenekleri neler?","Serilere göre bej, kum, vizon, gri, kurşun gri, antrasit ve siyah tonları bulunur. Her seri sayfasında mevcut renkler listelenir."),
 ("Bakımı nasıl yapılır?","Yüzeyi nemli bir bezle silmek yeterlidir. Büyük boyları taşırken saksıyı gövdesinden ve boşken kaldırın."),
 ("Nereden satın alabilirim?","Proje ve toptan siparişler için bize telefon veya WhatsApp üzerinden ulaşabilirsiniz. Serinova ürünlerine serinovashop.com üzerinden de ulaşabilirsiniz.")],
"en":[("What is fiberclay?","A composite of clay and glass fibre. It has the look of terracotta and stone, and weighs far less."),
 ("Can MOGRA planters be used outdoors?","Yes. Fiberclay resists frost, UV and rain. In winter, make sure drainage stays clear so no water stands inside the planter."),
 ("Are fiberclay planters heavy?","No. They are far lighter than concrete or stone planters of the same size, which reduces load on terraces and balconies."),
 ("Which size should I choose?","Choose by the root volume of your plant and the scale of the space. If you are unsure, message us on WhatsApp."),
 ("Do you offer project and trade pricing?","Yes. We price by quantity for architectural projects, hotels, landscape work and dealers. Use the form on the Architectural Support page."),
 ("What is the lead time?","It depends on stock and order quantity. Our quote states the delivery date."),
 ("Which colours are available?","Depending on the series: beige, sand, mink, grey, lead grey, anthracite and black. Each series page lists its colours."),
 ("How do I care for them?","Wipe the surface with a damp cloth. Lift large sizes by the body, and only when empty."),
 ("Where can I buy?","For project and trade orders, contact us by phone or WhatsApp. Serinova products are also available at serinovashop.com.")]}
if CMS and CMS[3]["faq"]: FAQ={l:[(x.get("q_"+l) or x.get("q_tr",""),x.get("a_"+l) or x.get("a_tr","")) for x in CMS[3]["faq"]] for l in ("tr","en")}
def sss(lang):
    tr,X,me,other,pre,P=ctx(lang,"sss")
    items="".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in FAQ[lang])
    body=ph(lang,pre,X("SSS","FAQ"),X("Sıkça sorulan sorular","Frequently asked questions"),X("Fiberclay, ölçüler, teslimat ve bakım hakkında kısa cevaplar.","Short answers on fiberclay, sizes, delivery and care."))+f'<section class="sec"><div class="wrap" style="max-width:900px">{items}<p style="margin-top:40px"><a class="btn btn-fill" href="https://wa.me/{WA}" target="_blank" rel="noopener">{X("Sorunuzu WhatsApp\'tan sorun","Ask us on WhatsApp")}</a></p></div></section>'
    fq={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ[lang]]}
    return me,layout(lang,me,other,X("Sıkça Sorulan Sorular | MOGRA Fiberclay Saksı","FAQ | MOGRA Fiberclay Planters"),X("MOGRA fiberclay saksılar hakkında sık sorulan sorular: dış mekân kullanımı, ağırlık, boy seçimi, proje fiyatı, teslim süresi ve bakım.","Frequently asked questions about MOGRA fiberclay planters: outdoor use, weight, sizing, project pricing, lead time and care."),body,head=ld(fq))

HOURS={"tr":[("Pazartesi – Cumartesi","09.00 – 18.00"),("Pazar","Kapalı")],"en":[("Monday – Saturday","09:00 – 18:00"),("Sunday","Closed")]}
if CMS and _st.get("hours"): HOURS={l:[(h.get("days_"+l) or h.get("days_tr",""),h.get("time_"+l) or h.get("time_tr","")) for h in _st["hours"]] for l in ("tr","en")}
def magaza(lang):
    tr,X,me,other,pre,P=ctx(lang,"mag")
    hrs="".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a,b in HOURS[lang])
    mq=quote(MAP_Q)
    body=ph(lang,pre,T[lang]["mag"],X("Mağaza ve satış noktası","Store and showroom"),X("MOGRA ve Serinova ürünlerini İSTOÇ'taki mağazamızda görebilir, proje ve toptan siparişleriniz için bizimle buradan görüşebilirsiniz.","See MOGRA and Serinova products at our store in İSTOÇ, Istanbul, and meet us here for project and trade orders."))+f'''
<section class="sec"><div class="wrap two store"><div class="contact-list">
<div><small>{X("Adres","Address")}</small><b>{ADDR_TR if tr else ADDR_EN}</b><a class="link-arrow" href="https://www.google.com/maps/search/?api=1&amp;query={mq}" target="_blank" rel="noopener">{X("Yol tarifi al →","Get directions →")}</a></div>
<div><small>{X("Telefon","Phone")}</small><b>{"<br>".join(f'<a href="tel:{b}">{a if tr else "+90 "+a[1:]}</a>' for a,b in TELS)}</b></div>
<div><small>WhatsApp</small><b><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PHONE if tr else PHONE_INT}</a></b></div>
<div><small>{X("Çalışma saatleri","Opening hours")}</small><table class="hours">{hrs}</table></div></div>
<div class="map"><iframe title="{X("MOGRA mağaza konumu","MOGRA store location")}" src="https://www.google.com/maps?q={mq}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>
<section class="sec stone"><div class="wrap two"><div class="prose"><span class="eyebrow">{X("Üretici","Manufacturer")}</span><h2 style="margin-top:8px">{X("Serinova çatısı altında, 1986'dan beri üretim.","Made under Serinova, a manufacturer since 1986.")}</h2>
<p>{X("MOGRA, 1986'da İstanbul'da kurulan Serinova'nın fiberclay saksı markasıdır. Ürünlerimizi doğrudan üretici olarak sunuyoruz; proje adedine göre fiyat, numune ve sevkiyat planını mağazamızda ya da WhatsApp üzerinden birlikte hazırlıyoruz.","MOGRA is the fiberclay planter brand of Serinova, founded in Istanbul in 1986. We sell directly as the manufacturer and plan pricing, samples and delivery for your project at the store or over WhatsApp.")}</p>
<p style="display:flex;gap:12px;flex-wrap:wrap;margin-top:20px"><a class="btn btn-fill" href="https://wa.me/{WA}" target="_blank" rel="noopener">{X("WhatsApp'tan yazın","Message on WhatsApp")}</a><a class="btn btn-line" href="{P("mim")}#teklif">{X("Teklif formu","Quote form")}</a></p></div>
<div class="banner" style="height:360px"><img src="{pre}img/titan/life/titan-bej-8.jpg" alt="MOGRA Titan" loading="lazy"></div></div></section>'''
    store={"@context":"https://schema.org","@type":"Store","name":"MOGRA · Serinova Plastik İSTOÇ","url":SITE+"/"+me,"image":SITE+"/img/titan/life/titan-bej-8.jpg",
           "telephone":["+902126591510","+902126593414",PHONE_INT.replace(" ","")],"email":MAIL,
           "address":{"@type":"PostalAddress","streetAddress":"İSTOÇ 15. Ada No:152, Mahmutbey Mah. 2433. Sk.","addressLocality":"Bağcılar","addressRegion":"İstanbul","addressCountry":"TR"},
           "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"18:00"}],
           "parentOrganization":{"@type":"Organization","name":"Serinova Plastik","foundingDate":"1986"}}
    return me,layout(lang,me,other,X("Mağaza ve Satış Noktası | MOGRA İSTOÇ","Store & Showroom | MOGRA Istanbul"),
        X("MOGRA fiberclay saksılar İSTOÇ mağazası: adres, telefon, çalışma saatleri ve yol tarifi. Serinova çatısı altında 1986'dan beri üretim.","MOGRA fiberclay planters store at İSTOÇ, Istanbul: address, phone, opening hours and directions. Made under Serinova since 1986."),
        body,cur="mag",og="img/titan/life/titan-bej-8.jpg",head=ld(store)+crumbs(lang,[("MOGRA",SITE+"/"+path(lang,"index")),(T[lang]["mag"],SITE+"/"+me)]))
def fdate(d,lang):
    y,m,g=d.split("-"); A=["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]; B=["January","February","March","April","May","June","July","August","September","October","November","December"]
    return f"{int(g)} {A[int(m)-1]} {y}" if lang=="tr" else f"{B[int(m)-1]} {int(g)}, {y}"
def blog_index(lang):
    tr,X,me,other,pre,P=ctx(lang,"blog")
    cards="".join(f'<a class="post-card" href="{pre}{bpath(lang,b)}"><img src="{pre}{b["img"]}" alt="" loading="lazy"><div><small>{fdate(b["date"],lang)}</small><h2>{E(b[lang]["title"])}</h2><p>{E(b[lang]["lead"])}</p><span class="link-arrow">{X("Yazıyı oku →","Read →")}</span></div></a>' for b in POSTS)
    body=ph(lang,pre,"Blog",X("Blog","Blog"),X("Fiberclay, saksı seçimi, bakım ve mekân düzeni üzerine yazılar.","Notes on fiberclay, choosing planters, care and styling spaces."))+f'<section class="sec"><div class="wrap posts">{cards}</div></section>'
    bl={"@context":"https://schema.org","@type":"Blog","name":"MOGRA Blog","url":SITE+"/"+me,"inLanguage":lang,
        "blogPost":[{"@type":"BlogPosting","headline":b[lang]["title"],"url":SITE+"/"+bpath(lang,b),"datePublished":b["date"]} for b in POSTS]}
    return me,layout(lang,me,other,X("Blog | MOGRA Fiberclay Saksı","Blog | MOGRA Fiberclay Planters"),X("MOGRA blog: fiberclay nedir, teras ve balkon için saksı seçimi, fiberclay saksı bakımı ve kullanım rehberi.","MOGRA blog: what fiberclay is, choosing planters for terraces and balconies, and fiberclay planter care."),body,cur="blog",og=POSTS[0]["img"],head=ld(bl))
def blog_post(b,lang):
    tr=lang=="tr"; X=(lambda a,c:a) if tr else (lambda a,c:c)
    me=bpath(lang,b); other=bpath("en" if tr else "tr",b); pre="../"*me.count("/"); P=lambda k=None,slug=None:(pre+path(lang,k,slug)) or "./"
    c=b[lang]; html_=""
    for kind,v in c["body"]:
        html_+=f"<h2>{E(v)}</h2>" if kind=="h" else (f"<p>{E(v)}</p>" if kind=="p" else "<ul>"+"".join(f"<li>{E(x)}</li>" for x in v)+"</ul>")
    others="".join(f'<li><a href="{pre}{bpath(lang,o)}">{E(o[lang]["title"])}</a></li>' for o in POSTS if o is not b)
    body=f'''<article><section class="page-hero"><div class="wrap" style="max-width:860px"><nav class="crumb"><a href="{P("index")}">MOGRA</a> / <a href="{P("blog")}">Blog</a></nav><h1>{E(c["title"])}</h1><p>{E(c["lead"])}</p><small style="color:var(--muted)">{fdate(b["date"],lang)} · MOGRA</small></div></section>
<div class="banner"><img src="{pre}{b["img"]}" alt="{E(c["title"])}"></div>
<section class="sec"><div class="wrap prose post" style="max-width:860px">{html_}
<div class="post-cta"><a class="btn btn-fill" href="{P("kol")}">{X("Koleksiyonu inceleyin","View the collection")}</a><a class="btn btn-line" href="https://wa.me/{WA}" target="_blank" rel="noopener">{X("WhatsApp'tan sorun","Ask on WhatsApp")}</a></div>
<h3 style="margin-top:48px">{X("Diğer yazılar","More articles")}</h3><ul>{others}</ul></div></section></article>'''
    art={"@context":"https://schema.org","@type":"Article","headline":c["title"],"description":c["desc"],"image":SITE+"/"+b["img"],"datePublished":b["date"],"dateModified":b["date"],"inLanguage":lang,
         "author":{"@type":"Organization","name":"MOGRA"},"publisher":{"@type":"Organization","name":"MOGRA","logo":{"@type":"ImageObject","url":SITE+"/img/brand/mogra-mark.png"}},"mainEntityOfPage":SITE+"/"+me}
    return me,layout(lang,me,other,c["title"]+" | MOGRA",c["desc"],body,cur="blog",og=b["img"],head=ld(art)+crumbs(lang,[("MOGRA",SITE+"/"+path(lang,"index")),("Blog",SITE+"/"+path(lang,"blog")),(c["title"],SITE+"/"+me)]))

# Netlify linkleri uzantısız sunuyor; canonical, hreflang, og:url, JSON-LD ve sitemap da aynı adresi göstersin
def pretty(c): return re.sub(r'(https://mogra\.com\.tr/(?:[^"\s<>]*/)?)index\.html',r'\1',re.sub(r'(https://mogra\.com\.tr/[^"\s<>]*?[^/"\s<>])(?<!/index)\.html(?=["<\s#?])',r'\1',c))
def W(p,c):
    f=OUT+"/"+(p if p and not p.endswith("/") else p+"index.html")
    os.makedirs(os.path.dirname(f),exist_ok=True); open(f,"w",encoding="utf-8").write(pretty(c))
pages=[]
for lang in ["tr","en"]:
    for fn in [index,koleksiyon,hakkimizda,fiberclay,mimari,iletisim,sss,magaza,blog_index]:
        me,h=fn(lang); W(me,h); pages.append(me)
    for b in POSTS:
        me,h=blog_post(b,lang); W(me,h); pages.append(me)
    for s in SER:
        me,h=seri(s,lang); W(me,h); pages.append(me)
# 404
nf=layout("tr","404.html","en/","Sayfa bulunamadı | MOGRA","Aradığınız sayfa bulunamadı.",'<section class="page-hero"><div class="wrap"><h1>Sayfa bulunamadı</h1><p>Aradığınız sayfa taşınmış ya da kaldırılmış olabilir. <a class="link-arrow" href="/koleksiyon.html">Koleksiyona dön →</a></p><p><a class="link-arrow" href="/en/collection.html">Page not found — go to the collection →</a></p></div></section><div style="height:80px"></div>')
W("404.html",nf.replace('<head>','<head><base href="/"><meta name="robots" content="noindex">',1))
# sitemap (hreflang)
BMAP={}
for b in POSTS: BMAP[bpath("tr",b)]=bpath("en",b); BMAP[bpath("en",b)]=bpath("tr",b)
def alt(p):
    if p in BMAP: return (p,BMAP[p]) if not p.startswith("en/") else (BMAP[p],p)
    if p.startswith("en/"):
        en=p; trp=p[3:].replace("series/","seri/")
        for k,(a,b) in PG.items(): trp=trp.replace(b,a) if trp==b else trp
    else:
        trp=p; en="en/"+p.replace("seri/","series/")
        for k,(a,b) in PG.items(): en=("en/"+b) if p==a else en
    return trp.replace("index.html",""),en.replace("index.html","")
xs=[]
for p in pages:
    trp,en=alt(p)
    xs.append(f'<url><loc>{SITE}/{p}</loc><xhtml:link rel="alternate" hreflang="tr" href="{SITE}/{trp}"/><xhtml:link rel="alternate" hreflang="en" href="{SITE}/{en}"/><xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/{trp}"/></url>')
open(OUT+"/sitemap.xml","w").write(pretty('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+"\n".join(xs)+"\n</urlset>\n"))
open(OUT+"/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(OUT+"/_headers","w").write("/img/*\n  Cache-Control: public, max-age=2592000\n/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/*\n  Cache-Control: public, max-age=86400\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n")
open(OUT+"/_redirects","w").write("https://www.mogra.com.tr/* https://mogra.com.tr/:splat 301!\nhttp://www.mogra.com.tr/* https://mogra.com.tr/:splat 301!\n")
print("ok",len(pages),"sayfa")
