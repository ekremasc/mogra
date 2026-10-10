import {defineType, defineField, defineArrayMember} from 'sanity'

const pair = (name, title, type = 'string', group, extra = {}) => [
  defineField({name: name + '_tr', title: title + ' (TR)', type, group, ...extra}),
  defineField({name: name + '_en', title: title + ' (EN)', type, group, ...extra}),
]

export const settings = defineType({
  name: 'settings', title: 'Site ayarları ve iletişim', type: 'document',
  groups: [{name: 'ilet', title: 'İletişim', default: true}, {name: 'magaza', title: 'Mağaza'}, {name: 'metin', title: 'Site metinleri'}, {name: 'dosya', title: 'Katalog'}],
  fields: [
    defineField({name: 'whatsapp', title: 'WhatsApp numarası (90 ile, boşluksuz)', type: 'string', group: 'ilet', description: 'Örn. 905444720903 — formlar ve butonlar bu numaraya gider.'}),
    defineField({name: 'phone', title: 'Cep telefonu (görünen)', type: 'string', group: 'ilet'}),
    defineField({name: 'email', title: 'E-posta', type: 'string', group: 'ilet'}),
    defineField({name: 'landlines', title: 'Sabit hatlar', type: 'array', group: 'magaza', of: [defineArrayMember({type: 'string'})]}),
    ...pair('address', 'Adres', 'text', 'magaza', {rows: 2}),
    defineField({name: 'mapQuery', title: 'Harita araması', type: 'string', group: 'magaza', description: 'Google Haritalar\'da konumu bulduran metin.'}),
    defineField({name: 'hours', title: 'Çalışma saatleri', type: 'array', group: 'magaza', of: [defineArrayMember({type: 'object', name: 'hour', fields: [
      {name: 'days_tr', title: 'Günler (TR)', type: 'string'}, {name: 'days_en', title: 'Days (EN)', type: 'string'},
      {name: 'time_tr', title: 'Saat (TR)', type: 'string'}, {name: 'time_en', title: 'Time (EN)', type: 'string'}],
      preview: {select: {title: 'days_tr', subtitle: 'time_tr'}}})]}),
    ...pair('topbar', 'Üst şerit yazısı', 'string', 'metin'),
    ...pair('footer', 'Alt bilgi (footer) metni', 'text', 'metin', {rows: 3}),
    defineField({name: 'catalog', title: 'Katalog PDF', type: 'file', group: 'dosya', options: {accept: 'application/pdf'}}),
  ],
  preview: {prepare: () => ({title: 'Site ayarları ve iletişim'})},
})

export const home = defineType({
  name: 'home', title: 'Ana sayfa', type: 'document',
  groups: [{name: 'hero', title: 'Giriş (hero)', default: true}, {name: 'vitrin', title: 'Vitrin'}, {name: 'mekan', title: 'Mekanlar'}],
  fields: [
    ...pair('heroTitle', 'Başlık', 'string', 'hero'),
    ...pair('heroText', 'Alt metin', 'text', 'hero', {rows: 2}),
    defineField({name: 'heroSeries', title: 'Butonun gideceği seri', type: 'reference', to: [{type: 'series'}], group: 'hero'}),
    defineField({name: 'heroImage', title: 'Görsel (masaüstü)', type: 'image', options: {hotspot: true}, group: 'hero'}),
    defineField({name: 'heroImageMobile', title: 'Görsel (mobil, dikey)', type: 'image', options: {hotspot: true}, group: 'hero'}),
    defineField({name: 'heroVideo', title: 'Video (MP4, sessiz oynar)', type: 'file', options: {accept: 'video/mp4'}, group: 'hero',
      description: 'Boş bırakırsanız yalnız görsel gösterilir. 10–15 sn, 2 MB altı önerilir.'}),
    defineField({name: 'featured', title: 'Öne çıkan seriler (kaydırmalı liste)', type: 'array', group: 'vitrin', of: [{type: 'reference', to: [{type: 'series'}]}]}),
    defineField({name: 'spaces', title: 'Mekanlar bölümü', type: 'array', group: 'mekan', of: [defineArrayMember({type: 'object', name: 'space', fields: [
      {name: 'image', title: 'Görsel', type: 'image', options: {hotspot: true}},
      {name: 'label_tr', title: 'Etiket (TR)', type: 'string'}, {name: 'label_en', title: 'Label (EN)', type: 'string'},
      {name: 'series', title: 'Seri', type: 'reference', to: [{type: 'series'}]}],
      preview: {select: {title: 'label_tr', media: 'image', s: 'series.name'}, prepare: ({title, media, s}) => ({title, subtitle: s, media})}})]}),
  ],
  preview: {prepare: () => ({title: 'Ana sayfa'})},
})

export const about = defineType({
  name: 'about', title: 'Hakkımızda', type: 'document',
  fields: [
    defineField({name: 'body_tr', title: 'Metin (TR) — paragraflar', type: 'array', of: [{type: 'text', rows: 4}]}),
    defineField({name: 'body_en', title: 'Text (EN) — paragraphs', type: 'array', of: [{type: 'text', rows: 4}]}),
    defineField({name: 'image', title: 'Üst görsel', type: 'image', options: {hotspot: true}}),
  ],
  preview: {prepare: () => ({title: 'Hakkımızda'})},
})

export const faq = defineType({
  name: 'faq', title: 'Sıkça sorulan sorular', type: 'document',
  fields: [defineField({name: 'items', title: 'Sorular', type: 'array', of: [defineArrayMember({type: 'object', name: 'qa', fields: [
    {name: 'q_tr', title: 'Soru (TR)', type: 'string'}, {name: 'a_tr', title: 'Cevap (TR)', type: 'text', rows: 3},
    {name: 'q_en', title: 'Question (EN)', type: 'string'}, {name: 'a_en', title: 'Answer (EN)', type: 'text', rows: 3}],
    preview: {select: {title: 'q_tr'}}})]})],
  preview: {prepare: () => ({title: 'Sıkça sorulan sorular'})},
})
