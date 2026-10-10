(function(){
  var WA="905444720903";
  var $=function(s,r){return (r||document).querySelector(s)}, $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  var hdr=$(".hdr"), tb=$(".topbar");
  function onScroll(){
    if(!hdr) return;
    var t=tb?tb.offsetHeight:0;
    document.documentElement.style.setProperty("--tb",Math.max(0,t-window.scrollY)+"px");
    hdr.classList.toggle("solid",window.scrollY>t+40);
  }
  if(document.body.classList.contains("has-hero")){onScroll();window.addEventListener("scroll",onScroll,{passive:true});window.addEventListener("resize",onScroll)}

  // mega menü
  var mb=$("[data-mega]"), mega=$(".mega"), closeT;
  function setMega(o){if(!mega)return;mega.hidden=!o;mb.setAttribute("aria-expanded",o);hdr.classList.toggle("menu-open",o)}
  if(mb&&mega){
    mb.addEventListener("click",function(){setMega(mega.hidden)});
    [mb,mega].forEach(function(el){
      el.addEventListener("mouseenter",function(){clearTimeout(closeT);setMega(true)});
      el.addEventListener("mouseleave",function(){closeT=setTimeout(function(){setMega(false)},180)});
    });
    document.addEventListener("keydown",function(e){if(e.key==="Escape")setMega(false)});
  }
  // mobil menü
  var dr=$(".drawer");
  $$("[data-drawer]").forEach(function(b){b.addEventListener("click",function(){dr.hidden=!dr.hidden;document.body.style.overflow=dr.hidden?"":"hidden"})});

  // hero slider
  var slides=$$(".slide"), dots=$$(".hero-dots button"), cur=0, timer;
  function go(i){if(!slides.length)return;slides[cur].classList.remove("on");dots[cur]&&dots[cur].classList.remove("on");cur=(i+slides.length)%slides.length;slides[cur].classList.add("on");dots[cur]&&dots[cur].classList.add("on");var c=$(".hero-count b");if(c)c.textContent=String(cur+1).padStart(2,"0")}
  var useVid=window.matchMedia&&!matchMedia("(max-width:700px)").matches&&!matchMedia("(prefers-reduced-motion: reduce)").matches&&!(navigator.connection&&navigator.connection.saveData);
  function vids(){if(!useVid)return;slides.forEach(function(s,i){var v=$("video",s);if(!v)return;if(i===cur){if(!v.src){v.src=v.dataset.src;v.addEventListener("playing",function(){s.classList.add("vid-on")},{once:true})}v.currentTime=0;var p=v.play();p&&p.catch(function(){})}else{v.pause()}})}
  var _go=go;go=function(i){_go(i);vids()};vids();
  function play(){clearInterval(timer);timer=setInterval(function(){go(cur+1)},7000)}
  if(slides.length>1){dots.forEach(function(d,i){d.addEventListener("click",function(){go(i);play()})});play()}

  // ray okları
  $$("[data-rail]").forEach(function(nav){
    var rail=document.getElementById(nav.getAttribute("data-rail"));
    $$("button",nav).forEach(function(b){b.addEventListener("click",function(){rail.scrollBy({left:(b.dataset.dir==="-1"?-1:1)*rail.clientWidth*.8,behavior:"smooth"})})});
  });

  // koleksiyon filtresi
  var grid=$("#grid");
  if(grid){
    var f={form:"all",color:"all",q:""}, cards=$$(".p-card",grid), empty=$("#empty");
    function apply(){
      var n=0;
      cards.forEach(function(c){
        var ok=(f.form==="all"||c.dataset.form===f.form)&&(f.color==="all"||c.dataset.colors.split("|").indexOf(f.color)>-1)&&(!f.q||c.dataset.name.indexOf(f.q)>-1);
        c.hidden=!ok;if(ok)n++;
      });
      empty.hidden=n>0;var cw=$("#count");cw.textContent=n+" "+cw.dataset.w;
    }
    $$("[data-f]").forEach(function(b){b.addEventListener("click",function(){
      var k=b.dataset.f;$$('[data-f="'+k+'"]').forEach(function(x){x.setAttribute("aria-pressed","false")});b.setAttribute("aria-pressed","true");f[k]=b.dataset.v;apply();
    })});
    $("#q").addEventListener("input",function(e){f.q=e.target.value.toLocaleLowerCase("tr").trim();apply()});
    var h=location.hash.slice(1);if(h){var t=$('[data-f="form"][data-v="'+h+'"]');if(t)t.click()}
  }

  // seri galerisi: renk + boy seçimi
  var main=$("#gmain");
  if(main){
    var thumbs=$$(".gal-thumbs button"), curColor=null, curSize="1", rows=$$(".sizes tr[data-size]"), sb=$("#stockbtn");
    function show(b){thumbs.forEach(function(x){x.setAttribute("aria-current","false")});b.setAttribute("aria-current","true");main.src=b.dataset.src;main.className=b.dataset.life?"cover":"";main.alt=b.dataset.alt}
    function lifeFor(size){var m=thumbs.filter(function(b){return b.dataset.life&&b.dataset.size===size});var c=m.filter(function(b){return b.dataset.color===curColor});return c.length?c:m}
    function refresh(){
      var life=lifeFor(curSize);
      thumbs.forEach(function(b){
        if(b.dataset.life&&b.dataset.size){b.hidden=life.indexOf(b)<0}
        else{b.hidden=!!(curColor&&b.dataset.color&&b.dataset.color!==curColor)}
      });
      if(sb){var r=$(".sizes tr.on"),c=$(".colors button[aria-pressed=true]");
        var m=sb.dataset.msg+(c?"\n"+sb.dataset.lColor+": "+c.textContent.trim():"")+(r?"\n"+sb.dataset.lSize+": "+r.dataset.label:"");
        sb.href="https://wa.me/"+WA+"?text="+encodeURIComponent(m)}
    }
    thumbs.forEach(function(b){b.addEventListener("click",function(){show(b)})});
    $$(".colors button").forEach(function(c){c.addEventListener("click",function(){
      $$(".colors button").forEach(function(x){x.setAttribute("aria-pressed","false")});c.setAttribute("aria-pressed","true");
      curColor=c.dataset.color;refresh();
      var t=thumbs.filter(function(b){return !b.hidden&&b.dataset.color===curColor})[0];if(t)show(t);
      var s=$("#selcolor");if(s)s.textContent=c.textContent.trim();
    })});
    rows.forEach(function(r){
      function pick(){rows.forEach(function(x){x.classList.remove("on");x.setAttribute("aria-pressed","false")});r.classList.add("on");r.setAttribute("aria-pressed","true");
        curSize=r.dataset.size;var s=$("#selsize");if(s)s.textContent=r.dataset.label;refresh();
        var t=lifeFor(curSize)[0];if(t){show(t);if(window.innerWidth<861)main.scrollIntoView({behavior:"smooth",block:"center"})}}
      r.addEventListener("click",pick);r.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" "){e.preventDefault();pick()}});
    });
    var first=$(".colors button");curColor=first?first.dataset.color:null;refresh();
  }
  // kartlardaki "Stok için sorun"
  $$(".stock-btn").forEach(function(b){
    function go(e){e.preventDefault();e.stopPropagation();window.open("https://wa.me/"+WA+"?text="+encodeURIComponent(b.dataset.wa),"_blank","noopener")}
    b.addEventListener("click",go);b.addEventListener("keydown",function(e){if(e.key==="Enter"||e.key===" ")go(e)});
  });
  // teklif formu: ?seri= ile seri seçili gelsin
  var fs=$("#f-seri"),qs=new URLSearchParams(location.search).get("seri");
  if(fs&&qs){Array.prototype.forEach.call(fs.options,function(o){if(o.text===qs)fs.value=o.value||o.text})}

  // formlar → WhatsApp
  $$("form[data-wa]").forEach(function(fm){
    fm.addEventListener("submit",function(e){
      e.preventDefault();
      var lines=[fm.dataset.wa];
      $$("input,select,textarea",fm).forEach(function(el){if(el.value.trim())lines.push(el.dataset.l+": "+el.value.trim())});
      window.open("https://wa.me/"+WA+"?text="+encodeURIComponent(lines.join("\n")),"_blank","noopener");
    });
  });
  var cs=$("#consent");
  if(cs){var st=null;try{st=localStorage.getItem("mogra-consent")}catch(e){}
    if(!st)cs.hidden=false;
    $$("[data-consent]",cs).forEach(function(b){b.addEventListener("click",function(){var ok=b.dataset.consent==="yes";
      try{localStorage.setItem("mogra-consent",ok?"yes":"no")}catch(e){}
      if(ok&&window.gtag)gtag("consent","update",{analytics_storage:"granted"});cs.hidden=true;})});}
  var y=$("#yil");if(y)y.textContent=new Date().getFullYear();
})();
