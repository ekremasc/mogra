import {defineConfig} from 'sanity'
import {structureTool} from 'sanity/structure'
import {visionTool} from '@sanity/vision'
import {trTRLocale} from '@sanity/locale-tr-tr'
import {schemaTypes, SINGLETONS} from './schemaTypes'
import {PROJECT_ID, DATASET} from './project'

const single = (S, id, title, icon) => S.listItem().title(title).id(id).icon(icon).child(S.document().schemaType(id).documentId(id).title(title))

export default defineConfig({
  name: 'mogra',
  title: 'MOGRA Panel',
  projectId: PROJECT_ID,
  dataset: DATASET,
  plugins: [
    structureTool({
      title: 'İçerik',
      structure: (S) => S.list().title('MOGRA').items([
        S.documentTypeListItem('series').title('Seriler').icon(() => '🪴').child(S.documentTypeList('series').title('Seriler').defaultOrdering([{field: 'order', direction: 'asc'}])),
        S.documentTypeListItem('post').title('Blog yazıları').icon(() => '📝'),
        S.divider(),
        single(S, 'home', 'Ana sayfa', () => '🏠'),
        single(S, 'about', 'Hakkımızda', () => '📖'),
        single(S, 'faq', 'Sıkça sorulan sorular', () => '❓'),
        single(S, 'settings', 'Site ayarları ve iletişim', () => '⚙️'),
      ]),
    }),
    visionTool({title: 'Sorgu'}),
    trTRLocale(),
  ],
  schema: {
    types: schemaTypes,
    templates: (t) => t.filter(({schemaType}) => !SINGLETONS.includes(schemaType)),
  },
  document: {
    actions: (prev, {schemaType}) => SINGLETONS.includes(schemaType) ? prev.filter(({action}) => !['unpublish', 'delete', 'duplicate'].includes(action)) : prev,
  },
})
