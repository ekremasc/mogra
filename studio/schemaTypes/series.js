import {defineType, defineField, defineArrayMember} from 'sanity'
import {COLORS, GROUPS} from './lists'

const colorField = defineField({name: 'color', title: 'Renk', type: 'string', options: {list: COLORS}})

export default defineType({
  name: 'series',
  title: 'Seri',
  type: 'document',
  groups: [
    {name: 'genel', title: 'Genel', default: true},
    {name: 'tr', title: 'Metinler (TR)'},
    {name: 'en', title: 'Metinler (EN)'},
    {name: 'boy', title: 'Boylar'},
    {name: 'gorsel', title: 'Görseller'},
  ],
  orderings: [{title: 'Sıra', name: 'order', by: [{field: 'order', direction: 'asc'}]}],
  fields: [
    defineField({name: 'name', title: 'Seri adı', type: 'string', group: 'genel', validation: (r) => r.required()}),
    defineField({name: 'slug', title: 'Adres (URL)', type: 'slug', group: 'genel', options: {source: 'name'},
      description: 'Sayfa adresi: mogra.com.tr/seri/…  Yayındaki serilerde değiştirmeyin.', validation: (r) => r.required()}),
    defineField({name: 'order', title: 'Sıra', type: 'number', group: 'genel', description: 'Koleksiyonda görünme sırası (küçük önce).'}),
    defineField({name: 'group', title: 'Form ailesi', type: 'string', group: 'genel', options: {list: GROUPS, layout: 'radio'}, validation: (r) => r.required()}),
    defineField({name: 'hidden', title: 'Sitede gizle', type: 'boolean', group: 'genel', initialValue: false}),
    defineField({name: 'colors', title: 'Renkler', type: 'array', group: 'genel', of: [{type: 'string'}], options: {list: COLORS},
      description: 'İlk renk sayfada varsayılan olarak seçili gelir.'}),

    defineField({name: 'form_tr', title: 'Form', type: 'string', group: 'tr'}),
    defineField({name: 'doku_tr', title: 'Doku', type: 'string', group: 'tr'}),
    defineField({name: 'kisa_tr', title: 'Kısa tanıtım', type: 'text', rows: 2, group: 'tr'}),
    defineField({name: 'lead_tr', title: 'Giriş paragrafı', type: 'text', rows: 3, group: 'tr'}),
    defineField({name: 'desc_tr', title: 'Ürün açıklaması (paragraflar)', type: 'array', group: 'tr', of: [{type: 'text', rows: 4}]}),
    defineField({name: 'tek_tr', title: 'Teknik özellikler', type: 'array', group: 'tr', of: [{type: 'string'}]}),
    defineField({name: 'use_tr', title: 'Kullanım alanları', type: 'array', group: 'tr', of: [{type: 'string'}]}),

    defineField({name: 'en_name', title: 'İngilizce ürün adı', type: 'string', group: 'en'}),
    defineField({name: 'form_en', title: 'Form', type: 'string', group: 'en'}),
    defineField({name: 'doku_en', title: 'Texture', type: 'string', group: 'en'}),
    defineField({name: 'kisa_en', title: 'Short intro', type: 'text', rows: 2, group: 'en'}),

    defineField({name: 'sizes', title: 'Boylar', type: 'array', group: 'boy',
      description: 'Küçükten büyüğe sıralayın. Sıra numarası (1, 2, 3…) mekân görsellerindeki "Boy no" ile eşleşir.',
      of: [defineArrayMember({type: 'object', name: 'size', fields: [
        {name: 'kind', title: 'Ölçü tipi', type: 'string', options: {list: [{title: 'Yuvarlak (Ø × Y)', value: 'r'}, {title: 'Köşeli (U × G × Y)', value: 'b'}], layout: 'radio'}, initialValue: 'r'},
        {name: 'd', title: 'Çap / Uzunluk (cm)', type: 'number'},
        {name: 'w', title: 'Genişlik (cm) — yalnız köşeli', type: 'number'},
        {name: 'h', title: 'Yükseklik (cm)', type: 'number'},
        {name: 'guide', title: 'Boy rehberi cümlesi (TR)', type: 'text', rows: 2},
      ], preview: {select: {k: 'kind', d: 'd', w: 'w', h: 'h'}, prepare: ({k, d, w, h}) => ({title: k === 'b' ? `${d} × ${w} × ${h} cm` : `Ø ${d} × ${h} cm`})}})]}),

    defineField({name: 'productImages', title: 'Ürün fotoğrafları (beyaz fon)', type: 'array', group: 'gorsel',
      of: [defineArrayMember({type: 'image', options: {hotspot: true}, fields: [
        colorField,
        {name: 'side', title: 'Yan açı', type: 'boolean', initialValue: false},
        {name: 'set', title: 'İkili set', type: 'boolean', initialValue: false},
      ]})], options: {layout: 'grid'}}),
    defineField({name: 'lifestyle', title: 'Mekân görselleri (boya göre)', type: 'array', group: 'gorsel',
      description: 'Her görsele renk ve boy numarası verin; sayfada seçilen boya göre gösterilir.',
      of: [defineArrayMember({type: 'image', options: {hotspot: true}, fields: [
        colorField,
        {name: 'size', title: 'Boy no', type: 'number', validation: (r) => r.min(1)},
        {name: 'tex', title: 'Doku notu (ör. Utah)', type: 'string'},
      ]})], options: {layout: 'grid'}}),
    defineField({name: 'drawings', title: 'Teknik çizimler', type: 'array', group: 'gorsel', of: [{type: 'image'}], options: {layout: 'grid'}}),
    defineField({name: 'extraLifestyle', title: 'Ek mekân görselleri (boy bilgisi olmayan)', type: 'array', group: 'gorsel', of: [{type: 'image', options: {hotspot: true}}], options: {layout: 'grid'}}),
  ],
  preview: {
    select: {title: 'name', group: 'group', media: 'productImages.0', hidden: 'hidden'},
    prepare: ({title, group, media, hidden}) => ({title: (hidden ? '🚫 ' : '') + title, subtitle: (GROUPS.find((g) => g.value === group) || {}).title, media}),
  },
})
