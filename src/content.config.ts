import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const guides = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    relatedTool: z.string().optional(),
    heroImage: z.string().optional(),
    heroAlt: z.string().optional(),
    keywords: z.array(z.string()).optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).optional(),
    images: z.array(z.object({ src: z.string(), alt: z.string(), caption: z.string() })).optional(),
  }),
});

export const collections = { guides };
