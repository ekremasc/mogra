# MOGRA

- `studio/` — Sanity paneli (https://mogra.sanity.studio). Şema değişikliğinden sonra: `cd studio && npx sanity deploy`
- `site/` — mogra.com.tr. Netlify her yayında `python3 _build/build.py` çalıştırır; içerik Sanity'den (proje `3ldd17c9`) çekilir.
- Panelde "Yayınla"ya basınca Sanity webhook'u Netlify build hook'unu tetikler; site 1–2 dk içinde güncellenir.
