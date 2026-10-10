import {defineType, defineField, defineArrayMember} from 'sanity'

const body = (name, title, group) => defineField({name, title, type: 'array', group, of: [
  defineArrayMember({type: 'block', styles: [{title: 'Paragraf', value: 'normal'}, {title: 'Ara başlık', value: 'h2'}],
    lists: [{title: 'Madde', value: 'bullet'}], marks: {decorators: [{title: 'Kalın', value: 'strong'}], annotations: []}}),
]})

export default defineType({
  name: 'post',
  title: 'Blog yazısı',
  type: 'document',
  groups: [{name: 'tr', title: 'Türkçe', default: true}, {name: 'en', title: 'English'}, {name: 'ayar', title: 'Ayarlar'}],
  fields: [
    defineField({name: 'title_tr', title: 'Başlık', type: 'string', group: 'tr', validation: (r) => r.required()}),
    defineField({name: 'slug_tr', title: 'Adres (URL)', type: 'slug', group: 'tr', options: {source: 'title_tr'}, validation: (r) => r.required()}),
    defineField({name: 'desc_tr', title: 'Google açıklaması (150–160 karakter)', type: 'text', rows: 2, group: 'tr', validation: (r) => r.max(170)}),
    defineField({name: 'lead_tr', title: 'Giriş (özet)', type: 'text', rows: 3, group: 'tr'}),
    body('body_tr', 'Yazı', 'tr'),
    defineField({name: 'title_en', title: 'Title', type: 'string', group: 'en'}),
    defineField({name: 'slug_en', title: 'URL', type: 'slug', group: 'en', options: {source: 'title_en'}}),
    defineField({name: 'desc_en', title: 'Google description', type: 'text', rows: 2, group: 'en'}),
    defineField({name: 'lead_en', title: 'Lead', type: 'text', rows: 3, group: 'en'}),
    body('body_en', 'Article', 'en'),
    defineField({name: 'date', title: 'Yayın tarihi', type: 'date', group: 'ayar', initialValue: () => new Date().toISOString().slice(0, 10)}),
    defineField({name: 'image', title: 'Kapak görseli', type: 'image', group: 'ayar', options: {hotspot: true}, validation: (r) => r.required()}),
  ],
  orderings: [{title: 'Yeni önce', name: 'dateDesc', by: [{field: 'date', direction: 'desc'}]}],
  preview: {select: {title: 'title_tr', subtitle: 'date', media: 'image'}},
})
